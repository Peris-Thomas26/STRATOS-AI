from __future__ import annotations

from typing import Any


def score_business_impact(
    internal_signal: dict[str, Any],
    external_signal: dict[str, Any] | None = None,
) -> float:
    """Estimate a rough impact score from 0.0 to 1.0 for a strategic finding."""
    score = 0.3
    if internal_signal.get("risk_level") == "high":
        score += 0.3
    if internal_signal.get("customer_impact") == "strategic_account":
        score += 0.2
    if external_signal and external_signal.get("source"):
        score += 0.2
    return min(score, 1.0)
