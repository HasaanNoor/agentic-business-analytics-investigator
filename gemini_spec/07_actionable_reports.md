# Actionable Reports

## Goal

Create readable reports that summarize incidents, forecasts, feature drivers, model quality, and recommended actions.

## Inputs

- `outputs/reports/investigation_reports.json`
- `outputs/reports/multi_agent_investigation_reports.json` when available
- `outputs/reports/forecast_summary.csv`
- `outputs/reports/shap_feature_importance.csv`
- `outputs/reports/model_metrics.csv`

## Outputs

- `outputs/reports/executive_operations_report.md`
- Related summary Markdown files created by earlier phases.

## Main files to create

- `src/agents/executive_report_agent.py`
- `tests/test_executive_report_agent.py`

## Required behavior

- Load investigation, forecast, SHAP, and model metric files.
- Write a Markdown report for business review.
- Use plain English.
- Include:
  - Top incidents.
  - Incident severity and likely impact.
  - Evidence from affected metrics.
  - Forecast outlook.
  - Important feature drivers.
  - Recommended next steps.
  - Limitations.
- The report writer may optionally call an external model only when an API key is present.
- If no API key is present, write a deterministic fallback report.
- Tests must not require a network call or API key.

## Acceptance criteria

- Report generation works without any API key.
- The Markdown report exists and includes incident, forecast, driver, recommendation, and limitation sections.
- Tests verify deterministic fallback behavior.
- Missing optional files should be handled with a clear message where practical.

## Test commands where relevant

```bash
python3 src/agents/executive_report_agent.py
python3 -m pytest tests/test_executive_report_agent.py
```
