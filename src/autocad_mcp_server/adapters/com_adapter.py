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
    def connect(self, visible: bool = True) -> Any:
        if pythoncom is None or win32com is None:
            raise AutoCADUnavailable("pywin32 is not available on this system")
        pythoncom.CoInitialize()
        app = win32com.client.Dispatch("AutoCAD.Application")
        app.Visible = visible
        return app

    def open_document(self, app: Any, drawing_path: Path) -> Any:
        return app.Documents.Open(str(drawing_path))

    def send_command(self, document: Any, command: str) -> None:
        document.SendCommand(command + "\n")
