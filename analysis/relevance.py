from __future__ import annotations

from typing import Iterable


def _tokenize(text: str) -> set[str]:
    return {token.lower() for token in text.replace("-", " ").replace("/", " ").split() if token}


def score_article_relevance(article: dict, company_name: str, competitor_names: Iterable[str] | None = None) -> float:
    """Return a relevance score between 0 and 1 for a given article against the company context."""
    competitor_names = list(competitor_names or [])
    text_blob = " ".join(
        [
            article.get("title") or "",
            article.get("summary") or "",
            article.get("content") or "",
        ]
    )
    lower_blob = text_blob.lower()

    score = 0.0
    company_tokens = _tokenize(company_name)
    matching_company_terms = company_tokens & _tokenize(lower_blob)
    if matching_company_terms:
        score += 0.6

    competitor_tokens = set()
    for competitor in competitor_names:
        competitor_tokens.update(_tokenize(competitor))
    if competitor_tokens & _tokenize(lower_blob):
        score += 0.1

    if any(keyword in lower_blob for keyword in ["expands", "opens", "launch", "competition", "rival", "market", "retail", "outlet", "new branch"]):
        score += 0.2

    if any(keyword in lower_blob for keyword in ["foot traffic", "pricing", "offer", "revenue", "retention", "demand"]):
        score += 0.1

    if score > 1.0:
        score = 1.0
    return round(score, 2)
