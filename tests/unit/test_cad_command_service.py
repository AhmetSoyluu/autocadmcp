from autocad_mcp_server.services.cad_command_service import CadCommandService


def test_build_lisp_draw_line() -> None:
    service = CadCommandService()
    lisp = service.build_lisp("draw_line", {"x1": 0, "y1": 0, "x2": 10, "y2": 5})
    assert "LINE" in lisp


def test_build_lisp_zoom_extents() -> None:
    service = CadCommandService()
    lisp = service.build_lisp("zoom_extents", {})
    assert "ZOOM" in lisp
