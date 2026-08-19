"""Entry point for PyFlow — high-performance async data processing engine.

This file will contain the CLI interface for the PyFlow engine.
"""

from __future__ import annotations

import argparse
import asyncio

from core.engine import PyFlowEngine
from models.config import PipelineConfig
from models.snapshot import Snapshot
from storage.snapshots import SnapshotStore


async def run_command(args) -> None:
    config = PipelineConfig(
        root=args.directory,
        extensions=set(args.extensions) if args.extensions else None,
        workers=args.workers,
        queue_size=args.queue_size,
        snapshot_dir=args.snapshots,
    )
    engine = PyFlowEngine(config)
    results = await engine.run()
    print(f"Processed: {len(results)}")
    print(f"Successful: {sum(1 for result in results if result.ok)}")
    if args.snapshot:
        path = SnapshotStore(args.snapshots).save(Snapshot.from_results(results, "run"))
        print(f"Snapshot: {path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PyFlow async data processing engine")
    parser.add_argument("directory", help="Directory to process")
    parser.add_argument("--extensions", nargs="*", help="Extensions to include, such as .txt .json")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--queue-size", type=int, default=1000)
    parser.add_argument("--snapshots", default="snapshots")
    parser.add_argument("--snapshot", action="store_true")
    return parser


def main() -> None:
    asyncio.run(run_command(build_parser().parse_args()))


if __name__ == "__main__":
    main()
