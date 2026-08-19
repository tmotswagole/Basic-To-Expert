"""Directory scanning and file discovery.

This module handles discovering files and streaming them lazily.
"""

from __future__ import annotations

from pathlib import Path

try:
    from .decorators import timed, validate_path
    from .models import DirectorySnapshot, FileInfo
except ImportError:
    from decorators import timed, validate_path
    from models import DirectorySnapshot, FileInfo


def stream_files(directory: str | Path):
    root = Path(directory)
    for path in root.rglob("*"):
        if path.is_file():
            yield path


@timed
@validate_path("directory")
def scan_directory(directory: str | Path) -> DirectorySnapshot:
    root = Path(directory).resolve()
    return DirectorySnapshot(root, [FileInfo(path) for path in stream_files(root)])


def scan_summary(snapshot: DirectorySnapshot) -> dict[str, int]:
    python_files = sum(1 for file in snapshot.files if file.extension == ".py")
    text_files = sum(1 for file in snapshot.files if file.extension in {".txt", ".md", ".csv", ".json"})
    return {
        "files": len(snapshot.files),
        "total_size": snapshot.total_size(),
        "python_files": python_files,
        "text_files": text_files,
        "other_files": len(snapshot.files) - python_files - text_files,
    }
