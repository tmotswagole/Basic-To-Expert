"""Decorators for timing, logging, and validation.

This module provides reusable decorators for the file processor.
"""

from __future__ import annotations

import functools
import time
from pathlib import Path

try:
    from .exceptions import DirectoryNotFoundError, FileNotFoundError
except ImportError:
    from exceptions import DirectoryNotFoundError, FileNotFoundError


OPERATION_HISTORY: list[dict[str, object]] = []


def timed(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        started = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - started
            OPERATION_HISTORY.append(
                {"operation": func.__name__.upper(), "duration": elapsed, "status": "TIMED"}
            )
            print(f"{func.__name__} took {elapsed:.3f}s")

    return wrapper


def logged(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        name = func.__name__.upper()
        OPERATION_HISTORY.append({"operation": name, "event": "started"})
        try:
            result = func(*args, **kwargs)
        except Exception:
            OPERATION_HISTORY.append({"operation": name, "event": "failed"})
            raise
        OPERATION_HISTORY.append({"operation": name, "event": "completed"})
        return result

    return wrapper


def validate_path(kind: str = "exists"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(path, *args, **kwargs):
            candidate = Path(path)
            if kind == "directory" and not candidate.is_dir():
                raise DirectoryNotFoundError(f"Directory not found: {candidate}")
            if kind == "file" and not candidate.is_file():
                raise FileNotFoundError(f"File not found: {candidate}")
            if kind == "exists" and not candidate.exists():
                raise FileNotFoundError(f"Path not found: {candidate}")
            return func(path, *args, **kwargs)

        return wrapper

    return decorator


def history() -> list[dict[str, object]]:
    return list(OPERATION_HISTORY)
