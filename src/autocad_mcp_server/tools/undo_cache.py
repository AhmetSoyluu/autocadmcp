from __future__ import annotations

import time

from autocad_mcp_server.services.drawing_state_cache import DrawingStateCache
from autocad_mcp_server.services.dwg_service import DWGService
from autocad_mcp_server.services.undo_redo_service import UndoRedoService
from autocad_mcp_server.tools.common import error_response, success_response


def register_undo_redo_tool(mcp, service: DWGService, undo_redo: UndoRedoService) -> None:
    @mcp.tool()
    async def undo_last_action(dwg_path: str, execution_mode: str = "auto") -> dict:
        """Undo the last recorded action on the drawing."""
        snapshot = undo_redo.pop_undo(dwg_path)
        if snapshot is None:
            return success_response("undo_last_action", "service", {"message": "Nothing to undo"}, [])
        try:
            drawing_path = service.sandbox.validate(dwg_path)
            result = await service._run_lisp_via_com_or_console(
                drawing_path, snapshot.lisp_to_undo, execution_mode,
                prefix="undo", operation_name="undo",
            )
            result.payload["undone_action"] = snapshot.description
            return success_response("undo_last_action", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("undo_last_action", execution_mode, exc)

    @mcp.tool()
    async def redo_last_action(dwg_path: str, execution_mode: str = "auto") -> dict:
        """Redo the last undone action on the drawing."""
        snapshot = undo_redo.pop_redo(dwg_path)
        if snapshot is None:
            return success_response("redo_last_action", "service", {"message": "Nothing to redo"}, [])
        try:
            drawing_path = service.sandbox.validate(dwg_path)
            result = await service._run_lisp_via_com_or_console(
                drawing_path, snapshot.lisp_to_redo, execution_mode,
                prefix="redo", operation_name="redo",
            )
            result.payload["redone_action"] = snapshot.description
            return success_response("redo_last_action", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("redo_last_action", execution_mode, exc)

    @mcp.tool()
    async def get_undo_history(dwg_path: str, limit: int = 20) -> dict:
        """Get the undo history for a drawing."""
        history = undo_redo.get_undo_history(dwg_path, limit)
        stats = undo_redo.get_stats(dwg_path)
        return success_response("get_undo_history", "service", {
            "drawing": dwg_path,
            "history": history,
            **stats,
        }, [])

    @mcp.tool()
    async def undo_multiple(dwg_path: str, count: int = 1, execution_mode: str = "auto") -> dict:
        """Undo multiple actions at once."""
        undone = []
        for _ in range(count):
            snapshot = undo_redo.pop_undo(dwg_path)
            if snapshot is None:
                break
            undone.append(snapshot.description)
        if not undone:
            return success_response("undo_multiple", "service", {"message": "Nothing to undo"}, [])
        try:
            lisp = f'(repeat {len(undone)} (command "_.U"))'
            drawing_path = service.sandbox.validate(dwg_path)
            result = await service._run_lisp_via_com_or_console(
                drawing_path, lisp, execution_mode,
                prefix="undo-multi", operation_name="undo_multiple",
            )
            result.payload["undone_actions"] = undone
            result.payload["undone_count"] = len(undone)
            return success_response("undo_multiple", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("undo_multiple", execution_mode, exc)

    @mcp.tool()
    async def set_undo_mark(dwg_path: str, execution_mode: str = "auto") -> dict:
        """Set an undo mark (group boundary) in the drawing."""
        try:
            drawing_path = service.sandbox.validate(dwg_path)
            lisp = '(command "_.UNDO" "_BE")'
            result = await service._run_lisp_via_com_or_console(
                drawing_path, lisp, execution_mode,
                prefix="undo-mark", operation_name="set_undo_mark",
            )
            return success_response("set_undo_mark", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("set_undo_mark", execution_mode, exc)

    @mcp.tool()
    async def end_undo_mark(dwg_path: str, execution_mode: str = "auto") -> dict:
        """End an undo group. All actions since set_undo_mark will undo as one."""
        try:
            drawing_path = service.sandbox.validate(dwg_path)
            lisp = '(command "_.UNDO" "_E")'
            result = await service._run_lisp_via_com_or_console(
                drawing_path, lisp, execution_mode,
                prefix="undo-end", operation_name="end_undo_mark",
            )
            return success_response("end_undo_mark", result.execution_mode, result.payload, result.warnings)
        except Exception as exc:
            return error_response("end_undo_mark", execution_mode, exc)


def register_cache_tool(mcp, service: DWGService, cache: DrawingStateCache) -> None:
    @mcp.tool()
    async def refresh_drawing_cache(dwg_path: str, execution_mode: str = "auto") -> dict:
        """Refresh the in-memory cache for a drawing (layers, blocks, styles, variables, extents)."""
        try:
            drawing_path = service.sandbox.validate(dwg_path)
            lisp = cache.build_refresh_lisp()
            result = await service._run_lisp_via_com_or_console(
                drawing_path, lisp, execution_mode,
                prefix="cache-refresh", operation_name="refresh_cache",
            )
            cached = cache.parse_refresh_output(str(drawing_path), result.payload.get("stdout", ""))
            return success_response("refresh_drawing_cache", result.execution_mode, {
                "drawing": str(drawing_path),
                "layers": cached.layer_names,
                "blocks": cached.block_names,
                "text_styles": cached.text_style_names,
                "linetypes": cached.linetype_names,
                "entity_count": cached.entity_count,
                "extents": cached.extents,
                "variables": cached.variables,
            }, result.warnings)
        except Exception as exc:
            return error_response("refresh_drawing_cache", execution_mode, exc)

    @mcp.tool()
    async def get_cached_drawing_state(dwg_path: str) -> dict:
        """Get the cached drawing state without querying AutoCAD. Returns None if cache is stale."""
        cached = cache.get(dwg_path)
        if cached is None:
            return success_response("get_cached_drawing_state", "service", {
                "cached": False,
                "message": "Cache is empty or expired. Use refresh_drawing_cache to populate.",
            }, [])
        return success_response("get_cached_drawing_state", "service", {
            "cached": True,
            "drawing": cached.drawing_path,
            "layers": cached.layer_names,
            "blocks": cached.block_names,
            "text_styles": cached.text_style_names,
            "linetypes": cached.linetype_names,
            "entity_count": cached.entity_count,
            "extents": cached.extents,
            "variables": cached.variables,
            "age_seconds": round(time.time() - cached.last_refreshed, 1),
        }, [])

    @mcp.tool()
    async def invalidate_cache(dwg_path: str = "") -> dict:
        """Invalidate the cache for a drawing (or all drawings if no path given)."""
        if dwg_path:
            cache.invalidate(dwg_path)
            return success_response("invalidate_cache", "service", {
                "invalidated": dwg_path,
            }, [])
        cache.invalidate_all()
        return success_response("invalidate_cache", "service", {
            "invalidated": "all",
        }, [])

    @mcp.tool()
    async def get_cache_stats() -> dict:
        """Get cache statistics for all cached drawings."""
        return success_response("get_cache_stats", "service", cache.get_stats(), [])


