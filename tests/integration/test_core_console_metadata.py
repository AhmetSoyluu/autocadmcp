import os

import pytest

from autocad_mcp_server.services.core_console_manager import CoreConsoleManager
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


def test_core_console_wrapper_adds_sentinel_markers() -> None:
    wrapped = CoreConsoleManager._wrap_script(CoreConsoleManager, '(princ "hello")')
    assert CoreConsoleManager.SENTINEL_BEGIN in wrapped
    assert CoreConsoleManager.SENTINEL_OK in wrapped
    assert CoreConsoleManager.SENTINEL_END in wrapped


def test_core_console_sentinel_validation_logic() -> None:
    sample = (
        f"{CoreConsoleManager.SENTINEL_BEGIN}\n"
        f"{CoreConsoleManager.SENTINEL_OK}\n"
        f"{CoreConsoleManager.SENTINEL_END}\n"
    )
    assert CoreConsoleManager._validate_sentinel(CoreConsoleManager, sample)


def test_electrical_runtime_fields_can_be_represented() -> None:
    payload = {
        'active_project_wdp': 'C:/CAD/demo.wdp',
        'electrical_standard': 'IEC_60617',
        'wd_m_initialized': True,
        'retained_failure_workspaces_count': 1,
    }
    assert payload['active_project_wdp'].endswith('.wdp')
    assert payload['electrical_standard'] == 'IEC_60617'
    assert payload['wd_m_initialized'] is True
