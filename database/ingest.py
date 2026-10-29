from __future__ import annotations

from pathlib import Path
from typing import Any

from connectors.solstice import (
    DATASET_NAME,
    build_dataset_catalog,
    fetch_all_rows_for_config,
    fetch_dataset_splits,
)
from database.schema import build_phase1_schema, insert_raw_record


# Create a stable record identifier when a config does not expose an explicit ID field.
def generate_record_identifier(config_name: str, row: dict[str, Any], index: int) -> str:
    """Generate a deterministic record ID for a Solstice row."""
    candidates = [
        "record_id",
        "id",
        "account_id",
        "employee_id",
        "incident_id",
        "opportunity_id",
        "meeting_id",
        "service_id",
        "document_id",
        "account_health_id",
    ]

    for field_name in candidates:
        value = row.get(field_name)
        if value not in (None, ""):
            return str(value)

    return f"{config_name}:{index}"


# Package each row for storage with full provenance and department mapping.
def prepare_record_for_storage(
    config_name: str,
    department: str,
    row: dict[str, Any],
    dataset_name: str,
    index: int,
) -> dict[str, Any]:
    """Return a provenance-aware raw record payload for DB insertion."""
    return {
        "record_id": generate_record_identifier(config_name, row, index),
        "department": department,
        "config_name": config_name,
        "dataset_name": dataset_name,
        "source_reference": f"https://huggingface.co/datasets/{dataset_name}",
        "record_payload": row,
    }


# Ingest the complete Solstice dataset into SQLite, grouped by department and config.
def ingest_solstice_dataset(
    db_path: str | Path = "data/processed/stratos.db",
    dataset_name: str = DATASET_NAME,
    split: str = "train",
) -> dict[str, Any]:
    """Download every Solstice config and persist the raw rows in the company knowledge base."""
    build_phase1_schema(db_path)

    catalog = build_dataset_catalog({"splits": fetch_dataset_splits(dataset_name)})
    processed_configs: list[str] = []
    row_count = 0

    for item in catalog:
        config_name = item.get("config")
        if not config_name:
            continue

        rows = fetch_all_rows_for_config(dataset_name=dataset_name, config_name=config_name, split=split)
        if not rows:
            continue

        for index, row in enumerate(rows):
            if not isinstance(row, dict):
                continue
            record = prepare_record_for_storage(
                config_name=config_name,
                department=item.get("department", "unknown"),
                row=row,
                dataset_name=dataset_name,
                index=index,
            )
            insert_raw_record(db_path, record)
            row_count += 1

        processed_configs.append(config_name)

    return {
        "config_count": len(processed_configs),
        "row_count": row_count,
        "configs": processed_configs,
    }
