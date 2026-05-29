from __future__ import annotations

from typing import Any


class BlockManagementService:
    """Generates AutoLISP/VLA for block management operations."""

    @staticmethod
    def _escape(value: Any) -> str:
        return str(value).replace('"', "").replace("\n", " ")

    def build_lisp(self, action: str, parameters: dict[str, Any]) -> str:  # noqa: C901
        if action == "create_block_definition":
            name = self._escape(parameters["block_name"])
            bx = parameters.get("base_x", 0)
            by = parameters.get("base_y", 0)
            handles = parameters.get("handles", [])
            selections = " ".join(f'(handent "{self._escape(h)}")' for h in handles)
            return (
                f'(command "_.-BLOCK" "{name}" "{bx},{by}" {selections} "")'
            )

        if action == "list_block_definitions":
            return (
                '(progn '
                '(vlax-for blk (vla-get-blocks (vla-get-activedocument (vlax-get-acad-object))) '
                '(if (and (= (vla-get-isxref blk) :vlax-false) (= (vla-get-islayout blk) :vlax-false)) '
                '(princ (strcat "MCP_BLOCK:" (vla-get-name blk) "\\n")))) (princ))'
            )

        if action == "get_block_attributes":
            handle = self._escape(parameters["handle"])
            return (
                f'(progn (setq obj (vlax-ename->vla-object (handent "{handle}")))'
                f' (if (= (vla-get-hasattributes obj) :vlax-true)'
                f' (progn (setq atts (vlax-safearray->list (vlax-variant-value (vla-getattributes obj))))'
                f' (foreach att atts (princ (strcat "MCP_ATTR:" (vla-get-tagstring att) "=" (vla-get-textstring att) "\\n")))))'
                f' (princ))'
            )

        if action == "set_block_attributes":
            handle = self._escape(parameters["handle"])
            attrs = parameters.get("attributes", {})
            set_lines = []
            for tag, val in attrs.items():
                set_lines.append(
                    f'(if (= (strcase (vla-get-tagstring att)) (strcase "{self._escape(tag)}")) '
                    f'(vla-put-textstring att "{self._escape(val)}"))'
                )
            inner = " ".join(set_lines)
            return (
                f'(progn (setq obj (vlax-ename->vla-object (handent "{handle}")))'
                f' (setq atts (vlax-safearray->list (vlax-variant-value (vla-getattributes obj))))'
                f' (foreach att atts {inner}) (princ))'
            )

        if action == "explode_block":
            handle = self._escape(parameters["handle"])
            return f'(command "_.EXPLODE" (handent "{handle}"))'

        if action == "rename_block":
            old = self._escape(parameters["old_name"])
            new = self._escape(parameters["new_name"])
            return f'(command "_.-RENAME" "_B" "{old}" "{new}")'

        if action == "count_block_references":
            name = self._escape(parameters["block_name"])
            return (
                f'(progn (setq cnt 0 ss (ssget "X" (list (cons 0 "INSERT") (cons 2 "{name}"))))'
                f' (if ss (setq cnt (sslength ss)))'
                f' (princ (strcat "MCP_RESULT:BLOCK_COUNT=" (itoa cnt))) (princ))'
            )

        if action == "export_block_to_file":
            name = self._escape(parameters["block_name"])
            output_path = self._escape(parameters.get("output_path", ""))
            return f'(command "_.WBLOCK" "{output_path}" "{name}")'

        if action == "import_block_from_file":
            source = self._escape(parameters["source_file"])
            name = self._escape(parameters.get("block_name", "*"))
            return f'(command "_.-INSERT" "{source}" "" "" "" "")'

        raise ValueError(f"Unsupported block management action: {action}")
