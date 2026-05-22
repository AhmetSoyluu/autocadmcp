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
        self.increment_processed_jobs()
        self.persist()

    def mark_com_health(self, healthy: bool) -> None:
        self.state.last_com_healthcheck_at = datetime.now(timezone.utc).isoformat()
        self.state.com_healthy = healthy
        self.persist()

    def record_electrical_context(
        self,
        active_project_wdp: str | None = None,
        electrical_standard: str | None = None,
        wd_m_initialized: bool | None = None,
    ) -> None:
        if active_project_wdp is not None:
            self.state.active_project_wdp = active_project_wdp
        if electrical_standard is not None:
            self.state.electrical_standard = electrical_standard
        if wd_m_initialized is not None:
            self.state.wd_m_initialized = wd_m_initialized
        self.persist()

    def record_job_success(self) -> None:
        self.increment_processed_jobs()
        self.state.last_failure_reason = None
        self.state.last_error_context = None
        self.persist()

    def record_job_failure(self, reason: str, context: dict[str, object] | None = None) -> None:
        self.state.last_failure_reason = reason
        self.state.last_error_context = context or {}
        self.increment_processed_jobs()
        self.persist()

    def increment_processed_jobs(self) -> None:
        self.state.total_jobs_processed += 1

    def set_retained_failure_workspaces(self, count: int) -> None:
        self.state.retained_failure_workspaces = count
        self.state.retained_failure_workspaces_count = count
        self.persist()

    def persist(self) -> None:
        self.state_file.write_text(json.dumps(asdict(self.state), ensure_ascii=False, indent=2), encoding="utf-8")
