# Executive Operations Report

## Executive Summary

The deterministic pipeline found 210 grouped incident(s). This report summarizes the top 5 incident(s), the forecast outlook, model drivers, historical incident comparisons, and recommended actions from structured pipeline outputs only.

## Key Incidents

### INC-143: Inventory shortage incident

- Date range: 2025-12-03 to 2025-12-20
- Severity: critical
- Affected region: Midwest
- Likely cause: Likely inventory shortage incident
- Business impact: Stockouts created lost sales and customer complaints.
- Previous successful resolution: Transferred inventory from another warehouse and expedited replenishment. (success False, recovery 4 day(s))
- Main anomaly: `inventory_shortage_period`
- Affected KPIs: `stockout_units` avg 196.5, range 0.0 to 470.0; `refund_rate` avg 0.0405, range 0.0141 to 0.101; `incident_signal` avg 0.9444, range 0.0 to 1.0; `net_revenue` avg 61642.6894, range 42227.85 to 108794.53; `shipping_delay_rate` avg 0.0779, range 0.0579 to 0.1508; `support_ticket_count` avg 219.1667, range 166.0 to 316.0; `warehouse_backlog` avg 607.0556, range 476.0 to 1080.0; `checkout_failure_rate` avg 0.031, range 0.0166 to 0.098; `avg_api_latency_ms` avg 206.6861, range 201.15 to 214.37; `website_visitors` avg 26067.0556, range 23707.0 to 28756.0; `lost_sales_units` avg 132.6111, range 0.0 to 252.0
- Evidence: Inventory shortage and revenue drop anomalies overlapped from 2025-12-03 to 2025-12-20. Lost sales units reached 252.00 during the incident.

### INC-192: Inventory shortage incident

- Date range: 2026-09-08 to 2026-09-26
- Severity: critical
- Affected region: Southeast
- Likely cause: Likely inventory shortage incident
- Business impact: Stockouts created lost sales and customer complaints.
- Previous successful resolution: Transferred inventory from another warehouse and expedited replenishment. (success False, recovery 4 day(s))
- Main anomaly: `inventory_shortage_period`
- Affected KPIs: `checkout_failure_rate` avg 0.0303, range 0.0164 to 0.0972; `stockout_units` avg 94.8421, range 0.0 to 137.0; `incident_signal` avg 0.9474, range 0.0 to 1.0; `refund_rate` avg 0.0272, range 0.0126 to 0.0786; `net_revenue` avg 72945.0268, range 33889.57 to 122302.05; `avg_api_latency_ms` avg 247.2305, range 199.92 to 478.48; `support_ticket_count` avg 208.4211, range 159.0 to 280.0; `website_visitors` avg 28064.7895, range 23949.0 to 33845.0; `shipping_delay_rate` avg 0.0714, range 0.0544 to 0.129; `warehouse_backlog` avg 547.8421, range 423.0 to 967.0; `lost_sales_units` avg 108.0, range 0.0 to 173.0
- Evidence: Inventory shortage and revenue drop anomalies overlapped from 2026-09-08 to 2026-09-26. Lost sales units reached 173.00 during the incident.

### INC-172: Inventory shortage incident

- Date range: 2026-05-17 to 2026-05-30
- Severity: critical
- Affected region: Southeast
- Likely cause: Likely inventory shortage incident
- Business impact: Stockouts created lost sales and customer complaints.
- Previous successful resolution: Transferred inventory from another warehouse and expedited replenishment. (success False, recovery 4 day(s))
- Main anomaly: `inventory_shortage_period`
- Affected KPIs: `stockout_units` avg 182.9286, range 87.0 to 474.0; `incident_signal` avg 1.0, range 1.0 to 1.0; `net_revenue` avg 74543.6721, range 57487.09 to 89469.0; `shipping_delay_rate` avg 0.0903, range 0.0564 to 0.1456; `refund_rate` avg 0.0237, range 0.0103 to 0.0352; `support_ticket_count` avg 219.8571, range 166.0 to 296.0; `warehouse_backlog` avg 663.0714, range 429.0 to 1046.0; `checkout_failure_rate` avg 0.0181, range 0.0164 to 0.02; `lost_sales_units` avg 96.5714, range 63.0 to 133.0
- Evidence: Inventory shortage and revenue drop anomalies overlapped from 2026-05-17 to 2026-05-30. Lost sales units reached 133.00 during the incident.

### INC-195: Inventory shortage incident

