from __future__ import annotations

from autocad_mcp_server.models.requests import AnnotationRequest
from autocad_mcp_server.services.dwg_service import DWGService
from autocad_mcp_server.tools.common import error_response, success_response


def register_annotation_tool(mcp, service: DWGService) -> None:
    @mcp.tool()
    async def add_leader(
        dwg_path: str,
        start_x: float,
        start_y: float,
        end_x: float,
        end_y: float,
        text: str = "",
        execution_mode: str = "auto",
    ) -> dict:
        """Add a leader (arrow with annotation text) from start point to end point."""
        request = AnnotationRequest(
            dwg_path=dwg_path,
            operation="add_leader",
            parameters={"start_x": start_x, "start_y": start_y, "end_x": end_x, "end_y": end_y, "text": text},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_annotation(request)
            return success_response("add_leader", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("add_leader", execution_mode, exc)

    @mcp.tool()
    async def add_multileader(
        dwg_path: str,
        start_x: float,
        start_y: float,
        landing_x: float,
        landing_y: float,
        text: str,
        execution_mode: str = "auto",
    ) -> dict:
        """Add a multileader (modern annotation with arrow and text box)."""
        request = AnnotationRequest(
            dwg_path=dwg_path,
            operation="add_multileader",
            parameters={"start_x": start_x, "start_y": start_y, "landing_x": landing_x, "landing_y": landing_y, "text": text},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_annotation(request)
            return success_response("add_multileader", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("add_multileader", execution_mode, exc)

    @mcp.tool()
    async def add_dimension_angular(
        dwg_path: str,
        cx: float,
        cy: float,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        text_x: float,
        text_y: float,
        execution_mode: str = "auto",
    ) -> dict:
        """Add an angular dimension between two lines from a vertex."""
        request = AnnotationRequest(
            dwg_path=dwg_path,
            operation="add_dimension_angular",
            parameters={"cx": cx, "cy": cy, "x1": x1, "y1": y1, "x2": x2, "y2": y2, "text_x": text_x, "text_y": text_y},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_annotation(request)
            return success_response("add_dimension_angular", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("add_dimension_angular", execution_mode, exc)

    @mcp.tool()
    async def add_dimension_radial(
        dwg_path: str,
        handle: str,
        text_x: float,
        text_y: float,
        execution_mode: str = "auto",
    ) -> dict:
        """Add a radial dimension to a circle or arc (identified by handle)."""
        request = AnnotationRequest(
            dwg_path=dwg_path,
            operation="add_dimension_radial",
            parameters={"handle": handle, "text_x": text_x, "text_y": text_y},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_annotation(request)
            return success_response("add_dimension_radial", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("add_dimension_radial", execution_mode, exc)

    @mcp.tool()
    async def add_dimension_diameter(
        dwg_path: str,
        handle: str,
        text_x: float,
        text_y: float,
        execution_mode: str = "auto",
    ) -> dict:
        """Add a diameter dimension to a circle or arc (identified by handle)."""
        request = AnnotationRequest(
            dwg_path=dwg_path,
            operation="add_dimension_diameter",
            parameters={"handle": handle, "text_x": text_x, "text_y": text_y},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_annotation(request)
            return success_response("add_dimension_diameter", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("add_dimension_diameter", execution_mode, exc)

    @mcp.tool()
    async def add_table(
        dwg_path: str,
        x: float,
        y: float,
        rows: int,
        columns: int,
        row_height: float = 10,
        col_width: float = 40,
        data: list[list[str]] | None = None,
        title: str = "",
        execution_mode: str = "auto",
    ) -> dict:
        """Create a table at (x,y) with optional data as a list of rows."""
        request = AnnotationRequest(
            dwg_path=dwg_path,
            operation="add_table",
            parameters={
                "x": x, "y": y, "rows": rows, "columns": columns,
                "row_height": row_height, "col_width": col_width,
                "data": data or [], "title": title,
            },
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_annotation(request)
            return success_response("add_table", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("add_table", execution_mode, exc)

    @mcp.tool()
    async def set_text_style(
        dwg_path: str,
        style_name: str,
        font_name: str = "Arial",
        height: float = 0,
        width_factor: float = 1.0,
        execution_mode: str = "auto",
    ) -> dict:
        """Create or modify a text style."""
        request = AnnotationRequest(
            dwg_path=dwg_path,
            operation="set_text_style",
            parameters={"style_name": style_name, "font_name": font_name, "height": height, "width_factor": width_factor},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_annotation(request)
            return success_response("set_text_style", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("set_text_style", execution_mode, exc)

    @mcp.tool()
    async def set_dimension_style(
        dwg_path: str,
        style_name: str,
        text_height: float = 2.5,
        arrow_size: float = 2.5,
        precision: int = 2,
        execution_mode: str = "auto",
    ) -> dict:
        """Create or modify a dimension style."""
        request = AnnotationRequest(
            dwg_path=dwg_path,
            operation="set_dimension_style",
            parameters={"style_name": style_name, "text_height": text_height, "arrow_size": arrow_size, "precision": precision},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_annotation(request)
            return success_response("set_dimension_style", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("set_dimension_style", execution_mode, exc)
