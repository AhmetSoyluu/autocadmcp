from __future__ import annotations

from typing import Any


class AnnotationService:
    """Generates AutoLISP/VLA for advanced annotation operations."""

    @staticmethod
    def _point(x: Any, y: Any) -> str:
        return f'"{x},{y}"'

    @staticmethod
    def _escape(value: Any) -> str:
        return str(value).replace('"', "").replace("\n", " ")

    def build_lisp(self, operation: str, parameters: dict[str, Any]) -> str:  # noqa: C901
        if operation == "add_leader":
            return (
                f'(command "_.LEADER" {self._point(parameters["start_x"], parameters["start_y"])} '
                f'{self._point(parameters["end_x"], parameters["end_y"])} "" '
                f'"{self._escape(parameters.get("text", ""))}" "")'
            )
        if operation == "add_multileader":
            return (
                f'(command "_.MLEADER" {self._point(parameters["start_x"], parameters["start_y"])} '
                f'{self._point(parameters["landing_x"], parameters["landing_y"])} '
                f'"{self._escape(parameters["text"])}")'
            )
        if operation == "add_dimension_angular":
            return (
                f'(command "_.DIMANGULAR" {self._point(parameters["cx"], parameters["cy"])} '
                f'{self._point(parameters["x1"], parameters["y1"])} '
                f'{self._point(parameters["x2"], parameters["y2"])} '
                f'{self._point(parameters["text_x"], parameters["text_y"])})'
            )
        if operation == "add_dimension_radial":
            handle = self._escape(parameters["handle"])
            return (
                f'(command "_.DIMRADIUS" (handent "{handle}") '
                f'{self._point(parameters["text_x"], parameters["text_y"])})'
            )
        if operation == "add_dimension_diameter":
            handle = self._escape(parameters["handle"])
            return (
                f'(command "_.DIMDIAMETER" (handent "{handle}") '
                f'{self._point(parameters["text_x"], parameters["text_y"])})'
            )
        if operation == "add_dimension_ordinate":
            return (
                f'(command "_.DIMORDINATE" {self._point(parameters["x"], parameters["y"])} '
                f'{self._point(parameters["leader_x"], parameters["leader_y"])})'
            )
        if operation == "add_table":
            rows = parameters.get("rows", 3)
            cols = parameters.get("columns", 3)
            rh = parameters.get("row_height", 10)
            cw = parameters.get("col_width", 40)
            return (
                f'(progn (setq tbl (vla-addtable '
                f'(vla-get-modelspace (vla-get-activedocument (vlax-get-acad-object))) '
                f'(vlax-3d-point {parameters["x"]} {parameters["y"]} 0) '
                f'{rows} {cols} {rh} {cw}))'
                f' (princ (strcat "MCP_RESULT:TABLE_HANDLE=" (vla-get-handle tbl))))'
            )
        if operation == "add_tolerance":
            return f'(command "_.TOLERANCE")'
        if operation == "set_text_style":
            name = self._escape(parameters["style_name"])
            font = self._escape(parameters.get("font_name", "Arial"))
            height = parameters.get("height", 0)
            wf = parameters.get("width_factor", 1.0)
            return (
                f'(command "_.-STYLE" "{name}" "{font}" "{height}" "{wf}" "0" "N" "N")'
            )
        if operation == "set_dimension_style":
            name = self._escape(parameters["style_name"])
            txt_h = parameters.get("text_height", 2.5)
            arr_sz = parameters.get("arrow_size", 2.5)
            return (
                f'(command "_.DIMSTYLE" "_S" "{name}")\n'
                f'(setvar "DIMTXT" {txt_h})\n'
                f'(setvar "DIMASZ" {arr_sz})\n'
                f'(command "_.DIMSTYLE" "_SA" "{name}")'
            )
        raise ValueError(f"Unsupported annotation operation: {operation}")
