from __future__ import annotations

import re
from dataclasses import dataclass

from autocad_mcp_server.utils.errors import PolicyViolation


@dataclass(frozen=True)
class LispPolicy:
    max_chars: int
    max_depth: int

    _blocked_tokens = {
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
        "eval",
        "read",
        "load",
        "vl-load-all",
        "vl-registry-read",
        "vl-registry-write",
    }

    _token_pattern = re.compile(r"\(([a-zA-Z0-9_\-\.\+:]+)")

    def _strip_strings_and_comments(self, text: str) -> str:
        no_comments = re.sub(r";.*$", "", text, flags=re.MULTILINE)
        no_strings = re.sub(r'"(?:[^"\\]|\\.)*"', '""', no_comments)
        return no_strings

    def _validate_structure(self, text: str) -> None:
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

    def _validate_tokens(self, text: str) -> None:
        for match in self._token_pattern.finditer(text):
            token = match.group(1).lower()
            if token in self._blocked_tokens:
                raise PolicyViolation(f"Blocked AutoLISP primitive detected: {token}")

    def validate(self, source: str) -> str:
        text = source.strip()
        if not text:
            raise PolicyViolation("AutoLISP source cannot be empty")
        if len(text) > self.max_chars:
            raise PolicyViolation(f"AutoLISP exceeds {self.max_chars} characters")

        sanitized = self._strip_strings_and_comments(text)
        self._validate_structure(sanitized)
        self._validate_tokens(sanitized)
        return text
