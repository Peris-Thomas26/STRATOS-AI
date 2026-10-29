from __future__ import annotations

from config.settings import get_settings
from connectors.solstice import build_dataset_catalog, fetch_dataset_splits
from database.ingest import ingest_solstice_dataset


# Run the initial Solstice dataset inspection and load the actual company knowledge base into SQLite.
def main() -> None:
    """Inspect Solstice metadata and persist the raw records into the Phase 1 knowledge base."""
    settings = get_settings()
    payload = {"splits": fetch_dataset_splits(settings.solstice_dataset)}
    catalog = build_dataset_catalog(payload)
    print(f"Discovered {len(catalog)} Solstice dataset configs.")

    summary = ingest_solstice_dataset(db_path=settings.db_path, dataset_name=settings.solstice_dataset)
    print(f"Ingested {summary['row_count']} rows across {summary['config_count']} configs.")
    for config_name in summary["configs"][:10]:
        print(f"- {config_name}")


if __name__ == "__main__":
    main()
