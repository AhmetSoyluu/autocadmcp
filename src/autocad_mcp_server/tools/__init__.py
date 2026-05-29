from __future__ import annotations

from autocad_mcp_server.services.drafting_script_service import DraftingScriptService
from autocad_mcp_server.services.drawing_state_cache import DrawingStateCache
from autocad_mcp_server.services.dwg_service import DWGService
from autocad_mcp_server.services.execution_queue import ExecutionQueue
from autocad_mcp_server.services.runtime_supervisor import RuntimeSupervisor
from autocad_mcp_server.services.undo_redo_service import UndoRedoService
from autocad_mcp_server.tools.analysis import register_analysis_tool
from autocad_mcp_server.tools.annotation import register_annotation_tool
from autocad_mcp_server.tools.batch_processing import register_batch_processing_tool
from autocad_mcp_server.tools.block_management import register_block_management_tool
from autocad_mcp_server.tools.cad_commands import register_cad_commands_tool
from autocad_mcp_server.tools.drafting import register_drafting_tool
from autocad_mcp_server.tools.export import register_export_tool
from autocad_mcp_server.tools.file_management import register_file_management_tool
from autocad_mcp_server.tools.geometry import register_geometry_tool
from autocad_mcp_server.tools.layers_blocks import register_layers_blocks_tool
from autocad_mcp_server.tools.lisp import register_lisp_tool
from autocad_mcp_server.tools.metadata import register_metadata_tool
from autocad_mcp_server.tools.status import register_status_tool
from autocad_mcp_server.tools.undo_cache import register_cache_tool, register_undo_redo_tool
from autocad_mcp_server.tools.xref_management import register_xref_management_tool


def register_tools(
    mcp,
    service: DWGService,
    supervisor: RuntimeSupervisor,
    queue: ExecutionQueue,
    drafting_service: DraftingScriptService,
    undo_redo: UndoRedoService | None = None,
    cache: DrawingStateCache | None = None,
) -> None:
    # Core tools
    register_metadata_tool(mcp, service)
    register_lisp_tool(mcp, service)
    register_geometry_tool(mcp, service)
    register_layers_blocks_tool(mcp, service)
    register_cad_commands_tool(mcp, service)
    register_drafting_tool(mcp, drafting_service)
    register_status_tool(mcp, supervisor, queue)
    # Expanded tools
    register_file_management_tool(mcp, service)
    register_annotation_tool(mcp, service)
    register_block_management_tool(mcp, service)
    register_xref_management_tool(mcp, service)
    register_export_tool(mcp, service)
    register_batch_processing_tool(mcp, service)
    register_analysis_tool(mcp, service)
    # Undo/Redo & Cache tools
    if undo_redo is not None:
        register_undo_redo_tool(mcp, service, undo_redo)
    if cache is not None:
        register_cache_tool(mcp, service, cache)


