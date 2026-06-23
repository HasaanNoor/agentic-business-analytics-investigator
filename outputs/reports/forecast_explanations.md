# Forecast Explainability Report

This report explains the selected deterministic forecasting models using SHAP where supported. Fallback explanations are used only when SHAP cannot explain a model cleanly.

### net_revenue

- Predicted KPI: `net_revenue`
- Selected model: `linear_regression`
- Explanation method: SHAP LinearExplainer
- Most recent forecast explained: 2027-01-07, forecast value `120013.005658`
- Features that mattered most: `website_visitors`, `conversion_rate`, `average_order_value`
- SHAP summary plot: `outputs/figures/shap_summary_net_revenue.png`

Prediction-level influence:
- `website_visitors` increased the forecast by about 38511.6066 model units (feature value: 34873.0000).
- `average_order_value` increased the forecast by about 7648.6774 model units (feature value: 98.1900).
- `rolling_avg_14d` decreased the forecast by about 5303.1025 model units (feature value: 130857.8317).

Limitations: SHAP attributions explain model behavior, not guaranteed real-world causality.

### support_ticket_count

- Predicted KPI: `support_ticket_count`
- Selected model: `xgboost`
- Explanation method: SHAP TreeExplainer
- Most recent forecast explained: 2027-01-07, forecast value `170.871185`
- Features that mattered most: `shipping_delay_rate`, `checkout_failure_rate`, `shipping_complaint_tickets_rolling_avg_7d`
- SHAP summary plot: `outputs/figures/shap_summary_support_ticket_count.png`

Prediction-level influence:
- `shipping_delay_rate` decreased the forecast by about 13.9351 model units (feature value: 0.0669).
- `checkout_failure_rate` decreased the forecast by about 12.5443 model units (feature value: 0.0188).
- `shipping_complaint_tickets_rolling_avg_7d` decreased the forecast by about 3.9529 model units (feature value: 37.0000).

Limitations: SHAP attributions explain model behavior, not guaranteed real-world causality.

### shipping_delay_rate

- Predicted KPI: `shipping_delay_rate`
- Selected model: `xgboost`
- Explanation method: SHAP TreeExplainer
- Most recent forecast explained: 2027-01-07, forecast value `0.068797`
- Features that mattered most: `warehouse_backlog`, `shipping_complaint_tickets`, `west_region_disruption`
- SHAP summary plot: `outputs/figures/shap_summary_shipping_delay_rate.png`

Prediction-level influence:
- `warehouse_backlog` decreased the forecast by about 0.0080 model units (feature value: 549.0000).
- `shipping_complaint_tickets` decreased the forecast by about 0.0018 model units (feature value: 37.0000).
- `west_region_disruption` increased the forecast by about 0.0002 model units (feature value: 0.0000).

Limitations: SHAP attributions explain model behavior, not guaranteed real-world causality.
