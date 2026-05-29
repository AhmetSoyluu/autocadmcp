from __future__ import annotations

from autocad_mcp_server.models.requests import FileManagementRequest
from autocad_mcp_server.services.dwg_service import DWGService
from autocad_mcp_server.tools.common import error_response, success_response


def register_file_management_tool(mcp, service: DWGService) -> None:
    @mcp.tool()
    async def create_new_drawing(
        dwg_path: str = "",
        template_path: str = "",
        execution_mode: str = "auto",
    ) -> dict:
        """Create a new empty DWG drawing. Optionally specify a template (.dwt) path."""
        request = FileManagementRequest(
            action="create_new",
            dwg_path=dwg_path,
            template_path=template_path,
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_file_management(request)
            return success_response("create_new_drawing", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("create_new_drawing", execution_mode, exc)

    @mcp.tool()
    async def open_drawing(dwg_path: str, execution_mode: str = "auto") -> dict:
        """Open a DWG file in the AutoCAD session."""
        request = FileManagementRequest(action="open", dwg_path=dwg_path, execution_mode=execution_mode)
        try:
            result = await service.execute_file_management(request)
            return success_response("open_drawing", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("open_drawing", execution_mode, exc)

    @mcp.tool()
    async def save_drawing(dwg_path: str = "", execution_mode: str = "auto") -> dict:
        """Save the active or specified drawing."""
        request = FileManagementRequest(action="save", dwg_path=dwg_path, execution_mode=execution_mode)
        try:
            result = await service.execute_file_management(request)
            return success_response("save_drawing", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("save_drawing", execution_mode, exc)

    @mcp.tool()
    async def save_drawing_as(
        dwg_path: str,
        save_format: str = "dwg",
        execution_mode: str = "auto",
    ) -> dict:
        """Save the active drawing to a new path. Format can be 'dwg', 'dxf', or 'dwt'."""
        request = FileManagementRequest(
            action="save_as", dwg_path=dwg_path, save_format=save_format, execution_mode=execution_mode,
        )
        try:
            result = await service.execute_file_management(request)
            return success_response("save_drawing_as", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("save_drawing_as", execution_mode, exc)

    @mcp.tool()
    async def close_drawing(
        dwg_path: str = "",
        save_changes: bool = True,
        execution_mode: str = "auto",
    ) -> dict:
        """Close a drawing. Optionally save or discard changes."""
        request = FileManagementRequest(
            action="close", dwg_path=dwg_path, save_changes=save_changes, execution_mode=execution_mode,
        )
        try:
            result = await service.execute_file_management(request)
            return success_response("close_drawing", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("close_drawing", execution_mode, exc)

    @mcp.tool()
    async def list_open_drawings(execution_mode: str = "auto") -> dict:
        """List all currently open drawings in AutoCAD."""
        request = FileManagementRequest(action="list_open", execution_mode=execution_mode)
        try:
            result = await service.execute_file_management(request)
            return success_response("list_open_drawings", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("list_open_drawings", execution_mode, exc)

    @mcp.tool()
    async def set_active_drawing(dwg_path: str, execution_mode: str = "auto") -> dict:
        """Set a specific open drawing as the active document."""
        request = FileManagementRequest(action="set_active", dwg_path=dwg_path, execution_mode=execution_mode)
        try:
            result = await service.execute_file_management(request)
            return success_response("set_active_drawing", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("set_active_drawing", execution_mode, exc)

    @mcp.tool()
    async def get_drawing_properties(dwg_path: str = "", execution_mode: str = "auto") -> dict:
        """Get detailed drawing properties (file size, version, creation date, etc.)."""
        request = FileManagementRequest(action="get_properties", dwg_path=dwg_path, execution_mode=execution_mode)
        try:
            result = await service.execute_file_management(request)
            return success_response("get_drawing_properties", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("get_drawing_properties", execution_mode, exc)
