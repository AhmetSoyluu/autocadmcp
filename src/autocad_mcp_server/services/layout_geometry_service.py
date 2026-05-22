from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BoundingBox:
    min_x: float
    min_y: float
    max_x: float
    max_y: float


def offset_label(x: float, y: float, dx: float = 10.0, dy: float = 5.0) -> tuple[float, float]:
    return (x + dx, y + dy)


def title_block_origin(base_x: float, base_y: float, sheet_width: float) -> tuple[float, float]:
    return (base_x + sheet_width + 50.0, base_y)


def legend_origin(base_x: float, base_y: float, legend_offset_x: float, legend_offset_y: float) -> tuple[float, float]:
    return (base_x + legend_offset_x, base_y + legend_offset_y)


def component_bbox(center_x: float, center_y: float, width: float, height: float) -> BoundingBox:
    half_w = width / 2.0
    half_h = height / 2.0
    return BoundingBox(center_x - half_w, center_y - half_h, center_x + half_w, center_y + half_h)


def break_segment_command(line_selector: str, bbox: BoundingBox, horizontal: bool = True) -> str:
    if horizontal:
        return f'(command "._break" {line_selector} "{bbox.min_x},{(bbox.min_y+bbox.max_y)/2}" "{bbox.max_x},{(bbox.min_y+bbox.max_y)/2}")'
    return f'(command "._break" {line_selector} "{(bbox.min_x+bbox.max_x)/2},{bbox.min_y}" "{(bbox.min_x+bbox.max_x)/2},{bbox.max_y}")'


def bypass_arc_commands(ix: float, iy: float, radius: float = 6.0) -> list[str]:
    return [
        f'(command "._line" "{ix-radius},{iy}" "{ix-radius/2},{iy}" "")',
        f'(command "._arc" "{ix-radius/2},{iy}" "{ix},{iy+radius}" "{ix+radius/2},{iy}")',
        f'(command "._line" "{ix+radius/2},{iy}" "{ix+radius},{iy}" "")',
    ]
