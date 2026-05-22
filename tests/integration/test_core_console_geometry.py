import pytest

from autocad_mcp_server.models.requests import QueryGeometryRequest
from autocad_mcp_server.services.geometry_query_service import GeometryQueryService


pytestmark = pytest.mark.integration


def test_geometry_script_contains_markers() -> None:
    request = QueryGeometryRequest(dwg_path="C:/CAD/sample.dwg")
    script = GeometryQueryService().build_script(request)
    assert "MCP_GEOM_BEGIN" in script
    assert "MCP_GEOM_END" in script
