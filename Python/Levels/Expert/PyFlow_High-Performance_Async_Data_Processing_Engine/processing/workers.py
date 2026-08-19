"""Worker processes and task execution.

This module manages worker processes and task distribution.
"""

from __future__ import annotations

import time

from models.file import FileRecord
from models.result import ProcessingResult
from processing.analyzer import analyze_text


def process_record(record: FileRecord) -> ProcessingResult:
    started = time.perf_counter()
    try:
        metadata = analyze_text(record.path) if record.extension in {".txt", ".log", ".md", ".py", ".csv"} else {}
        record.status = "processed"
        return ProcessingResult(
            path=str(record.path),
            checksum=record.checksum,
            status="processed",
            duration=time.perf_counter() - started,
            metadata=metadata,
        )
    except Exception as exc:
        record.status = "failed"
        return ProcessingResult(
            path=str(record.path),
            checksum=record.checksum,
            status="failed",
            duration=time.perf_counter() - started,
            error=str(exc),
        )
