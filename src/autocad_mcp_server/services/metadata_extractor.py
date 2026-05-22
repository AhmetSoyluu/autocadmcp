from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class MetadataExtractor:
    def build_script(self, include_text: bool, include_blocks: bool, include_layers: bool) -> str:
        lines: list[str] = [
            '(princ "MCP_META_BEGIN\\n")',
            '(princ (strcat "PROP:DWGNAME=" (getvar "DWGNAME") "\\n"))',
            '(princ (strcat "PROP:CTAB=" (getvar "CTAB") "\\n"))',
            '(princ (strcat "PROP:INSUNITS=" (itoa (getvar "INSUNITS")) "\\n"))',
        ]
        if include_layers:
            lines.extend(
                [
                    '(setq _mcp_layers (vla-get-layers (vla-get-activedocument (vlax-get-acad-object))))',
                    '(vlax-for _layer _mcp_layers (princ (strcat "LAYER:" (vla-get-name _layer) "\\n")))',
                ]
            )
        if include_blocks:
            lines.extend(
                [
                    '(setq _mcp_blocks (vla-get-blocks (vla-get-activedocument (vlax-get-acad-object))))',
                    '(vlax-for _blk _mcp_blocks (if (= :vlax-false (vla-get-islayout _blk)) (princ (strcat "BLOCK:" (vla-get-name _blk) "\\n"))))',
                ]
            )
        if include_text:
            lines.extend(
                [
                    '(setq _mcp_ms (vla-get-modelspace (vla-get-activedocument (vlax-get-acad-object))))',
                    '(vlax-for _ent _mcp_ms (setq _name (vla-get-objectname _ent)) (if (or (= _name "AcDbText") (= _name "AcDbMText")) (princ (strcat "TEXT:" (vl-string-subst " " "\\n" (vla-get-textstring _ent)) "\\n"))))',
                ]
            )
        lines.extend(['(princ "MCP_META_END\\n")', '(princ)'])
        return "\n".join(lines) + "\n"

    def extract_from_text(
        self,
        drawing_path: Path,
        stdout: str,
        include_text: bool,
        include_blocks: bool,
        include_layers: bool,
    ) -> dict[str, Any]:
        lines = [line.strip() for line in stdout.splitlines() if line.strip()]
        in_payload = False
        layers: list[str] = []
        blocks: list[str] = []
        texts: list[str] = []
        props: dict[str, str] = {}

        for line in lines:
            if line == "MCP_META_BEGIN":
                in_payload = True
                continue
            if line == "MCP_META_END":
                in_payload = False
                break
            if not in_payload:
                continue
            if line.startswith("PROP:"):
                key_value = line[5:]
                if "=" in key_value:
                    key, value = key_value.split("=", 1)
                    props[key] = value
            elif include_layers and line.startswith("LAYER:"):
                layers.append(line[6:])
            elif include_blocks and line.startswith("BLOCK:"):
                blocks.append(line[6:])
            elif include_text and line.startswith("TEXT:"):
                texts.append(line[5:])

        return {
            "drawing": str(drawing_path),
            "properties": props,
            "layers": layers,
            "blocks": blocks,
            "texts": texts,
            "summary": {
                "layer_count": len(layers),
                "block_count": len(blocks),
                "text_count": len(texts),
            },
            "raw_stdout": stdout if not any([layers, blocks, texts, props]) else None,
        }

    def to_json(self, payload: dict[str, Any]) -> str:
        return json.dumps(payload, ensure_ascii=False)
