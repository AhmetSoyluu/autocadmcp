from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from autocad_mcp_server.models.runtime import RuntimeState


class RuntimeSupervisor:
    def __init__(self, state_dir: Path) -> None:
        self.state_dir = state_dir
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.state_file = self.state_dir / "runtime_state.json"
        self.state = RuntimeState()

    def bootstrap(self) -> RuntimeState:
        if self.state_file.exists():
            try:
                data = json.loads(self.state_file.read_text(encoding="utf-8"))
                self.state = RuntimeState(**data)
            except Exception:
                self.state = RuntimeState(last_recovery_action="state_reset")
        self.state.last_started_at = datetime.now(timezone.utc).isoformat()
        self.persist()
        return self.state

    def update_queue_depth(self, depth: int) -> None:
        self.state.queue_depth = depth
        self.persist()

    def mark_core_console_success(self) -> None:
        self.state.last_core_console_success_at = datetime.now(timezone.utc).isoformat()
        self.state.core_console_healthy = True
        self.persist()

    def mark_com_health(self, healthy: bool) -> None:
        self.state.last_com_healthcheck_at = datetime.now(timezone.utc).isoformat()
        self.state.com_healthy = healthy
        self.persist()

    def set_retained_failure_workspaces(self, count: int) -> None:
        self.state.retained_failure_workspaces = count
        self.persist()

    def persist(self) -> None:
        self.state_file.write_text(json.dumps(asdict(self.state), ensure_ascii=False, indent=2), encoding="utf-8")
