from pathlib import Path

from autocad_mcp_server.services.runtime_supervisor import RuntimeSupervisor


def test_runtime_supervisor_persists_state(tmp_path: Path) -> None:
    supervisor = RuntimeSupervisor(tmp_path)
    state = supervisor.bootstrap()
    supervisor.update_queue_depth(3)
    supervisor.mark_core_console_success()

    assert state.last_started_at is not None
    assert supervisor.state.queue_depth == 3
    assert supervisor.state.last_core_console_success_at is not None
    assert (tmp_path / 'runtime_state.json').exists()
