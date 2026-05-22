from __future__ import annotations

from pathlib import Path

from autocad_mcp_server.utils.process_control import CommandResult, run_command


class CoreConsoleAdapter:
    def __init__(self, executable: Path) -> None:
        self.executable = executable

    def run_script(self, drawing_path: Path, script_path: Path, timeout_seconds: int) -> CommandResult:
        command = [
            str(self.executable),
            "/i",
            str(drawing_path),
            "/s",
            str(script_path),
        ]
        return run_command(command, timeout_seconds=timeout_seconds, cwd=script_path.parent)
