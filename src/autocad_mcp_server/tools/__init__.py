from autocad_mcp_server.services.drafting_script_service import DraftingScriptService
from autocad_mcp_server.services.dwg_service import DWGService
from autocad_mcp_server.services.execution_queue import ExecutionQueue
from autocad_mcp_server.services.runtime_supervisor import RuntimeSupervisor
from autocad_mcp_server.tools.drafting import register_drafting_tool
from autocad_mcp_server.tools.geometry import register_geometry_tool
from autocad_mcp_server.tools.layers_blocks import register_layers_blocks_tool
from autocad_mcp_server.tools.lisp import register_lisp_tool
from autocad_mcp_server.tools.metadata import register_metadata_tool
from autocad_mcp_server.tools.status import register_status_tool


def register_tools(
    mcp,
    service: DWGService,
    supervisor: RuntimeSupervisor,
    queue: ExecutionQueue,
    drafting_service: DraftingScriptService,
) -> None:
    register_metadata_tool(mcp, service)
    register_lisp_tool(mcp, service)
    register_geometry_tool(mcp, service)
    register_layers_blocks_tool(mcp, service)
    register_drafting_tool(mcp, drafting_service)
    register_status_tool(mcp, supervisor, queue)
