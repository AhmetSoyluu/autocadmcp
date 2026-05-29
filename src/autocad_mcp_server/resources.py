from __future__ import annotations

from autocad_mcp_server.services.drawing_state_cache import DrawingStateCache
from autocad_mcp_server.services.dwg_service import DWGService
from autocad_mcp_server.services.runtime_supervisor import RuntimeSupervisor


def register_resources(mcp, service: DWGService, supervisor: RuntimeSupervisor, cache: DrawingStateCache) -> None:
    """Register MCP Resources — browsable context about AutoCAD state."""

    @mcp.resource("autocad://server/status")
    async def server_status_resource() -> str:
        """Current server health and connection status."""
        state = supervisor.state
        lines = [
            "# AutoCAD MCP Server Status",
            "",
            f"- Core Console Healthy: {state.core_console_healthy}",
            f"- COM Healthy: {state.com_healthy}",
            f"- Queue Depth: {state.queue_depth}",
            f"- Total Jobs: {state.total_jobs_processed}",
            f"- Last Started: {state.last_started_at or 'N/A'}",
            f"- Last Failure: {state.last_failure_reason or 'None'}",
        ]
        return "\n".join(lines)

    @mcp.resource("autocad://server/capabilities")
    async def capabilities_resource() -> str:
        """List of all available tool categories and their operations."""
        return """# AutoCAD MCP Capabilities

## Drawing Operations
- draw_line, draw_circle, draw_rectangle, draw_polyline, draw_arc, draw_ellipse, draw_spline
- draw_3d_box, draw_3d_cylinder, draw_3d_sphere, draw_3d_cone

## Object Manipulation
- offset_object, mirror_object, array_rectangular, array_polar
- fillet_objects, chamfer_objects, explode_object, join_objects
- trim_object, extend_object, break_object, stretch_objects, align_objects
- move_object, rotate_object, scale_object, copy_object, erase_object

## 3D Booleans
- boolean_union, boolean_subtract, boolean_intersect

## Property Changes
- change_object_color, change_object_linetype, change_object_lineweight, change_object_layer

## Annotations
- add_leader, add_multileader
- add_dimension, add_dimension_angular, add_dimension_radial, add_dimension_diameter
- add_text, add_table
- set_text_style, set_dimension_style

## Block Management
- create_block_definition, list_block_definitions, insert_block
- get_block_attributes, set_block_attributes
- explode_block, rename_block, count_block_references, import_block_from_file

## External References
- attach_xref, detach_xref, reload_xref, bind_xref, list_xrefs
- attach_image, attach_pdf_underlay

## File Management
- create_new_drawing, open_drawing, save_drawing, save_drawing_as
- close_drawing, list_open_drawings, set_active_drawing, get_drawing_properties

## Export
- export_to_pdf, export_to_dxf, export_to_dwf, export_to_image, export_to_stl
- export_layer_to_pdf

## Batch Processing
- batch_execute_script, batch_update_attributes, batch_layer_standards
- batch_purge, batch_audit
- create_macro, run_macro, list_macros

## Analysis
- check_drawing_standards, find_overlapping_objects, find_duplicate_objects
- layer_usage_report, object_count_by_type, drawing_complexity_score
- detect_unclosed_polylines, compare_drawings, generate_bom
- calculate_total_line_length, find_text_containing, replace_text, list_all_text

## Undo/Redo
- undo_last_action, redo_last_action, undo_multiple
- get_undo_history, set_undo_mark, end_undo_mark

## Cache
- refresh_drawing_cache, get_cached_drawing_state, invalidate_cache, get_cache_stats

## Metadata & Query
- read_dwg_metadata, query_geometry
- execute_autolisp, manage_layers_and_blocks
- get_distance, get_angle, calculate_area

## Utilities
- purge_drawing, audit_drawing, zoom_extents
- send_command, get_server_status
"""

    @mcp.resource("autocad://drawings/cached")
    async def cached_drawings_resource() -> str:
        """Summary of all drawings currently in the state cache."""
        stats = cache.get_stats()
        if not stats["entries"]:
            return "# Cached Drawings\n\nNo drawings in cache. Use `refresh_drawing_cache` to populate."
        lines = ["# Cached Drawings", ""]
        for entry in stats["entries"]:
            stale_marker = " ⚠️ STALE" if entry["stale"] else " ✅"
            lines.append(f"## {entry['drawing']}{stale_marker}")
            lines.append(f"- Entities: {entry['entity_count']}")
            lines.append(f"- Layers: {entry['layers']}")
            lines.append(f"- Blocks: {entry['blocks']}")
            lines.append(f"- Age: {entry['age_seconds']}s")
            lines.append("")
        return "\n".join(lines)

    @mcp.resource("autocad://conventions/lisp")
    async def lisp_conventions_resource() -> str:
        """AutoLISP conventions and best practices for this MCP."""
        return """# AutoLISP Conventions for this MCP

## Object Selection
- Use `(handent "HANDLE")` to select objects by handle
- Use `(ssget "X" filter_list)` for selection sets
- Use `(vlax-ename->vla-object ent)` to convert to VLA objects

## Result Output
- Use `MCP_RESULT:KEY=VALUE` for structured results
- Use `MCP_BLOCK:`, `MCP_LAYER:`, `MCP_TEXT:` etc. for typed output lines
- Always end with `(princ)` to suppress echo

## VLA Patterns
- `(vlax-get-acad-object)` — Application object
- `(vla-get-activedocument ...)` — Active document
- `(vla-get-modelspace ...)` — Model space

## Command Conventions
- Always prefix commands with `_.` for internationalization
- Use `_` prefix for option keywords (e.g., `"_A"` for All)
- Pass coordinates as `"x,y"` or `"x,y,z"` strings

## Security
- Max LISP length: 4000 chars
- Max nesting depth: 16
- Forbidden: file I/O, shell execution, network access
"""

    @mcp.resource("autocad://conventions/layers")
    async def layer_conventions_resource() -> str:
        """Standard layer naming conventions for CAD drawings."""
        return """# CAD Layer Naming Conventions

## AIA/NCS Standard Layer Format
`<Discipline>-<Major Group>-<Minor Group 1>-<Minor Group 2>-<Status>`

## Common Discipline Codes
| Code | Discipline |
|------|-----------|
| A | Architectural |
| C | Civil |
| E | Electrical |
| F | Fire Protection |
| G | General |
| I | Interiors |
| L | Landscape |
| M | Mechanical |
| P | Plumbing |
| S | Structural |

## Common Major Groups
| Group | Description |
|-------|------------|
| WALL | Walls |
| DOOR | Doors |
| GLAZ | Windows/Glazing |
| COLS | Columns |
| FLOR | Floor |
| CEIL | Ceiling |
| ROOF | Roof |
| DIMS | Dimensions |
| ANNO | Annotations |
| SYMB | Symbols |
| EQPM | Equipment |
| FURN | Furniture |

## Status Suffixes
| Suffix | Meaning |
|--------|---------|
| -N | New work |
| -E | Existing |
| -D | Demolition |
| -T | Temporary |
| -F | Future |

## Color Standards
| Color | Common Use |
|-------|-----------|
| 1 (Red) | Walls, Structure |
| 2 (Yellow) | Text, Annotations |
| 3 (Green) | Doors, Windows |
| 4 (Cyan) | Furniture |
| 5 (Blue) | Equipment |
| 6 (Magenta) | Dimensions |
| 7 (White) | General/Viewport |
"""
