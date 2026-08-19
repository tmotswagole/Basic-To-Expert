"""Retry decorators with exponential backoff.

This module provides automatic retry logic for resilience.
"""

from __future__ import annotations

import asyncio
import functools
import time


def retry(attempts: int = 3, delay: float = 0.1, exceptions: tuple[type[Exception], ...] = (Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    last_error = exc
                    if attempt < attempts - 1:
                        time.sleep(delay * (2 ** attempt))
            raise last_error
        return wrapper
    return decorator


def async_retry(attempts: int = 3, delay: float = 0.1, exceptions: tuple[type[Exception], ...] = (Exception,)):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(attempts):
                try:
                    return await func(*args, **kwargs)
                except exceptions as exc:
                    last_error = exc
                    if attempt < attempts - 1:
                        await asyncio.sleep(delay * (2 ** attempt))
            raise last_error
        return wrapper
    return decorator
