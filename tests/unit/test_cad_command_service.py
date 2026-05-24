from autocad_mcp_server.services.cad_command_service import CadCommandService


def test_build_lisp_draw_line() -> None:
    service = CadCommandService()
    lisp = service.build_lisp("draw_line", {"x1": 0, "y1": 0, "x2": 10, "y2": 5})
    assert "LINE" in lisp


def test_build_lisp_zoom_extents() -> None:
    service = CadCommandService()
    lisp = service.build_lisp("zoom_extents", {})
    assert "ZOOM" in lisp


def test_build_lisp_draw_ellipse() -> None:
    service = CadCommandService()
    lisp = service.build_lisp(
        "draw_ellipse",
        {"cx": 0, "cy": 0, "ex": 10, "ey": 0, "other_axis_radius": 4},
    )
    assert "ELLIPSE" in lisp


def test_build_lisp_get_distance_contains_result_marker() -> None:
    service = CadCommandService()
    lisp = service.build_lisp("get_distance", {"x1": 0, "y1": 0, "x2": 3, "y2": 4})
    assert "MCP_RESULT:DISTANCE=" in lisp


def test_build_lisp_erase_object_uses_handle() -> None:
    service = CadCommandService()
    lisp = service.build_lisp("erase_object", {"handle": "ABCD"})
    assert "handent" in lisp
