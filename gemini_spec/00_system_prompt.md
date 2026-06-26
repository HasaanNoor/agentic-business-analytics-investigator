# System Prompt

## Goal

Build the complete Agentic Business Analytics Investigator project from the attached markdown specifications.

The project must be a Python application that generates synthetic ecommerce data, validates it, builds KPI summaries, detects anomalies, groups anomalies into incidents, trains forecasts, explains forecast drivers, writes reports, searches historical incidents, and exposes generated outputs through a read-only FastAPI backend.

## Inputs

- The markdown specification files in `gemini_spec/`.
- No private data.
- No API keys.
- No external database.

## Outputs

- A complete Python repository that follows the requested structure.
- Source code under `src/`.
- Tests under `tests/`.
- A plain-English `README.md`.
- Generated data and reports after the pipeline is run.

## Main files to create

- `requirements.txt`
- `README.md`
- Python modules under:
  - `src/ingestion/`
  - `src/analytics/`
  - `src/anomaly_detection/`
  - `src/investigation/`
  - `src/forecasting/`
  - `src/explainability/`
  - `src/agents/`
  - `src/rag/`
  - `src/api/`
- Tests under `tests/`.

## Required behavior

- Use Python.
- Keep code modular.
- Keep behavior deterministic unless a specification clearly says otherwise.
- Use fixed random seeds for synthetic data and model tests where possible.
- Use `pandas`, `numpy`, `scikit-learn`, `xgboost`, `shap`, `fastapi`, `uvicorn`, `sentence-transformers`, `matplotlib`, and `pytest`.
- Use simple functions and small modules.
- Avoid unnecessary complexity.
- Do not add a database.
- Do not add a dashboard.
- Do not add cloud deployment.
- Do not require API keys for the core pipeline or tests.
- Create tests for each major phase.
- Follow the repository structure described in the specs.
- Write all generated outputs to clear local paths under `data/` and `outputs/`.
- Do not rerun the full pipeline inside API request handlers.
- Read existing output files in the API.
- Return friendly errors when expected files are missing.

## Acceptance criteria

- The repository can be installed from `requirements.txt`.
- The full local pipeline can run from the commands in the README.
- The test suite passes with `python3 -m pytest`.
- Key modules compile with `python3 -m py_compile`.
- The FastAPI app starts with `python3 -m uvicorn src.api.main:app --reload`.
- All behavior is grounded in these specifications.
- Any assumption not stated in the specs is explained briefly.

## Test commands where relevant

```bash
python3 -m pytest
python3 -m py_compile src/api/main.py
python3 -m uvicorn src.api.main:app --reload
```
