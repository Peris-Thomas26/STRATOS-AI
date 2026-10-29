from __future__ import annotations

from collections import OrderedDict
from typing import Any


def deduplicate_external_signals(signals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Remove exact duplicates from external monitoring records using title and URL."""
    deduped: OrderedDict[tuple[str, str], dict[str, Any]] = OrderedDict()
    for signal in signals:
        key = (
            str(signal.get("title", "")).strip().lower(),
            str(signal.get("url", "")).strip().lower(),
        )
        if key not in deduped:
            deduped[key] = signal
    return list(deduped.values())
