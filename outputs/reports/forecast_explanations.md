# Forecast Explainability Report

This report explains the selected deterministic forecasting models using SHAP where supported. Fallback explanations are used only when SHAP cannot explain a model cleanly.

### net_revenue

- Predicted KPI: `net_revenue`
- Selected model: `linear_regression`
- Explanation method: SHAP LinearExplainer
- Most recent forecast explained: 2027-01-07, forecast value `101714.013209`
- Features that mattered most: `website_visitors`, `conversion_rate`, `average_order_value`
- SHAP summary plot: `outputs/figures/shap_summary_net_revenue.png`

Prediction-level influence:
- `website_visitors` increased the forecast by about 33313.9079 model units (feature value: 28691.0000).
- `average_order_value` increased the forecast by about 6818.3900 model units (feature value: 97.6700).
- `conversion_rate` decreased the forecast by about 4409.3265 model units (feature value: 0.0383).

Limitations: SHAP attributions explain model behavior, not guaranteed real-world causality.

### support_ticket_count

- Predicted KPI: `support_ticket_count`
- Selected model: `xgboost`
- Explanation method: SHAP TreeExplainer
- Most recent forecast explained: 2027-01-07, forecast value `187.297409`
- Features that mattered most: `shipping_delay_rate`, `active_customers`, `checkout_failure_rate`
- SHAP summary plot: `outputs/figures/shap_summary_support_ticket_count.png`

Prediction-level influence:
- `shipping_delay_rate` increased the forecast by about 11.9157 model units (feature value: 0.0815).
- `website_visitors` increased the forecast by about 5.3500 model units (feature value: 28691.0000).
- `active_customers` increased the forecast by about 3.2368 model units (feature value: 18845.0000).

Limitations: SHAP attributions explain model behavior, not guaranteed real-world causality.

### shipping_delay_rate

- Predicted KPI: `shipping_delay_rate`
- Selected model: `linear_regression`
- Explanation method: SHAP LinearExplainer
- Most recent forecast explained: 2027-01-07, forecast value `0.072088`
- Features that mattered most: `warehouse_backlog`, `east_region_disruption`, `shipping_complaint_tickets`
- SHAP summary plot: `outputs/figures/shap_summary_shipping_delay_rate.png`

Prediction-level influence:
- `warehouse_backlog` increased the forecast by about 0.0034 model units (feature value: 586.0000).
- `shipping_complaint_tickets` increased the forecast by about 0.0014 model units (feature value: 47.0000).
- `delivery_complaints` increased the forecast by about 0.0014 model units (feature value: 47.0000).

Limitations: SHAP attributions explain model behavior, not guaranteed real-world causality.
