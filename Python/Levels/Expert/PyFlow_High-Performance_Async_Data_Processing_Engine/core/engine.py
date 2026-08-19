"""Core pipeline engine.

This module orchestrates the data processing pipeline.
"""

from __future__ import annotations

from models.config import PipelineConfig
from models.result import ProcessingResult
from core.pipeline import Pipeline


class PyFlowEngine:
    def __init__(self, config: PipelineConfig):
        self.pipeline = Pipeline(config)

    async def run(self) -> list[ProcessingResult]:
        return await self.pipeline.run()
