"""File models and metadata.

This module defines FileRecord and related structures.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


def format_size(size: int) -> str:
    value = float(size)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if value < 1024 or unit == "TB":
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024
    return f"{value:.1f} TB"


def checksum_for_path(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        while chunk := file.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


class FileKey(tuple):
    _cache: dict[tuple[str, str], "FileKey"] = {}

    def __new__(cls, path: str | Path, checksum: str):
        key = (str(Path(path).resolve()), checksum)
        if key not in cls._cache:
            cls._cache[key] = super().__new__(cls, key)
        return cls._cache[key]

    @property
    def path(self) -> str:
        return self[0]

    @property
    def checksum(self) -> str:
        return self[1]


class FileRecord:
    def __init__(self, path: str | Path, status: str = "discovered", checksum: str | None = None):
        self.path = Path(path).resolve()
        if not self.path.is_file():
            raise FileNotFoundError(str(self.path))
        stat = self.path.stat()
        self.name = self.path.name
        self.extension = self.path.suffix.lower()
        self.size = stat.st_size
        self.modified_at = stat.st_mtime
        self.checksum = checksum or checksum_for_path(self.path)
        self.status = status

    @property
    def key(self) -> FileKey:
        return FileKey(self.path, self.checksum)

    def __repr__(self) -> str:
        return f"FileRecord(path={str(self.path)!r}, size={self.size}, checksum={self.checksum!r})"

    def __str__(self) -> str:
        return f"{self.name} - {format_size(self.size)} - {self.status}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FileRecord):
            return NotImplemented
        return self.path == other.path and self.checksum == other.checksum

    def __hash__(self) -> int:
        return hash((self.path, self.checksum))

    def __len__(self) -> int:
        with self.path.open("r", encoding="utf-8", errors="ignore") as file:
            return sum(1 for _ in file)

    def to_dict(self) -> dict[str, object]:
        return {
            "path": str(self.path),
            "name": self.name,
            "extension": self.extension,
            "size": self.size,
            "modified_at": self.modified_at,
            "checksum": self.checksum,
            "status": self.status,
        }


class SlimFileRecord:
    __slots__ = ("path", "name", "extension", "size", "modified_at", "checksum", "status")

    def __init__(self, path: str | Path, status: str = "discovered", checksum: str | None = None):
        record = FileRecord(path, status=status, checksum=checksum)
        self.path = record.path
        self.name = record.name
        self.extension = record.extension
        self.size = record.size
        self.modified_at = record.modified_at
        self.checksum = record.checksum
        self.status = record.status
