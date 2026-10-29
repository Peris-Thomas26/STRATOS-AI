from __future__ import annotations

from typing import Any


def summarize_account_health(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Return a compact view of account health based on account_health_daily records."""
    if not records:
        return {"account_count": 0, "average_health_score": 0.0, "risk_distribution": {}}

    scores = [float(item.get("health_score", 0.0)) for item in records if item.get("health_score") is not None]
    risk_counts: dict[str, int] = {}
    for item in records:
        risk = str(item.get("renewal_risk_band", "unknown"))
        risk_counts[risk] = risk_counts.get(risk, 0) + 1

    return {
        "account_count": len({item.get("account_id") for item in records if item.get("account_id")}),
        "average_health_score": sum(scores) / len(scores) if scores else 0.0,
        "risk_distribution": risk_counts,
    }


def summarize_incident_backlog(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Summarize incident volume and severity for operational analysis."""
    if not records:
        return {"incident_count": 0, "severity_breakdown": {}}

    severity_breakdown: dict[str, int] = {}
    for item in records:
        severity = str(item.get("severity", "unknown"))
        severity_breakdown[severity] = severity_breakdown.get(severity, 0) + 1

    return {"incident_count": len(records), "severity_breakdown": severity_breakdown}


def compute_department_snapshot(records: list[dict[str, Any]], department_field: str = "department") -> dict[str, int]:
    """Count records by department for a quick operational summary."""
    summary: dict[str, int] = {}
    for item in records:
        department = str(item.get(department_field, "unknown"))
        summary[department] = summary.get(department, 0) + 1
    return summary
