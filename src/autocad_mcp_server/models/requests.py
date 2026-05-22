from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator


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


class GenerateElectricalBlueprintRequest(BaseModel):
    project_name: str = Field(min_length=1)
    discipline: Literal[
        "architecture",
        "structure",
        "mechanical",
        "electrical",
        "weak_current",
        "mixed",
    ] = "mixed"
    systems: list[str] = Field(default_factory=list)
    base_point: tuple[float, float] = (0.0, 0.0)
    sheet_width: float = 841.0
    sheet_height: float = 594.0
    outer_wall_thickness: float = 20.0
    inner_wall_thickness: float = 10.0
    output_name: str = Field(min_length=1, pattern=r"^[A-Za-z0-9_.-]+$")
    title_block_title: str = "UNIVERSAL DRAFT"
    legend_offset_x: float = 5000.0
    legend_offset_y: float = 0.0
    drawing_standard: str = "IEC_60617"


class AutoCadCommandRequest(BaseModel):
    dwg_path: str
    operation: Literal[
        "draw_line",
        "draw_circle",
        "draw_rectangle",
        "draw_polyline",
        "add_text",
        "add_hatch",
        "add_dimension",
        "insert_block",
        "create_layer",
        "zoom_extents",
        "send_command",
    ]
    parameters: dict[str, Any] = Field(default_factory=dict)
    execution_mode: Literal["auto", "com", "core_console"] = "auto"

    @field_validator("parameters")
    @classmethod
    def _validate_parameters(cls, value: dict[str, Any]) -> dict[str, Any]:
        if len(value) > 50:
            raise ValueError("Too many parameters supplied")
        return value
