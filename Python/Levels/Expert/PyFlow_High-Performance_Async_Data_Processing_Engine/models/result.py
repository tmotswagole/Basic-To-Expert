"""Processing result models.

This module defines ProcessingResult and related structures.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ProcessingResult:
    path: str
    checksum: str
    status: str
    duration: float
    metadata: dict[str, object] = field(default_factory=dict)
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.status == "processed" and self.error is None

    def to_dict(self) -> dict[str, object]:
        return {
            "path": self.path,
            "checksum": self.checksum,
            "status": self.status,
            "duration": self.duration,
            "metadata": self.metadata,
            "error": self.error,
        }
