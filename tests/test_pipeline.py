from app import generate_daily_brief
from collectors.normalize import normalize_articles
from collectors.rss import parse_feed_entries
from analysis.relevance import score_article_relevance
from memory.database import fetch_recent_articles, init_schema, save_article
from reports.briefing import build_brief_markdown


def test_normalize_articles_deduplicates_by_url():
    articles = [
        {
            "title": "Harbour Coffee opens new branch",
            "url": "https://example.com/coffee-branch",
            "source": "Example Daily",
            "published_at": "2026-10-28T09:00:00+08:00",
            "summary": "Harbour Coffee expands in Causeway Bay.",
        },
        {
            "title": "Harbour Coffee opens new branch",
            "url": "https://example.com/coffee-branch",
            "source": "Example Daily",
            "published_at": "2026-10-29T09:00:00+08:00",
            "summary": "Harbour Coffee expands in Causeway Bay again.",
        },
    ]

    normalized = normalize_articles(articles)

    assert len(normalized) == 1
    assert normalized[0]["published_at"] == "2026-10-29T09:00:00+08:00"


def test_relevance_score_identifies_company_signal():
    article = {
        "title": "Harbour Coffee expands in Tsim Sha Tsui",
        "summary": "The coffee chain opens a new outlet nearby, increasing competition for local cafes.",
    }

    score = score_article_relevance(article, "Harbour Coffee", ["Harbour Coffee", "Pacific Brew", "The Daily Bean"])

    assert score > 0.7


def test_brief_markdown_includes_citations_and_summary():
    brief = build_brief_markdown(
        company_name="Harbour Coffee",
        items=[
            {
                "title": "Harbour Coffee opens in Tsim Sha Tsui",
                "source": "The Coffee Post",
                "url": "https://example.com/harbour",
                "summary": "New branch adds local competition.",
                "relevance_score": 0.92,
            }
        ],
    )

    assert "Harbour Coffee" in brief
    assert "https://example.com/harbour" in brief
    assert "Why it matters" in brief


def test_parse_feed_entries_extracts_article_fields():
    xml = '''
    <rss version="2.0">
      <channel>
        <title>Retail News</title>
        <item>
          <title>Harbour Coffee opens new branch</title>
          <link>https://example.com/harbour-branch</link>
          <description>New store expands in Tsim Sha Tsui.</description>
          <pubDate>Wed, 30 Oct 2024 09:00:00 +0800</pubDate>
        </item>
      </channel>
    </rss>
    '''

    entries = parse_feed_entries(xml)

    assert len(entries) == 1
    assert entries[0]["title"] == "Harbour Coffee opens new branch"
    assert entries[0]["url"] == "https://example.com/harbour-branch"
    assert "Tsim Sha Tsui" in entries[0]["summary"]


def test_database_persists_articles(tmp_path):
    db_path = tmp_path / "stratos.db"
    init_schema(db_path)

    save_article(
        db_path,
        {
            "title": "Harbour Coffee adds new outlet",
            "url": "https://example.com/harbour-outlet",
            "source": "Retail Watch",
            "published_at": "2026-10-29T09:00:00+08:00",
            "summary": "A new outlet increases local competition.",
        },
    )

    rows = fetch_recent_articles(db_path, limit=10)

    assert len(rows) == 1
    assert rows[0]["title"] == "Harbour Coffee adds new outlet"
    assert rows[0]["url"] == "https://example.com/harbour-outlet"


def test_generate_daily_brief_returns_relevant_items():
    items, brief_markdown = generate_daily_brief(
        "Harbour Coffee",
        ["Harbour Coffee", "Pacific Brew", "The Daily Bean"],
        [
            {
                "title": "Harbour Coffee opens new branch in Tsim Sha Tsui",
                "url": "https://example.com/harbour-tsim-sha-tsui",
                "source": "Retail News HK",
                "published_at": "2026-10-30T09:00:00+08:00",
                "summary": "The local coffee chain has opened a new outlet in a mixed-use district, increasing competition for nearby café traffic.",
            }
        ],
    )

    assert len(items) == 1
    assert "Harbour Coffee" in brief_markdown
    assert "https://example.com/harbour-tsim-sha-tsui" in brief_markdown
