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
    com_available = True
    drawing_open = True

    def run_lisp(self, drawing_path: Path, lisp_source: str) -> dict[str, str]:
        return {"status": "submitted", "drawing": str(drawing_path)}

    def manage_layers_and_blocks(self, drawing_path: Path, action: str, parameters: dict) -> dict:
        return {"status": "submitted", "drawing": str(drawing_path), "action": action}

    def run_cad_command(self, drawing_path: Path, command: str, operation: str) -> dict[str, str]:
        if not self.com_available:
            from autocad_mcp_server.utils.errors import AutoCADUnavailable

            raise AutoCADUnavailable("No running AutoCAD COM session found")
        if not self.drawing_open:
            from autocad_mcp_server.utils.errors import AutoCADUnavailable

            raise AutoCADUnavailable("Target drawing is not open in the active AutoCAD session")
        return {"status": "submitted", "drawing": str(drawing_path), "operation": operation}


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


def test_execute_cad_command_uses_com_when_requested(tmp_path: Path) -> None:
    root = tmp_path / "allowed"
    root.mkdir()
    drawing = root / "sample.dwg"
    drawing.write_text("x", encoding="utf-8")
    interop = FakeInteropManager()
    service = DWGService(
        sandbox=PathSandbox([root]),
        core_console_manager=FakeCoreConsoleManager(),
        interop_manager=interop,
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
                execution_mode="com",
            )
        )
    )

    assert result.execution_mode == "com"


def test_execute_cad_command_uses_core_console_when_requested(tmp_path: Path) -> None:
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
                execution_mode="core_console",
            )
        )
    )

    assert result.execution_mode == "core_console"


def test_execute_cad_command_auto_raises_when_drawing_not_open(tmp_path: Path) -> None:
    root = tmp_path / "allowed"
    root.mkdir()
    drawing = root / "sample.dwg"
    drawing.write_text("x", encoding="utf-8")
    interop = FakeInteropManager()
    interop.drawing_open = False
    service = DWGService(
        sandbox=PathSandbox([root]),
        core_console_manager=FakeCoreConsoleManager(),
        interop_manager=interop,
        metadata_extractor=MetadataExtractor(),
        geometry_query_service=GeometryQueryService(),
        layer_block_service=LayerBlockService(),
        lisp_runner=LispRunner(LispPolicy(max_chars=1000, max_depth=8)),
        cad_command_service=CadCommandService(),
    )

    try:
        asyncio.run(
            service.execute_cad_command(
                AutoCadCommandRequest(
                    dwg_path=str(drawing),
                    operation="zoom_extents",
                    parameters={},
                    execution_mode="auto",
                )
            )
        )
    except Exception as exc:
        assert "Target drawing is not open" in str(exc)
    else:
        raise AssertionError("Expected execute_cad_command to raise when drawing is not open")
