"""Snapshot storage and persistence.

This module handles snapshot creation and storage.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from exceptions import SnapshotError
from models.snapshot import Snapshot


class SnapshotStore:
    def __init__(self, directory: str | Path = "snapshots"):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def save(self, snapshot: Snapshot) -> Path:
        path = self.directory / f"{snapshot.id}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json"
        payload = {
            "id": snapshot.id,
            "created_at": snapshot.created_at,
            "files": snapshot.files,
        }
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return path

    def load(self, path: str | Path) -> Snapshot:
        try:
            payload = json.loads(Path(path).read_text(encoding="utf-8"))
            return Snapshot(payload["id"], payload["created_at"], payload["files"])
        except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
            raise SnapshotError(f"Invalid snapshot {path}: {exc}") from exc
