from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any

from autocad_mcp_server.models.requests import (
    AnalysisRequest,
    AnnotationRequest,
    AutoCadCommandRequest,
    BatchProcessingRequest,
    BlockManagementRequest,
    ExecuteAutolispRequest,
    ExportRequest,
    FileManagementRequest,
    ManageLayersAndBlocksRequest,
    QueryGeometryRequest,
    ReadDwgMetadataRequest,
    XrefManagementRequest,
)
from autocad_mcp_server.models.runtime import JobResult
from autocad_mcp_server.security.path_sandbox import PathSandbox
from autocad_mcp_server.services.analysis_service import AnalysisService
from autocad_mcp_server.services.annotation_service import AnnotationService
from autocad_mcp_server.services.block_management_service import BlockManagementService
from autocad_mcp_server.services.cad_command_service import CadCommandService
from autocad_mcp_server.services.core_console_manager import CoreConsoleManager
from autocad_mcp_server.services.export_service import ExportService
from autocad_mcp_server.services.file_management_service import FileManagementService
from autocad_mcp_server.services.geometry_query_service import GeometryQueryService
from autocad_mcp_server.services.interop_manager import InteropManager
from autocad_mcp_server.services.layer_block_service import LayerBlockService
from autocad_mcp_server.services.lisp_runner import LispRunner
from autocad_mcp_server.services.metadata_extractor import MetadataExtractor
from autocad_mcp_server.services.xref_management_service import XrefManagementService
from autocad_mcp_server.utils.errors import AutoCADUnavailable, ToolExecutionFailure


