from __future__ import annotations

from pathlib import Path

from autocad_mcp_server.security.lisp_policy import LispPolicy


class LispRunner:
    def __init__(self, policy: LispPolicy) -> None:
        self.policy = policy

    def validate(self, source: str) -> str:
        return self.policy.validate(source)

    def build_core_console_script(self, source: str) -> str:
        validated = self.validate(source)
        return f"{validated}\n(command \"_.QSAVE\")\n(princ)\n"

    def build_com_command(self, source: str) -> str:
        return self.validate(source)
