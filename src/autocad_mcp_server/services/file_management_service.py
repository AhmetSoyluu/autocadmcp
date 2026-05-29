from __future__ import annotations

from typing import Any


class FileManagementService:
    """Generates AutoLISP for file management operations."""

    @staticmethod
    def _escape(value: Any) -> str:
        return str(value).replace('"', "").replace("\n", " ")

    def build_lisp(self, action: str, dwg_path: str = "", template_path: str = "",
                   save_format: str = "dwg", save_changes: bool = True) -> str:
        if action == "create_new":
            if template_path:
                return f'(vla-open (vla-get-documents (vlax-get-acad-object)) "{self._escape(template_path)}")'
            return '(vla-add (vla-get-documents (vlax-get-acad-object)))'

        if action == "open":
            return f'(vla-open (vla-get-documents (vlax-get-acad-object)) "{self._escape(dwg_path)}")'

        if action == "save":
            if dwg_path:
                return f'(vla-save (vla-item (vla-get-documents (vlax-get-acad-object)) "{self._escape(dwg_path)}"))'
            return '(vla-save (vla-get-activedocument (vlax-get-acad-object)))'

        if action == "save_as":
            fmt_map = {"dwg": "acDwg", "dxf": "acDxf", "dwt": "acTemplate"}
            fmt = fmt_map.get(save_format, "acDwg")
            return (
                f'(vla-saveas (vla-get-activedocument (vlax-get-acad-object)) '
                f'"{self._escape(dwg_path)}" {fmt})'
            )

        if action == "close":
            save_arg = ":vlax-true" if save_changes else ":vlax-false"
            if dwg_path:
                return (
                    f'(vla-close (vla-item (vla-get-documents (vlax-get-acad-object)) '
                    f'"{self._escape(dwg_path)}") {save_arg})'
                )
            return f'(vla-close (vla-get-activedocument (vlax-get-acad-object)) {save_arg})'

        if action == "list_open":
            return (
                '(progn (setq docs (vla-get-documents (vlax-get-acad-object)))'
                ' (vlax-for doc docs (princ (strcat "MCP_DOC:" (vla-get-fullname doc) "\\n"))))'
            )

        if action == "set_active":
            return (
                f'(vla-put-activedocument (vlax-get-acad-object) '
                f'(vla-item (vla-get-documents (vlax-get-acad-object)) "{self._escape(dwg_path)}"))'
            )

        if action == "get_properties":
            return (
                '(progn (setq doc (vla-get-activedocument (vlax-get-acad-object)))'
                ' (princ (strcat "MCP_PROP:NAME=" (vla-get-name doc) "\\n"))'
                ' (princ (strcat "MCP_PROP:PATH=" (vla-get-fullname doc) "\\n"))'
                ' (princ (strcat "MCP_PROP:SAVED=" (if (= (vla-get-saved doc) :vlax-true) "Yes" "No") "\\n"))'
                ' (princ))'
            )

        raise ValueError(f"Unsupported file management action: {action}")
