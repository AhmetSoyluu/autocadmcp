import os

import pytest


pytestmark = pytest.mark.integration


def test_com_environment_declared() -> None:
    acad = os.getenv("AUTOCAD_MCP_ACAD_PATH")
    assert acad, "AUTOCAD_MCP_ACAD_PATH must be set for COM integration tests"
