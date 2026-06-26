# Testing And Validation

## Goal

Create tests that prove the project works end to end and that each module behaves correctly on controlled inputs.

## Inputs

- Source code under `src/`.
- Temporary test files created with `tmp_path`.
- Generated outputs from the local pipeline where needed.

## Outputs

- Passing pytest suite.
- Clear test failures when expected files, columns, or behavior are missing.

## Main files to create

- `tests/test_synthetic_data_validation.py`
- `tests/test_kpi_monitor.py`
- `tests/test_anomaly_detection.py`
- `tests/test_investigation_engine.py`
- `tests/test_forecasting.py`
- `tests/test_explainability.py`
- `tests/test_executive_report_agent.py`
- `tests/test_multi_agent_investigation.py`
- `tests/test_rag_retrieval.py`
- `tests/test_api.py`

## Required behavior

- Use `pytest`.
- Keep tests deterministic.
- Use temporary directories for tests that write files.
- Do not require network access in tests.
- Do not require API keys in tests.
- Use fake embedding models in RAG tests when needed.
- Test meaningful behavior:
  - Data files are generated with expected columns and date ranges.
  - Validation catches missing or invalid inputs.
  - KPI aggregation math is correct.
  - Anomaly detection finds known patterns.
  - Investigation groups anomalies and assigns causes.
  - Forecasting writes metrics and forecasts.
  - SHAP or fallback explanations write feature importance.
  - Report generation works without an API key.
  - Multi-agent findings include evidence and recommendations.
  - RAG retrieval returns ranked results.
  - API endpoints return JSON and friendly errors.
- Tests should use deterministic fake embedding models or mocked embedding calls when network access is unavailable.
- The production pipeline should continue using sentence-transformers.

## Acceptance criteria

- `python3 -m pytest` passes.
- Tests are specific enough to catch broken file paths, missing columns, and changed output shapes.
- Slow tests are acceptable if they remain local and deterministic.
- Key modules compile.

## Test commands where relevant

```bash
python3 -m pytest
python3 -m py_compile src/api/main.py
python3 -m py_compile src/rag/build_knowledge_base.py
python3 -m py_compile src/rag/retrieve_incidents.py
```
