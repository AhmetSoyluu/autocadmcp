from datetime import datetime, timezone

from autocad_mcp_server.models.runtime import RuntimeState
from autocad_mcp_server.tools.status import _compute_uptime_seconds


def test_compute_uptime_seconds_returns_non_negative() -> None:
    now = datetime.now(timezone.utc)
    seconds = _compute_uptime_seconds(now.isoformat())
    assert seconds >= 0


def test_status_runtime_state_shape_fields_exist() -> None:
    state = RuntimeState(
        total_jobs_processed=5,
        active_project_wdp='C:/CAD/demo.wdp',
        electrical_standard='IEC_60617',
        wd_m_initialized=True,
        retained_failure_workspaces_count=2,
        last_failure_reason='Duplicate Wire Number detected',
    )
    assert state.total_jobs_processed == 5
    assert state.active_project_wdp == 'C:/CAD/demo.wdp'
    assert state.electrical_standard == 'IEC_60617'
    assert state.wd_m_initialized is True
    assert state.retained_failure_workspaces_count == 2
    assert state.last_failure_reason == 'Duplicate Wire Number detected'
