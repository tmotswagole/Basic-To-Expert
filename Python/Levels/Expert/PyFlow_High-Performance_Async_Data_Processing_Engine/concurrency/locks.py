"""Async locks and synchronization primitives.

This module provides thread-safe shared state management.
"""

from __future__ import annotations

import asyncio


class AsyncCounter:
    def __init__(self):
        self.value = 0
        self._lock = asyncio.Lock()

    async def increment(self, amount: int = 1) -> int:
        async with self._lock:
            self.value += amount
            return self.value
