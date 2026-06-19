# Agentic Business Analytics Investigator

An AI-powered decision intelligence platform for detecting operational anomalies, investigating likely contributing factors, explaining outcomes, and recommending actions.

The project starts with a deterministic analytics foundation before adding LLM reasoning or agent orchestration. The first MVP uses a simulated enterprise operations dataset for **Northstar Commerce**, an ecommerce business with sales, checkout, infrastructure, inventory, logistics, and support signals.

## Current Repository Structure

```text
.
├── configs/
├── data/
│   ├── processed/
│   ├── raw/
│   └── synthetic/
├── notebooks/
├── outputs/
│   ├── figures/
│   └── reports/
├── src/
│   ├── agents
│   ├── analytics/
│   │   ├── __init__.py
│   │   └── kpi_monitor.py
│   ├── anomaly_detection/
│   │   ├── __init__.py
│   │   └── detect_anomalies.py
│   ├── dashboard
│   ├── explainability/
│   ├── forecasting/
│   ├── investigation/
│   │   └── investigate_anomalies.py
│   ├── ingestion/
│   │   ├── __init__.py
│   │   └── generate_synthetic_data.py
│   ├── orchestration
│   └── utils
├── tests/
├── README.md
└── requirements.txt
```

Some directories are placeholders for upcoming modules. The first implemented module is synthetic data generation under `src/ingestion`.

## Architecture

The system is designed as a deterministic-first decision intelligence pipeline:

```text
Synthetic/Public Data
  -> Ingestion and Validation
  -> KPI Modeling
  -> Forecasting and Baselines
  -> Anomaly Detection
  -> Contribution and Root-Cause Analysis
  -> Explainability Layer
  -> LLM-Assisted Narrative and Recommendations
  -> Dashboard/API
```

Early stages should be reproducible and testable without agent frameworks. LLMs are planned as a later reasoning and communication layer over structured analytical outputs.

## MVP Scope: Northstar Commerce

The initial MVP simulates daily and hourly enterprise operations data:

- Sales metrics
- API latency
- Checkout failures
- Support tickets
- Inventory levels
- Shipping delays
- Deployment events

The synthetic data includes realistic incidents that create linked signals across datasets:

- Failed deployment causing latency spikes, checkout failures, support ticket increases, and revenue decline.
- Inventory shortage causing lost sales.
- Shipping disruption causing delivery delays and customer complaints.

Generate the data with:

```bash
python3 src/ingestion/generate_synthetic_data.py
```

By default, CSV files are written to `data/synthetic/`. The generator accepts a reproducibility seed, date range, and output directory:

```bash
python3 src/ingestion/generate_synthetic_data.py \
  --seed 42 \
  --start-date 2025-01-01 \
  --end-date 2025-06-30 \
  --output-dir data/synthetic
```

Expected outputs:

- `sales_metrics_daily.csv`
- `api_latency_hourly.csv`
- `checkout_failures_hourly.csv`
- `support_tickets_daily.csv`
- `inventory_levels_daily.csv`
- `shipping_delays_daily.csv`
- `deployment_events.csv`

Validate and profile the generated data with:

```bash
python3 src/ingestion/validate_synthetic_data.py
```

The validator checks required files and columns, date/time parsing, duplicate metric keys, numeric null coverage, nonnegative operational metrics, rate bounds, and the expected injected incident windows. It writes a deterministic profiling report to:

```text
outputs/reports/synthetic_data_profile.md
```

The report includes row counts, date/time ranges, missing values, numeric descriptive statistics, and detected incident windows by affected metric file.

## Phase 2: Deterministic KPI Monitoring and Anomaly Detection

Phase 2 adds a non-LLM analytics layer over the synthetic data. It builds a daily KPI table and then flags unusual metric behavior with rolling averages, rolling standard deviations, z-scores, and percent change thresholds.

Build the daily KPI summary with:

```bash
python3 src/analytics/kpi_monitor.py
```

The KPI monitor reads CSV files from `data/synthetic/` and writes:

```text
outputs/reports/kpi_summary_daily.csv
```

The summary includes:

- Net revenue
- Conversion rate
- Refund rate, derived from support refund requests divided by orders
- Average API latency
- Checkout failure rate
- Support ticket count
- Stockout units
- Lost sales units
- Shipping delay rate
- Delivery complaints

It also writes simple KPI plots under:

```text
outputs/figures/
```

Detect anomalies with:

```bash
python3 src/anomaly_detection/detect_anomalies.py
```

The anomaly detector reads `outputs/reports/kpi_summary_daily.csv` and writes:

```text
outputs/reports/anomaly_events.csv
```

It flags deterministic event types for revenue drops, latency spikes, checkout failure spikes, support ticket spikes, inventory shortage periods, and shipping delay spikes. A simple anomaly count plot is also written to `outputs/figures/`.

Run the Phase 2 checks with:

```bash
python3 src/analytics/kpi_monitor.py
python3 src/anomaly_detection/detect_anomalies.py
python3 -m pytest
python3 -m py_compile src/analytics/kpi_monitor.py
python3 -m py_compile src/anomaly_detection/detect_anomalies.py
```

No LLMs or agent frameworks are used in Phase 2.

## Phase 3: Deterministic Investigation Engine

Phase 3 groups nearby anomaly events into incidents and explains them with deterministic rules. Consecutive anomaly dates separated by no more than three days are grouped into one incident by default. Each report includes the incident date range, main and related anomaly types, affected KPI summaries, possible contributing factors, supporting evidence, deployment events, and recommended next steps.

The engine recognizes these initial root-cause patterns:

- Latency spike plus checkout failure spike plus a recent failed deployment: likely deployment-related checkout incident.
- Inventory shortage plus lost sales plus revenue drop: likely inventory shortage incident.
- Shipping delay spike plus elevated delivery complaints: likely logistics disruption incident.

