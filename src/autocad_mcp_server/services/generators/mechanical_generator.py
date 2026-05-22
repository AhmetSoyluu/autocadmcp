from __future__ import annotations

from autocad_mcp_server.models.requests import GenerateElectricalBlueprintRequest


def build_mechanical(request: GenerateElectricalBlueprintRequest) -> list[str]:
    x, y = request.base_point
    return [
        '(setvar "CLAYER" "M-DUCT")',
        f'(command "._polyline" "{x+40},{y+420}" "{x+220},{y+420}" "{x+220},{y+500}" "")',
        f'(command "._offset" "12" (entlast) "{x+50},{y+430}")',
        '(setvar "CLAYER" "M-PIPE")',
        f'(command "._line" "{x+260},{y+430}" "{x+380},{y+430}" "")',
        f'(command "._circle" "{x+400},{y+430}" "14")',
        f'(command "._text" "J" "MC" "{x+400},{y+452}" "2.2" "0" "PUMP")',
    ]
