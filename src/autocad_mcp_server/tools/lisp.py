from __future__ import annotations

from autocad_mcp_server.models.requests import ExecuteAutolispRequest
from autocad_mcp_server.models.responses import ToolResponse
from autocad_mcp_server.services.dwg_service import DWGService


def register_lisp_tool(mcp, service: DWGService) -> None:
    @mcp.tool()
    async def execute_autolisp(
        dwg_path: str,
        lisp_source: str,
        target: str = "live_session",
        execution_mode: str = "auto",
    ) -> dict:
        request = ExecuteAutolispRequest(
            dwg_path=dwg_path,
            lisp_source=lisp_source,
            target=target,
            execution_mode=execution_mode,
        )
        result = await service.execute_autolisp(request)
        return ToolResponse(
            ok=result.success,
            tool_name="execute_autolisp",
            execution_mode=result.execution_mode,
            payload=result.payload,
            warnings=result.warnings,
        ).model_dump()
