from __future__ import annotations

from autocad_mcp_server.models.requests import BatchProcessingRequest
from autocad_mcp_server.services.dwg_service import DWGService
from autocad_mcp_server.tools.common import error_response, success_response


def register_batch_processing_tool(mcp, service: DWGService) -> None:
    @mcp.tool()
    async def batch_execute_script(
        dwg_paths: list[str],
        script_content: str,
        execution_mode: str = "auto",
    ) -> dict:
        """Execute the same AutoLISP/script on multiple DWG files."""
        request = BatchProcessingRequest(
            action="batch_execute_script",
            dwg_paths=dwg_paths,
            parameters={"script_content": script_content},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_batch_processing(request)
            return success_response("batch_execute_script", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("batch_execute_script", execution_mode, exc)

    @mcp.tool()
    async def batch_update_attributes(
        dwg_paths: list[str],
        block_name: str,
        attribute_updates: dict[str, str],
        execution_mode: str = "auto",
    ) -> dict:
        """Update block attributes across multiple drawings."""
        request = BatchProcessingRequest(
            action="batch_update_attributes",
            dwg_paths=dwg_paths,
            parameters={"block_name": block_name, "attribute_updates": attribute_updates},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_batch_processing(request)
            return success_response("batch_update_attributes", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("batch_update_attributes", execution_mode, exc)

    @mcp.tool()
    async def batch_layer_standards(
        dwg_paths: list[str],
        layer_definitions: list[dict],
        execution_mode: str = "auto",
    ) -> dict:
        """Apply a standard layer schema to multiple drawings. Each layer_def has name, color, linetype."""
        request = BatchProcessingRequest(
            action="batch_layer_standards",
            dwg_paths=dwg_paths,
            parameters={"layer_definitions": layer_definitions},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_batch_processing(request)
            return success_response("batch_layer_standards", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("batch_layer_standards", execution_mode, exc)

    @mcp.tool()
    async def batch_purge(dwg_paths: list[str], execution_mode: str = "auto") -> dict:
        """Purge unused elements from multiple drawings."""
        request = BatchProcessingRequest(
            action="batch_purge", dwg_paths=dwg_paths, execution_mode=execution_mode,
        )
        try:
            result = await service.execute_batch_processing(request)
            return success_response("batch_purge", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("batch_purge", execution_mode, exc)

    @mcp.tool()
    async def batch_audit(dwg_paths: list[str], execution_mode: str = "auto") -> dict:
        """Audit and fix errors in multiple drawings."""
        request = BatchProcessingRequest(
            action="batch_audit", dwg_paths=dwg_paths, execution_mode=execution_mode,
        )
        try:
            result = await service.execute_batch_processing(request)
            return success_response("batch_audit", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("batch_audit", execution_mode, exc)

    @mcp.tool()
    async def create_macro(
        macro_name: str,
        script_content: str,
        description: str = "",
        execution_mode: str = "auto",
    ) -> dict:
        """Save a reusable macro (script) for later execution."""
        request = BatchProcessingRequest(
            action="create_macro",
            parameters={"macro_name": macro_name, "script_content": script_content, "description": description},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_batch_processing(request)
            return success_response("create_macro", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("create_macro", execution_mode, exc)

    @mcp.tool()
    async def run_macro(
        macro_name: str,
        dwg_paths: list[str] | None = None,
        execution_mode: str = "auto",
    ) -> dict:
        """Execute a previously saved macro on one or more drawings."""
        request = BatchProcessingRequest(
            action="run_macro",
            dwg_paths=dwg_paths or [],
            parameters={"macro_name": macro_name},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_batch_processing(request)
            return success_response("run_macro", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("run_macro", execution_mode, exc)

    @mcp.tool()
    async def list_macros(execution_mode: str = "auto") -> dict:
        """List all saved macros."""
        request = BatchProcessingRequest(action="list_macros", execution_mode=execution_mode)
        try:
            result = await service.execute_batch_processing(request)
            return success_response("list_macros", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("list_macros", execution_mode, exc)
