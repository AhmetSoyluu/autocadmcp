from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class DrawingSnapshot:
    """A single undo/redo state snapshot."""
    timestamp: float
    description: str
    lisp_to_undo: str  # LISP expression to undo this action
    lisp_to_redo: str  # LISP expression to redo this action


class UndoRedoService:
    """Tracks undo/redo state per drawing using a per-drawing stack."""

    MAX_HISTORY = 50

    def __init__(self) -> None:
        # keyed by drawing_path (str) → undo_stack, redo_stack
        self._undo_stacks: dict[str, deque[DrawingSnapshot]] = {}
        self._redo_stacks: dict[str, deque[DrawingSnapshot]] = {}

    def _ensure_stacks(self, drawing_path: str) -> None:
        if drawing_path not in self._undo_stacks:
            self._undo_stacks[drawing_path] = deque(maxlen=self.MAX_HISTORY)
            self._redo_stacks[drawing_path] = deque(maxlen=self.MAX_HISTORY)

    def record_action(
        self,
        drawing_path: str,
        description: str,
        lisp_to_undo: str = '(command "_.U")',
        lisp_to_redo: str = '(command "_.MREDO" "1")',
    ) -> None:
        """Record an undoable action. Clears redo stack."""
        self._ensure_stacks(drawing_path)
        snapshot = DrawingSnapshot(
            timestamp=time.time(),
            description=description,
            lisp_to_undo=lisp_to_undo,
            lisp_to_redo=lisp_to_redo,
        )
        self._undo_stacks[drawing_path].append(snapshot)
        self._redo_stacks[drawing_path].clear()

    def can_undo(self, drawing_path: str) -> bool:
        return len(self._undo_stacks.get(drawing_path, [])) > 0

    def can_redo(self, drawing_path: str) -> bool:
        return len(self._redo_stacks.get(drawing_path, [])) > 0

    def pop_undo(self, drawing_path: str) -> DrawingSnapshot | None:
        """Pop the latest action from undo stack, push to redo."""
        self._ensure_stacks(drawing_path)
        if not self._undo_stacks[drawing_path]:
            return None
        snapshot = self._undo_stacks[drawing_path].pop()
        self._redo_stacks[drawing_path].append(snapshot)
        return snapshot

    def pop_redo(self, drawing_path: str) -> DrawingSnapshot | None:
        """Pop the latest action from redo stack, push to undo."""
        self._ensure_stacks(drawing_path)
        if not self._redo_stacks[drawing_path]:
            return None
        snapshot = self._redo_stacks[drawing_path].pop()
        self._undo_stacks[drawing_path].append(snapshot)
        return snapshot

    def get_undo_history(self, drawing_path: str, limit: int = 20) -> list[dict[str, Any]]:
        """Return recent undo history as a list of dicts."""
        self._ensure_stacks(drawing_path)
        stack = self._undo_stacks[drawing_path]
        items = list(stack)[-limit:]
        return [
            {"index": i, "description": s.description, "timestamp": s.timestamp}
            for i, s in enumerate(reversed(items))
        ]

    def clear_history(self, drawing_path: str) -> None:
        """Clear all undo/redo history for a drawing."""
        self._undo_stacks.pop(drawing_path, None)
        self._redo_stacks.pop(drawing_path, None)

    def get_stats(self, drawing_path: str) -> dict[str, Any]:
        self._ensure_stacks(drawing_path)
        return {
            "undo_depth": len(self._undo_stacks[drawing_path]),
            "redo_depth": len(self._redo_stacks[drawing_path]),
            "max_history": self.MAX_HISTORY,
        }
