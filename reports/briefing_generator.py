from __future__ import annotations

from typing import Any


def generate_management_brief(findings: list[dict[str, Any]]) -> str:
    """Generate a simple text summary of strategic findings for management review."""
    lines = ["# STRATOS Management Brief", ""]
    for idx, finding in enumerate(findings, start=1):
        lines.append(f"## Finding {idx}: {finding.get('title', 'Untitled finding')}")
        lines.append(f"- Impact: {finding.get('impact', 'unknown')}")
        lines.append(f"- Evidence: {finding.get('evidence', 'Not available')}")
        lines.append("")
    return "\n".join(lines)
