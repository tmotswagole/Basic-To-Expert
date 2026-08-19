"""Timing decorators for performance measurement.

This module provides decorators for timing function execution.
"""

from __future__ import annotations

import asyncio
import functools
import time


def timed(func):
    if asyncio.iscoroutinefunction(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            started = time.perf_counter()
            try:
                return await func(*args, **kwargs)
            finally:
                async_wrapper.last_duration = time.perf_counter() - started
        async_wrapper.last_duration = 0.0
        return async_wrapper

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        started = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            wrapper.last_duration = time.perf_counter() - started
    wrapper.last_duration = 0.0
    return wrapper
