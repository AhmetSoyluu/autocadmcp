from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class ReadDwgMetadataRequest(BaseModel):
    dwg_path: str
    include_text: bool = True
    include_blocks: bool = True
    include_layers: bool = True
    execution_mode: Literal["auto", "com", "core_console"] = "auto"


class ExecuteAutolispRequest(BaseModel):
    dwg_path: str
    lisp_source: str = Field(min_length=1)
    target: Literal["live_session", "background"] = "live_session"
    execution_mode: Literal["auto", "com", "core_console"] = "auto"


class QueryGeometryRequest(BaseModel):
    dwg_path: str
    entity_types: list[str] = Field(default_factory=list)
    layers: list[str] = Field(default_factory=list)
    block_names: list[str] = Field(default_factory=list)
    handles: list[str] = Field(default_factory=list)
    limit: int = 100
    execution_mode: Literal["auto", "com", "core_console"] = "auto"


class ManageLayersAndBlocksRequest(BaseModel):
    dwg_path: str
    action: Literal[
        "create_layer",
        "freeze_layer",
        "thaw_layer",
        "lock_layer",
        "unlock_layer",
        "insert_block",
    ]
    parameters: dict[str, Any] = Field(default_factory=dict)
    execution_mode: Literal["auto", "com", "core_console"] = "auto"
