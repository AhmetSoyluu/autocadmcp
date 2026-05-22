from autocad_mcp_server.services.layer_profile_service import build_layer_matrix


def test_layer_profile_contains_multidiscipline_layers() -> None:
    matrix = build_layer_matrix()
    assert 'A-WALL' in matrix
    assert 'A-AXIS' in matrix
    assert 'S-COL' in matrix
    assert 'M-DUCT' in matrix
    assert 'E-POWER' in matrix
