# Forecasting And SHAP

## Goal

Train forecasting models for important KPIs, generate short-term forecasts, and explain which input features drove the model outputs.

## Inputs

- `outputs/reports/kpi_summary_daily.csv`
- Trained models from `outputs/models/` for forecast generation.

## Outputs

- `outputs/reports/model_metrics.csv`
- `outputs/reports/model_comparison.csv`
- Model files in `outputs/models/`
- `outputs/reports/forecast_summary.csv`
- Forecast figures in `outputs/figures/`
- `outputs/reports/shap_feature_importance.csv`
- `outputs/reports/forecast_explanations.md`
- SHAP figures in `outputs/figures/`

## Main files to create

- `src/forecasting/train_forecasting_models.py`
- `src/forecasting/generate_forecasts.py`
- `src/explainability/explain_forecasts.py`
- `tests/test_forecasting.py`
- `tests/test_explainability.py`

## Required behavior

### Forecast training

- Train models for:
  - `net_revenue`
  - `support_ticket_count`
  - `shipping_delay_rate`
- Use features from the KPI table.
- Include lag features and rolling features where useful.
- For revenue, include business inputs such as visitors, conversion rate, order value, refund rate, checkout failures, latency, support tickets, stockouts, lost sales, and shipping delay rate.
- Avoid leakage for support forecasting. Do not use same-day support category counts to predict same-day `support_ticket_count`.
- Compare at least:
  - Linear Regression
  - Random Forest
  - XGBoost
- Save metrics such as RMSE and R2.
- Save the selected model for each KPI.
- Forecasting models should use historical lag features, rolling averages, and other historical information that is available at prediction time.
- The models should not depend on unknown future values of explanatory variables.

### Forecast generation

- Generate 7-day forecasts.
- Write rows with:
  - `date`
  - `kpi`
  - `forecast_day`
  - `prediction`
  - `model_name`

### SHAP explanations

- Explain feature importance for each selected forecast model.
- Use SHAP when possible.
- If SHAP cannot explain a model cleanly, write a clear deterministic fallback explanation instead of failing the whole pipeline.
- Write feature importance rows with:
  - `kpi`
  - `model_name`
  - `feature`
  - `mean_abs_attribution`
  - `rank`
  - `explanation_method`
- If SHAP cannot explain a selected model, use a deterministic fallback based on the model's native feature importance or coefficients to generate the explanation report.

## Acceptance criteria

- Training writes model metrics and model files.
- Forecast generation writes 7 forecast days for each target KPI.
- Explanation generation writes feature importance rows.
- Tests confirm models train, metrics are numeric, forecasts exist, and explanation output has expected columns.

## Test commands where relevant

```bash
python3 src/forecasting/train_forecasting_models.py
python3 src/forecasting/generate_forecasts.py
python3 src/explainability/explain_forecasts.py
python3 -m pytest tests/test_forecasting.py tests/test_explainability.py
```
