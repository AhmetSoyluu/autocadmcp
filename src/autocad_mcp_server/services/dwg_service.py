from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any

from autocad_mcp_server.models.requests import (
    AutoCadCommandRequest,
    ExecuteAutolispRequest,
    ManageLayersAndBlocksRequest,
    QueryGeometryRequest,
    ReadDwgMetadataRequest,
)
from autocad_mcp_server.models.runtime import JobResult
from autocad_mcp_server.security.path_sandbox import PathSandbox
from autocad_mcp_server.services.cad_command_service import CadCommandService
from autocad_mcp_server.services.core_console_manager import CoreConsoleManager
from autocad_mcp_server.services.geometry_query_service import GeometryQueryService
from autocad_mcp_server.services.interop_manager import InteropManager
from autocad_mcp_server.services.layer_block_service import LayerBlockService
from autocad_mcp_server.services.lisp_runner import LispRunner
from autocad_mcp_server.services.metadata_extractor import MetadataExtractor
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
    ) -> None:
        self.sandbox = sandbox
        self.core_console_manager = core_console_manager
        self.interop_manager = interop_manager
        self.metadata_extractor = metadata_extractor
        self.geometry_query_service = geometry_query_service
        self.layer_block_service = layer_block_service
        self.lisp_runner = lisp_runner
        self.cad_command_service = cad_command_service

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
        validated = self.lisp_runner.validate(lisp)

        if request.execution_mode == "com":
            payload = self.interop_manager.run_cad_command(drawing_path, validated, request.operation)
            return JobResult(success=True, execution_mode="com", payload=payload)

        if request.execution_mode == "auto":
            try:
                payload = self.interop_manager.run_cad_command(drawing_path, validated, request.operation)
                return JobResult(success=True, execution_mode="com", payload=payload)
            except AutoCADUnavailable as exc:
                raise ToolExecutionFailure(str(exc)) from exc

        core_script = validated + "\n(command \"_.QSAVE\")\n(princ)\n"
        result = await self.core_console_manager.run_script(
            drawing_path,
            core_script,
            prefix=f"cad-{request.operation}",
        )
        self._ensure_core_console_success(result)
        stdout = str(result["stdout"])
        payload = {
            "drawing": str(drawing_path),
            "operation": request.operation,
            "stdout": stdout,
            "stderr": result["stderr"],
        }
        measurement_payload = self._extract_measurement_payload(stdout)
        payload.update(measurement_payload)
        return JobResult(success=True, execution_mode="core_console", payload=payload)
