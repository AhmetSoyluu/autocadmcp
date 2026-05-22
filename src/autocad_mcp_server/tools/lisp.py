from __future__ import annotations

from autocad_mcp_server.models.requests import ExecuteAutolispRequest
from autocad_mcp_server.services.dwg_service import DWGService
from autocad_mcp_server.tools.common import error_response, success_response


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
        try:
            result = await service.execute_autolisp(request)
            return success_response(
                tool_name="execute_autolisp",
                execution_mode=result.execution_mode,
                payload=result.payload,
                warnings=result.warnings,
            )
        except Exception as exc:
            return error_response("execute_autolisp", execution_mode, exc)
