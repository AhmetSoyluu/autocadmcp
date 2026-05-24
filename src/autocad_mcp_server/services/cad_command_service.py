from __future__ import annotations

from typing import Any


class CadCommandService:
    @staticmethod
    def _point(x: Any, y: Any) -> str:
        return f'"{x},{y}"'

    @staticmethod
    def _escape_text(value: Any) -> str:
        return str(value).replace('"', "").replace("\n", " ")

    def build_lisp(self, operation: str, parameters: dict[str, Any]) -> str:
        if operation == "draw_line":
            return f'(command "_.LINE" {self._point(parameters["x1"], parameters["y1"])} {self._point(parameters["x2"], parameters["y2"])} "")'
        if operation == "draw_circle":
            return f'(command "_.CIRCLE" {self._point(parameters["cx"], parameters["cy"])} "{parameters["radius"]}")'
        if operation == "draw_rectangle":
            x = parameters["x"]
            y = parameters["y"]
            width = parameters["width"]
            height = parameters["height"]
            return f'(command "_.RECTANG" {self._point(x, y)} {self._point(x + width, y + height)})'
        if operation == "draw_polyline":
            points = parameters["points"]
            points_text = " ".join(self._point(x, y) for x, y in points)
            return f'(command "_.PLINE" {points_text} "")'
        if operation == "draw_ellipse":
            return (
                f'(command "_.ELLIPSE" "C" {self._point(parameters["cx"], parameters["cy"])} '
                f'{self._point(parameters["ex"], parameters["ey"])} "{parameters["other_axis_radius"]}")'
            )
        if operation == "draw_arc":
            return (
                f'(command "_.ARC" {self._point(parameters["x1"], parameters["y1"])} '
                f'{self._point(parameters["x2"], parameters["y2"])} {self._point(parameters["x3"], parameters["y3"])} )'
            )
        if operation == "draw_spline":
            points = parameters["points"]
            points_text = " ".join(self._point(x, y) for x, y in points)
            return f'(command "_.SPLINE" {points_text} "" "" "")'
        if operation == "add_text":
            return (
                f'(command "_.TEXT" {self._point(parameters["x"], parameters["y"])} "{parameters.get("height", 2.5)}" '
                f'"0" "{self._escape_text(parameters["text"])}")'
            )
        if operation == "add_hatch":
            return f'(command "_.-HATCH" "P" "{self._escape_text(parameters.get("pattern_name", "ANSI31"))}" "")'
        if operation == "add_dimension":
            return (
                f'(command "_.DIMALIGNED" {self._point(parameters["x1"], parameters["y1"])} '
                f'{self._point(parameters["x2"], parameters["y2"])} {self._point(parameters["text_x"], parameters["text_y"])} )'
            )
        if operation == "insert_block":
            return (
                f'(command "_.-INSERT" "{self._escape_text(parameters["block_name"])}" {self._point(parameters["x"], parameters["y"])} '
                f'"{parameters.get("scale", 1)}" "{parameters.get("scale", 1)}" "{parameters.get("rotation_deg", 0)}")'
            )
        if operation == "create_layer":
            color = parameters.get("color_index", 7)
            return (
                f'(command "_.-LAYER" "_Make" "{self._escape_text(parameters["name"])}" '
                f'"_Color" "{color}" "{self._escape_text(parameters["name"])}" "")'
            )
        if operation == "erase_object":
            return f'(command "_.ERASE" (handent "{self._escape_text(parameters["handle"])}") "")'
        if operation == "move_object":
            return (
                f'(command "_.MOVE" (handent "{self._escape_text(parameters["handle"])}") "" '
                f'{self._point(parameters["bx"], parameters["by"])} {self._point(parameters["dx"], parameters["dy"])} )'
            )
        if operation == "rotate_object":
            return (
                f'(command "_.ROTATE" (handent "{self._escape_text(parameters["handle"])}") "" '
                f'{self._point(parameters["bx"], parameters["by"])} "{parameters["angle_deg"]}")'
            )
        if operation == "scale_object":
            return (
                f'(command "_.SCALE" (handent "{self._escape_text(parameters["handle"])}") "" '
                f'{self._point(parameters["bx"], parameters["by"])} "{parameters["scale_factor"]}")'
            )
        if operation == "copy_object":
            return (
                f'(command "_.COPY" (handent "{self._escape_text(parameters["handle"])}") "" '
                f'{self._point(parameters["bx"], parameters["by"])} {self._point(parameters["dx"], parameters["dy"])} )'
            )
        if operation == "get_distance":
            return (
                f'(princ (strcat "MCP_RESULT:DISTANCE=" (rtos (distance {self._point(parameters["x1"], parameters["y1"])} '
                f'{self._point(parameters["x2"], parameters["y2"])} ) 2 6)))'
            )
        if operation == "get_angle":
            return (
                f'(princ (strcat "MCP_RESULT:ANGLE=" (rtos (* 180.0 (/ (angle {self._point(parameters["x1"], parameters["y1"])} '
                f'{self._point(parameters["x2"], parameters["y2"])} ) pi)) 2 6)))'
            )
        if operation == "calculate_area":
            handle = parameters.get("handle")
            if handle:
                return (
                    f'(princ (strcat "MCP_RESULT:AREA=" '
                    f'(rtos (vla-get-area (vlax-ename->vla-object (handent "{self._escape_text(handle)}"))) 2 6)))'
                )
            points = parameters["points"]
            points_text = " ".join(self._point(x, y) for x, y in points)
            return f'(command "_.PLINE" {points_text} "C")\n(command "_.AREA" "O" "L")'
        if operation == "purge_drawing":
            return '(command "_.-PURGE" "_A" "*" "_N")'
        if operation == "audit_drawing":
            return '(command "_.AUDIT" "_Y")'
        if operation == "zoom_extents":
            return '(command "_.ZOOM" "_E")'
        if operation == "send_command":
            command_string = self._escape_text(parameters["command_string"])
            return f'(command "{command_string}")'
        raise ValueError(f"Unsupported operation: {operation}")
