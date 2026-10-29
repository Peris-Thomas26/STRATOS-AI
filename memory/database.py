from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any


def get_connection(db_path: str | Path = "stratos.db") -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def init_schema(db_path: str | Path = "stratos.db") -> None:
    conn = get_connection(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url TEXT UNIQUE,
            source TEXT,
            published_at TEXT,
            summary TEXT,
            fetched_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def save_article(db_path: str | Path = "stratos.db", article: dict[str, Any] | None = None) -> dict[str, Any]:
    if not article:
        raise ValueError("Article data is required.")

    payload = {
        "title": article.get("title") or "Untitled",
        "url": article.get("url") or article.get("link") or "",
        "source": article.get("source") or "Unknown source",
        "published_at": article.get("published_at") or article.get("published") or datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "summary": article.get("summary") or article.get("excerpt") or "",
    }

    conn = get_connection(db_path)
    conn.execute(
        """
        INSERT OR REPLACE INTO articles (title, url, source, published_at, summary)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            payload["title"],
            payload["url"],
            payload["source"],
            payload["published_at"],
            payload["summary"],
        ),
    )
    conn.commit()
    conn.close()
    return payload


def fetch_recent_articles(db_path: str | Path = "stratos.db", limit: int = 20) -> list[dict[str, Any]]:
    conn = get_connection(db_path)
    rows = conn.execute(
        "SELECT * FROM articles ORDER BY published_at DESC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]
