from __future__ import annotations

import json
from pathlib import Path

from analysis.relevance import score_article_relevance
from collectors.normalize import normalize_articles
from collectors.rss import parse_feed_entries
from memory.database import fetch_recent_articles, init_schema, save_article
from reports.briefing import build_brief_markdown


def build_sample_feed_xml() -> str:
    return '''
    <rss version="2.0">
      <channel>
        <title>Retail News HK</title>
        <item>
          <title>Harbour Coffee opens new branch in Tsim Sha Tsui</title>
          <link>https://example.com/harbour-tsim-sha-tsui</link>
          <description>The local coffee chain has opened a new outlet in a mixed-use district, increasing competition for nearby café traffic.</description>
          <pubDate>Wed, 30 Oct 2024 09:00:00 +0800</pubDate>
        </item>
        <item>
          <title>Pacific Brew expands premium roast menu</title>
          <link>https://example.com/pacific-brew-menu</link>
          <description>Pacific Brew has launched a premium roast lineup targeting specialty buyers.</description>
          <pubDate>Tue, 29 Oct 2024 15:15:00 +0800</pubDate>
        </item>
      </channel>
    </rss>
    '''


def generate_daily_brief(company_name: str, watchlist: list[str], raw_articles: list[dict] | None = None, db_path: str | Path | None = None) -> tuple[list[dict], str]:
    if raw_articles is None:
        raw_articles = parse_feed_entries(build_sample_feed_xml())

    normalized = normalize_articles(raw_articles)
    relevant_items: list[dict] = []

    for article in normalized:
        score = score_article_relevance(article, company_name, watchlist)
        if score >= 0.65:
            article_with_score = dict(article)
            article_with_score["relevance_score"] = score
            relevant_items.append(article_with_score)

            if db_path is not None:
                save_article(db_path, article)

    if not relevant_items:
        relevant_items = [{
            "title": "No relevant item matched the current sample set",
            "source": "STRATOS AI",
            "url": "",
            "summary": "This is a placeholder generated when the current sample set is below relevance threshold.",
            "relevance_score": 0.0,
        }]

    return relevant_items, build_brief_markdown(company_name, relevant_items)


def main() -> None:
    project_root = Path(__file__).resolve().parent
    config_path = project_root / "config" / "sample_company.json"
    with config_path.open("r", encoding="utf-8") as file:
        company = json.load(file)

    db_path = project_root / "memory" / "stratos.db"
    init_schema(db_path)

    company_name = company["company_name"]
    watchlist = company.get("watchlist", [])

    relevant_items, brief_markdown = generate_daily_brief(company_name, watchlist, db_path=db_path)

    output_path = project_root / "examples" / "sample_briefing.md"
    output_path.write_text(brief_markdown, encoding="utf-8")

    print(f"STRATOS AI running for {company_name}")
    print(f"Relevant developments found: {len(relevant_items)}")
    print(f"Brief saved to: {output_path}")
    print(f"Stored in DB: {len(fetch_recent_articles(db_path, limit=10))} articles")
    print(brief_markdown)


if __name__ == "__main__":
    main()
