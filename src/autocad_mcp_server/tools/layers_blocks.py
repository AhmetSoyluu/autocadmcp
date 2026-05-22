from __future__ import annotations

from autocad_mcp_server.models.requests import ManageLayersAndBlocksRequest
from autocad_mcp_server.services.dwg_service import DWGService
from autocad_mcp_server.tools.common import error_response, success_response


def register_layers_blocks_tool(mcp, service: DWGService) -> None:
    @mcp.tool()
    async def manage_layers_and_blocks(
        dwg_path: str,
        action: str,
        parameters: dict | None = None,
        execution_mode: str = "auto",
    ) -> dict:
        request = ManageLayersAndBlocksRequest(
            dwg_path=dwg_path,
            action=action,
            parameters=parameters or {},
            execution_mode=execution_mode,
        )
        try:
            result = await service.manage_layers_and_blocks(request)
            return success_response(
                tool_name="manage_layers_and_blocks",
                execution_mode=result.execution_mode,
                payload=result.payload,
                warnings=result.warnings,
            )
        except Exception as exc:
            return error_response("manage_layers_and_blocks", execution_mode, exc)
