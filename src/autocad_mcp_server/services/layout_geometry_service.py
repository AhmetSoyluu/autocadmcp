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
