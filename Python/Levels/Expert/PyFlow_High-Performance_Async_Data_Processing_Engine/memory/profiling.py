"""Memory profiling and analysis.

This module provides tools for memory inspection and profiling.
"""

from __future__ import annotations

import gc
import sys
import tracemalloc


def object_size(obj) -> int:
    return sys.getsizeof(obj)


def memory_snapshot() -> dict[str, object]:
    if not tracemalloc.is_tracing():
        tracemalloc.start()
    current, peak = tracemalloc.get_traced_memory()
    return {
        "current": current,
        "peak": peak,
        "gc_counts": gc.get_count(),
    }
