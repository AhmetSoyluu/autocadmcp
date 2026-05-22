from __future__ import annotations

from autocad_mcp_server.models.requests import GenerateElectricalBlueprintRequest
from autocad_mcp_server.services.layout_geometry_service import break_segment_command, component_bbox


def build_architecture(request: GenerateElectricalBlueprintRequest) -> list[str]:
    x, y = request.base_point
    ow = request.outer_wall_thickness
    iw = request.inner_wall_thickness
    door_bbox = component_bbox(x + 180, y + 100, 40, 40)
    window_bbox = component_bbox(x + 270, y + 260, 60, 16)
    return [
        '(setvar "CLAYER" "A-WALL")',
        f'(command "._rectang" "{x},{y}" "{x+400},{y+260}")',
        f'(command "._offset" "{ow}" (entlast) "{x+ow},{y+ow}")',
        f'(command "._line" "{x+180},{y}" "{x+180},{y+260}" "")',
        f'(command "._offset" "{iw/2}" (entlast) "{x+185},{y+20}")',
        break_segment_command('(entlast)', door_bbox, horizontal=False),
        f'(command "._arc" "{x+180},{y+80}" "{x+220},{y+100}" "{x+180},{y+120}")',
        break_segment_command('(entlast)', window_bbox, horizontal=True),
    ]
