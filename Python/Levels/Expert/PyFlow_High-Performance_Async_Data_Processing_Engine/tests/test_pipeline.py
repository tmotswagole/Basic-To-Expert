"""Unit tests for pipeline execution.

This module contains tests for pipeline construction and execution.
"""

import asyncio

from core.engine import PyFlowEngine
from core.events import MetricsHandler
from models.config import PipelineConfig
from models.snapshot import Snapshot
from storage.snapshots import SnapshotStore


def test_pipeline_processes_files_and_writes_snapshot(tmp_path):
    (tmp_path / "a.txt").write_text("hello world\n", encoding="utf-8")
    (tmp_path / "b.log").write_text("ERROR timeout\n", encoding="utf-8")
    config = PipelineConfig(tmp_path, extensions={".txt", ".log"}, workers=2, queue_size=1)
    engine = PyFlowEngine(config)
    metrics = MetricsHandler()
    engine.pipeline.events.subscribe(metrics)

    results = asyncio.run(engine.run())

    assert len(results) == 2
    assert all(result.ok for result in results)
    assert metrics.counts["FileDiscovered"] == 2

    store = SnapshotStore(tmp_path / "snapshots")
    path = store.save(Snapshot.from_results(results, "test_run"))
    loaded = store.load(path)
    assert len(loaded.files) == 2
