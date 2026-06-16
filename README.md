# AI Research Copilot

AI Research Copilot is a personal research operating system for investment research, industry analysis, and technology trend evaluation.

The project is built in small phases. Each phase should keep the system runnable while adding one focused capability.

## Current Phase

| Phase | Goal | Status |
| --- | --- | --- |
| Phase 0 | Project skeleton and development environment | Complete |
| Phase 1 | Research Question API and local persistence | In Progress |

## Phase 0 Scope

Phase 0 creates the minimum maintainable Python project structure:

- FastAPI entrypoint with a health check.
- Streamlit entrypoint for the future web UI.
- `src/` package layout for application code.
- Basic configuration, logging, schema, and storage modules.
- Local data, docs, and tests directories.

## Project Structure

```text
ai-research-copilot/
├── apps/
│   ├── api/
│   │   └── main.py
│   └── web/
│       └── streamlit_app.py
├── src/
│   └── research_copilot/
│       ├── core/
│       ├── research_os/
│       ├── rag/
│       ├── memory/
│       ├── services/
│       └── utils/
├── data/
├── docs/
└── tests/
```

## Setup

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run API

```bash
uvicorn apps.api.main:app --reload
```

Health check:

```text
GET http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "ai-research-copilot",
  "version": "0.1.0"
}
```

## Research Question API

Research questions are the entry point for the research workflow. They are persisted through `LocalJSONStorage` in `data/storage/research_questions.json`.

Create a research question:

```text
POST http://127.0.0.1:8000/research-questions
```

```json
{
  "title": "X-FAB 是否是 AI 时代被低估的特色工艺 fab？",
  "description": "研究 X-FAB 是否受益于 AI 基础设施、特色工艺产能和光通信相关需求。",
  "company": "X-FAB",
  "theme": "AI infrastructure / specialty foundry"
}
```

List research questions:

```text
GET http://127.0.0.1:8000/research-questions
```

Get one research question:

```text
GET http://127.0.0.1:8000/research-questions/{question_id}
```

Update research question status:

```text
PATCH http://127.0.0.1:8000/research-questions/{question_id}
```

```json
{
  "status": "closed"
}
```

## Run Web App

```bash
streamlit run apps/web/streamlit_app.py
```

## Research OS Core Objects

The MVP Research OS starts with five Pydantic schemas in `src/research_copilot/research_os/schemas.py`:

- `ResearchQuestion`: the top-level question being investigated, with optional company/theme context and open/closed workflow status.
- `Hypothesis`: a testable belief tied to a research question, including optional prior belief and expected evidence.
- `ResearchSource`: an uploaded or indexed source document with file metadata, source quality, and primary-source flags.
- `EvidenceItem`: a cited evidence chunk linked back to a research question, source, and optional hypothesis.
- `ResearchLog`: a research activity record that captures the query, expectation, observation, belief updates, lessons, and next actions.

## MVP Local Storage

The MVP uses `LocalJSONStorage` in `src/research_copilot/research_os/storage.py` instead of a database. Business code should access Research OS records through this storage layer rather than reading or writing JSON files directly, so the implementation can later move to SQLite or PostgreSQL behind the same boundary.

By default, records are stored in `data/storage/`, with one JSON file per object type:

```text
data/storage/
├── research_questions.json
├── hypotheses.json
├── research_sources.json
├── evidence_items.json
└── research_logs.json
```

`LocalJSONStorage` supports saving a single record, retrieving by `id`, listing all records for a model, filtering by field equality, and updating a record by `id`. This is intentionally simple for Phase 0; concurrent writes, large JSON files, and advanced query patterns should be addressed when replacing the backend with a database.

## Tests

```bash
pytest
```
