from __future__ import annotations

from datetime import datetime, timezone

from autocad_mcp_server.services.execution_queue import ExecutionQueue
from autocad_mcp_server.services.runtime_supervisor import RuntimeSupervisor
from autocad_mcp_server.tools.common import success_response


def _compute_uptime_seconds(last_started_at: str | None) -> int:
    if not last_started_at:
        return 0
    started = datetime.fromisoformat(last_started_at)
    return max(0, int((datetime.now(timezone.utc) - started).total_seconds()))


def register_status_tool(mcp, supervisor: RuntimeSupervisor, queue: ExecutionQueue) -> None:
    @mcp.tool()
    async def get_server_status() -> dict:
        supervisor.update_queue_depth(queue.depth)
        state = supervisor.state
        status = "OPERATIONAL"
        if queue.depth > 0:
            status = "PROCESSING"
        elif state.last_failure_reason and not (state.core_console_healthy or state.com_healthy):
            status = "ERROR"

        return success_response(
            tool_name="get_server_status",
            execution_mode="service",
            payload={
                "status": status,
                "uptime_seconds": _compute_uptime_seconds(state.last_started_at),
                "queue_metrics": {
                    "current_depth": queue.depth,
                    "total_jobs_processed": state.total_jobs_processed,
                },
                "autocad_electrical_context": {
                    "core_console_active": state.core_console_healthy,
                    "active_project": state.active_project_wdp,
                    "standard": state.electrical_standard,
                    "wd_m_block_present": state.wd_m_initialized,
                },
                "recovery_and_audit": {
                    "retained_failures": state.retained_failure_workspaces_count,
                    "last_successful_run_timestamp": state.last_core_console_success_at,
                    "last_failure_reason": state.last_failure_reason,
                },
            },
            warnings=[],
        )
