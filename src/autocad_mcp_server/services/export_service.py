from __future__ import annotations

from typing import Any


class ExportService:
    """Generates AutoLISP/VLA for export and conversion operations."""

    @staticmethod
    def _escape(value: Any) -> str:
        return str(value).replace('"', "").replace("\n", " ")

    def build_lisp(self, fmt: str, parameters: dict[str, Any]) -> str:  # noqa: C901
        output = self._escape(parameters.get("output_path", ""))
        layout = self._escape(parameters.get("layout_name", "Model"))

        if fmt == "pdf":
            paper = self._escape(parameters.get("paper_size", "A3"))
            color_mode = parameters.get("color_mode", "color")
            style = "acad.ctb" if color_mode == "color" else "monochrome.ctb"
            return (
                f'(command "_.-PLOT" "_Y" "{layout}" "DWG To PDF.pc3" '
                f'"{paper}" "_M" "E" "F" "C" "_Y" "{style}" "_Y" "_N" "_N" "_N" '
                f'"{output}" "_Y")'
            )
        if fmt == "dxf":
            return f'(command "_.DXFOUT" "{output}")'
        if fmt == "dwf":
            return (
                f'(command "_.-PLOT" "_Y" "{layout}" "DWF6 ePlot.pc3" '
                f'"ISO A3 (420.00 x 297.00 MM)" "_M" "E" "F" "C" "_Y" "" "_Y" '
                f'_N" "_N" "_N" "{output}" "_Y")'
            )
        if fmt in ("png", "jpg", "bmp"):
            ext = fmt.upper()
            dpi = parameters.get("resolution_dpi", 300)
            return (
                f'(command "_.-PLOT" "_Y" "{layout}" "PublishToWeb {ext}.pc3" '
                f'"Custom ({dpi} x {dpi})" "_M" "E" "F" "C" "_Y" "" "_Y" '
                f'"_N" "_N" "_N" "{output}" "_Y")'
            )
        if fmt == "svg":
            return f'(command "_.EXPORT" "{output}" "svg")'
        if fmt == "stl":
            return f'(command "_.STLOUT" "" "_Y" "{output}")'
        raise ValueError(f"Unsupported export format: {fmt}")
