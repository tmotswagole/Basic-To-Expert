"""Unit tests for models.

This module contains tests for data models.
"""

from models.config import PipelineState
from models.file import FileKey, FileRecord, SlimFileRecord
from models.result import ProcessingResult


def test_file_record_object_protocol(tmp_path):
    path = tmp_path / "sample.txt"
    path.write_text("one\ntwo\n", encoding="utf-8")

    first = FileRecord(path)
    second = FileRecord(path)

    assert first == second
    assert first is not second
    assert hash(first) == hash(second)
    assert len(first) == 2
    assert "FileRecord" in repr(first)
    assert "sample.txt" in str(first)


def test_file_key_interning_and_slim_record(tmp_path):
    path = tmp_path / "sample.txt"
    path.write_text("hello", encoding="utf-8")
    record = FileRecord(path)

    assert FileKey(path, record.checksum) is FileKey(path, record.checksum)
    slim = SlimFileRecord(path)
    assert slim.name == "sample.txt"


def test_processing_result_and_pipeline_state_copy():
    result = ProcessingResult("a.txt", "abc", "processed", 0.1, {"lines": 1})
    assert result.ok
    assert result.to_dict()["metadata"] == {"lines": 1}

    state = PipelineState(configuration={"workers": 1}, results={"items": []})
    shallow = state.clone()
    deep = state.clone(deep=True)
    shallow.results["items"].append("shared")
    assert state.results["items"] == ["shared"]
    deep.results["items"].append("independent")
    assert state.results["items"] == ["shared"]
