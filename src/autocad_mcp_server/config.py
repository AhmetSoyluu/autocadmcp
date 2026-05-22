from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="AUTOCAD_MCP_",
        extra="ignore",
    )

    server_name: str = "autocadmcp"
    log_level: str = "INFO"
    allowed_dwg_roots: str = Field(default="")
    workspace_root: Path = Path("C:/temp/autocadmcp-workspaces")
    acad_path: Path | None = None
    accoreconsole_path: Path | None = None
    com_launch_if_missing: bool = False
    com_visible: bool = True
    com_timeout_seconds: int = 60
    core_console_timeout_seconds: int = 120
    max_entity_results: int = 200
    max_text_results: int = 200
    max_lisp_chars: int = 4000
    max_lisp_depth: int = 16
    keep_failed_workspaces: bool = True
    default_execution_mode: Literal["auto", "com", "core_console"] = "auto"

    @field_validator("workspace_root", mode="before")
    @classmethod
    def validate_workspace_root(cls, value: str | Path) -> Path:
        path = Path(value).expanduser()
        if not path.is_absolute():
            raise ValueError("workspace_root must be an absolute path")
        return path

    @property
    def allowed_root_paths(self) -> list[Path]:
        roots: list[Path] = []
        for raw in self.allowed_dwg_roots.split(";"):
            candidate = raw.strip()
            if not candidate:
                continue
            path = Path(candidate).expanduser()
            if not path.is_absolute():
                raise ValueError(f"Allowed DWG root must be absolute: {candidate}")
            roots.append(path)
        return roots
