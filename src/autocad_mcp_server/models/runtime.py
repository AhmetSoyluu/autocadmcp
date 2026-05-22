from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal


ExecutionMode = Literal["auto", "com", "core_console"]


@dataclass(slots=True)
class OperationContext:
    operation_id: str
    tool_name: str
    requested_mode: ExecutionMode
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(slots=True)
class JobResult:
    success: bool
    execution_mode: str
    payload: dict[str, Any]
    warnings: list[str] = field(default_factory=list)


@dataclass(slots=True)
class RuntimeState:
    queue_depth: int = 0
    core_console_healthy: bool = False
    com_healthy: bool = False
    last_started_at: str | None = None
    last_core_console_success_at: str | None = None
    last_com_healthcheck_at: str | None = None
    retained_failure_workspaces: int = 0
    retained_failure_workspaces_count: int = 0
    last_recovery_action: str | None = None
    active_project_wdp: str | None = None
    electrical_standard: str | None = None
    wd_m_initialized: bool = False
    last_error_context: dict[str, Any] | None = None
    total_jobs_processed: int = 0
    last_failure_reason: str | None = None
