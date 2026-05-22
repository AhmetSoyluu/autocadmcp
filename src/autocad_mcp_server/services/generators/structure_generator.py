from __future__ import annotations

from autocad_mcp_server.models.requests import GenerateElectricalBlueprintRequest


def build_structure(request: GenerateElectricalBlueprintRequest) -> list[str]:
    x, y = request.base_point
    return [
        '(setvar "CLAYER" "A-AXIS")',
        f'(command "._line" "{x+50},{y}" "{x+50},{y+320}" "")',
        f'(command "._line" "{x+200},{y}" "{x+200},{y+320}" "")',
        f'(command "._line" "{x+350},{y}" "{x+350},{y+320}" "")',
        f'(command "._line" "{x},{y+60}" "{x+420},{y+60}" "")',
        f'(command "._line" "{x},{y+180}" "{x+420},{y+180}" "")',
        '(setvar "CLAYER" "S-COL")',
        f'(command "._rectang" "{x+38},{y+48}" "{x+62},{y+72}")',
        f'(command "._rectang" "{x+188},{y+48}" "{x+212},{y+72}")',
        f'(command "._rectang" "{x+338},{y+168}" "{x+362},{y+192}")',
    ]
