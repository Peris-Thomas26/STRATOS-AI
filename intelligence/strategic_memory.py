from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class StrategicSignal:
    """A historical strategic insight with provenance and status tracking."""

    signal_id: str
    title: str
    description: str
    status: str = "new"
    evidence: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


def mark_signal_status(signal: StrategicSignal, new_status: str) -> StrategicSignal:
    """Update the lifecycle status of a strategic signal."""
    signal.status = new_status
    signal.updated_at = datetime.now(timezone.utc).isoformat()
    return signal
