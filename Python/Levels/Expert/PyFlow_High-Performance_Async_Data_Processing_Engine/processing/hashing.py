"""File hashing and checksum calculation.

This module implements various hashing strategies.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


def stream_chunks(path: str | Path, chunk_size: int = 1024 * 1024):
    with Path(path).open("rb") as file:
        while chunk := file.read(chunk_size):
            yield chunk


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    for chunk in stream_chunks(path):
        digest.update(chunk)
    return digest.hexdigest()
