from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


# Ensure the target database directory exists before writing Phase 1 ingestion results.
def ensure_db_parent(path: str | Path) -> None:
    """Create the parent directory for a SQLite database if it does not exist."""
    db_path = Path(path)
    db_path.parent.mkdir(parents=True, exist_ok=True)


# Create the minimal ingestion tables needed to hold Solstice data, provenance, and department metadata.
def build_phase1_schema(db_path: str | Path = "stratos.db") -> str:
    """Create the Phase 1 SQLite schema for the company knowledge base."""
    ensure_db_parent(db_path)
    conn = sqlite3.connect(str(db_path))
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS department_catalog (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                config_name TEXT NOT NULL UNIQUE,
                department TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS ingestion_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dataset_name TEXT NOT NULL,
                config_name TEXT NOT NULL,
                split TEXT NOT NULL,
                status TEXT NOT NULL,
                record_count INTEGER DEFAULT 0,
                started_at TEXT DEFAULT CURRENT_TIMESTAMP,
                completed_at TEXT
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS raw_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                record_id TEXT,
                department TEXT NOT NULL,
                config_name TEXT NOT NULL,
                source_reference TEXT,
                record_payload TEXT NOT NULL,
                ingested_at TEXT DEFAULT CURRENT_TIMESTAMP,
                dataset_name TEXT NOT NULL
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS normalized_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                record_id TEXT,
                department TEXT NOT NULL,
                config_name TEXT NOT NULL,
                normalized_payload TEXT NOT NULL,
                ingested_at TEXT DEFAULT CURRENT_TIMESTAMP,
                dataset_name TEXT NOT NULL
            )
            """
        )

        conn.commit()
    finally:
        conn.close()

    return str(db_path)


# Store each inbound record together with the department, config, and dataset provenance.
def insert_raw_record(db_path: str | Path, record: dict[str, Any]) -> int:
    """Persist a raw Solstice record and its provenance metadata in SQLite."""
    build_phase1_schema(db_path)
    conn = sqlite3.connect(str(db_path))
    try:
        record_id = record.get("record_id") or record.get("id") or "unknown"
        department = record.get("department") or "unknown"
        config_name = record.get("config_name", "unknown")
        source_reference = record.get("source_reference") or ""
        dataset_name = record.get("dataset_name") or "solsticestudioai/synthetic-enterprise-ops-pack-sample"

        conn.execute(
            """
            INSERT OR IGNORE INTO department_catalog (config_name, department, description)
            VALUES (?, ?, ?)
            """,
            (config_name, department, f"Auto-registered department mapping for {config_name}"),
        )

        cursor = conn.execute(
            """
            INSERT INTO raw_records (record_id, department, config_name, source_reference, record_payload, dataset_name)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                str(record_id),
                department,
                config_name,
                source_reference,
                json.dumps(record.get("record_payload", {}), default=str),
                dataset_name,
            ),
        )
        conn.commit()
        return int(cursor.lastrowid)
    finally:
        conn.close()


# Return a count for quick validation during Phase 1 ingestion and debugging.
def count_records(db_path: str | Path, table_name: str = "raw_records") -> int:
    """Return the number of rows stored in a SQLite table."""
    conn = sqlite3.connect(str(db_path))
    try:
        result = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()
        return int(result[0]) if result else 0
    finally:
        conn.close()
