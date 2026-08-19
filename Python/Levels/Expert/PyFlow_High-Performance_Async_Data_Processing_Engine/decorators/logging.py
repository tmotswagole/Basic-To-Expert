"""Logging decorators for observability.

This module provides logging decorators for function execution.
"""

from __future__ import annotations

import asyncio
import functools
import logging


def logged(func):
    logger = logging.getLogger(func.__module__)
    if asyncio.iscoroutinefunction(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            logger.info("%s started", func.__name__)
            try:
                result = await func(*args, **kwargs)
            except Exception:
                logger.exception("%s failed", func.__name__)
                raise
            logger.info("%s completed", func.__name__)
            return result
        return async_wrapper

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info("%s started", func.__name__)
        try:
            result = func(*args, **kwargs)
        except Exception:
            logger.exception("%s failed", func.__name__)
            raise
        logger.info("%s completed", func.__name__)
        return result
    return wrapper
