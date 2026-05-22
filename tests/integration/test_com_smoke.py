import os

import pytest


pytestmark = pytest.mark.integration


def test_com_environment_declared() -> None:
    acad = os.getenv("AUTOCAD_MCP_ACAD_PATH")
    if not acad:
        pytest.skip("AUTOCAD_MCP_ACAD_PATH is not set; skipping COM integration smoke test")
    assert acad
