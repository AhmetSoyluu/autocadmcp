import os
from pathlib import Path

import pytest

from autocad_mcp_server.services.metadata_extractor import MetadataExtractor


pytestmark = pytest.mark.integration


def test_core_console_metadata_environment_ready() -> None:
    accore = os.getenv("AUTOCAD_MCP_ACCORECONSOLE_PATH")
    roots = os.getenv("AUTOCAD_MCP_ALLOWED_DWG_ROOTS")
    if not accore or not roots:
        pytest.skip(
            "AUTOCAD_MCP_ACCORECONSOLE_PATH or AUTOCAD_MCP_ALLOWED_DWG_ROOTS is not set; skipping Core Console environment smoke test"
        )
    assert accore
    assert roots


def test_metadata_script_contains_markers() -> None:
    script = MetadataExtractor().build_script(include_text=True, include_blocks=True, include_layers=True)
    assert "MCP_META_BEGIN" in script
    assert "MCP_META_END" in script
