from __future__ import annotations

from dataclasses import dataclass

from autocad_mcp_server.utils.errors import PolicyViolation


@dataclass(frozen=True)
class LispPolicy:
    max_chars: int
    max_depth: int

    _blocked_tokens = (
        "startapp",
        "command-s",
        "vl-shell-execute",
        "shell",
        "powershell",
        "cmd.exe",
        "wscript.shell",
        "vl-file-copy",
        "open",
        "write-line",
        "read-line",
        "load_dialog",
    )

    def validate(self, source: str) -> str:
        text = source.strip()
        if not text:
            raise PolicyViolation("AutoLISP source cannot be empty")
        if len(text) > self.max_chars:
            raise PolicyViolation(f"AutoLISP exceeds {self.max_chars} characters")
        depth = 0
        max_seen = 0
        for char in text:
            if char == "(":
                depth += 1
                max_seen = max(max_seen, depth)
            elif char == ")":
                depth -= 1
            if depth < 0:
                raise PolicyViolation("AutoLISP has unbalanced parentheses")
        if depth != 0:
            raise PolicyViolation("AutoLISP has unbalanced parentheses")
        if max_seen > self.max_depth:
            raise PolicyViolation(f"AutoLISP nesting exceeds {self.max_depth}")

        lowered = text.lower()
        for token in self._blocked_tokens:
            if token in lowered:
                raise PolicyViolation(f"Blocked AutoLISP primitive detected: {token}")
        return text
