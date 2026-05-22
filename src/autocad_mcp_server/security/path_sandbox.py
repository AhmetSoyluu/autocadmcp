from __future__ import annotations

from pathlib import Path

from autocad_mcp_server.utils.errors import SandboxViolation


class PathSandbox:
    def __init__(self, allowed_roots: list[Path]) -> None:
        if not allowed_roots:
            raise ValueError("At least one allowed DWG root must be configured")
        self.allowed_roots = [self._normalize(root) for root in allowed_roots]

    def validate(self, candidate: str | Path) -> Path:
        normalized = self._normalize(Path(candidate))
        for root in self.allowed_roots:
            try:
                normalized.relative_to(root)
                return normalized
            except ValueError:
                continue
        raise SandboxViolation(f"Path is outside allowed roots: {normalized}")

    @staticmethod
    def _normalize(path: Path) -> Path:
        resolved = path.expanduser().resolve(strict=False)
        return Path(str(resolved).lower())
