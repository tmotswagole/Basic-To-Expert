"""Pipeline construction and management.

This module handles pipeline setup and execution.
"""

from __future__ import annotations

import asyncio
import time
from typing import Iterable

from cache.memory import MemoryCache
from core.events import Event, EventBus
from core.registry import ProcessorRegistry
from core.scheduler import AsyncScheduler
from models.config import PipelineConfig
from models.file import FileRecord
from models.result import ProcessingResult
from processing.scanner import deduplicate_files, filter_files, stream_files


class Pipeline:
    def __init__(
        self,
        config: PipelineConfig,
        registry: ProcessorRegistry | None = None,
        cache: MemoryCache | None = None,
        events: EventBus | None = None,
    ):
        self.config = config
        self.registry = registry or ProcessorRegistry()
        self.cache = cache or MemoryCache(max_size=config.cache_size)
        self.events = events or EventBus()
        self.scheduler = AsyncScheduler()

    def discover(self) -> Iterable[FileRecord]:
        return deduplicate_files(filter_files(stream_files(self.config.root), self.config.extensions))

    async def process_record(self, record: FileRecord) -> ProcessingResult:
        cached = self.cache.get(record.key)
        if cached is not None:
            self.events.publish(Event("CacheHit", {"path": str(record.path)}))
            await self.scheduler.record_processed(record.size, cached=True)
            return cached

        self.events.publish(Event("ProcessingStarted", {"path": str(record.path)}))
        processor = self.registry.get(record.extension)
        try:
            result = await asyncio.to_thread(processor.process, record)
        except Exception as exc:
            await self.scheduler.record_failed()
            result = ProcessingResult(str(record.path), record.checksum, "failed", 0, error=str(exc))
            self.events.publish(Event("ProcessingFailed", {"path": str(record.path), "error": str(exc)}))
            return result

        self.cache.set(record.key, result)
        await self.scheduler.record_processed(record.size)
        self.events.publish(Event("ProcessingCompleted", {"path": str(record.path)}))
        return result

    async def run(self) -> list[ProcessingResult]:
        queue: asyncio.Queue[FileRecord | None] = asyncio.Queue(maxsize=self.config.queue_size)
        results: list[ProcessingResult] = []

        async def producer():
            for record in self.discover():
                self.events.publish(Event("FileDiscovered", {"path": str(record.path)}))
                await queue.put(record)
            for _ in range(self.config.workers):
                await queue.put(None)

        async def consumer():
            while True:
                record = await queue.get()
                try:
                    if record is None:
                        return
                    results.append(await self.process_record(record))
                finally:
                    queue.task_done()

        started = time.perf_counter()
        consumers = [asyncio.create_task(consumer()) for _ in range(self.config.workers)]
        producer_task = asyncio.create_task(producer())
        try:
            await producer_task
            await queue.join()
            await asyncio.gather(*consumers)
        finally:
            for task in consumers:
                if not task.done():
                    task.cancel()
        self.events.publish(Event("PipelineCompleted", {"duration": time.perf_counter() - started}))
        return results


class PipelineSession:
    def __init__(self, config: PipelineConfig):
        self.pipeline = Pipeline(config)

    def __enter__(self):
        return self.pipeline

    def __exit__(self, exc_type, exc, tb):
        self.pipeline.events.publish(Event("PipelineShutdown"))
        return False


class AsyncPipelineSession(PipelineSession):
    async def __aenter__(self):
        return self.pipeline

    async def __aexit__(self, exc_type, exc, tb):
        self.pipeline.events.publish(Event("PipelineShutdown"))
        return False
