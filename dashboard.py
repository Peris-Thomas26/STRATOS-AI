from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from app import generate_daily_brief


def load_company_profile() -> dict:
    project_root = Path(__file__).resolve().parent
    config_path = project_root / "config" / "sample_company.json"
    with config_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def main() -> None:
    company = load_company_profile()
    company_name = company["company_name"]
    watchlist = company.get("watchlist", [])
    priorities = company.get("strategic_priorities", [])

    st.set_page_config(page_title=f"{company_name} Daily Brief", page_icon="📈", layout="wide")
    st.title(f"STRATOS AI — {company_name}")
    st.caption("From information overload to actionable strategic intelligence.")

    with st.sidebar:
        st.subheader("Company profile")
        st.write(f"Industry: {company.get('industry', 'Not specified')}")
        st.write(f"Geography: {company.get('geography', 'Not specified')}")
        st.write("Watchlist:")
        for item in watchlist:
            st.write(f"- {item}")
        st.write("Strategic priorities:")
        for item in priorities:
            st.write(f"- {item}")

    items, brief_markdown = generate_daily_brief(company_name, watchlist)

    col1, col2, col3 = st.columns(3)
    col1.metric("Relevant signals", len(items))
    col2.metric("Watchlist size", len(watchlist))
    col3.metric("Priority areas", len(priorities))

    st.subheader("Daily strategic brief")
    st.markdown(brief_markdown)

    st.subheader("Signal review")
    for item in items:
        with st.container(border=True):
            st.markdown(f"### {item.get('title', 'Untitled signal')}")
            st.caption(f"{item.get('source', 'Unknown source')} • relevance {item.get('relevance_score', 0.0):.2f}")
            st.write(item.get("summary", "No summary available."))
            if item.get("url"):
                st.markdown(f"[Open source]({item.get('url')})")

    st.subheader("Raw brief text")
    st.code(brief_markdown, language="markdown")


if __name__ == "__main__":
    main()
