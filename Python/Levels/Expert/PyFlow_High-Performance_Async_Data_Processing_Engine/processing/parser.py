"""File parsing and content extraction.

This module handles file parsing for various formats.
"""

from __future__ import annotations

import json
from pathlib import Path


def parse_text(path: str | Path) -> dict[str, object]:
    text = Path(path).read_text(encoding="utf-8", errors="ignore")
    return {"text": text, "characters": len(text), "words": len(text.split())}


def parse_json(path: str | Path) -> dict[str, object]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return {"json": data, "type": type(data).__name__}


def parse_file(path: str | Path) -> dict[str, object]:
    path = Path(path)
    if path.suffix.lower() == ".json":
        return parse_json(path)
    if path.suffix.lower() in {".txt", ".log", ".md", ".py", ".csv"}:
        return parse_text(path)
    return {"bytes": path.stat().st_size}
