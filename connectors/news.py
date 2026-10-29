from __future__ import annotations

from typing import Any

import feedparser
import requests


def fetch_rss_feed(url: str, timeout: int = 20) -> str:
    """Download a raw RSS or Atom feed payload from a public URL."""
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.text


def parse_news_entries(feed_text: str) -> list[dict[str, Any]]:
    """Convert feed text into a normalized list of article dictionaries."""
    parsed = feedparser.parse(feed_text)
    entries: list[dict[str, Any]] = []
    for item in parsed.entries:
        entries.append(
            {
                "title": getattr(item, "title", "Untitled"),
                "url": getattr(item, "link", ""),
                "summary": getattr(item, "summary", "") or getattr(item, "description", ""),
                "published_at": getattr(item, "published", "") or getattr(item, "updated", ""),
                "source": getattr(item, "source", None),
            }
        )
    return entries
