from __future__ import annotations

from autocad_mcp_server.services.execution_queue import ExecutionQueue
from autocad_mcp_server.services.runtime_supervisor import RuntimeSupervisor
from autocad_mcp_server.tools.common import success_response


def register_status_tool(mcp, supervisor: RuntimeSupervisor, queue: ExecutionQueue) -> None:
    @mcp.tool()
    async def get_server_status() -> dict:
        supervisor.update_queue_depth(queue.depth)
        return success_response(
            tool_name="get_server_status",
            execution_mode="service",
            payload={
                "queue_depth": queue.depth,
                "runtime_state": supervisor.state.__dict__,
            },
            warnings=[],
        )
