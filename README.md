# Agentic Business Analytics Investigator

This project investigates problems in a simulated ecommerce business called **Northstar Commerce**.

It creates business data, checks that the data is usable, tracks important metrics, finds unusual changes, groups those changes into incidents, forecasts a few key metrics, explains the forecasts, and writes reports.

The project is built in stages. Most stages are deterministic, which means they use fixed Python rules and reproducible data instead of asking an LLM to reason about the business. This makes the system easier to test before adding more advanced AI behavior.

## Repository Structure

```text
.
├── data/synthetic/                 # Generated business data
├── outputs/
│   ├── figures/                    # Charts
│   └── reports/                    # CSV, JSON, and markdown reports
├── src/
│   ├── agents/                     # Report and investigation agents
│   ├── analytics/                  # KPI summary builder
│   ├── anomaly_detection/          # Anomaly detection rules
│   ├── explainability/             # SHAP forecast explanations
│   ├── forecasting/                # Forecast model training and prediction
│   ├── ingestion/                  # Synthetic data generation and validation
│   └── investigation/              # Incident grouping and first-pass investigation
├── tests/
├── README.md
└── requirements.txt
```

Some folders are placeholders for future dashboard, API, or orchestration work.

## How The Pipeline Works

```text
Generate synthetic data
  -> Validate the generated files
  -> Build daily KPI summary
  -> Detect unusual KPI changes
  -> Group anomalies into incidents
  -> Forecast revenue, support tickets, and shipping delays
  -> Explain forecast drivers with SHAP
  -> Write incident and operations reports
  -> Review each incident with focused deterministic agents
```

## Phase 1: Synthetic Data And Validation

**What was added:** Phase 1 creates synthetic data for sales, checkout failures, API latency, support tickets, inventory levels, shipping delays, and software deployments.

**Why it was added:** The project needs realistic data with known incidents so the rest of the system can be tested. For example, the generator creates failed checkout deployments, inventory shortages, and shipping disruptions that show up across several metrics.

**How it affects the system:** Later phases can detect and investigate known problems. A failed checkout deployment can cause higher API latency, more checkout failures, more support tickets, and lower revenue.

Generate the data:

```bash
python3 src/ingestion/generate_synthetic_data.py
```

The default output folder is:

```text
data/synthetic/
```

Expected files:

- `sales_metrics_daily.csv`
- `api_latency_hourly.csv`
- `checkout_failures_hourly.csv`
- `support_tickets_daily.csv`
- `inventory_levels_daily.csv`
- `shipping_delays_daily.csv`
- `deployment_events.csv`

Validate the generated data:

```bash
python3 src/ingestion/validate_synthetic_data.py
```

The validator checks required columns, date parsing, duplicate rows, missing values, nonnegative counts, valid rates, and expected incident windows. It writes:

```text
outputs/reports/synthetic_data_profile.md
```

## Phase 2: KPI Monitoring And Anomaly Detection

**What was added:** Phase 2 combines the synthetic datasets into one daily KPI table, then flags unusual metric changes.

**Why it was added:** Incidents are easier to find when related metrics are in one place. For example, a checkout problem can be reviewed beside revenue, conversion rate, checkout failure rate, API latency, and support ticket volume.

**How it affects the system:** The output from this phase becomes the main input for investigation, forecasting, and later reporting.

Build the daily KPI summary:

```bash
python3 src/analytics/kpi_monitor.py
```

This writes:

```text
outputs/reports/kpi_summary_daily.csv
```

The KPI table includes:

- Revenue metrics such as `net_revenue`, `website_visitors`, `average_order_value`, `conversion_rate`, and `refund_rate`
- Platform metrics such as `avg_api_latency_ms` and `checkout_failure_rate`
- Support ticket totals and categories
- Inventory metrics such as `stockout_units` and `lost_sales_units`
- Logistics metrics such as `shipping_delay_rate`, `carrier_capacity_utilization`, `warehouse_backlog`, `delivery_complaints`, and regional disruption flags

Detect anomalies:

```bash
python3 src/anomaly_detection/detect_anomalies.py
```

This writes:

```text
outputs/reports/anomaly_events.csv
```

The detector looks for revenue drops, latency spikes, checkout failure spikes, support ticket spikes, inventory shortage periods, and shipping delay spikes.

## Phase 3: Deterministic Investigation Engine

**What was added:** Phase 3 groups nearby anomaly events into incidents and gives each incident a first explanation.

**Why it was added:** A real business problem usually affects more than one metric. For example, a shipping disruption can raise shipping delay rate, delivery complaints, support tickets, and sometimes lower revenue.

**How it affects the system:** Instead of reviewing isolated anomaly rows, users get incident reports with a date range, likely cause, evidence, affected KPIs, deployment events, and next steps.

