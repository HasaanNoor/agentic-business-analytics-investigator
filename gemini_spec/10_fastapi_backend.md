# FastAPI Backend

## Goal

Create a simple read-only API so users can access generated project outputs from a browser or deployed service.

## Inputs

- `outputs/reports/kpi_summary_daily.csv`
- `outputs/reports/multi_agent_investigation_reports.json`
- `outputs/reports/forecast_summary.csv`
- `outputs/reports/shap_feature_importance.csv`
- `outputs/reports/executive_operations_report.md`
- `outputs/rag/incident_knowledge_base.pkl`

## Outputs

- JSON responses from FastAPI endpoints.
- No new pipeline outputs during API requests.

## Main files to create

- `src/api/__init__.py`
- `src/api/main.py`
- `tests/test_api.py`

## Required behavior

- Use FastAPI.
- Keep all endpoints read-only.
- Do not rerun the full pipeline inside API request handlers.
- Load existing files from `outputs/`.
- Return clear JSON responses.
- Return friendly JSON errors if files are missing.
- Use FastAPI `TestClient` for tests.

Create these endpoints:

- `GET /health`
  - Return project status.
  - Include whether expected output files exist.
  - Return `ready` when all expected files exist and `degraded` when one or more are missing.
- `GET /kpis`
  - Return recent rows from `outputs/reports/kpi_summary_daily.csv`.
  - Support a safe `limit` query parameter.
- `GET /incidents`
  - Return enriched investigation reports from `outputs/reports/multi_agent_investigation_reports.json`.
- `GET /incidents/{incident_id}`
  - Return one incident by id.
  - Return 404 when the id is not found.
- `GET /forecasts`
  - Return `outputs/reports/forecast_summary.csv`.
- `GET /explanations`
  - Return top SHAP feature drivers from `outputs/reports/shap_feature_importance.csv`.
  - Support a safe `limit` query parameter.
- `GET /reports/actionable`
  - Return `outputs/reports/executive_operations_report.md` as Markdown content inside JSON.
- `GET /rag/search`
  - Accept query text.
  - Return similar historical incidents using the existing local RAG retrieval code.
  - Support a safe `top_k` query parameter.

## Acceptance criteria

- API module imports successfully.
- All listed endpoints exist.
- Missing files produce friendly 404 responses.
- API tests cover happy paths, missing files, incident lookup misses, and RAG search wiring.
- Uvicorn can start the app.

## Test commands where relevant

```bash
python3 -m uvicorn src.api.main:app --reload
python3 -m pytest tests/test_api.py
python3 -m py_compile src/api/main.py
```
