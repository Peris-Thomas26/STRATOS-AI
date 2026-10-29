from __future__ import annotations

from typing import Any

import requests

DATASET_NAME = "solsticestudioai/synthetic-enterprise-ops-pack-sample"
HF_BASE_URL = "https://datasets-server.huggingface.co"

DEPARTMENT_BY_CONFIG: dict[str, str] = {
    "accounts": "customer",
    "account_health_daily": "customer",
    "crm_activities": "customer",
    "opportunities": "customer",
    "employees": "people",
    "meetings": "people",
    "meeting_attendees": "people",
    "incidents": "operations",
    "deployments": "operations",
    "postmortems": "operations",
    "service_level_objectives": "operations",
    "epics": "engineering",
    "commits": "engineering",
    "code_files": "engineering",
    "dashboard_suggestions": "product",
    "document_links": "knowledge",
    "documents": "knowledge",
    "metric_definitions": "operations",
}


# Fetch the actual split metadata for the Solstice dataset before ingestion.
def fetch_dataset_splits(dataset_name: str = DATASET_NAME) -> list[dict[str, Any]]:
    """Return Solstice split metadata from the Hugging Face dataset API."""
    response = requests.get(
        f"{HF_BASE_URL}/splits",
        params={"dataset": dataset_name},
        timeout=30,
    )
    response.raise_for_status()
    return response.json().get("splits", [])


# Translate a config name into a high-level department for internal analysis.
def infer_department(config_name: str) -> str:
    """Map a dataset config to a business department label."""
    return DEPARTMENT_BY_CONFIG.get(config_name, "unknown")


# Build the department-aware catalog that Phase 1 uses to bootstrap the knowledge base.
def build_dataset_catalog(payload: dict[str, Any]) -> list[dict[str, str]]:
    """Create a department-aware catalog from a Hugging Face split payload."""
    catalog: list[dict[str, str]] = []
    for item in payload.get("splits", []):
        config_name = item.get("config")
        if not config_name:
            continue
        catalog.append(
            {
                "dataset": item.get("dataset", DATASET_NAME),
                "config": config_name,
                "split": item.get("split", "train"),
                "department": infer_department(config_name),
            }
        )
    return catalog


# Pull a single page of rows from one config to inspect schema and data shape.
def fetch_config_rows(
    dataset_name: str = DATASET_NAME,
    config_name: str = "accounts",
    split: str = "train",
    offset: int = 0,
    length: int = 100,
) -> dict[str, Any]:
    """Retrieve one batch of rows from a specific Solstice dataset config."""
    response = requests.get(
        f"{HF_BASE_URL}/rows",
        params={
            "dataset": dataset_name,
            "config": config_name,
            "split": split,
            "offset": offset,
            "length": length,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


# Download the full set of rows for one config when we need complete data ingestion.
def fetch_all_rows_for_config(
    dataset_name: str = DATASET_NAME,
    config_name: str = "accounts",
    split: str = "train",
) -> list[dict[str, Any]]:
    """Return every row from a single Solstice config in paginated batches."""
    all_rows: list[dict[str, Any]] = []
    offset = 0

    while True:
        result = fetch_config_rows(dataset_name, config_name, split=split, offset=offset, length=100)
        rows = result.get("rows", [])
        if not rows:
            break

        all_rows.extend([row.get("row", {}) for row in rows])
        offset += len(rows)

        if offset >= int(result.get("num_rows_total", offset)):
            break

    return all_rows