Generate investigation reports:

```bash
python3 src/investigation/investigate_anomalies.py
```

Inputs:

- `outputs/reports/kpi_summary_daily.csv`
- `outputs/reports/anomaly_events.csv`
- `data/synthetic/deployment_events.csv`

Outputs:

- `outputs/reports/investigation_reports.json`
- `outputs/reports/investigation_summary.md`

The investigation rules recognize examples such as:

- Latency spike plus checkout failure spike plus a failed deployment means a likely deployment-related checkout incident.
- Inventory shortage plus lost sales plus revenue drop means a likely inventory shortage incident.
- Shipping delay spike plus delivery complaints means a likely logistics disruption incident.

## Phase 4: Forecasting

**What was added:** Phase 4 trains models to forecast `net_revenue`, `support_ticket_count`, and `shipping_delay_rate`.

**Why it was added:** Forecasts provide a short-term view of where important KPIs may go next. For example, if support tickets are forecast to stay high after an incident, the business may need temporary staffing or customer messaging.

**How it affects the system:** Forecast outputs give later reports more context than historical incident evidence alone.

Train forecasting models:

```bash
python3 src/forecasting/train_forecasting_models.py
```

The trainer compares Linear Regression, Random Forest, and XGBoost models. It writes model metrics to:

```text
outputs/reports/model_metrics.csv
```

It also saves selected models in:

```text
outputs/models/
```

Generate 7-day forecasts:

```bash
python3 src/forecasting/generate_forecasts.py
```

This writes:

```text
outputs/reports/forecast_summary.csv
```

## Phase 5: Forecast Explanations

**What was added:** Phase 5 explains which input features mattered most to each forecast model.

**Why it was added:** A forecast is more useful when the user can see what drove it. For example, a revenue forecast may depend heavily on website visitors, conversion rate, average order value, checkout failures, and lost sales.

**How it affects the system:** Reports can include model drivers instead of only predicted values. This helps users understand whether a forecast is being shaped by demand, platform health, support activity, or logistics pressure.

Generate forecast explanations:

```bash
python3 src/explainability/explain_forecasts.py
```

Outputs:

- `outputs/reports/shap_feature_importance.csv`
- `outputs/reports/forecast_explanations.md`
- `outputs/figures/shap_summary_<kpi>.png`

SHAP is used for feature importance when possible. If a model cannot be explained cleanly, the script writes a clear fallback explanation instead of stopping the pipeline.

## Phase 6.5: Better Revenue Forecasting

**What was added:** Phase 6.5 adds more revenue-specific inputs to the revenue model.

**Why it was added:** Revenue is not explained well by past revenue alone. Ecommerce revenue depends on traffic, conversion, order value, refunds, checkout failures, stockouts, lost sales, and calendar patterns.

**How it affects the system:** The revenue model can learn clearer cause-and-effect patterns. For example, high website visitors with low conversion rate can point to a checkout or pricing problem, while stockouts and lost sales can explain revenue that fell despite demand.

Added revenue inputs include:

- `website_visitors`
- `active_customers`
- `average_order_value`
- `day_of_week`
- `month`
- `quarter`
- `is_weekend`
- `conversion_rate`
- `refund_rate`
- `checkout_failure_rate`
- `avg_api_latency_ms`
- `support_ticket_count`
- `stockout_units`
- `lost_sales_units`
- `shipping_delay_rate`

After these changes, the selected `net_revenue` model improved from about R² `0.65` and RMSE `8,487` to R² `0.95` and RMSE `4,858` on the generated dataset.

## Phase 7: More Realistic Support And Logistics Signals

**What was added:** Phase 7 adds support ticket categories and logistics drivers.

**Why it was added:** A total support ticket count does not explain what customers are complaining about. A shipping delay rate also does not explain whether the issue came from carrier capacity, warehouse backlog, or regional disruption.

**How it affects the system:** Forecasts and investigations can point to clearer business reasons. For example, shipping complaint tickets can rise when shipping delays rise, checkout issue tickets can rise when checkout failures rise, and warehouse backlog can explain higher delay rates.

Support ticket categories:

- `shipping_complaint_tickets`
- `checkout_issue_tickets`
- `billing_issue_tickets`
- `account_access_tickets`
- `general_support_tickets`

Logistics drivers:

- `carrier_capacity_utilization`
- `warehouse_backlog`
- `delivery_complaints`
- `east_region_disruption`
- `west_region_disruption`
- `south_region_disruption`
- `central_region_disruption`

Phase 7.1 also removes a support forecasting problem. Since `support_ticket_count` is the sum of ticket categories, the model should not use same-day category counts to predict the same-day total. It now uses prior-day and rolling category values plus operational signals that would reasonably be known before prediction.

