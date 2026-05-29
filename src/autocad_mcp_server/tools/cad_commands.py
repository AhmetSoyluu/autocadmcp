from __future__ import annotations

from autocad_mcp_server.models.requests import AutoCadCommandRequest
from autocad_mcp_server.services.dwg_service import DWGService
from autocad_mcp_server.tools.common import error_response, success_response


def register_cad_commands_tool(mcp, service: DWGService) -> None:  # noqa: C901
    # ─── BASIC DRAWING ────────────────────────────────────────────

    @mcp.tool()
    async def draw_line(dwg_path: str, x1: float, y1: float, x2: float, y2: float, execution_mode: str = "auto") -> dict:
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="draw_line",
            parameters={"x1": x1, "y1": y1, "x2": x2, "y2": y2},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("draw_line", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("draw_line", execution_mode, exc)

    @mcp.tool()
    async def draw_circle(dwg_path: str, cx: float, cy: float, radius: float, execution_mode: str = "auto") -> dict:
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="draw_circle",
            parameters={"cx": cx, "cy": cy, "radius": radius},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("draw_circle", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("draw_circle", execution_mode, exc)

    @mcp.tool()
    async def draw_rectangle(dwg_path: str, x: float, y: float, width: float, height: float, execution_mode: str = "auto") -> dict:
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="draw_rectangle",
            parameters={"x": x, "y": y, "width": width, "height": height},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("draw_rectangle", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("draw_rectangle", execution_mode, exc)

    @mcp.tool()
    async def draw_polyline(dwg_path: str, points: list[list[float]], execution_mode: str = "auto") -> dict:
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="draw_polyline",
            parameters={"points": points},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("draw_polyline", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("draw_polyline", execution_mode, exc)

    @mcp.tool()
    async def add_text(
        dwg_path: str,
        text: str,
        x: float,
        y: float,
        height: float = 2.5,
        execution_mode: str = "auto",
    ) -> dict:
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="add_text",
            parameters={"text": text, "x": x, "y": y, "height": height},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("add_text", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("add_text", execution_mode, exc)

    @mcp.tool()
    async def add_hatch(
        dwg_path: str,
        pattern_name: str = "ANSI31",
        execution_mode: str = "auto",
    ) -> dict:
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="add_hatch",
            parameters={"pattern_name": pattern_name},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("add_hatch", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("add_hatch", execution_mode, exc)

    @mcp.tool()
    async def add_dimension(
        dwg_path: str,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        text_x: float,
        text_y: float,
        execution_mode: str = "auto",
    ) -> dict:
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="add_dimension",
            parameters={
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2,
                "text_x": text_x,
                "text_y": text_y,
            },
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("add_dimension", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("add_dimension", execution_mode, exc)

    @mcp.tool()
    async def insert_block(
        dwg_path: str,
        block_name: str,
        x: float,
        y: float,
        scale: float = 1,
        rotation_deg: float = 0,
        execution_mode: str = "auto",
    ) -> dict:
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="insert_block",
            parameters={
                "block_name": block_name,
                "x": x,
                "y": y,
                "scale": scale,
                "rotation_deg": rotation_deg,
            },
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("insert_block", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("insert_block", execution_mode, exc)

    @mcp.tool()
    async def create_layer(
        dwg_path: str,
        name: str,
        color_index: int = 7,
        execution_mode: str = "auto",
    ) -> dict:
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="create_layer",
            parameters={"name": name, "color_index": color_index},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("create_layer", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("create_layer", execution_mode, exc)

    @mcp.tool()
    async def draw_ellipse(
        dwg_path: str,
        cx: float,
        cy: float,
        ex: float,
        ey: float,
        other_axis_radius: float,
        execution_mode: str = "auto",
    ) -> dict:
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="draw_ellipse",
            parameters={
                "cx": cx,
                "cy": cy,
                "ex": ex,
                "ey": ey,
                "other_axis_radius": other_axis_radius,
            },
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("draw_ellipse", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("draw_ellipse", execution_mode, exc)

    @mcp.tool()
    async def draw_arc(
        dwg_path: str,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        x3: float,
        y3: float,
        execution_mode: str = "auto",
    ) -> dict:
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="draw_arc",
            parameters={"x1": x1, "y1": y1, "x2": x2, "y2": y2, "x3": x3, "y3": y3},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("draw_arc", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("draw_arc", execution_mode, exc)

    @mcp.tool()
    async def draw_spline(dwg_path: str, points: list[list[float]], execution_mode: str = "auto") -> dict:
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="draw_spline",
            parameters={"points": points},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("draw_spline", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("draw_spline", execution_mode, exc)

    # ─── 3D PRIMITIVES ────────────────────────────────────────────

    @mcp.tool()
    async def draw_3d_box(
        dwg_path: str,
        length: float,
        width: float,
        height: float,
        x: float = 0,
        y: float = 0,
        z: float = 0,
        execution_mode: str = "auto",
    ) -> dict:
        """Draw a 3D solid box starting at corner (x,y,z) with given dimensions."""
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="draw_3d_box",
            parameters={"x": x, "y": y, "z": z, "length": length, "width": width, "height": height},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("draw_3d_box", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("draw_3d_box", execution_mode, exc)

    @mcp.tool()
    async def draw_3d_cylinder(
        dwg_path: str,
        radius: float,
        height: float,
        cx: float = 0,
        cy: float = 0,
        cz: float = 0,
        execution_mode: str = "auto",
    ) -> dict:
        """Draw a 3D solid cylinder centered at (cx,cy,cz)."""
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="draw_3d_cylinder",
            parameters={"cx": cx, "cy": cy, "cz": cz, "radius": radius, "height": height},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("draw_3d_cylinder", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("draw_3d_cylinder", execution_mode, exc)

    @mcp.tool()
    async def draw_3d_sphere(
        dwg_path: str,
        radius: float,
        cx: float = 0,
        cy: float = 0,
        cz: float = 0,
        execution_mode: str = "auto",
    ) -> dict:
        """Draw a 3D solid sphere centered at (cx,cy,cz)."""
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="draw_3d_sphere",
            parameters={"cx": cx, "cy": cy, "cz": cz, "radius": radius},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("draw_3d_sphere", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("draw_3d_sphere", execution_mode, exc)

    @mcp.tool()
    async def draw_3d_cone(
        dwg_path: str,
        radius: float,
        height: float,
        cx: float = 0,
        cy: float = 0,
        cz: float = 0,
        execution_mode: str = "auto",
    ) -> dict:
        """Draw a 3D solid cone centered at (cx,cy,cz)."""
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="draw_3d_cone",
            parameters={"cx": cx, "cy": cy, "cz": cz, "radius": radius, "height": height},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("draw_3d_cone", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("draw_3d_cone", execution_mode, exc)

    # ─── OBJECT MANIPULATION — EXISTING ──────────────────────────

    @mcp.tool()
    async def erase_object(dwg_path: str, handle: str, execution_mode: str = "auto") -> dict:
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="erase_object",
            parameters={"handle": handle},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("erase_object", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("erase_object", execution_mode, exc)

    @mcp.tool()
    async def move_object(
        dwg_path: str,
        handle: str,
        bx: float,
        by: float,
        dx: float,
        dy: float,
        execution_mode: str = "auto",
    ) -> dict:
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="move_object",
            parameters={"handle": handle, "bx": bx, "by": by, "dx": dx, "dy": dy},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("move_object", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("move_object", execution_mode, exc)

    @mcp.tool()
    async def rotate_object(
        dwg_path: str,
        handle: str,
        bx: float,
        by: float,
        angle_deg: float,
        execution_mode: str = "auto",
    ) -> dict:
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="rotate_object",
            parameters={"handle": handle, "bx": bx, "by": by, "angle_deg": angle_deg},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("rotate_object", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("rotate_object", execution_mode, exc)

    @mcp.tool()
    async def scale_object(
        dwg_path: str,
        handle: str,
        bx: float,
        by: float,
        scale_factor: float,
        execution_mode: str = "auto",
    ) -> dict:
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="scale_object",
            parameters={"handle": handle, "bx": bx, "by": by, "scale_factor": scale_factor},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("scale_object", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("scale_object", execution_mode, exc)

    @mcp.tool()
    async def copy_object(
        dwg_path: str,
        handle: str,
        bx: float,
        by: float,
        dx: float,
        dy: float,
        execution_mode: str = "auto",
    ) -> dict:
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="copy_object",
            parameters={"handle": handle, "bx": bx, "by": by, "dx": dx, "dy": dy},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("copy_object", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("copy_object", execution_mode, exc)

    # ─── OBJECT MANIPULATION — NEW ───────────────────────────────

    @mcp.tool()
    async def offset_object(
        dwg_path: str,
        handle: str,
        distance: float,
        side_x: float = 0,
        side_y: float = 0,
        execution_mode: str = "auto",
    ) -> dict:
        """Offset an object by a specified distance. side_x/side_y indicates which side to offset to."""
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="offset_object",
            parameters={"handle": handle, "distance": distance, "side_x": side_x, "side_y": side_y},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("offset_object", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("offset_object", execution_mode, exc)

    @mcp.tool()
    async def mirror_object(
        dwg_path: str,
        handle: str,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        execution_mode: str = "auto",
    ) -> dict:
        """Mirror an object across a line defined by two points. Original is kept."""
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="mirror_object",
            parameters={"handle": handle, "x1": x1, "y1": y1, "x2": x2, "y2": y2},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("mirror_object", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("mirror_object", execution_mode, exc)

    @mcp.tool()
    async def array_rectangular(
        dwg_path: str,
        handle: str,
        rows: int = 2,
        columns: int = 2,
        row_spacing: float = 100,
        col_spacing: float = 100,
        execution_mode: str = "auto",
    ) -> dict:
        """Create a rectangular array of an object."""
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="array_rectangular",
            parameters={
                "handle": handle,
                "rows": rows,
                "columns": columns,
                "row_spacing": row_spacing,
                "col_spacing": col_spacing,
            },
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("array_rectangular", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("array_rectangular", execution_mode, exc)

    @mcp.tool()
    async def array_polar(
        dwg_path: str,
        handle: str,
        cx: float,
        cy: float,
        count: int = 6,
        fill_angle: float = 360,
        execution_mode: str = "auto",
    ) -> dict:
        """Create a polar (circular) array of an object around center (cx,cy)."""
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="array_polar",
            parameters={"handle": handle, "cx": cx, "cy": cy, "count": count, "fill_angle": fill_angle},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("array_polar", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("array_polar", execution_mode, exc)

    @mcp.tool()
    async def fillet_objects(
        dwg_path: str,
        handle1: str,
        handle2: str,
        radius: float = 0,
        execution_mode: str = "auto",
    ) -> dict:
        """Apply a fillet (rounded corner) between two objects."""
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="fillet_objects",
            parameters={"handle1": handle1, "handle2": handle2, "radius": radius},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("fillet_objects", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("fillet_objects", execution_mode, exc)

    @mcp.tool()
    async def chamfer_objects(
        dwg_path: str,
        handle1: str,
        handle2: str,
        distance1: float = 10,
        distance2: float = 10,
        execution_mode: str = "auto",
    ) -> dict:
        """Apply a chamfer (angled corner) between two objects."""
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="chamfer_objects",
            parameters={"handle1": handle1, "handle2": handle2, "distance1": distance1, "distance2": distance2},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("chamfer_objects", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("chamfer_objects", execution_mode, exc)

    @mcp.tool()
    async def explode_object(dwg_path: str, handle: str, execution_mode: str = "auto") -> dict:
        """Explode a compound object (block, polyline, etc.) into individual entities."""
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="explode_object",
            parameters={"handle": handle},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("explode_object", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("explode_object", execution_mode, exc)

    @mcp.tool()
    async def join_objects(dwg_path: str, handles: list[str], execution_mode: str = "auto") -> dict:
        """Join multiple contiguous objects into a single entity."""
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="join_objects",
            parameters={"handles": handles},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("join_objects", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("join_objects", execution_mode, exc)

    @mcp.tool()
    async def break_object(
        dwg_path: str,
        handle: str,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        execution_mode: str = "auto",
    ) -> dict:
        """Break an object at two specified points."""
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="break_object",
            parameters={"handle": handle, "x1": x1, "y1": y1, "x2": x2, "y2": y2},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("break_object", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("break_object", execution_mode, exc)

    @mcp.tool()
    async def stretch_objects(
        dwg_path: str,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        bx: float,
        by: float,
        dx: float,
        dy: float,
        execution_mode: str = "auto",
    ) -> dict:
        """Stretch objects within a crossing window. (x1,y1)-(x2,y2) is the window, (bx,by)->(dx,dy) is displacement."""
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="stretch_objects",
            parameters={"x1": x1, "y1": y1, "x2": x2, "y2": y2, "bx": bx, "by": by, "dx": dx, "dy": dy},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("stretch_objects", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("stretch_objects", execution_mode, exc)

    @mcp.tool()
    async def align_objects(
        dwg_path: str,
        handle: str,
        src_x1: float,
        src_y1: float,
        dst_x1: float,
        dst_y1: float,
        src_x2: float,
        src_y2: float,
        dst_x2: float,
        dst_y2: float,
        scale: bool = False,
        execution_mode: str = "auto",
    ) -> dict:
        """Align an object using source and destination point pairs."""
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="align_objects",
            parameters={
                "handle": handle,
                "src_x1": src_x1, "src_y1": src_y1,
                "dst_x1": dst_x1, "dst_y1": dst_y1,
                "src_x2": src_x2, "src_y2": src_y2,
                "dst_x2": dst_x2, "dst_y2": dst_y2,
                "scale": scale,
            },
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("align_objects", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("align_objects", execution_mode, exc)

    @mcp.tool()
    async def trim_object(
        dwg_path: str,
        cutting_handle: str,
        target_x: float,
        target_y: float,
        execution_mode: str = "auto",
    ) -> dict:
        """Trim an object at a cutting boundary. target_x/target_y selects which side to trim."""
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="trim_object",
            parameters={"cutting_handle": cutting_handle, "target_x": target_x, "target_y": target_y},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("trim_object", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("trim_object", execution_mode, exc)

    @mcp.tool()
    async def extend_object(
        dwg_path: str,
        boundary_handle: str,
        target_x: float,
        target_y: float,
        execution_mode: str = "auto",
    ) -> dict:
        """Extend an object to reach a boundary edge."""
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="extend_object",
            parameters={"boundary_handle": boundary_handle, "target_x": target_x, "target_y": target_y},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("extend_object", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("extend_object", execution_mode, exc)

    # ─── 3D BOOLEAN OPERATIONS ───────────────────────────────────

    @mcp.tool()
    async def boolean_union(dwg_path: str, handle1: str, handle2: str, execution_mode: str = "auto") -> dict:
        """Unite two 3D solids into one."""
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="boolean_union",
            parameters={"handle1": handle1, "handle2": handle2},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("boolean_union", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("boolean_union", execution_mode, exc)

    @mcp.tool()
    async def boolean_subtract(dwg_path: str, handle1: str, handle2: str, execution_mode: str = "auto") -> dict:
        """Subtract one 3D solid from another."""
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="boolean_subtract",
            parameters={"handle1": handle1, "handle2": handle2},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("boolean_subtract", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("boolean_subtract", execution_mode, exc)

    @mcp.tool()
    async def boolean_intersect(dwg_path: str, handle1: str, handle2: str, execution_mode: str = "auto") -> dict:
        """Keep only the intersecting volume of two 3D solids."""
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="boolean_intersect",
            parameters={"handle1": handle1, "handle2": handle2},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("boolean_intersect", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("boolean_intersect", execution_mode, exc)

    # ─── MEASUREMENT ─────────────────────────────────────────────

    @mcp.tool()
    async def get_distance(
        dwg_path: str,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        execution_mode: str = "auto",
    ) -> dict:
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="get_distance",
            parameters={"x1": x1, "y1": y1, "x2": x2, "y2": y2},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("get_distance", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("get_distance", execution_mode, exc)

    @mcp.tool()
    async def get_angle(
        dwg_path: str,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        execution_mode: str = "auto",
    ) -> dict:
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="get_angle",
            parameters={"x1": x1, "y1": y1, "x2": x2, "y2": y2},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("get_angle", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("get_angle", execution_mode, exc)

    @mcp.tool()
    async def calculate_area(
        dwg_path: str,
        handle: str | None = None,
        points: list[list[float]] | None = None,
        execution_mode: str = "auto",
    ) -> dict:
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="calculate_area",
            parameters={"handle": handle, "points": points or []},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("calculate_area", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("calculate_area", execution_mode, exc)

    # ─── UTILITY ─────────────────────────────────────────────────

    @mcp.tool()
    async def purge_drawing(dwg_path: str, execution_mode: str = "auto") -> dict:
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="purge_drawing",
            parameters={},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("purge_drawing", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("purge_drawing", execution_mode, exc)

    @mcp.tool()
    async def audit_drawing(dwg_path: str, execution_mode: str = "auto") -> dict:
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="audit_drawing",
            parameters={},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("audit_drawing", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("audit_drawing", execution_mode, exc)

    @mcp.tool()
    async def zoom_extents(dwg_path: str, execution_mode: str = "auto") -> dict:
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="zoom_extents",
            parameters={},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("zoom_extents", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("zoom_extents", execution_mode, exc)

    @mcp.tool()
    async def send_command(dwg_path: str, command_string: str, execution_mode: str = "auto") -> dict:
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="send_command",
            parameters={"command_string": command_string},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("send_command", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("send_command", execution_mode, exc)

    # ─── OBJECT PROPERTIES ───────────────────────────────────────

    @mcp.tool()
    async def change_object_color(
        dwg_path: str,
        handle: str,
        color_index: int,
        execution_mode: str = "auto",
    ) -> dict:
        """Change the ACI color of an object (1=Red, 2=Yellow, 3=Green, etc.)."""
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="change_object_color",
            parameters={"handle": handle, "color_index": color_index},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("change_object_color", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("change_object_color", execution_mode, exc)

    @mcp.tool()
    async def change_object_linetype(
        dwg_path: str,
        handle: str,
        linetype: str,
        execution_mode: str = "auto",
    ) -> dict:
        """Change the linetype of an object (e.g. 'DASHED', 'CENTER', 'HIDDEN')."""
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="change_object_linetype",
            parameters={"handle": handle, "linetype": linetype},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("change_object_linetype", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("change_object_linetype", execution_mode, exc)

    @mcp.tool()
    async def change_object_lineweight(
        dwg_path: str,
        handle: str,
        lineweight: int,
        execution_mode: str = "auto",
    ) -> dict:
        """Change the lineweight of an object (in hundredths of mm, e.g. 50 = 0.50mm)."""
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="change_object_lineweight",
            parameters={"handle": handle, "lineweight": lineweight},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("change_object_lineweight", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("change_object_lineweight", execution_mode, exc)

    @mcp.tool()
    async def change_object_layer(
        dwg_path: str,
        handle: str,
        layer_name: str,
        execution_mode: str = "auto",
    ) -> dict:
        """Move an object to a different layer."""
        request = AutoCadCommandRequest(
            dwg_path=dwg_path,
            operation="change_object_layer",
            parameters={"handle": handle, "layer_name": layer_name},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_cad_command(request)
            return success_response("change_object_layer", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("change_object_layer", execution_mode, exc)

