"""Operation history tracking.

This module maintains a history of pipeline operations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class HistoryEntry:
    operation: str
    status: str
    duration: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))


class OperationHistory:
    def __init__(self):
        self.entries: list[HistoryEntry] = []

    def add(self, operation: str, status: str, duration: float = 0.0) -> None:
        self.entries.append(HistoryEntry(operation, status, duration))

    def list(self) -> list[HistoryEntry]:
        return list(self.entries)
