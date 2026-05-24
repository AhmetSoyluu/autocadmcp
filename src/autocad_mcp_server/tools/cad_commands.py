from __future__ import annotations

from autocad_mcp_server.models.requests import AutoCadCommandRequest
from autocad_mcp_server.services.dwg_service import DWGService
from autocad_mcp_server.tools.common import error_response, success_response


def register_cad_commands_tool(mcp, service: DWGService) -> None:
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