Current Phase 7.1 results:

| KPI | Selected model | RMSE | R² |
| --- | --- | ---: | ---: |
| `support_ticket_count` | XGBoost | `18.575684` | `0.862286` |
| `shipping_delay_rate` | Linear Regression | `0.014857` | `0.862143` |

## Phase 8: Executive Operations Report

**What was added:** Phase 8 writes an operations report from the investigation, forecast, explanation, and model metric files.

**Why it was added:** Users need one readable report instead of checking many CSV, JSON, and markdown files.

**How it affects the system:** The report summarizes top incidents, forecast outlook, important model drivers, recommended actions, and limitations.

Generate the report:

```bash
python3 src/agents/executive_report_agent.py
```

Output:

```text
outputs/reports/executive_operations_report.md
```

If `OPENAI_API_KEY` is set, the report agent can call the OpenAI API to write the markdown narrative from a structured evidence bundle. If no API key is set, it writes a deterministic fallback report. This keeps local development and tests runnable without network access.

Optional environment variables:

```bash
export OPENAI_API_KEY="your_api_key_here"
export OPENAI_MODEL="gpt-4o-mini"
```

## Phase 9: Multi-Agent Investigation Workflow

**What was added:** Phase 9 splits incident review into five deterministic agents:

- Revenue Agent
- Customer Support Agent
- Logistics Agent
- Platform Reliability Agent
- Coordinator Agent

**Why it was added:** One incident can affect different parts of the business. A failed checkout deployment may reduce revenue, increase checkout support tickets, raise API latency, and trigger rollback events. A shipping disruption may raise delay rates, warehouse backlog, delivery complaints, and shipping-related support tickets.

**How it affects the system:** Each specialist agent reviews the same incident from a different angle, then the coordinator combines the findings into one clear report. This proves the multi-agent workflow with simple Python rules before adding RAG, LLM reasoning, or an external agent framework.

Agent responsibilities:

- Revenue Agent checks revenue, conversion rate, refunds, website visitors, average order value, stockouts, and lost sales.
- Customer Support Agent checks support ticket count and ticket categories.
- Logistics Agent checks shipping delay rate, carrier utilization, warehouse backlog, delivery complaints, and regional disruption flags.
- Platform Reliability Agent checks API latency, checkout failure rate, deployment events, and rollback events.
- Coordinator Agent combines all findings into a final incident report with a title, date range, likely cause, evidence, recommendations, and confidence level.

Run Phase 9:

```bash
python3 src/agents/multi_agent_investigation.py
```

Inputs:

- `outputs/reports/investigation_reports.json`
- `outputs/reports/kpi_summary_daily.csv`
- `data/synthetic/deployment_events.csv`
- `outputs/reports/forecast_summary.csv`
- `outputs/reports/shap_feature_importance.csv`

Outputs:

- `outputs/reports/multi_agent_investigation_reports.json`
- `outputs/reports/multi_agent_investigation_summary.md`

No OpenAI calls, RAG, CrewAI, LangChain, AutoGen, or other agent framework is used in Phase 9.

## Run The Full Local Pipeline

```bash
python3 src/ingestion/generate_synthetic_data.py
python3 src/ingestion/validate_synthetic_data.py
python3 src/analytics/kpi_monitor.py
python3 src/anomaly_detection/detect_anomalies.py
python3 src/investigation/investigate_anomalies.py
python3 src/forecasting/train_forecasting_models.py
python3 src/forecasting/generate_forecasts.py
python3 src/explainability/explain_forecasts.py
python3 src/agents/executive_report_agent.py
python3 src/agents/multi_agent_investigation.py
python3 -m pytest
```

## Phase 9 Checks

```bash
python3 src/agents/multi_agent_investigation.py
python3 -m pytest
python3 -m py_compile src/agents/multi_agent_investigation.py
```

## Roadmap

- Add a dashboard for exploring KPIs, anomalies, incidents, forecasts, and reports.
- Add API endpoints for generated outputs.
- Add human review states for incident reports and recommendations.
- Add RAG only after the deterministic incident and report structure is stable.
- Add LLM reasoning where it can improve explanation quality without replacing tested analytics.

## Tech Stack

- Python
- pandas and NumPy
- scikit-learn
- XGBoost
- SHAP
- Matplotlib
- pytest
- OpenAI API for optional narrative reporting

## Development Principles

- Build testable Python rules before adding LLM reasoning.
- Keep each script focused on one job.
- Write outputs to clear file paths so each phase can be rerun.
- Use concrete business metrics, not vague explanations.
- Make reports useful for action: explain what happened, why it likely happened, what evidence supports it, and what to check next.
