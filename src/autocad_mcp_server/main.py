from __future__ import annotations

from fastmcp import FastMCP

from autocad_mcp_server.adapters.com_adapter import ComAdapter
from autocad_mcp_server.adapters.core_console_adapter import CoreConsoleAdapter
from autocad_mcp_server.config import Settings
from autocad_mcp_server.logging import configure_logging
from autocad_mcp_server.prompts import register_prompts
from autocad_mcp_server.resources import register_resources
from autocad_mcp_server.security.lisp_policy import LispPolicy
from autocad_mcp_server.security.path_sandbox import PathSandbox
from autocad_mcp_server.services.analysis_service import AnalysisService
from autocad_mcp_server.services.annotation_service import AnnotationService
from autocad_mcp_server.services.block_management_service import BlockManagementService
from autocad_mcp_server.services.cad_command_service import CadCommandService
from autocad_mcp_server.services.core_console_manager import CoreConsoleManager
from autocad_mcp_server.services.drafting_script_service import DraftingScriptService
from autocad_mcp_server.services.drawing_state_cache import DrawingStateCache
from autocad_mcp_server.services.dwg_service import DWGService
from autocad_mcp_server.services.execution_queue import ExecutionQueue
from autocad_mcp_server.services.export_service import ExportService
from autocad_mcp_server.services.file_management_service import FileManagementService
from autocad_mcp_server.services.geometry_query_service import GeometryQueryService
from autocad_mcp_server.services.interop_manager import InteropManager
from autocad_mcp_server.services.layer_block_service import LayerBlockService
from autocad_mcp_server.services.lisp_runner import LispRunner
from autocad_mcp_server.services.metadata_extractor import MetadataExtractor
from autocad_mcp_server.services.runtime_supervisor import RuntimeSupervisor
from autocad_mcp_server.services.undo_redo_service import UndoRedoService
from autocad_mcp_server.services.xref_management_service import XrefManagementService
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
    lisp_runner = LispRunner(lisp_policy)

    # New services
    undo_redo = UndoRedoService()
    cache = DrawingStateCache(ttl_seconds=30.0)

    service = DWGService(
        sandbox=sandbox,
        core_console_manager=core_console_manager,
        interop_manager=interop_manager,
        metadata_extractor=MetadataExtractor(),
        geometry_query_service=GeometryQueryService(),
        layer_block_service=LayerBlockService(),
        lisp_runner=lisp_runner,
        cad_command_service=CadCommandService(),
        file_management_service=FileManagementService(),
        annotation_service=AnnotationService(),
        block_management_service=BlockManagementService(),
        xref_management_service=XrefManagementService(),
        export_service=ExportService(),
        analysis_service=AnalysisService(),
    )
    drafting_service = DraftingScriptService(workspace_manager, lisp_policy)

    mcp = FastMCP(settings.server_name)

    # Register tools (including undo/redo and cache)
    register_tools(mcp, service, supervisor, queue, drafting_service, undo_redo, cache)

    # Register MCP Resources (browsable context)
    register_resources(mcp, service, supervisor, cache)

    # Register MCP Prompts (intelligent templates)
    register_prompts(mcp)

    return mcp


def main() -> None:
    server = build_server()
    server.run()


if __name__ == "__main__":
    main()

