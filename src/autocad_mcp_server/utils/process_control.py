from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from autocad_mcp_server.utils.errors import CoreConsoleTimeout, ToolExecutionFailure


@dataclass(slots=True)
class CommandResult:
    returncode: int
    stdout: str
    stderr: str


def run_command(command: list[str], timeout_seconds: int, cwd: Path | None = None) -> CommandResult:
    try:
        completed = subprocess.run(
            command,
            cwd=str(cwd) if cwd is not None else None,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise CoreConsoleTimeout(f"Command timed out after {timeout_seconds}s") from exc

    result = CommandResult(
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )
    if completed.returncode != 0:
        raise ToolExecutionFailure(
            f"Command failed with exit code {completed.returncode}: {completed.stderr.strip()}"
        )
    return result
