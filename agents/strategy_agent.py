from __future__ import annotations

from typing import Any


def prepare_evidence_summary(internal_records: list[dict[str, Any]], external_records: list[dict[str, Any]]) -> dict[str, Any]:
    """Package internal and external facts into a compact evidence bundle for strategy review."""
    return {
        "internal_record_count": len(internal_records),
        "external_record_count": len(external_records),
        "internal_summary": internal_records[:3],
        "external_summary": external_records[:3],
    }
