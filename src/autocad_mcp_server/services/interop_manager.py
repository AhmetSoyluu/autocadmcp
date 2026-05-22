from __future__ import annotations

import threading
from pathlib import Path
from typing import Any

from autocad_mcp_server.adapters.com_adapter import ComAdapter
from autocad_mcp_server.utils.errors import AutoCADUnavailable, ToolExecutionFailure


class InteropManager:
    def __init__(self, adapter: ComAdapter, visible: bool, launch_if_missing: bool) -> None:
        self.adapter = adapter
        self.visible = visible
        self.launch_if_missing = launch_if_missing
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
                document = self.adapter.open_document(app, drawing_path)
                self.adapter.send_command(document, lisp_source)
                return {"status": "submitted", "drawing": str(drawing_path)}
            except AutoCADUnavailable:
                raise
            except Exception as exc:
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
                document = self.adapter.open_document(app, drawing_path)
                return {
                    "status": "submitted",
                    "action": action,
                    "parameters": parameters,
                    "drawing": str(document.FullName),
                }
            except AutoCADUnavailable:
                raise
            except Exception as exc:
                raise ToolExecutionFailure(f"COM layer/block operation failed: {exc}") from exc
            finally:
                if document is not None:
                    try:
                        self.adapter.close_document(document, save_changes=False)
                    except Exception:
                        pass
                self.adapter.uninitialize_com()
