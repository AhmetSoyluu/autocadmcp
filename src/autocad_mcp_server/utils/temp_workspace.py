from __future__ import annotations

import shutil
import uuid
from pathlib import Path


class TempWorkspaceManager:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def create(self, prefix: str) -> Path:
        workspace = self.root / f"{prefix}-{uuid.uuid4().hex[:12]}"
        workspace.mkdir(parents=True, exist_ok=False)
        return workspace

    def cleanup(self, workspace: Path, keep: bool = False) -> None:
        if keep or not workspace.exists():
            return
        shutil.rmtree(workspace, ignore_errors=True)
