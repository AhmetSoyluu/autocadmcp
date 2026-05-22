from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from autocad_mcp_server.logging import get_logger


@dataclass(slots=True)
class AuditRecord:
    tool_name: str
    dwg_path: str | None
    execution_mode: str
    outcome: str
    message: str
    operation_id: str
    error_context: dict[str, Any] | None = None
    electrical_context: dict[str, Any] | None = None


def write_audit_record(record: AuditRecord, audit_file: Path | None = None) -> None:
    logger = get_logger()
    payload: dict[str, Any] = asdict(record)
    payload["timestamp"] = datetime.now(timezone.utc).isoformat()
    logger.info(f"AUDIT {payload}")
    if audit_file is not None:
        audit_file.parent.mkdir(parents=True, exist_ok=True)
        with audit_file.open("a", encoding="utf-8", errors="ignore") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
