from __future__ import annotations

from typing import Any


class CadCommandService:
    @staticmethod
    def _point(x: Any, y: Any) -> str:
        return f'"{x},{y}"'

    @staticmethod
    def _point3d(x: Any, y: Any, z: Any) -> str:
        return f'"{x},{y},{z}"'

    @staticmethod
    def _escape_text(value: Any) -> str:
        return str(value).replace('"', "").replace("\n", " ")

    def build_lisp(self, operation: str, parameters: dict[str, Any]) -> str:  # noqa: C901
        # ─── BASIC DRAWING ────────────────────────────────────────
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

        # ─── 3D PRIMITIVES ────────────────────────────────────────
        if operation == "draw_3d_box":
            x, y, z = parameters.get("x", 0), parameters.get("y", 0), parameters.get("z", 0)
            length = parameters["length"]
            width = parameters["width"]
            height = parameters["height"]
            return (
                f'(command "_.BOX" {self._point3d(x, y, z)} '
                f'"_L" "{length}" "{width}" "{height}")'
            )
        if operation == "draw_3d_cylinder":
            cx, cy, cz = parameters.get("cx", 0), parameters.get("cy", 0), parameters.get("cz", 0)
            radius = parameters["radius"]
            height = parameters["height"]
            return (
                f'(command "_.CYLINDER" {self._point3d(cx, cy, cz)} '
                f'"{radius}" "{height}")'
            )
        if operation == "draw_3d_sphere":
            cx, cy, cz = parameters.get("cx", 0), parameters.get("cy", 0), parameters.get("cz", 0)
            radius = parameters["radius"]
            return f'(command "_.SPHERE" {self._point3d(cx, cy, cz)} "{radius}")'
        if operation == "draw_3d_cone":
            cx, cy, cz = parameters.get("cx", 0), parameters.get("cy", 0), parameters.get("cz", 0)
            radius = parameters["radius"]
            height = parameters["height"]
            return (
                f'(command "_.CONE" {self._point3d(cx, cy, cz)} '
                f'"{radius}" "{height}")'
            )

        # ─── ANNOTATION ──────────────────────────────────────────
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

        # ─── BLOCKS & LAYERS ─────────────────────────────────────
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

        # ─── OBJECT MANIPULATION — EXISTING ──────────────────────
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

        # ─── OBJECT MANIPULATION — NEW ───────────────────────────
        if operation == "offset_object":
            distance = parameters["distance"]
            handle = self._escape_text(parameters["handle"])
            side_x = parameters.get("side_x", 0)
            side_y = parameters.get("side_y", 0)
            return (
                f'(command "_.OFFSET" "{distance}" '
                f'(handent "{handle}") {self._point(side_x, side_y)} "")'
            )
        if operation == "mirror_object":
            handle = self._escape_text(parameters["handle"])
            return (
                f'(command "_.MIRROR" (handent "{handle}") "" '
                f'{self._point(parameters["x1"], parameters["y1"])} '
                f'{self._point(parameters["x2"], parameters["y2"])} '
                f'"_N")'
            )
        if operation == "array_rectangular":
            handle = self._escape_text(parameters["handle"])
            rows = parameters.get("rows", 2)
            columns = parameters.get("columns", 2)
            row_spacing = parameters.get("row_spacing", 100)
            col_spacing = parameters.get("col_spacing", 100)
            return (
                f'(command "_.ARRAYRECT" (handent "{handle}") "" '
                f'"_R" "{rows}" "_COL" "{columns}" '
                f'"_U" "{row_spacing}" "_D" "{col_spacing}" "")'
            )
        if operation == "array_polar":
            handle = self._escape_text(parameters["handle"])
            cx = parameters["cx"]
            cy = parameters["cy"]
            count = parameters.get("count", 6)
            angle = parameters.get("fill_angle", 360)
            return (
                f'(command "_.ARRAYPOLAR" (handent "{handle}") "" '
                f'{self._point(cx, cy)} "_I" "{count}" "_F" "{angle}" "")'
            )
        if operation == "fillet_objects":
            radius = parameters.get("radius", 0)
            h1 = self._escape_text(parameters["handle1"])
            h2 = self._escape_text(parameters["handle2"])
            return (
                f'(command "_.FILLET" "_R" "{radius}" '
                f'(handent "{h1}") (handent "{h2}"))'
            )
        if operation == "chamfer_objects":
            dist1 = parameters.get("distance1", 10)
            dist2 = parameters.get("distance2", 10)
            h1 = self._escape_text(parameters["handle1"])
            h2 = self._escape_text(parameters["handle2"])
            return (
                f'(command "_.CHAMFER" "_D" "{dist1}" "{dist2}" '
                f'(handent "{h1}") (handent "{h2}"))'
            )
        if operation == "explode_object":
            handle = self._escape_text(parameters["handle"])
            return f'(command "_.EXPLODE" (handent "{handle}"))'
        if operation == "join_objects":
            handles = parameters["handles"]
            selections = " ".join(
                f'(handent "{self._escape_text(h)}")' for h in handles
            )
            return f'(command "_.JOIN" {selections} "")'
        if operation == "break_object":
            handle = self._escape_text(parameters["handle"])
            bx1 = parameters.get("x1", 0)
            by1 = parameters.get("y1", 0)
            bx2 = parameters.get("x2", 0)
            by2 = parameters.get("y2", 0)
            return (
                f'(command "_.BREAK" (handent "{handle}") '
                f'"_F" {self._point(bx1, by1)} {self._point(bx2, by2)})'
            )
        if operation == "stretch_objects":
            x1 = parameters["x1"]
            y1 = parameters["y1"]
            x2 = parameters["x2"]
            y2 = parameters["y2"]
            dx = parameters["dx"]
            dy = parameters["dy"]
            bx = parameters["bx"]
            by = parameters["by"]
            return (
                f'(command "_.STRETCH" "_C" '
                f'{self._point(x1, y1)} {self._point(x2, y2)} "" '
                f'{self._point(bx, by)} {self._point(dx, dy)})'
            )
        if operation == "align_objects":
            handle = self._escape_text(parameters["handle"])
            src1 = self._point(parameters["src_x1"], parameters["src_y1"])
            dst1 = self._point(parameters["dst_x1"], parameters["dst_y1"])
            src2 = self._point(parameters["src_x2"], parameters["src_y2"])
            dst2 = self._point(parameters["dst_x2"], parameters["dst_y2"])
            scale = '"_Y"' if parameters.get("scale", False) else '"_N"'
            return (
                f'(command "_.ALIGN" (handent "{handle}") "" '
                f'{src1} {dst1} {src2} {dst2} "" {scale})'
            )
        if operation == "trim_object":
            cutting_handle = self._escape_text(parameters["cutting_handle"])
            target_x = parameters["target_x"]
            target_y = parameters["target_y"]
            return (
                f'(command "_.TRIM" (handent "{cutting_handle}") "" '
                f'{self._point(target_x, target_y)} "")'
            )
        if operation == "extend_object":
            boundary_handle = self._escape_text(parameters["boundary_handle"])
            target_x = parameters["target_x"]
            target_y = parameters["target_y"]
            return (
                f'(command "_.EXTEND" (handent "{boundary_handle}") "" '
                f'{self._point(target_x, target_y)} "")'
            )

        # ─── 3D BOOLEAN ──────────────────────────────────────────
        if operation == "boolean_union":
            h1 = self._escape_text(parameters["handle1"])
            h2 = self._escape_text(parameters["handle2"])
            return f'(command "_.UNION" (handent "{h1}") (handent "{h2}") "")'
        if operation == "boolean_subtract":
            h1 = self._escape_text(parameters["handle1"])
            h2 = self._escape_text(parameters["handle2"])
            return f'(command "_.SUBTRACT" (handent "{h1}") "" (handent "{h2}") "")'
        if operation == "boolean_intersect":
            h1 = self._escape_text(parameters["handle1"])
            h2 = self._escape_text(parameters["handle2"])
            return f'(command "_.INTERSECT" (handent "{h1}") (handent "{h2}") "")'

        # ─── MEASUREMENT ─────────────────────────────────────────
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

        # ─── UTILITY ─────────────────────────────────────────────
        if operation == "purge_drawing":
            return '(command "_.-PURGE" "_A" "*" "_N")'
        if operation == "audit_drawing":
            return '(command "_.AUDIT" "_Y")'
        if operation == "zoom_extents":
            return '(command "_.ZOOM" "_E")'
        if operation == "send_command":
            command_string = self._escape_text(parameters["command_string"])
            return f'(command "{command_string}")'

        # ─── OBJECT PROPERTIES ───────────────────────────────────
        if operation == "change_object_color":
            handle = self._escape_text(parameters["handle"])
            color = parameters["color_index"]
            return (
                f'(vla-put-color (vlax-ename->vla-object (handent "{handle}")) {color})'
            )
        if operation == "change_object_linetype":
            handle = self._escape_text(parameters["handle"])
            linetype = self._escape_text(parameters["linetype"])
            return (
                f'(vla-put-linetype (vlax-ename->vla-object (handent "{handle}")) "{linetype}")'
            )
        if operation == "change_object_lineweight":
            handle = self._escape_text(parameters["handle"])
            lineweight = parameters["lineweight"]
            return (
                f'(vla-put-lineweight (vlax-ename->vla-object (handent "{handle}")) {lineweight})'
            )
        if operation == "change_object_layer":
            handle = self._escape_text(parameters["handle"])
            layer = self._escape_text(parameters["layer_name"])
            return (
                f'(vla-put-layer (vlax-ename->vla-object (handent "{handle}")) "{layer}")'
            )

        raise ValueError(f"Unsupported operation: {operation}")
