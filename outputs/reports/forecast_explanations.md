# Forecast Explainability Report

This report explains the selected deterministic forecasting models using SHAP where supported. Fallback explanations are used only when SHAP cannot explain a model cleanly.

### net_revenue

- Predicted KPI: `net_revenue`
- Selected model: `linear_regression`
- Explanation method: SHAP LinearExplainer
- Most recent forecast explained: 2025-07-07, forecast value `40483.582308`
- Features that mattered most: `previous_day_value`, `lag_14d`, `rolling_avg_3d`
- SHAP summary plot: `outputs/figures/shap_summary_net_revenue.png`

Prediction-level influence:
- `rolling_avg_3d` decreased the forecast by about 3655.1533 model units (feature value: 54867.1359).
- `lag_14d` decreased the forecast by about 3354.0851 model units (feature value: 34631.3000).
- `previous_day_value` increased the forecast by about 2535.1356 model units (feature value: 51097.8055).

Limitations: SHAP attributions explain model behavior, not guaranteed real-world causality.

### support_ticket_count

- Predicted KPI: `support_ticket_count`
- Selected model: `random_forest`
- Explanation method: SHAP TreeExplainer
- Most recent forecast explained: 2025-07-07, forecast value `209.245339`
- Features that mattered most: `previous_day_value`, `lag_7d`, `rolling_avg_3d`
- SHAP summary plot: `outputs/figures/shap_summary_support_ticket_count.png`

Prediction-level influence:
- `previous_day_value` decreased the forecast by about 8.3101 model units (feature value: 217.8535).
- `lag_7d` decreased the forecast by about 6.6591 model units (feature value: 215.0000).
- `rolling_avg_3d` decreased the forecast by about 1.6525 model units (feature value: 219.4871).

Limitations: SHAP attributions explain model behavior, not guaranteed real-world causality.

### shipping_delay_rate

- Predicted KPI: `shipping_delay_rate`
- Selected model: `random_forest`
- Explanation method: SHAP TreeExplainer
- Most recent forecast explained: 2025-07-07, forecast value `0.054604`
- Features that mattered most: `previous_day_value`, `rolling_avg_7d`, `rolling_avg_3d`
- SHAP summary plot: `outputs/figures/shap_summary_shipping_delay_rate.png`

Prediction-level influence:
- `previous_day_value` decreased the forecast by about 0.0038 model units (feature value: 0.0557).
- `rolling_avg_7d` decreased the forecast by about 0.0013 model units (feature value: 0.0552).
- `lag_14d` increased the forecast by about 0.0008 model units (feature value: 0.0628).

Limitations: SHAP attributions explain model behavior, not guaranteed real-world causality.
