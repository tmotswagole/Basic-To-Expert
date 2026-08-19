"""Snapshot creation and comparison.

This module manages snapshots of directories and compares them.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

try:
    from .decorators import logged, timed, validate_path
    from .exceptions import InvalidSnapshotError
    from .scanner import scan_directory
except ImportError:
    from decorators import logged, timed, validate_path
    from exceptions import InvalidSnapshotError
    from scanner import scan_directory


@timed
@logged
@validate_path("directory")
def create_snapshot(directory: str | Path, output_dir: str | Path = "snapshots") -> Path:
    snapshot = scan_directory(directory)
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    filename = f"snapshot_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')}.json"
    path = destination / filename
    payload = {
        "root": str(snapshot.root),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "files": snapshot.as_mapping(),
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def load_snapshot(path: str | Path) -> dict[str, object]:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise InvalidSnapshotError(f"Could not load snapshot {path}: {exc}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("files"), dict):
        raise InvalidSnapshotError(f"Snapshot {path} is missing a files mapping.")
    return data


@timed
def compare_snapshots(old_snapshot: str | Path, new_snapshot: str | Path) -> dict[str, list[str]]:
    old = load_snapshot(old_snapshot)["files"]
    new = load_snapshot(new_snapshot)["files"]
    old_keys = set(old)
    new_keys = set(new)
    common = old_keys & new_keys
    modified = sorted(
        key
        for key in common
        if old[key]["checksum"] != new[key]["checksum"]
        or old[key]["size"] != new[key]["size"]
    )
    unchanged = sorted(key for key in common if key not in modified)
    return {
        "new": sorted(new_keys - old_keys),
        "modified": modified,
        "deleted": sorted(old_keys - new_keys),
        "unchanged": unchanged,
    }
