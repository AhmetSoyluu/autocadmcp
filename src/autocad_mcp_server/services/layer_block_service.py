from __future__ import annotations

from typing import Any


class LayerBlockService:
    def build_lisp(self, action: str, parameters: dict[str, Any]) -> str:
        if action == "create_layer":
            name = parameters["name"]
            color = parameters.get("color", 7)
            return f'(command "_.-LAYER" "_Make" "{name}" "_Color" "{color}" "{name}" "")'
        if action == "freeze_layer":
            name = parameters["name"]
            return f'(command "_.-LAYER" "_Freeze" "{name}" "")'
        if action == "thaw_layer":
            name = parameters["name"]
            return f'(command "_.-LAYER" "_Thaw" "{name}" "")'
        if action == "lock_layer":
            name = parameters["name"]
            return f'(command "_.-LAYER" "_Lock" "{name}" "")'
        if action == "unlock_layer":
            name = parameters["name"]
            return f'(command "_.-LAYER" "_Unlock" "{name}" "")'
        if action == "insert_block":
            name = parameters["name"]
            x = parameters.get("x", 0)
            y = parameters.get("y", 0)
            scale = parameters.get("scale", 1)
            rotation = parameters.get("rotation", 0)
            return f'(command "_.-INSERT" "{name}" "{x},{y}" "{scale}" "{scale}" "{rotation}")'
        raise ValueError(f"Unsupported action: {action}")