class DWGService:
    def __init__(
        self,
        sandbox: PathSandbox,
        core_console_manager: CoreConsoleManager,
        interop_manager: InteropManager,
        metadata_extractor: MetadataExtractor,
        geometry_query_service: GeometryQueryService,
        layer_block_service: LayerBlockService,
        lisp_runner: LispRunner,
        cad_command_service: CadCommandService,
        file_management_service: FileManagementService | None = None,
        annotation_service: AnnotationService | None = None,
        block_management_service: BlockManagementService | None = None,
        xref_management_service: XrefManagementService | None = None,
        export_service: ExportService | None = None,
        analysis_service: AnalysisService | None = None,
    ) -> None:
        self.sandbox = sandbox
        self.core_console_manager = core_console_manager
        self.interop_manager = interop_manager
        self.metadata_extractor = metadata_extractor
        self.geometry_query_service = geometry_query_service
        self.layer_block_service = layer_block_service
        self.lisp_runner = lisp_runner
        self.cad_command_service = cad_command_service
        # New service dependencies (optional for backwards compat)
        self.file_management_service = file_management_service or FileManagementService()
        self.annotation_service = annotation_service or AnnotationService()
        self.block_management_service = block_management_service or BlockManagementService()
        self.xref_management_service = xref_management_service or XrefManagementService()
        self.export_service = export_service or ExportService()
        self.analysis_service = analysis_service or AnalysisService()

    @staticmethod
    def _ensure_core_console_success(result: dict[str, Any]) -> None:
        if not bool(result.get("sentinel_ok")):
            raise ToolExecutionFailure("Core Console output sentinel validation failed")

    @staticmethod
    def _extract_measurement_payload(stdout: str) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        for line in stdout.splitlines():
            if not line.startswith("MCP_RESULT:"):
                continue
            key, _, value = line.removeprefix("MCP_RESULT:").partition("=")
            if key and value:
                payload[key.lower()] = value.strip()
        return payload

    # ─── Generic LISP execution helper ──────────────────────────

    async def _run_lisp_via_com_or_console(
        self,
        drawing_path: Path,
        lisp: str,
        execution_mode: str,
        prefix: str,
        operation_name: str = "",
    ) -> JobResult:
        """Run validated LISP with COM-first, core-console-fallback pattern."""
        validated = self.lisp_runner.validate(lisp)

        if execution_mode == "com":
            payload = self.interop_manager.run_cad_command(drawing_path, validated, operation_name)
            return JobResult(success=True, execution_mode="com", payload=payload)

        if execution_mode == "auto":
            try:
                payload = self.interop_manager.run_cad_command(drawing_path, validated, operation_name)
                return JobResult(success=True, execution_mode="com", payload=payload)
            except AutoCADUnavailable:
                pass  # Fall through to core console

        # Core console fallback (used when COM is unavailable)
        core_script = validated + '\n(command "_.QSAVE")\n(princ)\n'
        result = await self.core_console_manager.run_script(drawing_path, core_script, prefix=prefix)
        try:
            self._ensure_core_console_success(result)
        except ToolExecutionFailure as exc:
            raise ToolExecutionFailure(
                f"Both COM and Core Console execution failed. "
                f"Ensure AutoCAD is running and the file is accessible. "
                f"Core Console error: {exc}"
            ) from exc
        stdout = str(result["stdout"])
        payload = {
            "drawing": str(drawing_path),
            "operation": operation_name,
            "stdout": stdout,
            "stderr": result["stderr"],
        }
        measurement_payload = self._extract_measurement_payload(stdout)
        payload.update(measurement_payload)
        return JobResult(success=True, execution_mode="core_console", payload=payload)

    # ─── Existing methods ───────────────────────────────────────

    async def read_dwg_metadata(self, request: ReadDwgMetadataRequest) -> JobResult:
        drawing_path = self.sandbox.validate(request.dwg_path)
        script = self.metadata_extractor.build_script(
            include_text=request.include_text,
            include_blocks=request.include_blocks,
            include_layers=request.include_layers,
        )
        result = await self.core_console_manager.run_script(drawing_path, script, prefix="metadata")
        self._ensure_core_console_success(result)
        payload = self.metadata_extractor.extract_from_text(
            drawing_path,
            str(result["stdout"]),
            include_text=request.include_text,
            include_blocks=request.include_blocks,
            include_layers=request.include_layers,
        )
        return JobResult(success=True, execution_mode="core_console", payload=payload)

    async def query_geometry(self, request: QueryGeometryRequest) -> JobResult:
        drawing_path = self.sandbox.validate(request.dwg_path)
        script = self.geometry_query_service.build_script(request)
        result = await self.core_console_manager.run_script(drawing_path, script, prefix="geometry")
        self._ensure_core_console_success(result)
        payload = self.geometry_query_service.parse_output(drawing_path, str(result["stdout"]))
        return JobResult(success=True, execution_mode="core_console", payload=payload)

    async def execute_autolisp(self, request: ExecuteAutolispRequest) -> JobResult:
        drawing_path = self.sandbox.validate(request.dwg_path)
        validated = self.lisp_runner.validate(request.lisp_source)
        if request.target == "background":
            script = self.lisp_runner.build_core_console_script(validated)
            result = await self.core_console_manager.run_script(drawing_path, script, prefix="lisp")
            self._ensure_core_console_success(result)
            payload: dict[str, Any] = {
                "drawing": str(drawing_path),
                "stdout": result["stdout"],
                "stderr": result["stderr"],
            }
            return JobResult(success=True, execution_mode="core_console", payload=payload)

        try:
            payload = self.interop_manager.run_lisp(drawing_path, validated)
            return JobResult(success=True, execution_mode="com", payload=payload)
        except AutoCADUnavailable:
            script = self.lisp_runner.build_core_console_script(validated)
            result = await self.core_console_manager.run_script(drawing_path, script, prefix="lisp-fallback")
            self._ensure_core_console_success(result)
            payload = {
                "drawing": str(drawing_path),
                "stdout": result["stdout"],
                "stderr": result["stderr"],
                "fallback_reason": "com_unavailable",
            }
            return JobResult(
                success=True,
                execution_mode="core_console",
                payload=payload,
                warnings=["COM unavailable; executed in Core Console fallback mode."],
            )

    async def manage_layers_and_blocks(self, request: ManageLayersAndBlocksRequest) -> JobResult:
        drawing_path = self.sandbox.validate(request.dwg_path)
        lisp = self.layer_block_service.build_lisp(request.action, request.parameters)
        validated = self.lisp_runner.validate(lisp)
        if request.execution_mode == "core_console":
            result = await self.core_console_manager.run_script(drawing_path, validated + "\n(princ)\n", prefix="layers")
            self._ensure_core_console_success(result)
            payload = {
                "drawing": str(drawing_path),
                "action": request.action,
                "stdout": result["stdout"],
                "stderr": result["stderr"],
            }
            return JobResult(success=True, execution_mode="core_console", payload=payload)

        try:
            payload = self.interop_manager.manage_layers_and_blocks(
                drawing_path,
                request.action,
                request.parameters,
            )
            payload["operation_id"] = uuid.uuid4().hex
            return JobResult(success=True, execution_mode="com", payload=payload)
        except AutoCADUnavailable:
            result = await self.core_console_manager.run_script(
                drawing_path,
                validated + "\n(princ)\n",
                prefix="layers-fallback",
            )
            self._ensure_core_console_success(result)
            payload = {
                "drawing": str(drawing_path),
                "action": request.action,
                "stdout": result["stdout"],
                "stderr": result["stderr"],
                "fallback_reason": "com_unavailable",
            }
            return JobResult(
                success=True,
                execution_mode="core_console",
                payload=payload,
                warnings=["COM unavailable; executed in Core Console fallback mode."],
            )
        except ToolExecutionFailure:
            raise

    async def execute_cad_command(self, request: AutoCadCommandRequest) -> JobResult:
        drawing_path = self.sandbox.validate(request.dwg_path)
        lisp = self.cad_command_service.build_lisp(request.operation, request.parameters)
        return await self._run_lisp_via_com_or_console(
            drawing_path, lisp, request.execution_mode,
            prefix=f"cad-{request.operation}", operation_name=request.operation,
        )

    # ─── New service methods ────────────────────────────────────

    async def execute_file_management(self, request: FileManagementRequest) -> JobResult:
        if request.dwg_path:
            self.sandbox.validate(request.dwg_path)
        try:
            payload = self.interop_manager.run_file_command(
                lisp_source="",
                action=request.action,
                dwg_path=request.dwg_path,
                template_path=request.template_path,
                save_format=request.save_format,
                save_changes=request.save_changes,
            )
            return JobResult(success=True, execution_mode="com", payload=payload)
        except AutoCADUnavailable as exc:
            raise ToolExecutionFailure(f"File management requires live AutoCAD session: {exc}") from exc

    async def execute_annotation(self, request: AnnotationRequest) -> JobResult:
        drawing_path = self.sandbox.validate(request.dwg_path)
        lisp = self.annotation_service.build_lisp(request.operation, request.parameters)
        return await self._run_lisp_via_com_or_console(
            drawing_path, lisp, request.execution_mode,
            prefix=f"annotation-{request.operation}", operation_name=request.operation,
        )

    async def execute_block_management(self, request: BlockManagementRequest) -> JobResult:
        drawing_path = self.sandbox.validate(request.dwg_path)
        lisp = self.block_management_service.build_lisp(request.action, request.parameters)
        return await self._run_lisp_via_com_or_console(
            drawing_path, lisp, request.execution_mode,
            prefix=f"block-{request.action}", operation_name=request.action,
        )

    async def execute_xref_management(self, request: XrefManagementRequest) -> JobResult:
        drawing_path = self.sandbox.validate(request.dwg_path)
        lisp = self.xref_management_service.build_lisp(request.action, request.parameters)
        return await self._run_lisp_via_com_or_console(
            drawing_path, lisp, request.execution_mode,
            prefix=f"xref-{request.action}", operation_name=request.action,
        )

    async def execute_export(self, request: ExportRequest) -> JobResult:
        drawing_path = self.sandbox.validate(request.dwg_path)
        params = {
            "output_path": request.output_path,
            "layout_name": request.layout_name,
            "paper_size": request.paper_size,
            "scale": request.scale,
            "color_mode": request.color_mode,
            "resolution_dpi": request.resolution_dpi,
            "layers_to_include": request.layers_to_include,
        }
        lisp = self.export_service.build_lisp(request.format, params)
        return await self._run_lisp_via_com_or_console(
            drawing_path, lisp, request.execution_mode,
            prefix=f"export-{request.format}", operation_name=f"export_{request.format}",
        )

    async def execute_analysis(self, request: AnalysisRequest) -> JobResult:
        drawing_path = self.sandbox.validate(request.dwg_path)
        lisp = self.analysis_service.build_lisp(request.operation, request.parameters)
        return await self._run_lisp_via_com_or_console(
            drawing_path, lisp, request.execution_mode,
            prefix=f"analysis-{request.operation}", operation_name=request.operation,
        )

    async def execute_batch_processing(self, request: BatchProcessingRequest) -> JobResult:
        """Batch operations iterate over multiple files."""
        results: list[dict[str, Any]] = []
        errors: list[str] = []

        if request.action in ("create_macro", "list_macros", "run_macro"):
            # Macro management doesn't iterate over files
            return JobResult(
                success=True,
                execution_mode="com",
                payload={"action": request.action, "status": "macro_placeholder", "parameters": request.parameters},
            )

        for dwg in request.dwg_paths:
            try:
                drawing_path = self.sandbox.validate(dwg)

                if request.action == "batch_execute_script":
                    script = request.parameters.get("script_content", "")
                    validated = self.lisp_runner.validate(script)
                    core_script = validated + '\n(command "_.QSAVE")\n(princ)\n'
                    result = await self.core_console_manager.run_script(drawing_path, core_script, prefix="batch-script")
                    self._ensure_core_console_success(result)
                    results.append({"file": str(drawing_path), "status": "ok", "stdout": result["stdout"]})

                elif request.action == "batch_purge":
                    core_script = '(command "_.-PURGE" "_A" "*" "_N")\n(command "_.QSAVE")\n(princ)\n'
                    result = await self.core_console_manager.run_script(drawing_path, core_script, prefix="batch-purge")
                    self._ensure_core_console_success(result)
                    results.append({"file": str(drawing_path), "status": "purged"})

                elif request.action == "batch_audit":
                    core_script = '(command "_.AUDIT" "_Y")\n(command "_.QSAVE")\n(princ)\n'
                    result = await self.core_console_manager.run_script(drawing_path, core_script, prefix="batch-audit")
                    self._ensure_core_console_success(result)
                    results.append({"file": str(drawing_path), "status": "audited"})

                else:
                    results.append({"file": str(drawing_path), "status": "unsupported_action"})

            except Exception as exc:
                errors.append(f"{dwg}: {exc}")

        payload: dict[str, Any] = {
            "action": request.action,
            "processed": len(results),
            "results": results,
        }
        if errors:
            payload["errors"] = errors

        return JobResult(
            success=len(errors) == 0,
            execution_mode="core_console",
            payload=payload,
            warnings=errors if errors else [],
        )

