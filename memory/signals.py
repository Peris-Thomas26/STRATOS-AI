from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Signal:
    title: str
    classification: str
    status: str = "new"
    evidence: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "classification": self.classification,
            "status": self.status,
            "evidence": self.evidence,
            "notes": self.notes,
        }
