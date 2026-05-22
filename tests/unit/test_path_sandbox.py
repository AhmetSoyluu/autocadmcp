from pathlib import Path

import pytest

from autocad_mcp_server.security.path_sandbox import PathSandbox
from autocad_mcp_server.utils.errors import SandboxViolation


def test_accepts_path_inside_allowed_root(tmp_path: Path) -> None:
    root = tmp_path / "allowed"
    root.mkdir()
    drawing = root / "sample.dwg"
    sandbox = PathSandbox([root])

    validated = sandbox.validate(drawing)

    assert str(validated).endswith("sample.dwg")


def test_rejects_path_outside_allowed_root(tmp_path: Path) -> None:
    root = tmp_path / "allowed"
    other = tmp_path / "other"
    root.mkdir()
    other.mkdir()
    drawing = other / "sample.dwg"
    sandbox = PathSandbox([root])

    with pytest.raises(SandboxViolation):
        sandbox.validate(drawing)
