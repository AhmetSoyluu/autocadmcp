from __future__ import annotations

from pathlib import Path

from autocad_mcp_server.utils.errors import ExecutableNotFound


def _common_autocad_paths(executable: str) -> list[Path]:
    bases = [
        Path("C:/Program Files/Autodesk/AutoCAD 2025"),
        Path("C:/Program Files/Autodesk/AutoCAD 2024"),
        Path("C:/Program Files/Autodesk/AutoCAD 2023"),
    ]
    return [base / executable for base in bases]


def discover_executable(configured_path: Path | None, executable: str) -> Path:
    if configured_path is not None:
        if configured_path.exists():
            return configured_path
        raise ExecutableNotFound(f"Configured executable not found: {configured_path}")

    for candidate in _common_autocad_paths(executable):
        if candidate.exists():
            return candidate

    raise ExecutableNotFound(f"Unable to locate {executable}")
