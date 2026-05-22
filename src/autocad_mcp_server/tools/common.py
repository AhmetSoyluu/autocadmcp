from __future__ import annotations

from typing import Any

from autocad_mcp_server.models.responses import ToolResponse
from autocad_mcp_server.utils.errors import (
    AutoCADUnavailable,
    CoreConsoleTimeout,
    ExecutableNotFound,
    PolicyViolation,
    SandboxViolation,
    ToolExecutionFailure,
)


def success_response(
    tool_name: str,
    execution_mode: str,
    payload: dict[str, Any],
    warnings: list[str] | None = None,
) -> dict[str, Any]:
    return ToolResponse(
        ok=True,
        tool_name=tool_name,
        execution_mode=execution_mode,
        payload=payload,
        warnings=warnings or [],
    ).model_dump()


def error_response(tool_name: str, execution_mode: str, exc: Exception) -> dict[str, Any]:
    error_code = "UNEXPECTED_ERROR"
    if isinstance(exc, SandboxViolation):
        error_code = "SANDBOX_VIOLATION"
    elif isinstance(exc, PolicyViolation):
        error_code = "POLICY_VIOLATION"
    elif isinstance(exc, AutoCADUnavailable):
        error_code = "AUTOCAD_UNAVAILABLE"
    elif isinstance(exc, CoreConsoleTimeout):
        error_code = "CORE_CONSOLE_TIMEOUT"
    elif isinstance(exc, ExecutableNotFound):
        error_code = "EXECUTABLE_NOT_FOUND"
    elif isinstance(exc, ToolExecutionFailure):
        error_code = "TOOL_EXECUTION_FAILURE"

    return ToolResponse(
        ok=False,
        tool_name=tool_name,
        execution_mode=execution_mode,
        payload={},
        warnings=[],
        error=str(exc),
        error_code=error_code,
    ).model_dump()
