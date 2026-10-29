from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


# List which tables are present so we can quickly validate the dataset ingestion state.
def fetch_table_names(db_path: str | Path) -> list[str]:
    """Return all table names currently present in the SQLite database."""
    conn = sqlite3.connect(str(db_path))
    try:
        rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
        return [row[0] for row in rows]
    finally:
        conn.close()


# Count rows in a targeted table to verify ingestion completeness.
def count_records(db_path: str | Path, table_name: str) -> int:
    """Count rows in a database table."""
    conn = sqlite3.connect(str(db_path))
    try:
        row = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()
        return int(row[0]) if row else 0
    finally:
        conn.close()


# Aggregate live record counts per department so the first dashboard can summarize the company knowledge base.
def fetch_department_summary(db_path: str | Path) -> list[dict[str, Any]]:
    """Return a simple summary of records grouped by department."""
    conn = sqlite3.connect(str(db_path))
    try:
        rows = conn.execute(
            """
            SELECT department, COUNT(*) AS record_count
            FROM raw_records
            GROUP BY department
            ORDER BY record_count DESC
            """
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()
