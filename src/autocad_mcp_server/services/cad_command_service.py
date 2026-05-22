from __future__ import annotations

from typing import Any


class CadCommandService:
    def build_lisp(self, operation: str, parameters: dict[str, Any]) -> str:
        if operation == "draw_line":
            return f'(command "_.LINE" "{parameters["x1"]},{parameters["y1"]}" "{parameters["x2"]},{parameters["y2"]}" "")'
        if operation == "draw_circle":
            return f'(command "_.CIRCLE" "{parameters["cx"]},{parameters["cy"]}" "{parameters["radius"]}")'
        if operation == "draw_rectangle":
            x = parameters["x"]
            y = parameters["y"]
            width = parameters["width"]
            height = parameters["height"]
            return f'(command "_.RECTANG" "{x},{y}" "{x + width},{y + height}")'
        if operation == "draw_polyline":
            points = parameters["points"]
            points_text = " ".join(f'"{x},{y}"' for x, y in points)
            return f'(command "_.PLINE" {points_text} "")'
        if operation == "add_text":
            return (
                f'(command "_.TEXT" "{parameters["x"]},{parameters["y"]}" "{parameters.get("height", 2.5)}" '
                f'"0" "{parameters["text"]}")'
            )
        if operation == "add_hatch":
            return f'(command "_.-HATCH" "P" "{parameters.get("pattern_name", "ANSI31")}" "")'
        if operation == "add_dimension":
            return (
                f'(command "_.DIMALIGNED" "{parameters["x1"]},{parameters["y1"]}" '
                f'"{parameters["x2"]},{parameters["y2"]}" "{parameters["text_x"]},{parameters["text_y"]}")'
            )
        if operation == "insert_block":
            return (
                f'(command "_.-INSERT" "{parameters["block_name"]}" "{parameters["x"]},{parameters["y"]}" '
                f'"{parameters.get("scale", 1)}" "{parameters.get("scale", 1)}" "{parameters.get("rotation_deg", 0)}")'
            )
        if operation == "create_layer":
            color = parameters.get("color_index", 7)
            return f'(command "_.-LAYER" "_Make" "{parameters["name"]}" "_Color" "{color}" "{parameters["name"]}" "")'
        if operation == "zoom_extents":
            return '(command "_.ZOOM" "_E")'
        if operation == "send_command":
            command_string = str(parameters["command_string"]).replace('"', "")
            return f'(command "{command_string}")'
        raise ValueError(f"Unsupported operation: {operation}")
