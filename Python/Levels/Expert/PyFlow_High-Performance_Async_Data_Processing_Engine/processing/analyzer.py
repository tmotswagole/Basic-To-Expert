"""File analysis and feature extraction.

This module performs CPU-heavy analysis on files.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path


def analyze_text(path: str | Path) -> dict[str, object]:
    lines = words = characters = 0
    frequencies: Counter[str] = Counter()
    with Path(path).open("r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            tokens = line.split()
            lines += 1
            words += len(tokens)
            characters += len(line)
            frequencies.update(token.strip(".,:;!?()[]{}\"'").lower() for token in tokens)
    return {
        "lines": lines,
        "words": words,
        "characters": characters,
        "top_words": frequencies.most_common(10),
    }


def cpu_heavy_analysis(path: str | Path) -> dict[str, object]:
    return analyze_text(path)
