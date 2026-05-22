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
