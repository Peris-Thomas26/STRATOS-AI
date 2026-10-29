from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Runtime configuration for STRATOS."""

    project_root: Path
    db_path: str
    solstice_dataset: str
    gemini_api_key: str


def get_settings() -> Settings:
    """Load settings from environment variables and project defaults."""
    project_root = Path(__file__).resolve().parent.parent
    return Settings(
        project_root=project_root,
        db_path=os.getenv("STRATOS_DB_PATH", str(project_root / "data" / "processed" / "stratos.db")),
        solstice_dataset=os.getenv(
            "STRATOS_SOLSTICE_DATASET",
            "solsticestudioai/synthetic-enterprise-ops-pack-sample",
        ),
        gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
    )
