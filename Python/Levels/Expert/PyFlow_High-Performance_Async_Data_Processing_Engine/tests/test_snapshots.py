"""Unit tests for snapshot operations.

This module contains tests for snapshot creation and comparison.
"""

from models.result import ProcessingResult
from models.snapshot import Snapshot


def test_snapshot_compare():
    old = Snapshot.from_results(
        [
            ProcessingResult("a.txt", "1", "processed", 0),
            ProcessingResult("b.txt", "2", "processed", 0),
        ],
        "old",
    )
    new = Snapshot.from_results(
        [
            ProcessingResult("a.txt", "changed", "processed", 0),
            ProcessingResult("c.txt", "3", "processed", 0),
        ],
        "new",
    )

    diff = old.compare(new)
    assert diff["modified"] == ["a.txt"]
    assert diff["deleted"] == ["b.txt"]
    assert diff["new"] == ["c.txt"]
