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

    def _get_or_open_document(self, app: Any, drawing_path: Path) -> tuple[Any, bool]:
        """Get already-open document or open it. Returns (document, opened_by_us)."""
        document = self.adapter.get_open_document(app, drawing_path)
        if document is not None:
            return document, False
        document = self.adapter.open_document(app, drawing_path)
        return document, True

    def _save_and_close_if_needed(self, document: Any, opened_by_us: bool) -> None:
        """Save document and close it only if we opened it."""
        if not opened_by_us:
            return
        try:
            # Save first to prevent "Save changes?" dialog
            document.Save()
        except Exception:
            pass
        try:
            document.Close(save_changes=True)
        except Exception:
            pass

    def run_lisp(self, drawing_path: Path, lisp_source: str) -> dict[str, str]:
        with self._lock:
            document = None
            opened_by_us = False
            try:
                self.adapter.initialize_com()
                app = self._connect()
                self.supervisor.mark_com_health(True)
                self.supervisor.record_electrical_context(
                    active_project_wdp=str(drawing_path.with_suffix('.wdp')),
                    wd_m_initialized=True,
                )
                document, opened_by_us = self._get_or_open_document(app, drawing_path)
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
                self._save_and_close_if_needed(document, opened_by_us)
                self.adapter.uninitialize_com()

    def manage_layers_and_blocks(self, drawing_path: Path, action: str, parameters: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            document = None
            opened_by_us = False
            try:
                self.adapter.initialize_com()
                app = self._connect()
                self.supervisor.mark_com_health(True)
                self.supervisor.record_electrical_context(
                    active_project_wdp=str(drawing_path.with_suffix('.wdp')),
                    wd_m_initialized=True,
                )
                document, opened_by_us = self._get_or_open_document(app, drawing_path)
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
                self._save_and_close_if_needed(document, opened_by_us)
                self.adapter.uninitialize_com()

    def run_file_command(self, lisp_source: str, action: str, dwg_path: str = "", template_path: str = "",
                         save_format: str = "dwg", save_changes: bool = True) -> dict[str, Any]:
        """Execute file management commands (create, open, save, close, etc.)
        These operations may not need a pre-existing document."""
        with self._lock:
            try:
                self.adapter.initialize_com()
                app = self._connect()
                self.supervisor.mark_com_health(True)

                if action == "create_new":
                    if template_path:
                        app.Documents.Add(template_path)
                    else:
                        app.Documents.Add()
                    doc = app.ActiveDocument
                    if dwg_path:
                        try:
                            doc.SaveAs(dwg_path)
                        except Exception:
                            pass
                    return {"status": "created", "drawing": str(doc.FullName), "action": action}

                if action == "open":
                    doc = app.Documents.Open(dwg_path)
                    return {"status": "opened", "drawing": str(doc.FullName), "action": action}

                if action == "save":
                    if dwg_path:
                        for d in app.Documents:
                            if str(d.FullName).lower() == dwg_path.lower():
                                d.Save()
                                return {"status": "saved", "drawing": dwg_path, "action": action}
                        raise ToolExecutionFailure(f"Document not found: {dwg_path}")
                    doc = app.ActiveDocument
                    doc.Save()
                    return {"status": "saved", "drawing": str(doc.FullName), "action": action}

                if action == "save_as":
                    doc = app.ActiveDocument
                    doc.SaveAs(dwg_path)
                    return {"status": "saved_as", "drawing": dwg_path, "action": action}

                if action == "close":
                    save = save_changes
                    if dwg_path:
                        for d in app.Documents:
                            if str(d.FullName).lower() == dwg_path.lower():
                                d.Close(save)
                                return {"status": "closed", "drawing": dwg_path, "action": action}
                        raise ToolExecutionFailure(f"Document not found: {dwg_path}")
                    doc = app.ActiveDocument
                    name = str(doc.FullName)
                    doc.Close(save)
                    return {"status": "closed", "drawing": name, "action": action}

                if action == "list_open":
                    docs = []
                    for d in app.Documents:
                        docs.append(str(d.FullName))
                    return {"status": "listed", "drawings": docs, "action": action}

                if action == "set_active":
                    for d in app.Documents:
                        if str(d.FullName).lower() == dwg_path.lower():
                            app.ActiveDocument = d
                            return {"status": "activated", "drawing": dwg_path, "action": action}
                    raise ToolExecutionFailure(f"Document not found among open drawings: {dwg_path}")

                if action == "get_properties":
                    doc = app.ActiveDocument
                    return {
                        "status": "properties",
                        "name": doc.Name,
                        "full_path": str(doc.FullName),
                        "saved": doc.Saved,
                        "action": action,
                    }

                # Fallback: send as command on active document
                doc = app.ActiveDocument
                doc.SendCommand(lisp_source + "\n")
                self.supervisor.record_job_success()
                return {"status": "submitted", "drawing": str(doc.FullName), "action": action}

            except AutoCADUnavailable as exc:
                self.supervisor.mark_com_health(False)
                self.supervisor.record_job_failure(str(exc), {"operation": action})
                raise
            except ToolExecutionFailure:
                raise
            except Exception as exc:
                self.supervisor.mark_com_health(False)
                self.supervisor.record_job_failure(str(exc), {"operation": action})
                raise ToolExecutionFailure(f"File management operation failed: {exc}") from exc
            finally:
                self.adapter.uninitialize_com()

    def run_cad_command(self, drawing_path: Path, command: str, operation: str) -> dict[str, Any]:
        with self._lock:
            document = None
            opened_by_us = False
            try:
                self.adapter.initialize_com()
                app = self._connect()
                self.supervisor.mark_com_health(True)
                document, opened_by_us = self._get_or_open_document(app, drawing_path)
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
                self._save_and_close_if_needed(document, opened_by_us)
                self.adapter.uninitialize_com()
