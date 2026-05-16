from __future__ import annotations

from typing import Protocol


class IdGeneratorPort(Protocol):
    def new(self) -> str:
        """Generate a new stable identifier for aggregates or read-model records."""
