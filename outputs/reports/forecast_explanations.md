# Forecast Explainability Report

This report explains the selected deterministic forecasting models using SHAP where supported. Fallback explanations are used only when SHAP cannot explain a model cleanly.

### net_revenue

- Predicted KPI: `net_revenue`
- Selected model: `linear_regression`
- Explanation method: SHAP LinearExplainer
- Most recent forecast explained: 2027-01-07, forecast value `66788.517977`
- Features that mattered most: `lag_7d`, `lag_14d`, `conversion_rate`
- SHAP summary plot: `outputs/figures/shap_summary_net_revenue.png`

Prediction-level influence:
- `rolling_avg_7d` increased the forecast by about 3660.8523 model units (feature value: 75611.3709).
- `lag_7d` increased the forecast by about 3543.9582 model units (feature value: 72232.8500).
- `conversion_rate` decreased the forecast by about 3346.7180 model units (feature value: 0.0383).

Limitations: SHAP attributions explain model behavior, not guaranteed real-world causality.

### support_ticket_count

- Predicted KPI: `support_ticket_count`
- Selected model: `random_forest`
- Explanation method: SHAP TreeExplainer
- Most recent forecast explained: 2027-01-07, forecast value `215.493560`
- Features that mattered most: `previous_day_value`, `shipping_delay_rate`, `checkout_failure_rate`
- SHAP summary plot: `outputs/figures/shap_summary_support_ticket_count.png`

Prediction-level influence:
- `previous_day_value` decreased the forecast by about 9.7585 model units (feature value: 214.8033).
- `shipping_delay_rate` decreased the forecast by about 1.7527 model units (feature value: 0.0535).
- `avg_api_latency_ms` decreased the forecast by about 0.9297 model units (feature value: 202.1900).

Limitations: SHAP attributions explain model behavior, not guaranteed real-world causality.

### shipping_delay_rate

- Predicted KPI: `shipping_delay_rate`
- Selected model: `linear_regression`
- Explanation method: SHAP LinearExplainer
- Most recent forecast explained: 2027-01-07, forecast value `0.057052`
- Features that mattered most: `shipping_disruption_flag`, `delivery_complaints`, `previous_day_value`
- SHAP summary plot: `outputs/figures/shap_summary_shipping_delay_rate.png`

Prediction-level influence:
- `delivery_complaints` increased the forecast by about 0.0011 model units (feature value: 35.0000).
- `shipping_disruption_flag` decreased the forecast by about 0.0008 model units (feature value: 0.0000).
- `rolling_avg_7d` decreased the forecast by about 0.0004 model units (feature value: 0.0562).

Limitations: SHAP attributions explain model behavior, not guaranteed real-world causality.
