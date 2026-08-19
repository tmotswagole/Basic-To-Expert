"""Process pool for CPU-bound work.

This module manages multiprocessing pools for heavy computation.
"""

from __future__ import annotations

import asyncio
from concurrent.futures import ProcessPoolExecutor
from typing import Callable


class ProcessPool:
    def __init__(self, max_workers: int | None = None):
        self.executor = ProcessPoolExecutor(max_workers=max_workers)

    async def run(self, func: Callable, *args):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.executor, func, *args)

    def shutdown(self) -> None:
        self.executor.shutdown(wait=True, cancel_futures=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.shutdown()
        return False
