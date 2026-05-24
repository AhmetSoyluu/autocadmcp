from __future__ import annotations

import threading
from pathlib import Path
from typing import Any

from autocad_mcp_server.adapters.com_adapter import ComAdapter
from autocad_mcp_server.services.runtime_supervisor import RuntimeSupervisor
from autocad_mcp_server.utils.audit import AuditRecord, write_audit_record
from autocad_mcp_server.utils.errors import AutoCADUnavailable, ToolExecutionFailure


class InteropManager:
    def __init__(
        self,
        adapter: ComAdapter,
        visible: bool,
        launch_if_missing: bool,
        supervisor: RuntimeSupervisor,
        audit_file: Path,
    ) -> None:
        self.adapter = adapter
        self.visible = visible
        self.launch_if_missing = launch_if_missing
        self.supervisor = supervisor
        self.audit_file = audit_file
        self._lock = threading.RLock()

    def _connect(self) -> Any:
        try:
            return self.adapter.connect(
                visible=self.visible,
                launch_if_missing=self.launch_if_missing,
            )
        except AutoCADUnavailable:
            raise
        except Exception as exc:
            raise AutoCADUnavailable(f"Unable to connect to AutoCAD COM session: {exc}") from exc

    def run_lisp(self, drawing_path: Path, lisp_source: str) -> dict[str, str]:
        with self._lock:
            document = None
            try:
                self.adapter.initialize_com()
                app = self._connect()
                self.supervisor.mark_com_health(True)
                self.supervisor.record_electrical_context(
                    active_project_wdp=str(drawing_path.with_suffix('.wdp')),
                    wd_m_initialized=True,
                )
                document = self.adapter.open_document(app, drawing_path)
                self.adapter.send_command(document, lisp_source)
                self.supervisor.record_job_success()
                write_audit_record(
                    AuditRecord(
                        tool_name="execute_autolisp",
                        dwg_path=str(drawing_path),
                        execution_mode="com",
                        outcome="success",
                        message="COM AutoLISP submitted",
                        operation_id="com-lisp",
                        electrical_context={"active_project_wdp": str(drawing_path.with_suffix('.wdp')), "wd_m_initialized": True},
                    ),
                    self.audit_file,
                )
                return {"status": "submitted", "drawing": str(drawing_path)}
            except AutoCADUnavailable as exc:
                self.supervisor.mark_com_health(False)
                self.supervisor.record_job_failure(str(exc), {"drawing_path": str(drawing_path), "operation": "execute_autolisp"})
                raise
            except Exception as exc:
                self.supervisor.mark_com_health(False)
                self.supervisor.record_job_failure(str(exc), {"drawing_path": str(drawing_path), "operation": "execute_autolisp"})
                raise ToolExecutionFailure(f"COM AutoLISP execution failed: {exc}") from exc
            finally:
                if document is not None:
                    try:
                        self.adapter.close_document(document, save_changes=False)
                    except Exception:
                        pass
                self.adapter.uninitialize_com()

    def manage_layers_and_blocks(self, drawing_path: Path, action: str, parameters: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            document = None
            try:
                self.adapter.initialize_com()
                app = self._connect()
                self.supervisor.mark_com_health(True)
                self.supervisor.record_electrical_context(
                    active_project_wdp=str(drawing_path.with_suffix('.wdp')),
                    wd_m_initialized=True,
                )
                document = self.adapter.open_document(app, drawing_path)
                self.supervisor.record_job_success()
                write_audit_record(
                    AuditRecord(
                        tool_name="manage_layers_and_blocks",
                        dwg_path=str(drawing_path),
                        execution_mode="com",
                        outcome="success",
                        message=f"COM action submitted: {action}",
                        operation_id="com-layers-blocks",
                        electrical_context={"active_project_wdp": str(drawing_path.with_suffix('.wdp')), "wd_m_initialized": True},
                    ),
                    self.audit_file,
                )
                return {
                    "status": "submitted",
                    "action": action,
                    "parameters": parameters,
                    "drawing": str(document.FullName),
                }
            except AutoCADUnavailable as exc:
                self.supervisor.mark_com_health(False)
                self.supervisor.record_job_failure(str(exc), {"drawing_path": str(drawing_path), "operation": action})
                raise
            except Exception as exc:
                self.supervisor.mark_com_health(False)
                self.supervisor.record_job_failure(str(exc), {"drawing_path": str(drawing_path), "operation": action})
                raise ToolExecutionFailure(f"COM layer/block operation failed: {exc}") from exc
            finally:
                if document is not None:
                    try:
                        self.adapter.close_document(document, save_changes=False)
                    except Exception:
                        pass
                self.adapter.uninitialize_com()

    def run_cad_command(self, drawing_path: Path, command: str, operation: str) -> dict[str, Any]:
        with self._lock:
            try:
                self.adapter.initialize_com()
                app = self._connect()
                self.supervisor.mark_com_health(True)
                document = self.adapter.get_open_document(app, drawing_path)
                if document is None:
                    raise AutoCADUnavailable("Target drawing is not open in the active AutoCAD session")
                self.adapter.send_command(document, command)
                self.supervisor.record_job_success()
                write_audit_record(
                    AuditRecord(
                        tool_name="execute_cad_command",
                        dwg_path=str(drawing_path),
                        execution_mode="com",
                        outcome="success",
                        message=f"COM CAD command submitted: {operation}",
                        operation_id="com-cad-command",
                        electrical_context={"active_project_wdp": str(drawing_path.with_suffix('.wdp')), "wd_m_initialized": True},
                    ),
                    self.audit_file,
                )
                return {
                    "status": "submitted",
                    "drawing": str(document.FullName),
                    "operation": operation,
                }
            except AutoCADUnavailable as exc:
                self.supervisor.mark_com_health(False)
                self.supervisor.record_job_failure(str(exc), {"drawing_path": str(drawing_path), "operation": operation})
                raise
            except Exception as exc:
                self.supervisor.mark_com_health(False)
                self.supervisor.record_job_failure(str(exc), {"drawing_path": str(drawing_path), "operation": operation})
                raise ToolExecutionFailure(f"COM CAD command execution failed: {exc}") from exc
            finally:
                self.adapter.uninitialize_com()
