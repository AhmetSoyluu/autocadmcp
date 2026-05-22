from pathlib import Path

from autocad_mcp_server.services.runtime_supervisor import RuntimeSupervisor


def test_runtime_supervisor_persists_state(tmp_path: Path) -> None:
    supervisor = RuntimeSupervisor(tmp_path)
    state = supervisor.bootstrap()
    supervisor.update_queue_depth(3)
    supervisor.mark_core_console_success()
    supervisor.record_electrical_context(
        active_project_wdp='C:/CAD/demo.wdp',
        electrical_standard='IEC_60617',
        wd_m_initialized=True,
    )

    assert state.last_started_at is not None
    assert supervisor.state.queue_depth == 3
    assert supervisor.state.last_core_console_success_at is not None
    assert supervisor.state.active_project_wdp == 'C:/CAD/demo.wdp'
    assert supervisor.state.electrical_standard == 'IEC_60617'
    assert supervisor.state.wd_m_initialized is True
    assert (tmp_path / 'runtime_state.json').exists()


def test_runtime_supervisor_records_failure_context(tmp_path: Path) -> None:
    supervisor = RuntimeSupervisor(tmp_path)
    supervisor.bootstrap()
    supervisor.record_job_failure('Duplicate Wire Number detected', {'sheet': '002', 'component_tag': 'K1'})

    assert supervisor.state.last_failure_reason == 'Duplicate Wire Number detected'
    assert supervisor.state.last_error_context == {'sheet': '002', 'component_tag': 'K1'}
