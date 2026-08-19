"""Configuration models.

This module defines pipeline configuration and settings.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class PipelineConfig:
    root: Path | str
    extensions: set[str] | None = None
    workers: int = 4
    queue_size: int = 1000
    cache_size: int = 10_000
    snapshot_dir: Path | str = "snapshots"
    use_process_pool: bool = False

    def __post_init__(self) -> None:
        self.root = Path(self.root).resolve()
        self.snapshot_dir = Path(self.snapshot_dir)
        if self.workers < 1:
            raise ValueError("workers must be at least 1")
        if self.queue_size < 1:
            raise ValueError("queue_size must be at least 1")
        if self.cache_size < 1:
            raise ValueError("cache_size must be at least 1")
        if self.extensions is not None:
            self.extensions = {item.lower() for item in self.extensions}


@dataclass
class PipelineState:
    configuration: dict[str, object] = field(default_factory=dict)
    statistics: dict[str, int] = field(default_factory=dict)
    active_files: list[str] = field(default_factory=list)
    results: dict[str, list[object]] = field(default_factory=dict)

    def clone(self, deep: bool = False):
        import copy

        return copy.deepcopy(self) if deep else copy.copy(self)
