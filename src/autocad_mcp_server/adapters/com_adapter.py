from __future__ import annotations

from pathlib import Path
from typing import Any

from autocad_mcp_server.utils.errors import AutoCADUnavailable

try:
    import pythoncom
    import win32com.client
except ImportError:
    pythoncom = None
    win32com = None


class ComAdapter:
    def initialize_com(self) -> None:
        if pythoncom is None:
            raise AutoCADUnavailable("pywin32 is not available on this system")
        pythoncom.CoInitialize()

    def uninitialize_com(self) -> None:
        if pythoncom is not None:
            pythoncom.CoUninitialize()

    def connect(self, visible: bool = True, launch_if_missing: bool = False) -> Any:
        if win32com is None:
            raise AutoCADUnavailable("pywin32 is not available on this system")

        try:
            app = win32com.client.GetActiveObject("AutoCAD.Application")
            app.Visible = visible
            return app
        except Exception:
            if not launch_if_missing:
                raise AutoCADUnavailable("No running AutoCAD COM session found")

        app = win32com.client.Dispatch("AutoCAD.Application")
        app.Visible = visible
        return app

    def open_document(self, app: Any, drawing_path: Path) -> Any:
        return app.Documents.Open(str(drawing_path))

    def close_document(self, document: Any, save_changes: bool = False) -> None:
        document.Close(save_changes)

    def send_command(self, document: Any, command: str) -> None:
        document.SendCommand(command + "\n")
