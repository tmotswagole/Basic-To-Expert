"""Unit tests for worker processes.

This module contains tests for CPU-bound task execution.
"""

from processing.scanner import batch_files, deduplicate_files, filter_files, stream_files
from processing.workers import process_record


def test_scanner_pipeline_and_worker(tmp_path):
    (tmp_path / "a.txt").write_text("hello hello\n", encoding="utf-8")
    (tmp_path / "b.bin").write_bytes(b"\x00\x01")

    records = list(filter_files(stream_files(tmp_path), {".txt"}))
    assert len(records) == 1
    assert list(batch_files(records, 10))[0] == records
    assert list(deduplicate_files(records + records)) == records

    result = process_record(records[0])
    assert result.ok
    assert result.metadata["words"] == 2
