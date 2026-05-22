from __future__ import annotations

from autocad_mcp_server.models.requests import QueryGeometryRequest
from autocad_mcp_server.models.responses import ToolResponse
from autocad_mcp_server.services.dwg_service import DWGService


def register_geometry_tool(mcp, service: DWGService) -> None:
    @mcp.tool()
    async def query_geometry(
        dwg_path: str,
        entity_types: list[str] | None = None,
        layers: list[str] | None = None,
        block_names: list[str] | None = None,
        handles: list[str] | None = None,
        limit: int = 100,
        execution_mode: str = "auto",
    ) -> dict:
        request = QueryGeometryRequest(
            dwg_path=dwg_path,
            entity_types=entity_types or [],
            layers=layers or [],
            block_names=block_names or [],
            handles=handles or [],
            limit=limit,
            execution_mode=execution_mode,
        )
        result = await service.query_geometry(request)
        return ToolResponse(
            ok=result.success,
            tool_name="query_geometry",
            execution_mode=result.execution_mode,
            payload=result.payload,
            warnings=result.warnings,
        ).model_dump()
