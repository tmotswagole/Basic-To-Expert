"""Cache eviction strategies.

This module implements LRU, TTL, and other eviction policies.
"""

from __future__ import annotations

import time
from collections import OrderedDict


class LRUEviction:
    def evict(self, store: OrderedDict):
        if store:
            return store.popitem(last=False)
        return None


def expired(created_at: float, ttl: float | None) -> bool:
    return ttl is not None and time.monotonic() - created_at > ttl
