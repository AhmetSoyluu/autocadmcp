from __future__ import annotations

from autocad_mcp_server.models.requests import GenerateElectricalBlueprintRequest
from autocad_mcp_server.services.drafting_script_service import DraftingScriptService
from autocad_mcp_server.tools.common import error_response, success_response


def register_drafting_tool(mcp, drafting_service: DraftingScriptService) -> None:
    @mcp.tool()
    async def generate_electrical_blueprint(
        project_name: str,
        discipline: str = "mixed",
        systems: list[str] | None = None,
        base_point: tuple[float, float] = (0.0, 0.0),
        output_name: str = "electrical_blueprint",
        legend_offset_x: float = 5000.0,
        legend_offset_y: float = 0.0,
        drawing_standard: str = "IEC_60617",
    ) -> dict:
        request = GenerateElectricalBlueprintRequest(
            project_name=project_name,
            discipline=discipline,
            systems=systems or [],
            base_point=base_point,
            output_name=output_name,
            legend_offset_x=legend_offset_x,
            legend_offset_y=legend_offset_y,
            drawing_standard=drawing_standard,
        )
        try:
            payload = drafting_service.generate(request)
            return success_response(
                tool_name="generate_electrical_blueprint",
                execution_mode="generation",
                payload=payload,
                warnings=[],
            )
        except Exception as exc:
            return error_response("generate_electrical_blueprint", "generation", exc)
