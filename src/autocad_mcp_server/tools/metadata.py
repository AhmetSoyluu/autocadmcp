from __future__ import annotations

from autocad_mcp_server.models.requests import ReadDwgMetadataRequest
from autocad_mcp_server.models.responses import ToolResponse
from autocad_mcp_server.services.dwg_service import DWGService


def register_metadata_tool(mcp, service: DWGService) -> None:
    @mcp.tool()
    async def read_dwg_metadata(
        dwg_path: str,
        include_text: bool = True,
        include_blocks: bool = True,
        include_layers: bool = True,
        execution_mode: str = "auto",
    ) -> dict:
        request = ReadDwgMetadataRequest(
            dwg_path=dwg_path,
            include_text=include_text,
            include_blocks=include_blocks,
            include_layers=include_layers,
            execution_mode=execution_mode,
        )
        result = await service.read_dwg_metadata(request)
        return ToolResponse(
            ok=result.success,
            tool_name="read_dwg_metadata",
            execution_mode=result.execution_mode,
            payload=result.payload,
            warnings=result.warnings,
        ).model_dump()
