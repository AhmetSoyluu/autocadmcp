from __future__ import annotations

from typing import Any


class XrefManagementService:
    """Generates AutoLISP/VLA for external reference operations."""

    @staticmethod
    def _escape(value: Any) -> str:
        return str(value).replace('"', "").replace("\n", " ")

    def build_lisp(self, action: str, parameters: dict[str, Any]) -> str:
        if action == "attach_xref":
            path = self._escape(parameters["xref_path"])
            x = parameters.get("x", 0)
            y = parameters.get("y", 0)
            scale = parameters.get("scale", 1.0)
            rot = parameters.get("rotation_deg", 0)
            return (
                f'(command "_.-XREF" "_A" "{path}" "{x},{y}" "{scale}" "{scale}" "{rot}")'
            )
        if action == "detach_xref":
            name = self._escape(parameters["xref_name"])
            return f'(command "_.-XREF" "_D" "{name}")'
        if action == "reload_xref":
            name = self._escape(parameters["xref_name"])
            return f'(command "_.-XREF" "_R" "{name}")'
        if action == "bind_xref":
            name = self._escape(parameters["xref_name"])
            return f'(command "_.-XREF" "_B" "{name}")'
        if action == "list_xrefs":
            return (
                '(progn (vlax-for blk (vla-get-blocks (vla-get-activedocument (vlax-get-acad-object))) '
                '(if (= (vla-get-isxref blk) :vlax-true) '
                '(princ (strcat "MCP_XREF:" (vla-get-name blk) '
                '"=" (vla-get-path blk) "\\n")))) (princ))'
            )
        if action == "attach_image":
            path = self._escape(parameters["image_path"])
            x = parameters.get("x", 0)
            y = parameters.get("y", 0)
            scale = parameters.get("scale", 1.0)
            rot = parameters.get("rotation_deg", 0)
            return (
                f'(command "_.-IMAGE" "_A" "{path}" "{x},{y}" "{scale}" "{rot}")'
            )
        if action == "attach_pdf_underlay":
            path = self._escape(parameters["pdf_path"])
            page = parameters.get("page", 1)
            x = parameters.get("x", 0)
            y = parameters.get("y", 0)
            scale = parameters.get("scale", 1.0)
            return (
                f'(command "_.PDFATTACH" "{path}" "{page}" "{x},{y}" "{scale}" "0")'
            )
        if action == "manage_xref_paths":
            return '(command "_.-XREF" "?")'
        raise ValueError(f"Unsupported xref action: {action}")
