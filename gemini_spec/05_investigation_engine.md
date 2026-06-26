# Investigation Engine

## Goal

Group nearby anomaly rows into incidents and create first-pass incident reports.

## Inputs

- `outputs/reports/kpi_summary_daily.csv`
- `outputs/reports/anomaly_events.csv`
- `data/synthetic/deployment_events.csv`

## Outputs

- `outputs/reports/investigation_reports.json`
- `outputs/reports/investigation_summary.md`

## Main files to create

- `src/investigation/investigate_anomalies.py`
- `tests/test_investigation_engine.py`

## Required behavior

- Load KPI summary, anomaly events, and deployment events.
- Sort anomalies by date.
- Group anomalies that occur close together into one incident.
- Assign stable incident ids such as `INC-001`, `INC-002`, and so on.
- Include each incident date range.
- Include main anomaly type and related anomaly types.
- Use deterministic rules to infer likely cause.
- Include affected KPIs and supporting evidence.
- Include deployment context when a deployment occurred near the incident.
- Include enriched fields:
  - `incident_severity`
  - `affected_region`
  - `root_cause_category`
  - `business_impact_summary`
  - `resolution_action`
  - `resolution_success`
  - `recovery_days`
  - `affected_metrics`
- Recognize common patterns:
  - Latency spike plus checkout failure spike near a failed deployment means a likely deployment-related checkout incident.
  - Inventory shortage plus lost sales plus revenue drop means a likely inventory shortage incident.
  - Shipping delay spike plus delivery complaints means a likely logistics disruption.
  - Refund spike, visitor surge, backlog spike, carrier outage, supplier delay, weather disruption, fraud spike, and API degradation should be labeled clearly.
- Write a JSON report with an `incidents` list.
- Write a Markdown summary for humans.
- Anomalies occurring within a three-day window may be grouped into the same business incident when they are determined to be part of the same underlying event.
- Grouping should remain deterministic and produce consistent incident identifiers across repeated runs.

## Acceptance criteria

- Investigation output exists after running the script.
- JSON output contains a list of incidents.
- Each incident has an id, title or main anomaly type, date range, cause, evidence, and recommended next steps.
- Enriched incident fields are present.
- Tests verify grouping, cause classification, deployment context, and output writing.

## Test commands where relevant

```bash
python3 src/investigation/investigate_anomalies.py
python3 -m pytest tests/test_investigation_engine.py
```
