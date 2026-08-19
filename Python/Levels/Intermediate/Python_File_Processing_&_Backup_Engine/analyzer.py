"""File analysis and streaming.

This module analyzes individual files and streams their contents.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

try:
    from .decorators import timed, validate_path
except ImportError:
    from decorators import timed, validate_path


def stream_lines(path: str | Path):
    with Path(path).open("r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            yield line


def non_empty_lines(lines):
    for line in lines:
        if line.strip():
            yield line


def normalize_lines(lines):
    for line in lines:
        yield line.strip().lower()


def filter_lines(lines, keyword: str):
    keyword = keyword.lower()
    for line in lines:
        if keyword in line.lower():
            yield line


def stream_chunks(path: str | Path, chunk_size: int = 4096):
    with Path(path).open("rb") as file:
        while chunk := file.read(chunk_size):
            yield chunk


def calculate_checksum(path: str | Path) -> str:
    digest = hashlib.sha256()
    for chunk in stream_chunks(path):
        digest.update(chunk)
    return digest.hexdigest()


@timed
@validate_path("file")
def analyze_file(path: str | Path) -> dict[str, object]:
    path = Path(path)
    lines = words = characters = empty_lines = longest_line = 0
    for line in stream_lines(path):
        lines += 1
        characters += len(line)
        words += len(line.split())
        if not line.strip():
            empty_lines += 1
        longest_line = max(longest_line, len(line.rstrip("\n")))
    return {
        "path": str(path),
        "name": path.name,
        "lines": lines,
        "words": words,
        "characters": characters,
        "empty_lines": empty_lines,
        "longest_line": longest_line,
        "average_line_length": characters / lines if lines else 0,
        "size": path.stat().st_size,
    }
