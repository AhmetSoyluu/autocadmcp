from __future__ import annotations

from autocad_mcp_server.models.requests import ManageLayersAndBlocksRequest
from autocad_mcp_server.models.responses import ToolResponse
from autocad_mcp_server.services.dwg_service import DWGService


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
        result = await service.manage_layers_and_blocks(request)
        return ToolResponse(
            ok=result.success,
            tool_name="manage_layers_and_blocks",
            execution_mode=result.execution_mode,
            payload=result.payload,
            warnings=result.warnings,
        ).model_dump()
