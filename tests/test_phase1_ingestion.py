from __future__ import annotations

import sqlite3

from connectors.solstice import build_dataset_catalog
from database.ingest import ingest_solstice_dataset
from database.schema import build_phase1_schema, insert_raw_record


def test_build_dataset_catalog_extracts_configs_and_departments():
    payload = {
        "splits": [
            {"dataset": "solsticestudioai/synthetic-enterprise-ops-pack-sample", "config": "accounts", "split": "train"},
            {"dataset": "solsticestudioai/synthetic-enterprise-ops-pack-sample", "config": "employees", "split": "train"},
            {"dataset": "solsticestudioai/synthetic-enterprise-ops-pack-sample", "config": "incidents", "split": "train"},
        ]
    }

    catalog = build_dataset_catalog(payload)

    assert [item["config"] for item in catalog] == ["accounts", "employees", "incidents"]
    assert {item["department"] for item in catalog} == {"customer", "people", "operations"}


def test_build_phase1_schema_creates_expected_tables(tmp_path):
    db_path = tmp_path / "solstice.db"

    build_phase1_schema(db_path)

    with sqlite3.connect(db_path) as conn:
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;"
        ).fetchall()

    table_names = {row[0] for row in tables}
    assert {"ingestion_runs", "raw_records", "normalized_records", "department_catalog"}.issubset(table_names)


def test_insert_raw_record_persists_provenance(tmp_path):
    db_path = tmp_path / "solstice.db"
    build_phase1_schema(db_path)

    record = {
        "record_id": "A001",
        "department": "customer",
        "config_name": "accounts",
        "record_payload": {"account_id": "A001", "status": "customer"},
        "source_reference": "https://huggingface.co/datasets/solsticestudioai/synthetic-enterprise-ops-pack-sample",
    }

    insert_raw_record(db_path, record)

    with sqlite3.connect(db_path) as conn:
        rows = conn.execute("SELECT record_id, department, config_name FROM raw_records").fetchall()

    assert rows == [("A001", "customer", "accounts")]


def test_ingest_solstice_dataset_persists_rows(tmp_path, monkeypatch):
    db_path = tmp_path / "solstice.db"

    def fake_fetch_dataset_splits(dataset_name):
        return [
            {"dataset": dataset_name, "config": "accounts", "split": "train"},
            {"dataset": dataset_name, "config": "employees", "split": "train"},
        ]

    def fake_fetch_all_rows_for_config(dataset_name, config_name, split="train"):
        if config_name == "accounts":
            return [{"account_id": "A001", "status": "customer"}, {"account_id": "A002", "status": "prospect"}]
        return [{"employee_id": "E001", "department": "engineering"}]

    monkeypatch.setattr("database.ingest.fetch_dataset_splits", fake_fetch_dataset_splits)
    monkeypatch.setattr("database.ingest.fetch_all_rows_for_config", fake_fetch_all_rows_for_config)

    summary = ingest_solstice_dataset(db_path=db_path)

    assert summary["config_count"] == 2
    assert summary["row_count"] == 3
    with sqlite3.connect(db_path) as conn:
        raw_count = conn.execute("SELECT COUNT(*) FROM raw_records").fetchone()[0]
        dept_count = conn.execute("SELECT COUNT(DISTINCT department) FROM raw_records").fetchone()[0]

    assert raw_count == 3
    assert dept_count >= 2
