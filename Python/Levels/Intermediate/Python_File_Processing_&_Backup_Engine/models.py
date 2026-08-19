"""Domain models for the file processor.

This module contains FileInfo, Directory, and Snapshot models.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path


def _checksum(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        while chunk := file.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def format_size(size: int) -> str:
    value = float(size)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if value < 1024 or unit == "TB":
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024
    return f"{value:.1f} TB"


@dataclass
class FileInfo:
    path: Path | str
    checksum: str | None = None
    name: str = field(init=False)
    extension: str = field(init=False)
    size: int = field(init=False)
    modified_time: float = field(init=False)

    def __post_init__(self) -> None:
        self.path = Path(self.path).resolve()
        if not self.path.is_file():
            raise FileNotFoundError(str(self.path))
        stat = self.path.stat()
        self.name = self.path.name
        self.extension = self.path.suffix.lower()
        self.size = stat.st_size
        self.modified_time = stat.st_mtime
        if self.checksum is None:
            self.checksum = _checksum(self.path)

    def __repr__(self) -> str:
        return f"FileInfo(path={str(self.path)!r}, size={self.size})"

    def __str__(self) -> str:
        return f"{self.name} - {format_size(self.size)}"

    def __len__(self) -> int:
        try:
            with self.path.open("r", encoding="utf-8", errors="ignore") as file:
                return sum(1 for _ in file)
        except OSError:
            return 0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FileInfo):
            return NotImplemented
        return self.path == other.path

    def __hash__(self) -> int:
        return hash(self.path)

    def to_dict(self) -> dict[str, object]:
        return {
            "path": str(self.path),
            "name": self.name,
            "extension": self.extension,
            "size": self.size,
            "modified_time": self.modified_time,
            "checksum": self.checksum,
        }


@dataclass
class DirectorySnapshot:
    root: Path | str
    files: list[FileInfo]

    def __post_init__(self) -> None:
        self.root = Path(self.root).resolve()

    def as_mapping(self) -> dict[str, dict[str, object]]:
        mapping = {}
        for file in self.files:
            key = str(file.path.relative_to(self.root)) if file.path.is_relative_to(self.root) else str(file.path)
            mapping[key] = file.to_dict()
        return mapping

    def total_size(self) -> int:
        return sum(file.size for file in self.files)
