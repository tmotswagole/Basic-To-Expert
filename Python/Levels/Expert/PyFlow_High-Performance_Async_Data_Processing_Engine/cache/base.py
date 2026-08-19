"""Base cache implementation.

This module defines the cache interface and protocol.
"""

from __future__ import annotations

from typing import Generic, Protocol, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class Cache(Protocol[K, V]):
    def get(self, key: K, default: V | None = None) -> V | None: ...
    def set(self, key: K, value: V) -> None: ...
    def delete(self, key: K) -> None: ...
    def contains(self, key: K) -> bool: ...
    def clear(self) -> None: ...


class CacheStats(dict):
    @property
    def hit_rate(self) -> float:
        total = self.get("hits", 0) + self.get("misses", 0)
        return self.get("hits", 0) / total if total else 0.0
