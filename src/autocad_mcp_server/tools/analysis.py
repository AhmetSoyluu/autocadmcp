from __future__ import annotations

from autocad_mcp_server.models.requests import AnalysisRequest
from autocad_mcp_server.services.dwg_service import DWGService
from autocad_mcp_server.tools.common import error_response, success_response


def register_analysis_tool(mcp, service: DWGService) -> None:
    @mcp.tool()
    async def check_drawing_standards(
        dwg_path: str,
        standards_file: str = "",
        execution_mode: str = "auto",
    ) -> dict:
        """Check drawing against CAD standards (.dws file)."""
        request = AnalysisRequest(
            dwg_path=dwg_path, operation="check_drawing_standards",
            parameters={"standards_file": standards_file}, execution_mode=execution_mode,
        )
        try:
            result = await service.execute_analysis(request)
            return success_response("check_drawing_standards", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("check_drawing_standards", execution_mode, exc)

    @mcp.tool()
    async def find_overlapping_objects(
        dwg_path: str,
        tolerance: float = 0.001,
        execution_mode: str = "auto",
    ) -> dict:
        """Find objects that overlap or are positioned on top of each other."""
        request = AnalysisRequest(
            dwg_path=dwg_path, operation="find_overlapping_objects",
            parameters={"tolerance": tolerance}, execution_mode=execution_mode,
        )
        try:
            result = await service.execute_analysis(request)
            return success_response("find_overlapping_objects", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("find_overlapping_objects", execution_mode, exc)

    @mcp.tool()
    async def find_duplicate_objects(
        dwg_path: str,
        tolerance: float = 0.001,
        execution_mode: str = "auto",
    ) -> dict:
        """Find duplicate (identical) objects in the drawing."""
        request = AnalysisRequest(
            dwg_path=dwg_path, operation="find_duplicate_objects",
            parameters={"tolerance": tolerance}, execution_mode=execution_mode,
        )
        try:
            result = await service.execute_analysis(request)
            return success_response("find_duplicate_objects", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("find_duplicate_objects", execution_mode, exc)

    @mcp.tool()
    async def layer_usage_report(dwg_path: str, execution_mode: str = "auto") -> dict:
        """Generate a report of layer usage statistics (object count per layer, frozen/locked status)."""
        request = AnalysisRequest(
            dwg_path=dwg_path, operation="layer_usage_report", execution_mode=execution_mode,
        )
        try:
            result = await service.execute_analysis(request)
            return success_response("layer_usage_report", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("layer_usage_report", execution_mode, exc)

    @mcp.tool()
    async def object_count_by_type(dwg_path: str, execution_mode: str = "auto") -> dict:
        """Count objects grouped by entity type (LINE, CIRCLE, INSERT, etc.)."""
        request = AnalysisRequest(
            dwg_path=dwg_path, operation="object_count_by_type", execution_mode=execution_mode,
        )
        try:
            result = await service.execute_analysis(request)
            return success_response("object_count_by_type", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("object_count_by_type", execution_mode, exc)

    @mcp.tool()
    async def drawing_complexity_score(dwg_path: str, execution_mode: str = "auto") -> dict:
        """Calculate a complexity score based on entity count, layer count, and block usage."""
        request = AnalysisRequest(
            dwg_path=dwg_path, operation="drawing_complexity_score", execution_mode=execution_mode,
        )
        try:
            result = await service.execute_analysis(request)
            return success_response("drawing_complexity_score", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("drawing_complexity_score", execution_mode, exc)

    @mcp.tool()
    async def detect_unclosed_polylines(dwg_path: str, execution_mode: str = "auto") -> dict:
        """Find polylines that are not closed (open boundary issues)."""
        request = AnalysisRequest(
            dwg_path=dwg_path, operation="detect_unclosed_polylines", execution_mode=execution_mode,
        )
        try:
            result = await service.execute_analysis(request)
            return success_response("detect_unclosed_polylines", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("detect_unclosed_polylines", execution_mode, exc)

    @mcp.tool()
    async def compare_drawings(
        dwg_path: str,
        compare_with: str,
        execution_mode: str = "auto",
    ) -> dict:
        """Compare two drawings and report differences."""
        request = AnalysisRequest(
            dwg_path=dwg_path, operation="compare_drawings",
            parameters={"compare_with": compare_with}, execution_mode=execution_mode,
        )
        try:
            result = await service.execute_analysis(request)
            return success_response("compare_drawings", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("compare_drawings", execution_mode, exc)

    @mcp.tool()
    async def generate_bom(
        dwg_path: str,
        block_filter: str = "",
        execution_mode: str = "auto",
    ) -> dict:
        """Generate a Bill of Materials from block references and their attributes."""
        request = AnalysisRequest(
            dwg_path=dwg_path, operation="generate_bom",
            parameters={"block_filter": block_filter}, execution_mode=execution_mode,
        )
        try:
            result = await service.execute_analysis(request)
            return success_response("generate_bom", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("generate_bom", execution_mode, exc)

    @mcp.tool()
    async def calculate_total_line_length(
        dwg_path: str,
        layer: str = "",
        execution_mode: str = "auto",
    ) -> dict:
        """Calculate total line/polyline length, optionally filtered by layer."""
        request = AnalysisRequest(
            dwg_path=dwg_path, operation="calculate_total_line_length",
            parameters={"layer": layer}, execution_mode=execution_mode,
        )
        try:
            result = await service.execute_analysis(request)
            return success_response("calculate_total_line_length", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("calculate_total_line_length", execution_mode, exc)

    @mcp.tool()
    async def find_text_containing(
        dwg_path: str,
        search_text: str,
        case_sensitive: bool = False,
        execution_mode: str = "auto",
    ) -> dict:
        """Search for text objects containing a specific string."""
        request = AnalysisRequest(
            dwg_path=dwg_path, operation="find_text_containing",
            parameters={"search_text": search_text, "case_sensitive": case_sensitive},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_analysis(request)
            return success_response("find_text_containing", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("find_text_containing", execution_mode, exc)

    @mcp.tool()
    async def replace_text(
        dwg_path: str,
        find_text: str,
        replace_with: str,
        case_sensitive: bool = False,
        execution_mode: str = "auto",
    ) -> dict:
        """Find and replace text across all text objects in the drawing."""
        request = AnalysisRequest(
            dwg_path=dwg_path, operation="replace_text",
            parameters={"find_text": find_text, "replace_with": replace_with, "case_sensitive": case_sensitive},
            execution_mode=execution_mode,
        )
        try:
            result = await service.execute_analysis(request)
            return success_response("replace_text", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("replace_text", execution_mode, exc)

    @mcp.tool()
    async def list_all_text(dwg_path: str, execution_mode: str = "auto") -> dict:
        """List all text/mtext objects with their content, position, and layer."""
        request = AnalysisRequest(
            dwg_path=dwg_path, operation="list_all_text", execution_mode=execution_mode,
        )
        try:
            result = await service.execute_analysis(request)
            return success_response("list_all_text", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("list_all_text", execution_mode, exc)
