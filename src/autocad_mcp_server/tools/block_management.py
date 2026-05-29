from __future__ import annotations

from autocad_mcp_server.models.requests import BlockManagementRequest
from autocad_mcp_server.services.dwg_service import DWGService
from autocad_mcp_server.tools.common import error_response, success_response


def register_block_management_tool(mcp, service: DWGService) -> None:
    @mcp.tool()
    async def create_block_definition(
        dwg_path: str,
        block_name: str,
        handles: list[str],
        base_x: float = 0,
        base_y: float = 0,
        execution_mode: str = "auto",
    ) -> dict:
        """Create a block definition from existing objects (identified by handles)."""
        request = BlockManagementRequest(
            dwg_path=dwg_path,
            action="create_block_definition",
            parameters={"block_name": block_name, "handles": handles, "base_x": base_x, "base_y": base_y},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_block_management(request)
            return success_response("create_block_definition", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("create_block_definition", execution_mode, exc)

    @mcp.tool()
    async def list_block_definitions(dwg_path: str, execution_mode: str = "auto") -> dict:
        """List all block definitions in the drawing."""
        request = BlockManagementRequest(
            dwg_path=dwg_path, action="list_block_definitions", execution_mode=execution_mode,
        )
        try:
            result = await service.execute_block_management(request)
            return success_response("list_block_definitions", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("list_block_definitions", execution_mode, exc)

    @mcp.tool()
    async def get_block_attributes(
        dwg_path: str, handle: str, execution_mode: str = "auto",
    ) -> dict:
        """Read attribute tag/value pairs from a block reference."""
        request = BlockManagementRequest(
            dwg_path=dwg_path,
            action="get_block_attributes",
            parameters={"handle": handle},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_block_management(request)
            return success_response("get_block_attributes", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("get_block_attributes", execution_mode, exc)

    @mcp.tool()
    async def set_block_attributes(
        dwg_path: str,
        handle: str,
        attributes: dict[str, str],
        execution_mode: str = "auto",
    ) -> dict:
        """Update attribute values on a block reference. Keys are tag names, values are new strings."""
        request = BlockManagementRequest(
            dwg_path=dwg_path,
            action="set_block_attributes",
            parameters={"handle": handle, "attributes": attributes},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_block_management(request)
            return success_response("set_block_attributes", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("set_block_attributes", execution_mode, exc)

    @mcp.tool()
    async def explode_block(dwg_path: str, handle: str, execution_mode: str = "auto") -> dict:
        """Explode a block reference into its constituent objects."""
        request = BlockManagementRequest(
            dwg_path=dwg_path, action="explode_block",
            parameters={"handle": handle}, execution_mode=execution_mode,
        )
        try:
            result = await service.execute_block_management(request)
            return success_response("explode_block", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("explode_block", execution_mode, exc)

    @mcp.tool()
    async def rename_block(
        dwg_path: str, old_name: str, new_name: str, execution_mode: str = "auto",
    ) -> dict:
        """Rename a block definition."""
        request = BlockManagementRequest(
            dwg_path=dwg_path, action="rename_block",
            parameters={"old_name": old_name, "new_name": new_name},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_block_management(request)
            return success_response("rename_block", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("rename_block", execution_mode, exc)

    @mcp.tool()
    async def count_block_references(
        dwg_path: str, block_name: str, execution_mode: str = "auto",
    ) -> dict:
        """Count how many times a block definition is referenced in the drawing."""
        request = BlockManagementRequest(
            dwg_path=dwg_path, action="count_block_references",
            parameters={"block_name": block_name}, execution_mode=execution_mode,
        )
        try:
            result = await service.execute_block_management(request)
            return success_response("count_block_references", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("count_block_references", execution_mode, exc)

    @mcp.tool()
    async def import_block_from_file(
        dwg_path: str,
        source_file: str,
        block_name: str,
        execution_mode: str = "auto",
    ) -> dict:
        """Import a block definition from an external DWG file."""
        request = BlockManagementRequest(
            dwg_path=dwg_path, action="import_block_from_file",
            parameters={"source_file": source_file, "block_name": block_name},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_block_management(request)
            return success_response("import_block_from_file", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("import_block_from_file", execution_mode, exc)
