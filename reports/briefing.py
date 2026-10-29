from __future__ import annotations


def build_brief_markdown(company_name: str, items: list[dict]) -> str:
    """Create a simple Markdown briefing from a list of articles deemed relevant."""
    lines = [
        f"# Strategic Brief for {company_name}",
        "",
        "## Summary",
        f"{len(items)} relevant developments were identified for review.",
        "",
        "## Items",
    ]

    for idx, item in enumerate(items, start=1):
        title = item.get("title", "Untitled item")
        source = item.get("source", "Unknown source")
        url = item.get("url", "")
        summary = item.get("summary", "No summary available.")
        score = item.get("relevance_score", 0.0)

        lines.append(f"{idx}. **{title}**")
        lines.append(f"   - Source: {source}")
        lines.append(f"   - Relevance score: {score:.2f}")
        lines.append(f"   - URL: {url}")
        lines.append(f"   - Summary: {summary}")
        lines.append("   - Why it matters: This development may change competitive conditions and deserves a check against local demand, pricing, and retention assumptions.")
        lines.append("   - Suggested action: Validate the source, map nearby demand, and review whether any operational response is needed.")
        lines.append("")

    return "\n".join(lines)
