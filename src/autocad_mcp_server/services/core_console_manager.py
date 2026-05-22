from __future__ import annotations

import uuid
from pathlib import Path

from autocad_mcp_server.adapters.core_console_adapter import CoreConsoleAdapter
from autocad_mcp_server.services.execution_queue import ExecutionQueue
from autocad_mcp_server.services.runtime_supervisor import RuntimeSupervisor
from autocad_mcp_server.utils.audit import AuditRecord, write_audit_record
from autocad_mcp_server.utils.temp_workspace import TempWorkspaceManager


class CoreConsoleManager:
    SENTINEL_BEGIN = "MCP_RUN_BEGIN"
    SENTINEL_END = "MCP_RUN_END"
    SENTINEL_OK = "MCP_STATUS:OK"

    def __init__(
        self,
        adapter: CoreConsoleAdapter,
        queue: ExecutionQueue,
        workspace_manager: TempWorkspaceManager,
        timeout_seconds: int,
        keep_failed_workspaces: bool,
        supervisor: RuntimeSupervisor,
        audit_file: Path,
    ) -> None:
        self.adapter = adapter
        self.queue = queue
        self.workspace_manager = workspace_manager
        self.timeout_seconds = timeout_seconds
        self.keep_failed_workspaces = keep_failed_workspaces
        self.supervisor = supervisor
        self.audit_file = audit_file

    def _wrap_script(self, script_contents: str) -> str:
        return (
            f'(princ "{self.SENTINEL_BEGIN}\\n")\n'
            + script_contents.rstrip()
            + "\n"
            + f'(princ "{self.SENTINEL_OK}\\n")\n'
            + f'(princ "{self.SENTINEL_END}\\n")\n(princ)\n'
        )

    def _validate_sentinel(self, stdout: str) -> bool:
        return (
            self.SENTINEL_BEGIN in stdout
            and self.SENTINEL_OK in stdout
            and self.SENTINEL_END in stdout
        )

    async def run_script(self, drawing_path: Path, script_contents: str, prefix: str) -> dict[str, str | int | bool]:
        async def operation() -> dict[str, str | int | bool]:
            job_id = uuid.uuid4().hex
            workspace = self.workspace_manager.create(prefix)
            script_path = workspace / "job.scr"
            wrapped = self._wrap_script(script_contents)
            script_path.write_text(wrapped, encoding="utf-8")
            self.workspace_manager.write_manifest(
                workspace,
                {
                    "job_id": job_id,
                    "drawing_path": str(drawing_path),
                    "prefix": prefix,
                    "status": "running",
                },
            )
            try:
                result = self.adapter.run_script(drawing_path, script_path, self.timeout_seconds)
                sentinel_ok = self._validate_sentinel(result.stdout)
                self.workspace_manager.write_manifest(
                    workspace,
                    {
                        "job_id": job_id,
                        "drawing_path": str(drawing_path),
                        "prefix": prefix,
                        "status": "completed",
                        "returncode": result.returncode,
                        "sentinel_ok": sentinel_ok,
                    },
                )
                self.supervisor.mark_core_console_success()
                self.supervisor.record_electrical_context(active_project_wdp=str(drawing_path.with_suffix('.wdp')))
                write_audit_record(
                    AuditRecord(
                        tool_name=prefix,
                        dwg_path=str(drawing_path),
                        execution_mode="core_console",
                        outcome="success",
                        message="Core Console run completed",
                        operation_id=job_id,
                        electrical_context={"active_project_wdp": str(drawing_path.with_suffix('.wdp'))},
                    ),
                    self.audit_file,
                )
                self.workspace_manager.cleanup(workspace, keep=False)
                return {
                    "job_id": job_id,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "returncode": result.returncode,
                    "workspace": str(workspace),
                    "sentinel_ok": sentinel_ok,
                }
            except Exception as exc:
                self.workspace_manager.write_manifest(
                    workspace,
                    {
                        "job_id": job_id,
                        "drawing_path": str(drawing_path),
                        "prefix": prefix,
                        "status": "failed",
                    },
                )
                retained = self.workspace_manager.count_retained_workspaces() if self.keep_failed_workspaces else 0
                self.supervisor.set_retained_failure_workspaces(retained)
                self.supervisor.record_job_failure(
                    reason=str(exc),
                    context={
                        "job_id": job_id,
                        "drawing_path": str(drawing_path),
                        "prefix": prefix,
                    },
                )
                write_audit_record(
                    AuditRecord(
                        tool_name=prefix,
                        dwg_path=str(drawing_path),
                        execution_mode="core_console",
                        outcome="failure",
                        message=str(exc),
                        operation_id=job_id,
                        error_context={
                            "job_id": job_id,
                            "drawing_path": str(drawing_path),
                            "prefix": prefix,
                        },
                    ),
                    self.audit_file,
                )
                self.workspace_manager.cleanup(workspace, keep=self.keep_failed_workspaces)
                raise

        return await self.queue.run(operation)
