"""File discovery and scanning.

This module implements lazy file discovery as a generator.
"""

from __future__ import annotations

from pathlib import Path

from models.file import FileRecord


def stream_files(directory: str | Path):
    root = Path(directory)
    for path in root.rglob("*"):
        if path.is_file():
            yield FileRecord(path)


def filter_files(records, extensions: set[str] | None = None):
    if extensions is None:
        yield from records
        return
    normalized = {item.lower() for item in extensions}
    for record in records:
        if record.extension in normalized:
            yield record


def deduplicate_files(records):
    seen = set()
    for record in records:
        if record.key in seen:
            continue
        seen.add(record.key)
        yield record


def batch_files(records, size: int):
    batch = []
    for record in records:
        batch.append(record)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch
