"""In-memory cache implementation.

This module implements a generic in-memory cache with eviction.
"""

from __future__ import annotations

import time
from collections import OrderedDict
from typing import Generic, TypeVar

from cache.base import CacheStats
from cache.eviction import expired

K = TypeVar("K")
V = TypeVar("V")


class MemoryCache(Generic[K, V]):
    def __init__(self, max_size: int = 1000, ttl: float | None = None):
        self.max_size = max_size
        self.ttl = ttl
        self._store: OrderedDict[K, tuple[float, V]] = OrderedDict()
        self._stats = CacheStats(hits=0, misses=0, evictions=0)

    def get(self, key: K, default: V | None = None) -> V | None:
        item = self._store.get(key)
        if item is None:
            self._stats["misses"] += 1
            return default
        created_at, value = item
        if expired(created_at, self.ttl):
            self.delete(key)
            self._stats["misses"] += 1
            return default
        self._store.move_to_end(key)
        self._stats["hits"] += 1
        return value

    def set(self, key: K, value: V) -> None:
        self._store[key] = (time.monotonic(), value)
        self._store.move_to_end(key)
        while len(self._store) > self.max_size:
            self._store.popitem(last=False)
            self._stats["evictions"] += 1

    def delete(self, key: K) -> None:
        self._store.pop(key, None)

    def contains(self, key: K) -> bool:
        sentinel = object()
        return self.get(key, sentinel) is not sentinel

    def clear(self) -> None:
        self._store.clear()

    def stats(self) -> CacheStats:
        stats = CacheStats(self._stats)
        stats["entries"] = len(self._store)
        return stats
