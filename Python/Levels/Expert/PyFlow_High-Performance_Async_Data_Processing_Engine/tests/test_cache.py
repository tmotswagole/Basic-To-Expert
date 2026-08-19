"""Unit tests for cache implementation.

This module contains tests for cache behavior and eviction.
"""

import time

from cache.memory import MemoryCache


def test_memory_cache_lru_and_stats():
    cache = MemoryCache(max_size=2)
    cache.set("a", 1)
    cache.set("b", 2)
    assert cache.get("a") == 1
    cache.set("c", 3)
    assert cache.get("b") is None
    stats = cache.stats()
    assert stats["hits"] == 1
    assert stats["misses"] == 1
    assert stats["evictions"] == 1
    assert stats["entries"] == 2


def test_memory_cache_ttl():
    cache = MemoryCache(max_size=2, ttl=0.01)
    cache.set("a", 1)
    time.sleep(0.02)
    assert cache.get("a") is None
