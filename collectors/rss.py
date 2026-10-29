from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import feedparser
import requests


def _parsed_time_to_iso(value: Any) -> str | None:
    if not value:
        return None
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value).isoformat()
        except ValueError:
            return None
    if hasattr(value, "tm_year"):
        try:
            return datetime(*value[:6], tzinfo=timezone.utc).isoformat()
        except TypeError:
            return None
    return None


def parse_feed_entries(feed_data: str) -> list[dict[str, Any]]:
    """Parse a raw RSS/Atom feed string into normalized article dictionaries."""
    parsed = feedparser.parse(feed_data)
    channel_title = getattr(parsed.feed, "title", None) or "Unknown source"
    articles: list[dict[str, Any]] = []

    for entry in parsed.entries:
        title = getattr(entry, "title", None) or "Untitled"
        link = getattr(entry, "link", None)
        summary = getattr(entry, "summary", None) or getattr(entry, "description", None) or ""
        published_value = getattr(entry, "published", None) or getattr(entry, "updated", None)
        published_at = _parsed_time_to_iso(getattr(entry, "published_parsed", None)) or _parsed_time_to_iso(getattr(entry, "updated_parsed", None)) or published_value or ""

        source = getattr(entry, "source", None)
        source_title = getattr(source, "title", None) or channel_title

        articles.append(
            {
                "title": str(title).strip(),
                "url": str(link).strip() if link else "",
                "source": str(source_title).strip(),
                "published_at": published_at,
                "summary": str(summary).strip(),
                "content": str(summary).strip(),
            }
        )

    return articles


def fetch_feed_entries(url: str, timeout: int = 15) -> list[dict[str, Any]]:
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return parse_feed_entries(response.text)
