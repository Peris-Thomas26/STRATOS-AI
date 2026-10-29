# STRATOS AI

From information overload to actionable strategic intelligence.

STRATOS AI is an open-source, work-in-progress AI agent that helps small businesses and startup teams monitor their competitive environment. It collects public information, evaluates how developments may affect a company, tracks changes over time, and prepares a concise daily strategic briefing with supporting links.

## Project status

Planning / pre-MVP. This repository contains the project skeleton and a thin working slice of the pipeline.

## Core intent

STRATOS aims to answer:

- What changed in the market or competitive landscape?
- Why does it matter to this company?
- Is this new, developing, contradicted, or resolved?
- What should the team investigate or consider next?

## Proposed MVP

1. Company profile and watchlist.
2. Public-source monitoring.
3. Normalization and deduplication.
4. Relevance and evidence checks.
5. Strategic analysis and briefing.
6. Daily brief saved as Markdown.

## Suggested repository layout

```text
stratos-ai/
├── README.md
├── .gitignore
├── .env.example
├── requirements.txt
├── app.py
├── config/
│   └── sample_company.json
├── collectors/
│   ├── __init__.py
│   └── normalize.py
├── analysis/
│   ├── __init__.py
│   └── relevance.py
├── memory/
│   ├── __init__.py
│   ├── database.py
│   └── signals.py
├── reports/
│   ├── __init__.py
│   ├── briefing.py
│   └── email.py
├── tests/
│   └── test_pipeline.py
├── examples/
│   └── sample_briefing.md
└── .github/
    └── workflows/
        └── daily.yml
```

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pytest -q
python app.py
```

The current implementation includes a thin end-to-end slice:

- sample company profile
- article normalization and deduplication
- relevance scoring
- Markdown briefing generation

## Example brief output

```md
# Strategic Brief for Harbour Coffee

## Summary
One notable development was identified today.

## Items
- Harbour Coffee opens in Tsim Sha Tsui
  - Source: The Coffee Post
  - URL: https://example.com/harbour
  - Why it matters: This indicates local expansion and increased competitive pressure.
  - Suggested action: Review nearby demand and local pricing assumptions.
```

## Disclaimer

This repository is an early prototype and does not replace professional business advice or verified market research.
