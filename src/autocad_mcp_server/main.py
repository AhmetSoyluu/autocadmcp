from __future__ import annotations

from fastmcp import FastMCP

from autocad_mcp_server.adapters.com_adapter import ComAdapter
from autocad_mcp_server.adapters.core_console_adapter import CoreConsoleAdapter
from autocad_mcp_server.config import Settings
from autocad_mcp_server.logging import configure_logging
from autocad_mcp_server.security.lisp_policy import LispPolicy
from autocad_mcp_server.security.path_sandbox import PathSandbox
from autocad_mcp_server.services.core_console_manager import CoreConsoleManager
from autocad_mcp_server.services.dwg_service import DWGService
from autocad_mcp_server.services.execution_queue import ExecutionQueue
from autocad_mcp_server.services.geometry_query_service import GeometryQueryService
from autocad_mcp_server.services.interop_manager import InteropManager
from autocad_mcp_server.services.layer_block_service import LayerBlockService
from autocad_mcp_server.services.lisp_runner import LispRunner
from autocad_mcp_server.services.metadata_extractor import MetadataExtractor
from autocad_mcp_server.services.runtime_supervisor import RuntimeSupervisor
from autocad_mcp_server.tools import register_tools
from autocad_mcp_server.utils.discovery import discover_executable
from autocad_mcp_server.utils.temp_workspace import TempWorkspaceManager


def build_server() -> FastMCP:
    settings = Settings()
    configure_logging(settings.log_level)

    for path in [settings.profile_root, settings.state_dir, settings.audit_log_dir, settings.runtime_log_dir, settings.workspace_root]:
        path.mkdir(parents=True, exist_ok=True)

    supervisor = RuntimeSupervisor(settings.state_dir)
    supervisor.bootstrap()

    sandbox = PathSandbox(settings.allowed_root_paths)
    lisp_policy = LispPolicy(
        max_chars=settings.max_lisp_chars,
        max_depth=settings.max_lisp_depth,
    )
    queue = ExecutionQueue()
    supervisor.update_queue_depth(queue.depth)
    workspace_manager = TempWorkspaceManager(settings.workspace_root)
    core_console_adapter = CoreConsoleAdapter(
        discover_executable(settings.accoreconsole_path, "accoreconsole.exe")
    )
    audit_file = settings.audit_log_dir / "audit.jsonl"
    core_console_manager = CoreConsoleManager(
        adapter=core_console_adapter,
        queue=queue,
        workspace_manager=workspace_manager,
        timeout_seconds=settings.core_console_timeout_seconds,
        keep_failed_workspaces=settings.keep_failed_workspaces,
        supervisor=supervisor,
        audit_file=audit_file,
    )
    interop_manager = InteropManager(
        adapter=ComAdapter(),
        visible=settings.com_visible,
        launch_if_missing=settings.com_launch_if_missing,
        supervisor=supervisor,
        audit_file=audit_file,
    )
    service = DWGService(
        sandbox=sandbox,
        core_console_manager=core_console_manager,
        interop_manager=interop_manager,
        metadata_extractor=MetadataExtractor(),
        geometry_query_service=GeometryQueryService(),
        layer_block_service=LayerBlockService(),
        lisp_runner=LispRunner(lisp_policy),
    )

    mcp = FastMCP(settings.server_name)
    register_tools(mcp, service, supervisor, queue)
    return mcp


def main() -> None:
    server = build_server()
    server.run()


if __name__ == "__main__":
    main()
