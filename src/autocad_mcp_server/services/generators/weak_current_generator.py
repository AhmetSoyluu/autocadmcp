from __future__ import annotations

from autocad_mcp_server.models.requests import GenerateElectricalBlueprintRequest


def build_weak_current(request: GenerateElectricalBlueprintRequest) -> list[str]:
    x, y = request.base_point
    return [
        '(setvar "CLAYER" "E-ZA-YANGIN")',
        f'(command "._circle" "{x+120},{y+180}" "6")',
        f'(command "._text" "J" "MC" "{x+120},{y+170}" "2" "0" "SD")',
        '(setvar "CLAYER" "E-ZA-CCTV")',
        f'(command "._line" "{x+260},{y+210}" "{x+272},{y+218}" "")',
        f'(command "._circle" "{x+274},{y+220}" "3")',
        '(setvar "CLAYER" "E-DATA")',
        f'(command "._polyline" "{x+60},{y+80}" "{x+70},{y+80}" "{x+60},{y+90}" "C")',
        f'(command "._text" "J" "MC" "{x+65},{y+92}" "2" "0" "DATA")',
    ]