Generate the investigation reports with:

```bash
python3 src/investigation/investigate_anomalies.py
```

The engine reads:

- `outputs/reports/kpi_summary_daily.csv`
- `outputs/reports/anomaly_events.csv`
- `data/synthetic/deployment_events.csv`

It writes:

- `outputs/reports/investigation_reports.json`
- `outputs/reports/investigation_summary.md`

Run the complete deterministic pipeline and checks with:

```bash
python3 src/analytics/kpi_monitor.py
python3 src/anomaly_detection/detect_anomalies.py
python3 src/investigation/investigate_anomalies.py
python3 -m pytest
python3 -m py_compile src/investigation/investigate_anomalies.py
```

No OpenAI API, LLMs, or agent frameworks are used in Phase 3.

## Phase 4: Deterministic Forecasting Layer

Phase 4 adds a reproducible machine learning forecasting layer for forward-looking KPI baselines. It reads the daily KPI summary and trains one forecasting model family per target KPI:

- `net_revenue`
- `support_ticket_count`
- `shipping_delay_rate`

Each target uses the same lag-based feature architecture:

- Previous day value
- 3-day rolling average
- 7-day rolling average
- 14-day rolling average
- 7-day lag
- 14-day lag

Rolling features are shifted so the current day is never used to predict itself. Train/test splits preserve time ordering and do not shuffle records.

Train forecasting models with:

```bash
python3 src/forecasting/train_forecasting_models.py
```

The trainer evaluates:

- Linear Regression baseline
- Random Forest Regressor
- XGBoost Regressor

Models are evaluated with MAE, RMSE, and R². The best model for each KPI is selected by lowest RMSE, with MAE as a deterministic tie-breaker. Metrics are written to:

```text
outputs/reports/model_metrics.csv
```

Selected model artifacts are written to `outputs/models/`, and actual-vs-predicted plots are written under:

```text
outputs/figures/
```

Generate 7-day KPI forecasts with:

```bash
python3 src/forecasting/generate_forecasts.py
```

Forecasts are generated iteratively so each predicted day feeds the lag features for the next day. Results are written to:

```text
outputs/reports/forecast_summary.csv
```

Forecast extension plots are also written to `outputs/figures/`.

Run the Phase 4 checks with:

```bash
python3 src/forecasting/train_forecasting_models.py
python3 src/forecasting/generate_forecasts.py
python3 -m pytest
python3 -m py_compile src/forecasting/train_forecasting_models.py
python3 -m py_compile src/forecasting/generate_forecasts.py
```

No OpenAI API, SHAP analysis, dashboards, or agent orchestration are used in Phase 4.

## Phase 5: Forecast Explainability with SHAP

Phase 5 explains why each selected forecasting model produced its forecast. It loads the trained model artifacts from `outputs/models/`, regenerates the same lag-based feature datasets used during training, reads `outputs/reports/model_metrics.csv` and `outputs/reports/forecast_summary.csv`, and explains the selected models for:

- `net_revenue`
- `support_ticket_count`
- `shipping_delay_rate`

SHAP is used because it provides feature-level attributions for individual predictions while also supporting aggregate feature importance. Tree-based models use `TreeExplainer` where possible. Linear Regression uses `LinearExplainer`, with a coefficient-based fallback if SHAP cannot explain the model cleanly. If a model type cannot be explained safely, the script writes a clear fallback explanation instead of failing the pipeline.

Generate forecast explanations with:

```bash
python3 src/explainability/explain_forecasts.py
```

The explainability script writes:

```text
outputs/reports/shap_feature_importance.csv
outputs/reports/forecast_explanations.md
outputs/figures/shap_summary_<kpi>.png
```

The markdown report describes the predicted KPI, selected model, most important features, prediction-level feature influence for the most recent forecast, and limitations. These explanations are grounded in model outputs only; no OpenAI API, LLM reporting, RAG, dashboards, or agent orchestration are used in Phase 5.

Run the Phase 5 checks with:

```bash
python3 src/explainability/explain_forecasts.py
python3 -m pytest
python3 -m py_compile src/explainability/explain_forecasts.py
```

## Roadmap

1. **Data foundation**
   - Synthetic dataset generation
   - Schema checks and data quality validation
   - Deterministic incident labels for evaluation

2. **Analytics layer**
   - Deterministic KPI summaries
   - Rolling baselines and trend checks
   - Incident-aware metric joins

3. **Detection layer**
   - Rolling z-score and percent-change anomaly detection
   - Future forecasting-based anomaly detection
   - Future robust-statistical detectors
   - Evaluation against injected incident labels

4. **Investigation layer**
   - Contribution analysis across metrics and entities
   - Root-cause candidate ranking
   - Explainability with SHAP or model-native attributions where appropriate

5. **Decision layer**
   - Recommendation rules
   - LLM-assisted executive summaries
   - Human review workflow

6. **Interface layer**
   - Streamlit dashboard for MVP exploration
   - FastAPI endpoints for metric, anomaly, and investigation outputs

## Tech Stack

- Python
- pandas and NumPy
- scikit-learn
- XGBoost
- SHAP
- FastAPI
- Streamlit
- SQLAlchemy and PostgreSQL
- Plotly and Matplotlib
- pytest
- OpenAI API for later narrative and recommendation workflows

## Development Principles

- Build deterministic analytical behavior before adding agents.
- Keep data generation, transformations, detection, and explanations modular.
- Make incident labels explicit so models and rules can be evaluated.
- Prefer reproducible scripts with configurable seeds and clear file outputs.
- Add LLM reasoning only after structured analytics can explain what happened.
