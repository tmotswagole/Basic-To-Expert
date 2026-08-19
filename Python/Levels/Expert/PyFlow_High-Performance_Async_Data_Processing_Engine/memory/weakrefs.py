"""Weak reference utilities.

This module implements weak reference patterns for registries.
"""

from __future__ import annotations

import weakref


class WeakRegistry:
    def __init__(self):
        self._items = weakref.WeakValueDictionary()

    def add(self, key: str, value) -> None:
        self._items[key] = value

    def get(self, key: str):
        return self._items.get(key)

    def keys(self):
        return list(self._items.keys())
