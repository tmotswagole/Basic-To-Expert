"""Event system for pipeline notifications.

This module defines and manages pipeline events.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass(slots=True)
class Event:
    name: str
    payload: dict[str, object] = field(default_factory=dict)


class EventHandler(Protocol):
    def handle(self, event: Event) -> None: ...


class EventBus:
    def __init__(self):
        self._handlers: list[EventHandler] = []

    def subscribe(self, handler: EventHandler) -> None:
        self._handlers.append(handler)

    def publish(self, event: Event) -> None:
        for handler in list(self._handlers):
            handler.handle(event)


class MetricsHandler:
    def __init__(self):
        self.counts: dict[str, int] = {}

    def handle(self, event: Event) -> None:
        self.counts[event.name] = self.counts.get(event.name, 0) + 1
