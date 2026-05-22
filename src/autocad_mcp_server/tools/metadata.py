from __future__ import annotations

from autocad_mcp_server.models.requests import ReadDwgMetadataRequest
from autocad_mcp_server.services.dwg_service import DWGService
from autocad_mcp_server.tools.common import error_response, success_response


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
        try:
            result = await service.read_dwg_metadata(request)
            return success_response(
                tool_name="read_dwg_metadata",
                execution_mode=result.execution_mode,
                payload=result.payload,
                warnings=result.warnings,
            )
        except Exception as exc:
            return error_response("read_dwg_metadata", execution_mode, exc)
