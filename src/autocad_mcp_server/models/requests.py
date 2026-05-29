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


# ─── FILE MANAGEMENT ────────────────────────────────────────────

class FileManagementRequest(BaseModel):
    action: Literal[
        "create_new",
        "open",
        "save",
        "save_as",
        "close",
        "list_open",
        "set_active",
        "get_properties",
    ]
    dwg_path: str = ""
    template_path: str = ""
    save_format: Literal["dwg", "dxf", "dwt"] = "dwg"
    save_changes: bool = True
    execution_mode: Literal["auto", "com", "core_console"] = "auto"


# ─── ANNOTATION ──────────────────────────────────────────────────

class AnnotationRequest(BaseModel):
    dwg_path: str
    operation: Literal[
        "add_leader",
        "add_multileader",
        "add_dimension_angular",
        "add_dimension_radial",
        "add_dimension_diameter",
        "add_dimension_ordinate",
        "add_table",
        "add_tolerance",
        "set_text_style",
        "set_dimension_style",
    ]
    parameters: dict[str, Any] = Field(default_factory=dict)
    execution_mode: Literal["auto", "com", "core_console"] = "auto"


# ─── BLOCK MANAGEMENT ───────────────────────────────────────────

class BlockManagementRequest(BaseModel):
    dwg_path: str
    action: Literal[
        "create_block_definition",
        "list_block_definitions",
        "get_block_attributes",
        "set_block_attributes",
        "explode_block",
        "rename_block",
        "count_block_references",
        "export_block_to_file",
        "import_block_from_file",
    ]
    parameters: dict[str, Any] = Field(default_factory=dict)
    execution_mode: Literal["auto", "com", "core_console"] = "auto"


# ─── XREF MANAGEMENT ────────────────────────────────────────────

class XrefManagementRequest(BaseModel):
    dwg_path: str
    action: Literal[
        "attach_xref",
        "detach_xref",
        "reload_xref",
        "bind_xref",
        "list_xrefs",
        "attach_image",
        "attach_pdf_underlay",
        "manage_xref_paths",
    ]
    parameters: dict[str, Any] = Field(default_factory=dict)
    execution_mode: Literal["auto", "com", "core_console"] = "auto"


# ─── EXPORT & CONVERSION ────────────────────────────────────────

class ExportRequest(BaseModel):
    dwg_path: str
    format: Literal[
        "pdf",
        "dxf",
        "dwf",
        "svg",
        "png",
        "jpg",
        "bmp",
        "stl",
    ]
    output_path: str = ""
    layout_name: str = "Model"
    scale: float = 1.0
    paper_size: str = "A3"
    color_mode: Literal["color", "monochrome", "grayscale"] = "color"
    layers_to_include: list[str] = Field(default_factory=list)
    resolution_dpi: int = 300
    execution_mode: Literal["auto", "com", "core_console"] = "auto"


# ─── BATCH PROCESSING ───────────────────────────────────────────

class BatchProcessingRequest(BaseModel):
    action: Literal[
        "batch_execute_script",
        "batch_update_attributes",
        "batch_layer_standards",
        "batch_convert_format",
        "batch_purge",
        "batch_audit",
        "create_macro",
        "run_macro",
        "list_macros",
    ]
    dwg_paths: list[str] = Field(default_factory=list)
    parameters: dict[str, Any] = Field(default_factory=dict)
    execution_mode: Literal["auto", "com", "core_console"] = "auto"


# ─── ANALYSIS & VALIDATION ──────────────────────────────────────

class AnalysisRequest(BaseModel):
    dwg_path: str
    operation: Literal[
        "check_drawing_standards",
        "find_overlapping_objects",
        "find_duplicate_objects",
        "find_zero_length_entities",
        "layer_usage_report",
        "object_count_by_type",
        "drawing_complexity_score",
        "detect_unclosed_polylines",
        "validate_dimensions",
        "compare_drawings",
        "generate_bom",
        "calculate_total_line_length",
        "count_blocks_in_area",
        "measure_perimeter",
        "find_text_containing",
        "replace_text",
        "list_all_text",
    ]
    parameters: dict[str, Any] = Field(default_factory=dict)
    execution_mode: Literal["auto", "com", "core_console"] = "auto"


# ─── EXPANDED CAD COMMANDS ───────────────────────────────────────

class AutoCadCommandRequest(BaseModel):
    dwg_path: str
    operation: Literal[
        # Basic drawing
        "draw_line",
        "draw_circle",
        "draw_rectangle",
        "draw_polyline",
        "draw_ellipse",
        "draw_arc",
        "draw_spline",
        # 3D primitives
        "draw_3d_box",
        "draw_3d_cylinder",
        "draw_3d_sphere",
        "draw_3d_cone",
        # Annotation
        "add_text",
        "add_hatch",
        "add_dimension",
        # Blocks & Layers
        "insert_block",
        "create_layer",
        # Object manipulation — existing
        "erase_object",
        "move_object",
        "rotate_object",
        "scale_object",
        "copy_object",
        # Object manipulation — new
        "offset_object",
        "mirror_object",
        "array_rectangular",
        "array_polar",
        "fillet_objects",
        "chamfer_objects",
        "explode_object",
        "join_objects",
        "break_object",
        "stretch_objects",
        "align_objects",
        "trim_object",
        "extend_object",
        # 3D Boolean
        "boolean_union",
        "boolean_subtract",
        "boolean_intersect",
        # Measurement
        "get_distance",
        "get_angle",
        "calculate_area",
        # Utility
        "purge_drawing",
        "audit_drawing",
        "zoom_extents",
        "send_command",
        # Object properties
        "change_object_color",
        "change_object_linetype",
        "change_object_lineweight",
        "change_object_layer",
    ]
    parameters: dict[str, Any] = Field(default_factory=dict)
    execution_mode: Literal["auto", "com", "core_console"] = "auto"

    @field_validator("parameters")
    @classmethod
    def _validate_parameters(cls, value: dict[str, Any]) -> dict[str, Any]:
        if len(value) > 50:
            raise ValueError("Too many parameters supplied")
        return value

    @field_validator("parameters")
    @classmethod
    def _validate_numeric_parameters(cls, value: dict[str, Any]) -> dict[str, Any]:
        for key in ("radius", "other_axis_radius", "scale_factor"):
            numeric = value.get(key)
            if numeric is not None and float(numeric) <= 0:
                raise ValueError(f"{key} must be greater than zero")
        points = value.get("points")
        if points is not None and len(points) == 0:
            raise ValueError("points must not be empty")
        return value
