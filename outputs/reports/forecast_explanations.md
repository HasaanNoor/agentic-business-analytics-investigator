# Forecast Explainability Report

This report explains the selected deterministic forecasting models using SHAP where supported. Fallback explanations are used only when SHAP cannot explain a model cleanly.

### net_revenue

- Predicted KPI: `net_revenue`
- Selected model: `linear_regression`
- Explanation method: SHAP LinearExplainer
- Most recent forecast explained: 2027-01-07, forecast value `101628.634690`
- Features that mattered most: `website_visitors`, `conversion_rate`, `average_order_value`
- SHAP summary plot: `outputs/figures/shap_summary_net_revenue.png`

Prediction-level influence:
- `website_visitors` increased the forecast by about 33673.9117 model units (feature value: 28691.0000).
- `average_order_value` increased the forecast by about 6817.4361 model units (feature value: 97.6700).
- `conversion_rate` decreased the forecast by about 4519.4064 model units (feature value: 0.0383).

Limitations: SHAP attributions explain model behavior, not guaranteed real-world causality.

### support_ticket_count

- Predicted KPI: `support_ticket_count`
- Selected model: `random_forest`
- Explanation method: SHAP TreeExplainer
- Most recent forecast explained: 2027-01-07, forecast value `214.241878`
- Features that mattered most: `previous_day_value`, `shipping_delay_rate`, `avg_api_latency_ms`
- SHAP summary plot: `outputs/figures/shap_summary_support_ticket_count.png`

Prediction-level influence:
- `previous_day_value` decreased the forecast by about 10.0815 model units (feature value: 212.8649).
- `shipping_delay_rate` decreased the forecast by about 1.6946 model units (feature value: 0.0665).
- `avg_api_latency_ms` decreased the forecast by about 1.5255 model units (feature value: 205.8900).

Limitations: SHAP attributions explain model behavior, not guaranteed real-world causality.

### shipping_delay_rate

- Predicted KPI: `shipping_delay_rate`
- Selected model: `random_forest`
- Explanation method: SHAP TreeExplainer
- Most recent forecast explained: 2027-01-07, forecast value `0.053737`
- Features that mattered most: `delivery_complaints`, `rolling_avg_3d`, `previous_day_value`
- SHAP summary plot: `outputs/figures/shap_summary_shipping_delay_rate.png`

Prediction-level influence:
- `delivery_complaints` decreased the forecast by about 0.0025 model units (feature value: 20.0000).
- `lag_7d` decreased the forecast by about 0.0015 model units (feature value: 0.0665).
- `rolling_avg_7d` increased the forecast by about 0.0008 model units (feature value: 0.0566).

Limitations: SHAP attributions explain model behavior, not guaranteed real-world causality.
