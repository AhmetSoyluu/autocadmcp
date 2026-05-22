from autocad_mcp_server.services.titleblock_legend_service import build_legend, build_title_block


def test_title_block_contains_title() -> None:
    text = build_title_block(0, 0, 'MAIN DRAWING')
    assert 'MAIN DRAWING' in text
    assert 'PROJECT TITLE BLOCK' in text


def test_legend_contains_items() -> None:
    text = build_legend(0, 0, ['WALL = Architectural Wall', 'DUCT = Mechanical Duct'])
    assert 'SYMBOL LEGEND' in text
    assert 'WALL = Architectural Wall' in text
    assert 'DUCT = Mechanical Duct' in text
