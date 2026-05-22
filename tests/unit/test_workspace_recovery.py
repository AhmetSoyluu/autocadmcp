from pathlib import Path

from autocad_mcp_server.utils.temp_workspace import TempWorkspaceManager


def test_cleanup_stale_workspaces_removes_untracked_dirs(tmp_path: Path) -> None:
    manager = TempWorkspaceManager(tmp_path)
    stale = tmp_path / 'stale-job'
    stale.mkdir()
    tracked = manager.create('tracked')
    manager.write_manifest(tracked, {'job_id': '1'})

    removed = manager.cleanup_stale_workspaces()

    assert removed == 1
    assert not stale.exists()
    assert tracked.exists()
