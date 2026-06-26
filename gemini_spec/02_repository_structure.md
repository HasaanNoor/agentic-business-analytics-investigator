# Repository Structure

## Goal

Create a clear repository layout where each project phase has its own source folder and tests.

## Inputs

- Markdown specs in `gemini_spec/`.
- Python package dependencies in `requirements.txt`.

## Outputs

- A repository that can be run and tested locally.

## Main files to create

```text
.
├── data/
│   └── synthetic/
├── outputs/
│   ├── figures/
│   ├── models/
│   ├── rag/
│   └── reports/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── coordinator_agent.py
│   │   ├── executive_report_agent.py
│   │   ├── logistics_agent.py
│   │   ├── multi_agent_investigation.py
│   │   ├── platform_agent.py
│   │   ├── revenue_agent.py
│   │   └── support_agent.py
│   ├── analytics/
│   │   ├── __init__.py
│   │   └── kpi_monitor.py
│   ├── anomaly_detection/
│   │   ├── __init__.py
│   │   └── detect_anomalies.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── dashboard/
│   ├── explainability/
│   │   ├── __init__.py
│   │   └── explain_forecasts.py
│   ├── forecasting/
│   │   ├── __init__.py
│   │   ├── generate_forecasts.py
│   │   └── train_forecasting_models.py
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── generate_synthetic_data.py
│   │   └── validate_synthetic_data.py
│   ├── investigation/
│   │   └── investigate_anomalies.py
│   ├── orchestration/
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── build_knowledge_base.py
│   │   └── retrieve_incidents.py
│   └── utils/
├── tests/
├── README.md
└── requirements.txt
```

## Required behavior

- Use importable Python packages under `src/`.
- Use script entry points guarded by `if __name__ == "__main__":`.
- Keep placeholder folders empty unless a spec requires code there.
- Write tests for behavior, not just file existence.
- Use relative default paths so the project works from the repository root.

## Acceptance criteria

- Imports such as `from src.analytics.kpi_monitor import build_daily_kpi_summary` work.
- Tests can import all modules without changing the Python path manually in test files.
- Output folders are created by scripts when needed.

## Test commands where relevant

```bash
python3 -m pytest
```
