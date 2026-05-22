from autocad_mcp_server.services.dwg_service import DWGService
from autocad_mcp_server.tools.geometry import register_geometry_tool
from autocad_mcp_server.tools.layers_blocks import register_layers_blocks_tool
from autocad_mcp_server.tools.lisp import register_lisp_tool
from autocad_mcp_server.tools.metadata import register_metadata_tool


def register_tools(mcp, service: DWGService) -> None:
    register_metadata_tool(mcp, service)
    register_lisp_tool(mcp, service)
    register_geometry_tool(mcp, service)
    register_layers_blocks_tool(mcp, service)
