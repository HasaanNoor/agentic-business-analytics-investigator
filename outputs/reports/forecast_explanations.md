# Forecast Explainability Report

This report explains the selected deterministic forecasting models using SHAP where supported. Fallback explanations are used only when SHAP cannot explain a model cleanly.

### net_revenue

- Predicted KPI: `net_revenue`
- Selected model: `linear_regression`
- Explanation method: SHAP LinearExplainer
- Most recent forecast explained: 2025-07-07, forecast value `42988.532546`
- Features that mattered most: `conversion_rate`, `refund_rate`, `checkout_failure_rate`
- SHAP summary plot: `outputs/figures/shap_summary_net_revenue.png`

Prediction-level influence:
- `lag_14d` decreased the forecast by about 2686.1126 model units (feature value: 34631.3000).
- `rolling_avg_3d` decreased the forecast by about 2552.4638 model units (feature value: 54564.4546).
- `refund_rate` increased the forecast by about 2348.2778 model units (feature value: 0.0319).

Limitations: SHAP attributions explain model behavior, not guaranteed real-world causality.

### support_ticket_count

- Predicted KPI: `support_ticket_count`
- Selected model: `linear_regression`
- Explanation method: SHAP LinearExplainer
- Most recent forecast explained: 2025-07-07, forecast value `216.651663`
- Features that mattered most: `shipping_delay_rate`, `rolling_avg_7d`, `avg_api_latency_ms`
- SHAP summary plot: `outputs/figures/shap_summary_support_ticket_count.png`

Prediction-level influence:
- `avg_api_latency_ms` decreased the forecast by about 3.9115 model units (feature value: 198.8900).
- `rolling_avg_7d` decreased the forecast by about 2.4284 model units (feature value: 217.2968).
- `shipping_delay_rate` decreased the forecast by about 1.9616 model units (feature value: 0.0573).

Limitations: SHAP attributions explain model behavior, not guaranteed real-world causality.

### shipping_delay_rate

- Predicted KPI: `shipping_delay_rate`
- Selected model: `linear_regression`
- Explanation method: SHAP LinearExplainer
- Most recent forecast explained: 2025-07-07, forecast value `0.054105`
- Features that mattered most: `shipping_disruption_flag`, `delivery_complaints`, `rolling_avg_14d`
- SHAP summary plot: `outputs/figures/shap_summary_shipping_delay_rate.png`

Prediction-level influence:
- `shipping_disruption_flag` decreased the forecast by about 0.0052 model units (feature value: 0.0000).
- `rolling_avg_14d` decreased the forecast by about 0.0005 model units (feature value: 0.0556).
- `delivery_complaints` increased the forecast by about 0.0005 model units (feature value: 26.0000).

Limitations: SHAP attributions explain model behavior, not guaranteed real-world causality.
