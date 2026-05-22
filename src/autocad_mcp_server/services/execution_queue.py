from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeVar

T = TypeVar("T")


class ExecutionQueue:
    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._depth = 0

    @property
    def depth(self) -> int:
        return self._depth

    async def run(self, operation: Callable[[], Awaitable[T]]) -> T:
        self._depth += 1
        try:
            async with self._lock:
                return await operation()
        finally:
            self._depth -= 1
