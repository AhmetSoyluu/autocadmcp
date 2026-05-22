import json
from pathlib import Path

from autocad_mcp_server.utils.audit import AuditRecord, write_audit_record


def test_audit_writer_appends_jsonl(tmp_path: Path) -> None:
    audit_file = tmp_path / 'audit.jsonl'
    write_audit_record(AuditRecord('tool', 'a.dwg', 'core_console', 'ok', 'done', '1'), audit_file)
    write_audit_record(AuditRecord('tool', 'b.dwg', 'com', 'ok', 'done', '2'), audit_file)

    lines = audit_file.read_text(encoding='utf-8').strip().splitlines()
    assert len(lines) == 2
    first = json.loads(lines[0])
    second = json.loads(lines[1])
    assert first['operation_id'] == '1'
    assert second['operation_id'] == '2'
