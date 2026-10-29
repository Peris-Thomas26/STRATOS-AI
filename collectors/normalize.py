from __future__ import annotations

from datetime import datetime
from typing import Any, Iterable


def _parse_published_at(value: Any) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return None
    return None


def normalize_articles(articles: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Normalize article fields and remove duplicates by URL, keeping the latest version."""
    normalized_by_url: dict[str, dict[str, Any]] = {}

    for article in articles:
        raw_url = article.get("url") or article.get("link")
        if not raw_url:
            continue

        normalized = {
            "title": article.get("title") or "Untitled",
            "url": raw_url,
            "source": article.get("source") or "Unknown source",
            "published_at": article.get("published_at") or article.get("published") or "",
            "summary": article.get("summary") or article.get("excerpt") or "",
            "content": article.get("content") or article.get("body") or "",
        }

        existing = normalized_by_url.get(raw_url)
        if existing is None:
            normalized_by_url[raw_url] = normalized
            continue

        existing_dt = _parse_published_at(existing.get("published_at"))
        candidate_dt = _parse_published_at(normalized.get("published_at"))

        if candidate_dt and (existing_dt is None or candidate_dt > existing_dt):
            normalized_by_url[raw_url] = normalized

    normalized = list(normalized_by_url.values())
    normalized.sort(key=lambda item: _parse_published_at(item.get("published_at")) or datetime.min, reverse=True)
    return normalized
