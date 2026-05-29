from __future__ import annotations

from typing import Any


class AnalysisService:
    """Generates AutoLISP/VLA for drawing analysis and validation operations."""

    @staticmethod
    def _escape(value: Any) -> str:
        return str(value).replace('"', "").replace("\n", " ")

    def build_lisp(self, operation: str, parameters: dict[str, Any]) -> str:  # noqa: C901
        if operation == "check_drawing_standards":
            std = self._escape(parameters.get("standards_file", ""))
            if std:
                return f'(command "_.STANDARDS" "{std}")'
            return '(command "_.CHECKSTANDARDS")'

        if operation == "find_overlapping_objects":
            tol = parameters.get("tolerance", 0.001)
            return f'(command "_.OVERKILL" "_A" "" "_T" "{tol}" "")'

        if operation == "find_duplicate_objects":
            return '(command "_.OVERKILL" "_A" "" "")'

        if operation == "find_zero_length_entities":
            return (
                '(progn (setq cnt 0 ss (ssget "X" (list (cons 0 "LINE"))))'
                ' (if ss (repeat (setq i (sslength ss)) (setq i (1- i) ent (ssname ss i))'
                ' (setq ed (entget ent)) (if (equal (cdr (assoc 10 ed)) (cdr (assoc 11 ed)) 0.0001)'
                ' (progn (setq cnt (1+ cnt)) (princ (strcat "MCP_ZEROLEN:" (cdr (assoc 5 ed)) "\\n"))))))'
                ' (princ (strcat "MCP_RESULT:ZERO_LENGTH_COUNT=" (itoa cnt))) (princ))'
            )

        if operation == "layer_usage_report":
            return (
                '(progn (vlax-for layer (vla-get-layers (vla-get-activedocument (vlax-get-acad-object)))'
                ' (setq lname (vla-get-name layer))'
                ' (setq ss (ssget "X" (list (cons 8 lname))))'
                ' (setq cnt (if ss (sslength ss) 0))'
                ' (princ (strcat "MCP_LAYER:" lname "=" (itoa cnt)'
                ' ",frozen=" (if (= (vla-get-freeze layer) :vlax-true) "Y" "N")'
                ' ",locked=" (if (= (vla-get-lock layer) :vlax-true) "Y" "N") "\\n")))'
                ' (princ))'
            )

        if operation == "object_count_by_type":
            return (
                '(progn (setq types nil ss (ssget "X"))'
                ' (if ss (repeat (setq i (sslength ss)) (setq i (1- i) ent (ssname ss i))'
                ' (setq tp (cdr (assoc 0 (entget ent))))'
                ' (setq pair (assoc tp types))'
                ' (if pair (setq types (subst (cons tp (1+ (cdr pair))) pair types))'
                ' (setq types (cons (cons tp 1) types)))))'
                ' (foreach p types (princ (strcat "MCP_TYPE:" (car p) "=" (itoa (cdr p)) "\\n")))'
                ' (princ))'
            )

        if operation == "drawing_complexity_score":
            return (
                '(progn'
                ' (setq ss (ssget "X") ecnt (if ss (sslength ss) 0))'
                ' (setq lcnt 0) (vlax-for l (vla-get-layers (vla-get-activedocument (vlax-get-acad-object))) (setq lcnt (1+ lcnt)))'
                ' (setq bcnt 0) (vlax-for b (vla-get-blocks (vla-get-activedocument (vlax-get-acad-object))) (setq bcnt (1+ bcnt)))'
                ' (setq score (+ ecnt (* lcnt 10) (* bcnt 5)))'
                ' (princ (strcat "MCP_RESULT:ENTITIES=" (itoa ecnt)'
                ' ",LAYERS=" (itoa lcnt) ",BLOCKS=" (itoa bcnt)'
                ' ",COMPLEXITY_SCORE=" (itoa score)))'
                ' (princ))'
            )

        if operation == "detect_unclosed_polylines":
            return (
                '(progn (setq cnt 0 ss (ssget "X" (list (cons 0 "*POLYLINE"))))'
                ' (if ss (repeat (setq i (sslength ss)) (setq i (1- i) ent (ssname ss i))'
                ' (setq obj (vlax-ename->vla-object ent))'
                ' (if (= (vla-get-closed obj) :vlax-false)'
                ' (progn (setq cnt (1+ cnt))'
                ' (princ (strcat "MCP_UNCLOSED:" (vla-get-handle obj) "\\n"))))))'
                ' (princ (strcat "MCP_RESULT:UNCLOSED_COUNT=" (itoa cnt))) (princ))'
            )

        if operation == "validate_dimensions":
            return (
                '(progn (setq cnt 0 ss (ssget "X" (list (cons 0 "DIMENSION"))))'
                ' (if ss (setq cnt (sslength ss)))'
                ' (princ (strcat "MCP_RESULT:DIMENSION_COUNT=" (itoa cnt))) (princ))'
            )

        if operation == "compare_drawings":
            compare = self._escape(parameters.get("compare_with", ""))
            return f'(command "_.COMPARE" "{compare}")'

        if operation == "generate_bom":
            block_filter = self._escape(parameters.get("block_filter", "*"))
            return (
                f'(progn (setq ss (ssget "X" (list (cons 0 "INSERT") (cons 2 "{block_filter}"))))'
                f' (if ss (repeat (setq i (sslength ss)) (setq i (1- i) ent (ssname ss i))'
                f' (setq obj (vlax-ename->vla-object ent))'
                f' (princ (strcat "MCP_BOM:" (vla-get-effectivename obj)))'
                f' (if (= (vla-get-hasattributes obj) :vlax-true)'
                f' (progn (setq atts (vlax-safearray->list (vlax-variant-value (vla-getattributes obj))))'
                f' (foreach att atts (princ (strcat "|" (vla-get-tagstring att) "=" (vla-get-textstring att))))))'
                f' (princ "\\n"))) (princ))'
            )

        if operation == "calculate_total_line_length":
            layer = parameters.get("layer", "")
            filter_list = '(list (cons 0 "LINE,LWPOLYLINE"))'
            if layer:
                filter_list = f'(list (cons 0 "LINE,LWPOLYLINE") (cons 8 "{self._escape(layer)}"))'
            return (
                f'(progn (setq total 0.0 ss (ssget "X" {filter_list}))'
                f' (if ss (repeat (setq i (sslength ss)) (setq i (1- i) ent (ssname ss i))'
                f' (setq obj (vlax-ename->vla-object ent))'
                f' (setq total (+ total (vla-get-length obj)))))'
                f' (princ (strcat "MCP_RESULT:TOTAL_LENGTH=" (rtos total 2 6))) (princ))'
            )

        if operation == "count_blocks_in_area":
            x1 = parameters.get("x1", 0)
            y1 = parameters.get("y1", 0)
            x2 = parameters.get("x2", 0)
            y2 = parameters.get("y2", 0)
            return (
                f'(progn (setq cnt 0 ss (ssget "C" (list {x1} {y1}) (list {x2} {y2})'
                f' (list (cons 0 "INSERT"))))'
                f' (if ss (setq cnt (sslength ss)))'
                f' (princ (strcat "MCP_RESULT:BLOCKS_IN_AREA=" (itoa cnt))) (princ))'
            )

        if operation == "measure_perimeter":
            handle = self._escape(parameters.get("handle", ""))
            return (
                f'(progn (setq obj (vlax-ename->vla-object (handent "{handle}")))'
                f' (princ (strcat "MCP_RESULT:PERIMETER=" (rtos (vla-get-length obj) 2 6))) (princ))'
            )

        if operation == "find_text_containing":
            search = self._escape(parameters.get("search_text", ""))
            return (
                f'(progn (setq cnt 0 ss (ssget "X" (list (cons 0 "TEXT,MTEXT"))))'
                f' (if ss (repeat (setq i (sslength ss)) (setq i (1- i) ent (ssname ss i))'
                f' (setq obj (vlax-ename->vla-object ent))'
                f' (if (vl-string-search "{search}" (vla-get-textstring obj))'
                f' (progn (setq cnt (1+ cnt))'
                f' (princ (strcat "MCP_TEXT_FOUND:" (vla-get-handle obj) "=" (vla-get-textstring obj) "\\n"))))))'
                f' (princ (strcat "MCP_RESULT:FOUND_COUNT=" (itoa cnt))) (princ))'
            )

        if operation == "replace_text":
            find = self._escape(parameters.get("find_text", ""))
            replace = self._escape(parameters.get("replace_with", ""))
            return (
                f'(progn (setq cnt 0 ss (ssget "X" (list (cons 0 "TEXT,MTEXT"))))'
                f' (if ss (repeat (setq i (sslength ss)) (setq i (1- i) ent (ssname ss i))'
                f' (setq obj (vlax-ename->vla-object ent) txt (vla-get-textstring obj))'
                f' (if (vl-string-search "{find}" txt)'
                f' (progn (setq cnt (1+ cnt))'
                f' (vla-put-textstring obj (vl-string-subst "{replace}" "{find}" txt))))))'
                f' (princ (strcat "MCP_RESULT:REPLACED_COUNT=" (itoa cnt))) (princ))'
            )

        if operation == "list_all_text":
            return (
                '(progn (setq ss (ssget "X" (list (cons 0 "TEXT,MTEXT"))))'
                ' (if ss (repeat (setq i (sslength ss)) (setq i (1- i) ent (ssname ss i))'
                ' (setq obj (vlax-ename->vla-object ent))'
                ' (princ (strcat "MCP_TEXT:" (vla-get-handle obj)'
                ' "|layer=" (vla-get-layer obj)'
                ' "|text=" (vla-get-textstring obj) "\\n"))))'
                ' (princ))'
            )

        raise ValueError(f"Unsupported analysis operation: {operation}")
