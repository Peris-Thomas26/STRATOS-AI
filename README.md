# STRATOS AI

STRATOS AI is an AI-powered strategic intelligence and decision-support system for enterprise problem detection, internal business analysis, and external signal monitoring.

The project is designed to help management understand what is changing inside a company, what external developments matter, why they matter, and what decisions or investigations should be considered.


## Project vision

STRATOS answers the question:

"Given the company's current internal performance, strategic objectives, and changing external environment, what developments require management's attention, why do they matter, and what actions should be considered?"

This is not a chatbot, not a generic SWOT generator, and not a news summarizer. SWOT remains an analytical framework within the system, not the product itself.

## Case study company

The primary internal information source is the Solstice Synthetic Enterprise Operations Pack dataset:

- Dataset: https://huggingface.co/datasets/solsticestudioai/synthetic-enterprise-ops-pack-sample
- Coverage includes sales, customer accounts, engineering, incidents, IT operations, employee and organisational records, and internal collaboration data.
- The system must use the actual dataset as the authoritative source of internal facts.

## System architecture

STRATOS is built around five major components:

1. Company Knowledge Base
   - central SQLite repository for Solstice records
   - provenance tracking and ingestion timestamps
   - reusable query layer for operational analysis

2. Internal Business Intelligence
   - department-based analysis using actual operational fields only
   - SQL and Pandas for numerical and relational analysis

3. External Intelligence Monitoring
   - RSS and public data feeds for relevant external developments
   - deduplication and source evidence tracking

4. Strategic Impact Engine
   - links internal evidence to external developments
   - distinguishes facts, interpretations, assumptions, and hypotheses

5. Strategic Memory and Decision Support
   - historical signal tracking
   - identifies new, unchanged, developing, contradicted, or resolved findings

## Repository structure

```text
STRATOS-AI/
├── app.py
├── main.py
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── config/
│   ├── __init__.py
│   └── settings.py
├── connectors/
│   ├── __init__.py
│   ├── solstice.py
│   ├── news.py
│   └── economic_data.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── synthetic/
├── database/
│   ├── __init__.py
│   ├── schema.py
│   └── queries.py
├── intelligence/
│   ├── __init__.py
│   ├── internal_analysis.py
│   ├── external_analysis.py
│   ├── impact_engine.py
│   └── strategic_memory.py
├── agents/
│   ├── __init__.py
│   └── strategy_agent.py
├── reports/
│   ├── __init__.py
│   └── briefing_generator.py
├── tests/
│   └── test_phase1_ingestion.py
├── .github/
│   └── workflows/
│       └── ci.yml
└── pytest.ini
```

## Phase 1: dataset exploration and integration

This is the current milestone.

### Goal

Build a reliable company knowledge base using actual Solstice records and keep the evidence layer clean before introducing strategic reasoning.

### Deliverables

- live dataset discovery through Hugging Face
- actual config and schema inspection
- department-based dataset mapping
- SQLite ingestion with provenance tracking
- raw record storage and normalized record storage
- reusable database query functions

### Current implementation focus

- Inspect all available Solstice dataset configs
- Map each config to a department
- Persist raw records and metadata
- Preserve source identifiers and ingestion timestamps
- Use deterministic code for validation and aggregation
- Delay LLM-based interpretation until the evidence base is robust

## Phase 2: internal intelligence

After Phase 1 stabilizes, the project will add analytical modules for:

- account health and retention risk
- sales pipeline persistence
- customer relationship movement
- engineering and deployment issues
- operational incident trends
- cross-departmental dependencies

These analyses will use actual dataset fields and SQL/Pandas rather than LLM-only reasoning.

## Phase 3: external intelligence

Once the internal foundation works, external monitoring will include:

- RSS and public news sources
- relevant public economic indicators
- regulatory and industry signals
- deduplication and source traceability

## Phase 4 and beyond

The later stages will connect internal evidence with external developments and build a strategic impact engine, memory layer, and management briefing workflow.

## Engineering rules

- Do not invent company records.
- Preserve original identifiers and relationships.
- Keep synthetic and real data distinguishable.
- Do not treat LLM outputs as verified facts.
- Use environment variables for credentials.
- Prefer SQL and Pandas for quantitative analysis.
- Keep the system modular and reviewable.
- Avoid unnecessary frameworks or multi-agent orchestration until the workflow is truly complex.

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pytest -q
python main.py
```

## Notes

- The current implementation is a Phase 1 foundation for data provenance and structured company intelligence.
- The repository is intentionally lean and reviewable so future analytical components can be added incrementally.
