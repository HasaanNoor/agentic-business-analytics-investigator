# Executive Operations Report

## Executive Summary

The deterministic pipeline found 64 grouped incident(s). This report summarizes the top 5 incident(s), the forecast outlook, model drivers, and recommended actions from structured pipeline outputs only.

## Key Incidents

### INC-055: Inventory shortage incident

- Date range: 2026-09-01 to 2026-09-24
- Likely cause: Likely inventory shortage incident
- Main anomaly: `inventory_shortage_period`
- Affected KPIs: `net_revenue` avg 59179.59, range 32242.51 to 90618.66; `support_ticket_count` avg 178.7083, range 139.0 to 237.0; `shipping_delay_rate` avg 0.064, range 0.056 to 0.0746; `stockout_units` avg 76.1667, range 0.0 to 139.0; `checkout_failure_rate` avg 0.018, range 0.016 to 0.0201; `lost_sales_units` avg 82.5833, range 0.0 to 178.0
- Evidence: Inventory shortage and revenue drop anomalies overlapped from 2026-09-01 to 2026-09-24. Lost sales units reached 178.00 during the incident.

### INC-046: Inventory shortage incident

- Date range: 2026-05-04 to 2026-05-30
- Likely cause: Likely inventory shortage incident
- Main anomaly: `inventory_shortage_period`
- Affected KPIs: `net_revenue` avg 68093.4626, range 47213.13 to 95761.81; `avg_api_latency_ms` avg 207.7707, range 197.54 to 215.99; `shipping_delay_rate` avg 0.0638, range 0.0579 to 0.0738; `stockout_units` avg 43.3333, range 0.0 to 129.0; `support_ticket_count` avg 169.1481, range 143.0 to 191.0; `lost_sales_units` avg 40.3333, range 0.0 to 130.0
- Evidence: Inventory shortage and revenue drop anomalies overlapped from 2026-05-04 to 2026-05-30. Lost sales units reached 130.00 during the incident.

### INC-033: Inventory shortage incident

- Date range: 2025-12-01 to 2025-12-16
- Likely cause: Likely inventory shortage incident
- Main anomaly: `inventory_shortage_period`
- Affected KPIs: `net_revenue` avg 43789.6631, range 28434.33 to 62556.48; `stockout_units` avg 97.5, range 0.0 to 135.0; `support_ticket_count` avg 178.75, range 153.0 to 210.0; `shipping_delay_rate` avg 0.0661, range 0.051 to 0.0759; `lost_sales_units` avg 134.0625, range 0.0 to 190.0
- Evidence: Inventory shortage and revenue drop anomalies overlapped from 2025-12-01 to 2025-12-16. Lost sales units reached 190.00 during the incident.

### INC-056: Logistics disruption incident

- Date range: 2026-10-03 to 2026-10-14
- Likely cause: Likely logistics disruption incident
- Main anomaly: `shipping_delay_spike`
- Affected KPIs: `checkout_failure_rate` avg 0.0182, range 0.0166 to 0.0197; `net_revenue` avg 63679.7817, range 44608.19 to 95497.0; `shipping_delay_rate` avg 0.1817, range 0.0658 to 0.2306; `support_ticket_count` avg 277.1667, range 159.0 to 321.0; `delivery_complaints` avg 129.25, range 29.0 to 165.0
- Evidence: Shipping delay anomalies occurred from 2026-10-03 to 2026-10-14. Delivery complaints reached 165.00 versus a prior average of 32.29.

### INC-045: Deployment-related checkout incident

- Date range: 2026-04-13 to 2026-04-21
- Likely cause: Likely deployment-related checkout incident
- Main anomaly: `checkout_failure_spike`
- Affected KPIs: `net_revenue` avg 45398.3344, range 22240.78 to 79260.17; `checkout_failure_rate` avg 0.0985, range 0.0175 to 0.1728; `avg_api_latency_ms` avg 490.3289, range 204.56 to 733.8; `support_ticket_count` avg 293.7778, range 139.0 to 439.0; `shipping_delay_rate` avg 0.0631, range 0.0553 to 0.0732; `conversion_rate` avg 0.0315, range 0.0197 to 0.0432
- Evidence: Latency and checkout failure anomalies occurred together from 2026-04-13 to 2026-04-21. 2 failed or rollback deployment event(s) occurred within the investigation window.

## Forecast Outlook

- `net_revenue` is forecast up from 101159.301356 on 2027-01-01 to 101714.013209 on 2027-01-07 using `linear_regression`.
- `shipping_delay_rate` is forecast up from 0.071877 on 2027-01-01 to 0.072088 on 2027-01-07 using `linear_regression`.
- `support_ticket_count` is forecast down from 187.731323 on 2027-01-01 to 187.297409 on 2027-01-07 using `xgboost`.

## Main Business Drivers

- `net_revenue`: top SHAP drivers are `website_visitors`, `conversion_rate`, `average_order_value` (SHAP LinearExplainer, `linear_regression`).
- `shipping_delay_rate`: top SHAP drivers are `warehouse_backlog`, `east_region_disruption`, `shipping_complaint_tickets` (SHAP LinearExplainer, `linear_regression`).
- `support_ticket_count`: top SHAP drivers are `shipping_delay_rate`, `active_customers`, `checkout_failure_rate` (SHAP TreeExplainer, `xgboost`).

## Recommended Actions

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.
- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.
- Review the failed checkout deployment, dependency changes, and rollback results.
- Validate checkout success rate, API latency, and revenue after rollback.

## Limitations

- This report does not read raw full datasets and does not add RAG, dashboard, or API behavior.
- The narrative is grounded in deterministic incident, forecast, SHAP, and model-metric outputs.
- SHAP attributions explain model behavior and should not be treated as proof of real-world causality.
- `net_revenue` uses `linear_regression` with RMSE 4964.673018 and R2 0.948033; Forecast metrics measure historical test performance; they do not prove causal relationships or guarantee future accuracy.
- `shipping_delay_rate` uses `linear_regression` with RMSE 0.014857 and R2 0.862143; Forecast metrics measure historical test performance; they do not prove causal relationships or guarantee future accuracy.
- `support_ticket_count` uses `xgboost` with RMSE 18.575684 and R2 0.862286; Forecast metrics measure historical test performance; they do not prove causal relationships or guarantee future accuracy.
