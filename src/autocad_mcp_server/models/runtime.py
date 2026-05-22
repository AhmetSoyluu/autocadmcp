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
