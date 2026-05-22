from autocad_mcp_server.services.layout_geometry_service import legend_origin, offset_label, title_block_origin


def test_offset_label_applies_clearance() -> None:
    x, y = offset_label(10, 20)
    assert x > 10
    assert y > 20


def test_title_block_origin_moves_outside_sheet() -> None:
    x, y = title_block_origin(0, 0, 841)
    assert x > 841
    assert y == 0


def test_legend_origin_uses_offsets() -> None:
    x, y = legend_origin(0, 0, 5000, 50)
    assert x == 5000
    assert y == 50