- Date range: 2026-10-04 to 2026-10-17
- Severity: critical
- Affected region: Northeast
- Likely cause: Likely inventory shortage incident
- Business impact: Stockouts created lost sales and customer complaints.
- Previous successful resolution: Transferred inventory from another warehouse and expedited replenishment. (success False, recovery 4 day(s))
- Main anomaly: `inventory_shortage_period`
- Affected KPIs: `checkout_failure_rate` avg 0.0334, range 0.0157 to 0.0935; `incident_signal` avg 1.0, range 1.0 to 1.0; `refund_rate` avg 0.0423, range 0.0232 to 0.0928; `net_revenue` avg 74411.2071, range 54237.15 to 102917.38; `support_ticket_count` avg 322.7143, range 271.0 to 443.0; `shipping_delay_rate` avg 0.1899, range 0.0652 to 0.2117; `warehouse_backlog` avg 1330.9286, range 556.0 to 1451.0; `stockout_units` avg 160.4286, range 0.0 to 477.0; `lost_sales_units` avg 24.5, range 0.0 to 78.0
- Evidence: Inventory shortage and revenue drop anomalies overlapped from 2026-10-04 to 2026-10-17. Lost sales units reached 78.00 during the incident.

### INC-100: Logistics disruption incident

- Date range: 2025-05-02 to 2025-05-14
- Severity: critical
- Affected region: Midwest
- Likely cause: Likely logistics disruption incident
- Business impact: Shipping delays increased delivery complaints and delayed order completion.
- Previous successful resolution: Rerouted affected orders through backup carriers and prioritized delayed deliveries. (success False, recovery 4 day(s))
- Main anomaly: `shipping_delay_spike`
- Affected KPIs: `incident_signal` avg 1.0, range 1.0 to 1.0; `checkout_failure_rate` avg 0.036, range 0.0169 to 0.0979; `avg_api_latency_ms` avg 269.5138, range 204.61 to 482.1; `net_revenue` avg 71733.6838, range 49234.63 to 100695.89; `support_ticket_count` avg 293.0769, range 221.0 to 358.0; `shipping_delay_rate` avg 0.1442, range 0.0562 to 0.2264; `warehouse_backlog` avg 993.3077, range 417.0 to 1541.0; `website_visitors` avg 23550.4615, range 19429.0 to 28969.0; `delivery_complaints` avg 112.6923, range 26.0 to 176.0
- Evidence: Shipping delay anomalies occurred from 2025-05-02 to 2025-05-14. Delivery complaints reached 176.00 versus a prior average of 53.00.

## Forecast Outlook

- `net_revenue` is forecast down from 120837.405024 on 2027-01-01 to 120013.005658 on 2027-01-07 using `linear_regression`.
- `shipping_delay_rate` is forecast down from 0.069278 on 2027-01-01 to 0.068797 on 2027-01-07 using `xgboost`.
- `support_ticket_count` is forecast up from 168.54924 on 2027-01-01 to 170.871185 on 2027-01-07 using `xgboost`.

## Main Business Drivers

- `net_revenue`: top SHAP drivers are `website_visitors`, `conversion_rate`, `average_order_value` (SHAP LinearExplainer, `linear_regression`).
- `shipping_delay_rate`: top SHAP drivers are `warehouse_backlog`, `shipping_complaint_tickets`, `west_region_disruption` (SHAP TreeExplainer, `xgboost`).
- `support_ticket_count`: top SHAP drivers are `shipping_delay_rate`, `checkout_failure_rate`, `shipping_complaint_tickets_rolling_avg_7d` (SHAP TreeExplainer, `xgboost`).

## Recommended Actions

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.
- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## Limitations

- This report does not read raw full datasets and does not add RAG, dashboard, or API behavior.
- The narrative is grounded in deterministic incident, forecast, SHAP, and model-metric outputs.
- SHAP attributions explain model behavior and should not be treated as proof of real-world causality.
- `net_revenue` uses `linear_regression` with RMSE 6271.453003 and R2 0.939947; Forecast metrics measure historical test performance; they do not prove causal relationships or guarantee future accuracy.
- `shipping_delay_rate` uses `xgboost` with RMSE 0.005375 and R2 0.982761; Forecast metrics measure historical test performance; they do not prove causal relationships or guarantee future accuracy.
- `support_ticket_count` uses `xgboost` with RMSE 24.159161 and R2 0.856275; Forecast metrics measure historical test performance; they do not prove causal relationships or guarantee future accuracy.
