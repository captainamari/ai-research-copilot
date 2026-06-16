# AI Research Copilot

AI Research Copilot is a personal research operating system for investment research, industry analysis, and technology trend evaluation.

The project is built in small phases. Each phase should keep the system runnable while adding one focused capability.

## Current Phase

| Phase | Goal | Status |
| --- | --- | --- |
| Phase 0 | Project skeleton and development environment | In Progress |

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

## Run Web App

```bash
streamlit run apps/web/streamlit_app.py
```

## Tests

```bash
pytest
```
