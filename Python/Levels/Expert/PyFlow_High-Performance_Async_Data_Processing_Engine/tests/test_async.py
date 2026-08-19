"""Unit tests for async functionality.

This module contains tests for asynchronous operations.
"""

import asyncio

from concurrency.async_pool import AsyncWorkerPool
from concurrency.locks import AsyncCounter
from core.scheduler import AsyncScheduler


def test_async_worker_pool_and_counter():
    async def run():
        pool = AsyncWorkerPool(workers=2, queue_size=1)

        async def double(value):
            await asyncio.sleep(0)
            return value * 2

        results = await pool.map([1, 2, 3], double)
        counter = AsyncCounter()
        await asyncio.gather(*(counter.increment() for _ in range(5)))
        return sorted(results), counter.value

    results, count = asyncio.run(run())
    assert results == [2, 4, 6]
    assert count == 5


def test_scheduler_metrics_lock():
    async def run():
        scheduler = AsyncScheduler()
        await asyncio.gather(*(scheduler.record_processed(10) for _ in range(3)))
        await scheduler.record_failed()
        return scheduler.metrics

    metrics = asyncio.run(run())
    assert metrics.processed == 3
    assert metrics.failed == 1
    assert metrics.bytes_processed == 30
