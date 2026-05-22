from __future__ import annotations

from autocad_mcp_server.models.requests import GenerateElectricalBlueprintRequest


def build_electrical(request: GenerateElectricalBlueprintRequest) -> list[str]:
    x, y = request.base_point
    return [
        '(setvar "CLAYER" "E-AG-BUSBAR")',
        f'(command "._line" "{x+80},{y+320}" "{x+200},{y+320}" "")',
        f'(command "._line" "{x+80},{y+312}" "{x+200},{y+312}" "")',
        '(setvar "CLAYER" "E-OG-TRAFO")',
        f'(command "._rectang" "{x+420},{y+300}" "{x+500},{y+350}")',
        f'(command "._text" "J" "MC" "{x+460},{y+325}" "3" "0" "TRAFO")',
        '(setvar "CLAYER" "E-POWER")',
        f'(command "._polyline" "{x+200},{y+316}" "{x+320},{y+316}" "{x+320},{y+330}" "{x+420},{y+330}" "")',
    ]
