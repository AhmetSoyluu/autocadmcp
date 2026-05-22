from __future__ import annotations

from autocad_mcp_server.models.requests import GenerateElectricalBlueprintRequest


def build_architecture(request: GenerateElectricalBlueprintRequest) -> list[str]:
    x, y = request.base_point
    ow = request.outer_wall_thickness
    iw = request.inner_wall_thickness
    return [
        '(setvar "CLAYER" "A-WALL")',
        f'(command "._rectang" "{x},{y}" "{x+400},{y+260}")',
        f'(command "._offset" "{ow}" (entlast) "{x+ow},{y+ow}")',
        f'(command "._line" "{x+180},{y}" "{x+180},{y+260}" "")',
        f'(command "._offset" "{iw/2}" (entlast) "{x+185},{y+20}")',
        f'(command "._break" (entlast) "{x+180},{y+80}" "{x+180},{y+120}")',
        f'(command "._arc" "{x+180},{y+80}" "{x+220},{y+100}" "{x+180},{y+120}")',
        f'(command "._break" (entlast) "{x+240},{y+260}" "{x+300},{y+260}")',
    ]
