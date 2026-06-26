# Multi-Agent Workflow

## Goal

Review each incident with several deterministic specialist modules and combine their findings into one enriched incident report.

## Inputs

- `outputs/reports/investigation_reports.json`
- `outputs/reports/kpi_summary_daily.csv`
- `data/synthetic/deployment_events.csv`
- `outputs/reports/forecast_summary.csv`
- `outputs/reports/shap_feature_importance.csv`
- Optional retrieved historical incidents from the local RAG workflow.

## Outputs

- `outputs/reports/multi_agent_investigation_reports.json`
- `outputs/reports/multi_agent_investigation_summary.md`

## Main files to create

- `src/agents/revenue_agent.py`
- `src/agents/support_agent.py`
- `src/agents/logistics_agent.py`
- `src/agents/platform_agent.py`
- `src/agents/coordinator_agent.py`
- `src/agents/multi_agent_investigation.py`
- `tests/test_multi_agent_investigation.py`

## Required behavior

- Use deterministic Python functions for each specialist module.
- Do not require an external agent framework.
- Do not require network access.
- Revenue Agent should review:
  - Revenue.
  - Conversion rate.
  - Refund rate.
  - Website visitors.
  - Average order value.
  - Stockouts and lost sales.
- Customer Support Agent should review:
  - Total support tickets.
  - Support ticket categories.
- Logistics Agent should review:
  - Shipping delay rate.
  - Carrier capacity utilization.
  - Warehouse backlog.
  - Delivery complaints.
  - Regional disruption flags.
- Platform Reliability Agent should review:
  - API latency.
  - Checkout failure rate.
  - Deployment and rollback events.
- Coordinator Agent should combine findings into:
  - Final title.
  - Likely cause.
  - Evidence.
  - Recommended next steps.
  - Confidence level.
  - Historical incident context when supplied.
- Multi-agent output should keep enriched fields from the investigation engine.
- The multi-agent workflow consumes retrieved historical incidents from the RAG layer.
- It does not build or update the RAG knowledge base.

- Each agent receives:
  - current incident
  - KPI evidence
  - forecast context
  - SHAP explanation
  - retrieved historical incidents

- The coordinator combines these findings into the final investigation report.

## Acceptance criteria

- Running `src/agents/multi_agent_investigation.py` writes JSON and Markdown outputs.
- Each incident includes agent findings.
- Coordinator output includes combined evidence and recommendations.
- Historical context is included when retrieved incidents are supplied.
- Tests cover each specialist path and coordinator behavior.

## Test commands where relevant

```bash
python3 src/agents/multi_agent_investigation.py
python3 -m pytest tests/test_multi_agent_investigation.py
```
