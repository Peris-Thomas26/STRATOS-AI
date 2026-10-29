from __future__ import annotations

from typing import Any

import requests


def fetch_fred_series(series_id: str, api_key: str | None = None, limit: int = 10) -> dict[str, Any]:
    """Fetch a FRED time series for macroeconomic monitoring."""
    params: dict[str, Any] = {"series_id": series_id, "limit": limit, "file_type": "json"}
    if api_key:
        params["api_key"] = api_key

    response = requests.get(
        "https://api.stlouisfed.org/fred/series/observations",
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
