from __future__ import annotations

import json
import shutil
import uuid
from pathlib import Path
from typing import Any


class TempWorkspaceManager:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def create(self, prefix: str) -> Path:
        workspace = self.root / f"{prefix}-{uuid.uuid4().hex[:12]}"
        workspace.mkdir(parents=True, exist_ok=False)
        return workspace

    def write_manifest(self, workspace: Path, data: dict[str, Any]) -> None:
        (workspace / "manifest.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def cleanup(self, workspace: Path, keep: bool = False) -> None:
        if keep or not workspace.exists():
            return
        shutil.rmtree(workspace, ignore_errors=True)

    def cleanup_stale_workspaces(self) -> int:
        removed = 0
        for child in self.root.iterdir():
            if child.is_dir() and not (child / "manifest.json").exists():
                shutil.rmtree(child, ignore_errors=True)
                removed += 1
        return removed

    def count_retained_workspaces(self) -> int:
        return sum(1 for child in self.root.iterdir() if child.is_dir())
