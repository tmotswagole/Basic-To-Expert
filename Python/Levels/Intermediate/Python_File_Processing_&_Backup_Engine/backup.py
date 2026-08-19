"""Backup operations and management.

This module handles backup creation and restoration.
"""

from __future__ import annotations

import shutil
from contextlib import contextmanager
from pathlib import Path

try:
    from .exceptions import BackupError, DirectoryNotFoundError
except ImportError:
    from exceptions import BackupError, DirectoryNotFoundError


class BackupOperation:
    def __init__(self, source: str | Path, destination: str | Path):
        self.source = Path(source)
        self.destination = Path(destination)
        self.created_paths: list[Path] = []

    def __enter__(self):
        if not self.source.exists():
            raise DirectoryNotFoundError(f"Source not found: {self.source}")
        self.destination.mkdir(parents=True, exist_ok=True)
        return self

    def copy(self) -> int:
        copied = 0
        try:
            if self.source.is_file():
                target = self.destination / self.source.name
                shutil.copy2(self.source, target)
                self.created_paths.append(target)
                return 1
            for path in self.source.rglob("*"):
                if path.is_dir():
                    continue
                relative = path.relative_to(self.source)
                target = self.destination / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, target)
                self.created_paths.append(target)
                copied += 1
        except OSError as exc:
            raise BackupError(str(exc)) from exc
        return copied

    def verify(self) -> bool:
        return all(path.exists() for path in self.created_paths)

    def __exit__(self, exc_type, exc, tb) -> bool:
        if exc_type is not None:
            for path in reversed(self.created_paths):
                try:
                    path.unlink(missing_ok=True)
                except OSError:
                    pass
            return False
        if not self.verify():
            raise BackupError("Backup verification failed.")
        return False


@contextmanager
def backup_operation(source: str | Path, destination: str | Path):
    operation = BackupOperation(source, destination)
    with operation as active:
        yield active
