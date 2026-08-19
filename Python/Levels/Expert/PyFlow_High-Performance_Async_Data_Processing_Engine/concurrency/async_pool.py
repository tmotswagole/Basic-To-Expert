"""Async worker pool for concurrent tasks.

This module manages asynchronous task execution.
"""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable, Iterable


class AsyncWorkerPool:
    def __init__(self, workers: int = 4, queue_size: int = 1000):
        self.workers = workers
        self.queue: asyncio.Queue = asyncio.Queue(maxsize=queue_size)

    async def map(self, items: Iterable, handler: Callable[[object], Awaitable[object]]) -> list[object]:
        results: list[object] = []

        async def worker():
            while True:
                item = await self.queue.get()
                if item is None:
                    self.queue.task_done()
                    break
                try:
                    results.append(await handler(item))
                finally:
                    self.queue.task_done()

        tasks = [asyncio.create_task(worker()) for _ in range(self.workers)]
        for item in items:
            await self.queue.put(item)
        for _ in tasks:
            await self.queue.put(None)
        await self.queue.join()
        await asyncio.gather(*tasks)
        return results
