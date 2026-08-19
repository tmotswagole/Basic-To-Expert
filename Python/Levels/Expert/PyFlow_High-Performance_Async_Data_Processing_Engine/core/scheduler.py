"""Async scheduler for concurrent task execution.

This module manages the async event loop and task scheduling.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass


@dataclass
class Metrics:
    processed: int = 0
    failed: int = 0
    cached: int = 0
    bytes_processed: int = 0


class AsyncScheduler:
    def __init__(self):
        self.metrics = Metrics()
        self._lock = asyncio.Lock()

    async def record_processed(self, size: int, cached: bool = False) -> None:
        async with self._lock:
            self.metrics.processed += 1
            self.metrics.bytes_processed += size
            if cached:
                self.metrics.cached += 1

    async def record_failed(self) -> None:
        async with self._lock:
            self.metrics.failed += 1
