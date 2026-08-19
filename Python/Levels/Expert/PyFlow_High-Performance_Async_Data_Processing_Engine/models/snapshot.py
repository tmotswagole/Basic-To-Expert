"""Snapshot models for state capture.

This module defines snapshot structures for processing state.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from models.result import ProcessingResult


@dataclass(slots=True)
class Snapshot:
    id: str
    created_at: str
    files: dict[str, dict[str, object]] = field(default_factory=dict)

    @classmethod
    def from_results(cls, results: list[ProcessingResult], id: str = "run") -> "Snapshot":
        return cls(
            id=id,
            created_at=datetime.now().isoformat(timespec="seconds"),
            files={result.path: result.to_dict() for result in results},
        )

    def compare(self, other: "Snapshot") -> dict[str, list[str]]:
        old_keys = set(self.files)
        new_keys = set(other.files)
        common = old_keys & new_keys
        modified = sorted(
            key for key in common if self.files[key].get("checksum") != other.files[key].get("checksum")
        )
        return {
            "new": sorted(new_keys - old_keys),
            "modified": modified,
            "deleted": sorted(old_keys - new_keys),
            "unchanged": sorted(key for key in common if key not in modified),
        }
