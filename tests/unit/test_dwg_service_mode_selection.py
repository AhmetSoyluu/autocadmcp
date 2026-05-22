import asyncio
from pathlib import Path

from autocad_mcp_server.models.requests import AutoCadCommandRequest, ExecuteAutolispRequest
from autocad_mcp_server.models.runtime import JobResult
from autocad_mcp_server.security.lisp_policy import LispPolicy
from autocad_mcp_server.security.path_sandbox import PathSandbox
from autocad_mcp_server.services.cad_command_service import CadCommandService
from autocad_mcp_server.services.dwg_service import DWGService
from autocad_mcp_server.services.geometry_query_service import GeometryQueryService
from autocad_mcp_server.services.layer_block_service import LayerBlockService
from autocad_mcp_server.services.lisp_runner import LispRunner
from autocad_mcp_server.services.metadata_extractor import MetadataExtractor


class FakeCoreConsoleManager:
    async def run_script(self, drawing_path: Path, script_contents: str, prefix: str) -> dict[str, str | int]:
        return {
            "stdout": "ok",
            "stderr": "",
            "returncode": 0,
            "workspace": str(drawing_path.parent),
            "sentinel_ok": True,
        }


class FakeInteropManager:
    def run_lisp(self, drawing_path: Path, lisp_source: str) -> dict[str, str]:
        return {"status": "submitted", "drawing": str(drawing_path)}

    def manage_layers_and_blocks(self, drawing_path: Path, action: str, parameters: dict) -> dict:
        return {"status": "submitted", "drawing": str(drawing_path), "action": action}


def test_execute_autolisp_uses_com_for_live_session(tmp_path: Path) -> None:
    root = tmp_path / "allowed"
    root.mkdir()
    drawing = root / "sample.dwg"
    drawing.write_text("x", encoding="utf-8")
    service = DWGService(
        sandbox=PathSandbox([root]),
        core_console_manager=FakeCoreConsoleManager(),
        interop_manager=FakeInteropManager(),
        metadata_extractor=MetadataExtractor(),
        geometry_query_service=GeometryQueryService(),
        layer_block_service=LayerBlockService(),
        lisp_runner=LispRunner(LispPolicy(max_chars=1000, max_depth=8)),
        cad_command_service=CadCommandService(),
    )

    result: JobResult = asyncio.run(
        service.execute_autolisp(
            ExecuteAutolispRequest(dwg_path=str(drawing), lisp_source='(princ "x")', target="live_session")
        )
    )

    assert result.execution_mode == "com"


def test_execute_cad_command_uses_core_console(tmp_path: Path) -> None:
    root = tmp_path / "allowed"
    root.mkdir()
    drawing = root / "sample.dwg"
    drawing.write_text("x", encoding="utf-8")
    service = DWGService(
        sandbox=PathSandbox([root]),
        core_console_manager=FakeCoreConsoleManager(),
        interop_manager=FakeInteropManager(),
        metadata_extractor=MetadataExtractor(),
        geometry_query_service=GeometryQueryService(),
        layer_block_service=LayerBlockService(),
        lisp_runner=LispRunner(LispPolicy(max_chars=1000, max_depth=8)),
        cad_command_service=CadCommandService(),
    )

    result: JobResult = asyncio.run(
        service.execute_cad_command(
            AutoCadCommandRequest(
                dwg_path=str(drawing),
                operation="zoom_extents",
                parameters={},
                execution_mode="auto",
            )
        )
    )

    assert result.execution_mode == "core_console"
