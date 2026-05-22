from __future__ import annotations

from pathlib import Path
from typing import Any

from autocad_mcp_server.models.requests import QueryGeometryRequest


class GeometryQueryService:
    def build_script(self, request: QueryGeometryRequest) -> str:
        type_filter = " ".join(request.entity_types).upper() if request.entity_types else "*"
        layer_filter = " ".join(request.layers) if request.layers else "*"
        lines = [
            '(princ "MCP_GEOM_BEGIN\\n")',
            '(setq _mcp_ms (vla-get-modelspace (vla-get-activedocument (vlax-get-acad-object))))',
            f'(setq _mcp_type_filter "{type_filter}")',
            f'(setq _mcp_layer_filter "{layer_filter}")',
            '(vlax-for _ent _mcp_ms',
            '  (setq _name (strcase (vla-get-objectname _ent)))',
            '  (setq _layer (vla-get-layer _ent))',
            '  (if (and (or (= _mcp_type_filter "*") (wcmatch _name (strcat "*" _mcp_type_filter "*")))',
            '           (or (= _mcp_layer_filter "*") (wcmatch _layer (strcat "*" _mcp_layer_filter "*"))))',
            '      (progn',
            '        (setq _obj (vlax-vla-object->ename _ent))',
            '        (setq _bb (vl-catch-all-apply \"vla-GetBoundingBox\" (list _ent \"minpt\" \"maxpt\")))',
            '        (setq _len (if (vlax-property-available-p _ent \"Length\") (vlax-get-property _ent \"Length\") -1))',
            '        (setq _area (if (vlax-property-available-p _ent \"Area\") (vlax-get-property _ent \"Area\") -1))',
            '        (princ (strcat "ENTITY:" _name "|LAYER:" _layer "|HANDLE:" (vla-get-handle _ent) "|LEN:" (rtos _len 2 6) "|AREA:" (rtos _area 2 6) "\\n"))',
            '      )',
            '  )',
            ')',
            '(princ "MCP_GEOM_END\\n")',
            '(princ)',
        ]
        return "\n".join(lines) + "\n"

    def parse_output(self, drawing_path: Path, stdout: str) -> dict[str, Any]:
        rows = [line.strip() for line in stdout.splitlines() if line.strip()]
        in_payload = False
        matches: list[dict[str, str]] = []

        for row in rows:
            if row == "MCP_GEOM_BEGIN":
                in_payload = True
                continue
            if row == "MCP_GEOM_END":
                break
            if not in_payload or not row.startswith("ENTITY:"):
                continue
            fields: dict[str, str] = {}
            for part in row.split("|"):
                if ":" not in part:
                    continue
                key, value = part.split(":", 1)
                fields[key.lower()] = value
            matches.append(fields)

        return {
            "drawing": str(drawing_path),
            "matches": matches,
            "count": len(matches),
            "raw_stdout": stdout if not matches else None,
        }
