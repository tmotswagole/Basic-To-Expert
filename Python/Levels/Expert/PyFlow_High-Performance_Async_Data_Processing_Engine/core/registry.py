"""Registry for processors and handlers.

This module manages plugin registration and lookup.
"""

from __future__ import annotations

from typing import Protocol

from models.file import FileRecord
from models.result import ProcessingResult
from processing.workers import process_record


class Processor(Protocol):
    def process(self, record: FileRecord) -> ProcessingResult: ...


class DefaultProcessor:
    def process(self, record: FileRecord) -> ProcessingResult:
        return process_record(record)


class ProcessorRegistry:
    def __init__(self):
        self._processors: dict[str, Processor] = {}
        self.default = DefaultProcessor()

    def register(self, extension: str, processor: Processor) -> None:
        self._processors[extension.lower()] = processor

    def get(self, extension: str) -> Processor:
        return self._processors.get(extension.lower(), self.default)
