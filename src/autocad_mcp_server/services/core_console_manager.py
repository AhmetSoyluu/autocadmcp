from __future__ import annotations

from pathlib import Path

from autocad_mcp_server.adapters.core_console_adapter import CoreConsoleAdapter
from autocad_mcp_server.services.execution_queue import ExecutionQueue
from autocad_mcp_server.utils.temp_workspace import TempWorkspaceManager


class CoreConsoleManager:
    def __init__(
        self,
        adapter: CoreConsoleAdapter,
        queue: ExecutionQueue,
        workspace_manager: TempWorkspaceManager,
        timeout_seconds: int,
        keep_failed_workspaces: bool,
    ) -> None:
        self.adapter = adapter
        self.queue = queue
        self.workspace_manager = workspace_manager
        self.timeout_seconds = timeout_seconds
        self.keep_failed_workspaces = keep_failed_workspaces

    async def run_script(self, drawing_path: Path, script_contents: str, prefix: str) -> dict[str, str | int]:
        async def operation() -> dict[str, str | int]:
            workspace = self.workspace_manager.create(prefix)
            script_path = workspace / "job.scr"
            script_path.write_text(script_contents, encoding="utf-8")
            try:
                result = self.adapter.run_script(drawing_path, script_path, self.timeout_seconds)
                self.workspace_manager.cleanup(workspace, keep=False)
                return {
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "returncode": result.returncode,
                    "workspace": str(workspace),
                }
            except Exception:
                self.workspace_manager.cleanup(workspace, keep=self.keep_failed_workspaces)
                raise

        return await self.queue.run(operation)
