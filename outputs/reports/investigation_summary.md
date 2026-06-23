# Deterministic Investigation Summary

Generated from anomaly events grouped with a maximum consecutive-event gap of 1 days.
Total incidents: **210**

## INC-001: Shipping Delay Spike Incident

- **Date range:** 2024-01-08 to 2024-01-08
- **Severity:** low
- **Affected region:** All regions
- **Likely cause:** Likely logistics incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success True, recovery 3 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** None

### Evidence

- 1 event(s) for shipping_delay_spike were grouped within 2024-01-08 to 2024-01-08.

### Affected KPIs

- `shipping_delay_rate`: min 0.0668, max 0.0668, average 0.0668 (1 anomaly event(s))

### Recommended Next Steps

- Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- Compare the current incident with similar historical incidents before finalizing recommendations.
- Monitor affected metrics until recovery is confirmed.

## INC-002: Latency Spike Incident

- **Date range:** 2024-01-10 to 2024-01-11
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely platform reliability incident
- **Root cause category:** platform reliability
- **Business impact:** API latency slowed checkout and increased support volume.
- **Resolution:** Reduced API latency by rolling back the slow dependency and scaling checkout workers.
- **Outcome:** success True, recovery 3 day(s)
- **Main anomaly:** `latency_spike`
- **Related anomalies:** `shipping_delay_spike`, `support_ticket_spike`

### Evidence

- 3 event(s) for latency_spike were grouped within 2024-01-10 to 2024-01-11.

### Affected KPIs

- `shipping_delay_rate`: min 0.0625, max 0.0677, average 0.0651 (1 anomaly event(s))
- `support_ticket_count`: min 160.0, max 164.0, average 162.0 (1 anomaly event(s))
- `avg_api_latency_ms`: min 208.16, max 216.41, average 212.285 (1 anomaly event(s))

### Recommended Next Steps

- Reduced API latency by rolling back the slow dependency and scaling checkout workers.
- Compare the current incident with similar historical incidents before finalizing recommendations.
- Monitor affected metrics until recovery is confirmed.

## INC-003: Inventory shortage incident

- **Date range:** 2024-01-13 to 2024-01-16
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `inventory_shortage`, `latency_spike`, `refund_spike`, `revenue_drop`, `shipping_delay_spike`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2024-01-13 to 2024-01-16.
- Lost sales units reached 98.00 during the incident.

### Affected KPIs

- `incident_signal`: min 0.0, max 1.0, average 0.5 (1 anomaly event(s))
- `stockout_units`: min 0.0, max 441.0, average 203.25 (2 anomaly event(s))
- `refund_rate`: min 0.0332, max 0.0461, average 0.0386 (1 anomaly event(s))
- `net_revenue`: min 27908.1, max 53760.5, average 38235.08 (2 anomaly event(s))
- `shipping_delay_rate`: min 0.0604, max 0.0705, average 0.0652 (1 anomaly event(s))
- `avg_api_latency_ms`: min 205.97, max 218.06, average 209.32 (1 anomaly event(s))
- `lost_sales_units`: min 0.0, max 98.0, average 40.0 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-004: Inventory shortage incident

- **Date range:** 2024-01-18 to 2024-01-20
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `refund_spike`, `revenue_drop`, `supplier_delay`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2024-01-18 to 2024-01-20.
- Lost sales units reached 114.00 during the incident.

### Affected KPIs

- `stockout_units`: min 436.0, max 516.0, average 468.3333 (3 anomaly event(s))
- `refund_rate`: min 0.0332, max 0.0671, average 0.0481 (1 anomaly event(s))
- `net_revenue`: min 24071.82, max 29651.2, average 26557.8967 (3 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `lost_sales_units`: min 73.0, max 114.0, average 92.0 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-005: Logistics disruption incident

- **Date range:** 2024-01-23 to 2024-01-24
- **Severity:** critical
- **Affected region:** Midwest
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `refund_spike`, `support_ticket_spike`, `warehouse_backlog_spike`, `warehouse_staffing_shortage`

### Evidence

- Shipping delay anomalies occurred from 2024-01-23 to 2024-01-24.
- Delivery complaints reached 123.00 versus a prior average of 22.50.

### Affected KPIs

- `refund_rate`: min 0.05, max 0.0566, average 0.0533 (2 anomaly event(s))
- `shipping_delay_rate`: min 0.1245, max 0.1424, average 0.1335 (2 anomaly event(s))
- `support_ticket_count`: min 216.0, max 241.0, average 228.5 (2 anomaly event(s))
- `warehouse_backlog`: min 857.0, max 931.0, average 894.0 (2 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `delivery_complaints`: min 98.0, max 123.0, average 110.5 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-006: Logistics disruption incident

- **Date range:** 2024-01-28 to 2024-01-30
- **Severity:** critical
- **Affected region:** West
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `carrier_outage`, `refund_spike`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2024-01-28 to 2024-01-30.
- Delivery complaints reached 114.00 versus a prior average of 34.07.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.046, max 0.0638, average 0.0554 (2 anomaly event(s))
- `shipping_delay_rate`: min 0.12, max 0.1403, average 0.129 (3 anomaly event(s))
- `support_ticket_count`: min 221.0, max 244.0, average 233.0 (3 anomaly event(s))
- `warehouse_backlog`: min 924.0, max 1043.0, average 976.3333 (3 anomaly event(s))
- `delivery_complaints`: min 95.0, max 114.0, average 107.3333 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-007: Refund spike incident

- **Date range:** 2024-02-02 to 2024-02-03
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success True, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** `support_ticket_spike`

### Evidence

- Refund anomalies occurred from 2024-02-02 to 2024-02-03.
- Refund rate reached 0.1469 versus a prior average of 0.0412.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.1273, max 0.1469, average 0.1371 (2 anomaly event(s))
- `support_ticket_count`: min 198.0, max 216.0, average 207.0 (1 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-008: Demand surge incident

- **Date range:** 2024-02-07 to 2024-02-09
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely marketing campaign or holiday demand surge
- **Root cause category:** demand surge
- **Business impact:** Traffic increased quickly, creating capacity and support pressure.
- **Resolution:** Added support coverage and monitored checkout capacity during the traffic surge.
- **Outcome:** success False, recovery 2 day(s)
- **Main anomaly:** `visitor_surge`
- **Related anomalies:** `api_degradation`, `checkout_failure_spike`, `latency_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Visitor surge anomalies occurred from 2024-02-07 to 2024-02-09.
- Website visitors reached 13789.00 versus a prior average of 12391.36.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `checkout_failure_rate`: min 0.0925, max 0.0981, average 0.0953 (3 anomaly event(s))
- `avg_api_latency_ms`: min 470.26, max 480.81, average 476.6833 (3 anomaly event(s))
- `net_revenue`: min 32003.73, max 34853.03, average 33281.5333 (3 anomaly event(s))
- `website_visitors`: min 11759.0, max 13789.0, average 12872.0 (1 anomaly event(s))
- `support_ticket_count`: min 202.0, max 224.0, average 209.3333 (1 anomaly event(s))

### Recommended Next Steps

- Confirm whether a campaign, holiday event, or promotion drove the traffic increase.
- Add support coverage and monitor checkout, inventory, and fulfillment capacity.
- Keep successful demand actions active only while service levels remain healthy.

## INC-009: Demand surge incident

- **Date range:** 2024-02-12 to 2024-02-13
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely marketing campaign or holiday demand surge
- **Root cause category:** demand surge
- **Business impact:** Traffic increased quickly, creating capacity and support pressure.
- **Resolution:** Added support coverage and monitored checkout capacity during the traffic surge.
- **Outcome:** success True, recovery 2 day(s)
- **Main anomaly:** `visitor_surge`
- **Related anomalies:** `marketing_campaign_surge`

### Evidence

- Visitor surge anomalies occurred from 2024-02-12 to 2024-02-13.
- Website visitors reached 16295.00 versus a prior average of 12679.57.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `website_visitors`: min 14926.0, max 16295.0, average 15610.5 (2 anomaly event(s))

### Recommended Next Steps

- Confirm whether a campaign, holiday event, or promotion drove the traffic increase.
- Add support coverage and monitor checkout, inventory, and fulfillment capacity.
- Keep successful demand actions active only while service levels remain healthy.

## INC-010: Logistics disruption incident

- **Date range:** 2024-02-17 to 2024-02-19
- **Severity:** critical
- **Affected region:** West
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `holiday_demand_surge`, `support_ticket_spike`, `visitor_surge`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2024-02-17 to 2024-02-19.
- Delivery complaints reached 71.00 versus a prior average of 25.29.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.1102, max 0.1168, average 0.1143 (3 anomaly event(s))
- `support_ticket_count`: min 196.0, max 247.0, average 228.3333 (2 anomaly event(s))
- `website_visitors`: min 15331.0, max 16558.0, average 16043.0 (2 anomaly event(s))
- `warehouse_backlog`: min 834.0, max 895.0, average 871.0 (3 anomaly event(s))
- `delivery_complaints`: min 58.0, max 71.0, average 62.6667 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-011: Logistics disruption incident

- **Date range:** 2024-02-22 to 2024-02-23
- **Severity:** critical
- **Affected region:** Northeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `refund_spike`, `regional_weather_disruption`, `revenue_drop`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2024-02-22 to 2024-02-23.
- Delivery complaints reached 111.00 versus a prior average of 32.64.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `net_revenue`: min 29341.22, max 39634.47, average 34487.845 (2 anomaly event(s))
- `shipping_delay_rate`: min 0.1354, max 0.1428, average 0.1391 (2 anomaly event(s))
- `support_ticket_count`: min 223.0, max 238.0, average 230.5 (2 anomaly event(s))
- `warehouse_backlog`: min 879.0, max 1060.0, average 969.5 (2 anomaly event(s))
- `refund_rate`: min 0.0395, max 0.0681, average 0.0538 (1 anomaly event(s))
- `delivery_complaints`: min 100.0, max 111.0, average 105.5 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-012: Refund spike incident

- **Date range:** 2024-02-27 to 2024-02-29
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** `checkout_failure_spike`, `fraud_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Refund anomalies occurred from 2024-02-27 to 2024-02-29.
- Refund rate reached 0.1383 versus a prior average of 0.0354.

### Affected KPIs

- `checkout_failure_rate`: min 0.0948, max 0.0978, average 0.0962 (3 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.1321, max 0.1383, average 0.1354 (3 anomaly event(s))
- `support_ticket_count`: min 231.0, max 267.0, average 246.6667 (2 anomaly event(s))
- `net_revenue`: min 36916.62, max 43017.72, average 39942.17 (1 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-013: Inventory shortage incident

- **Date range:** 2024-03-03 to 2024-03-04
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `inventory_shortage`, `revenue_drop`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2024-03-03 to 2024-03-04.
- Lost sales units reached 104.00 during the incident.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `stockout_units`: min 463.0, max 520.0, average 491.5 (2 anomaly event(s))
- `net_revenue`: min 37584.2, max 39537.43, average 38560.815 (1 anomaly event(s))
- `lost_sales_units`: min 89.0, max 104.0, average 96.5 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-014: Demand surge incident

- **Date range:** 2024-03-06 to 2024-03-06
- **Severity:** low
- **Affected region:** All regions
- **Likely cause:** Likely marketing campaign or holiday demand surge
- **Root cause category:** demand surge
- **Business impact:** Traffic increased quickly, creating capacity and support pressure.
- **Resolution:** Added support coverage and monitored checkout capacity during the traffic surge.
- **Outcome:** success True, recovery 1 day(s)
- **Main anomaly:** `visitor_surge`
- **Related anomalies:** None

### Evidence

- Visitor surge anomalies occurred from 2024-03-06 to 2024-03-06.
- Website visitors reached 14677.00 versus a prior average of 13277.00.

### Affected KPIs

- `website_visitors`: min 14677.0, max 14677.0, average 14677.0 (1 anomaly event(s))

### Recommended Next Steps

- Confirm whether a campaign, holiday event, or promotion drove the traffic increase.
- Add support coverage and monitor checkout, inventory, and fulfillment capacity.
- Keep successful demand actions active only while service levels remain healthy.

## INC-015: Inventory shortage incident

- **Date range:** 2024-03-08 to 2024-03-10
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `latency_spike`, `revenue_drop`, `shipping_delay_spike`, `supplier_delay`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2024-03-08 to 2024-03-10.
- Lost sales units reached 117.00 during the incident.

### Affected KPIs

- `stockout_units`: min 452.0, max 525.0, average 480.3333 (3 anomaly event(s))
- `net_revenue`: min 30495.18, max 38681.36, average 34031.97 (2 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `avg_api_latency_ms`: min 208.43, max 216.92, average 213.0467 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.0577, max 0.0677, average 0.0612 (1 anomaly event(s))
- `lost_sales_units`: min 71.0, max 117.0, average 97.3333 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-016: Logistics disruption incident

- **Date range:** 2024-03-13 to 2024-03-14
- **Severity:** critical
- **Affected region:** Northeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `refund_spike`, `support_ticket_spike`, `warehouse_backlog_spike`, `warehouse_staffing_shortage`

### Evidence

- Shipping delay anomalies occurred from 2024-03-13 to 2024-03-14.
- Delivery complaints reached 110.00 versus a prior average of 28.36.

### Affected KPIs

- `shipping_delay_rate`: min 0.1222, max 0.1269, average 0.1246 (2 anomaly event(s))
- `support_ticket_count`: min 236.0, max 272.0, average 254.0 (2 anomaly event(s))
- `warehouse_backlog`: min 845.0, max 948.0, average 896.5 (2 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0435, max 0.0586, average 0.051 (1 anomaly event(s))
- `delivery_complaints`: min 100.0, max 110.0, average 105.0 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-017: Logistics disruption incident

- **Date range:** 2024-03-18 to 2024-03-20
- **Severity:** critical
- **Affected region:** Southeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `carrier_outage`, `refund_spike`, `revenue_drop`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2024-03-18 to 2024-03-20.
- Delivery complaints reached 125.00 versus a prior average of 38.00.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0389, max 0.0597, average 0.0524 (2 anomaly event(s))
- `net_revenue`: min 36695.97, max 60332.33, average 44895.1233 (2 anomaly event(s))
- `shipping_delay_rate`: min 0.1246, max 0.1399, average 0.1327 (3 anomaly event(s))
- `support_ticket_count`: min 251.0, max 289.0, average 267.6667 (3 anomaly event(s))
- `warehouse_backlog`: min 867.0, max 990.0, average 939.3333 (3 anomaly event(s))
- `delivery_complaints`: min 109.0, max 125.0, average 116.0 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-018: Refund spike incident

- **Date range:** 2024-03-23 to 2024-03-24
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success True, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** None

### Evidence

- Refund anomalies occurred from 2024-03-23 to 2024-03-24.
- Refund rate reached 0.1261 versus a prior average of 0.0373.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.1053, max 0.1261, average 0.1157 (2 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-019: Checkout Failure Spike Incident

- **Date range:** 2024-03-28 to 2024-03-30
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely platform reliability incident
- **Root cause category:** platform reliability
- **Business impact:** Checkout failures reduced conversion and increased customer contacts.
- **Resolution:** Rolled back the risky checkout change and added checkout health checks.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `api_degradation`, `latency_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- 12 event(s) for checkout_failure_spike were grouped within 2024-03-28 to 2024-03-30.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `checkout_failure_rate`: min 0.0898, max 0.1012, average 0.0964 (3 anomaly event(s))
- `avg_api_latency_ms`: min 474.22, max 483.35, average 479.4633 (3 anomaly event(s))
- `support_ticket_count`: min 245.0, max 250.0, average 248.0 (3 anomaly event(s))
- `net_revenue`: min 36551.05, max 42423.83, average 39322.5033 (2 anomaly event(s))

### Recommended Next Steps

- Rolled back the risky checkout change and added checkout health checks.
- Compare the current incident with similar historical incidents before finalizing recommendations.
- Monitor affected metrics until recovery is confirmed.

## INC-020: Demand surge incident

- **Date range:** 2024-04-02 to 2024-04-03
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely marketing campaign or holiday demand surge
- **Root cause category:** demand surge
- **Business impact:** Traffic increased quickly, creating capacity and support pressure.
- **Resolution:** Added support coverage and monitored checkout capacity during the traffic surge.
- **Outcome:** success True, recovery 2 day(s)
- **Main anomaly:** `visitor_surge`
- **Related anomalies:** `marketing_campaign_surge`

### Evidence

- Visitor surge anomalies occurred from 2024-04-02 to 2024-04-03.
- Website visitors reached 18621.00 versus a prior average of 14125.00.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `website_visitors`: min 18017.0, max 18621.0, average 18319.0 (2 anomaly event(s))

### Recommended Next Steps

- Confirm whether a campaign, holiday event, or promotion drove the traffic increase.
- Add support coverage and monitor checkout, inventory, and fulfillment capacity.
- Keep successful demand actions active only while service levels remain healthy.

## INC-021: Logistics disruption incident

- **Date range:** 2024-04-07 to 2024-04-09
- **Severity:** critical
- **Affected region:** Southeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `holiday_demand_surge`, `refund_spike`, `support_ticket_spike`, `visitor_surge`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2024-04-07 to 2024-04-09.
- Delivery complaints reached 74.00 versus a prior average of 25.29.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.1087, max 0.1389, average 0.1227 (3 anomaly event(s))
- `website_visitors`: min 17300.0, max 18735.0, average 18082.0 (2 anomaly event(s))
- `warehouse_backlog`: min 840.0, max 1000.0, average 908.3333 (3 anomaly event(s))
- `refund_rate`: min 0.0149, max 0.0339, average 0.0241 (1 anomaly event(s))
- `support_ticket_count`: min 196.0, max 240.0, average 211.3333 (1 anomaly event(s))
- `delivery_complaints`: min 56.0, max 74.0, average 62.3333 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-022: Logistics disruption incident

- **Date range:** 2024-04-12 to 2024-04-14
- **Severity:** critical
- **Affected region:** Midwest
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `refund_spike`, `regional_weather_disruption`, `revenue_drop`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2024-04-12 to 2024-04-14.
- Delivery complaints reached 135.00 versus a prior average of 34.00.

### Affected KPIs

- `refund_rate`: min 0.0332, max 0.0674, average 0.0517 (2 anomaly event(s))
- `incident_signal`: min 0.0, max 1.0, average 0.6667 (1 anomaly event(s))
- `net_revenue`: min 36372.75, max 48214.8, average 43768.42 (3 anomaly event(s))
- `shipping_delay_rate`: min 0.0609, max 0.1484, average 0.118 (2 anomaly event(s))
- `support_ticket_count`: min 147.0, max 265.0, average 222.0 (2 anomaly event(s))
- `warehouse_backlog`: min 490.0, max 1049.0, average 853.0 (2 anomaly event(s))
- `delivery_complaints`: min 29.0, max 135.0, average 91.3333 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-023: Refund spike incident

- **Date range:** 2024-04-17 to 2024-04-19
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** `checkout_failure_spike`, `fraud_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Refund anomalies occurred from 2024-04-17 to 2024-04-19.
- Refund rate reached 0.1478 versus a prior average of 0.0310.

### Affected KPIs

- `checkout_failure_rate`: min 0.0907, max 0.0945, average 0.0924 (3 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.1146, max 0.1478, average 0.1365 (3 anomaly event(s))
- `net_revenue`: min 31208.45, max 46211.17, average 38960.59 (2 anomaly event(s))
- `support_ticket_count`: min 228.0, max 280.0, average 259.0 (2 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-024: Inventory shortage incident

- **Date range:** 2024-04-22 to 2024-04-23
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `inventory_shortage`, `revenue_drop`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2024-04-22 to 2024-04-23.
- Lost sales units reached 99.00 during the incident.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `stockout_units`: min 331.0, max 468.0, average 399.5 (2 anomaly event(s))
- `net_revenue`: min 39291.74, max 40359.02, average 39825.38 (2 anomaly event(s))
- `lost_sales_units`: min 74.0, max 99.0, average 86.5 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-025: Inventory shortage incident

- **Date range:** 2024-04-27 to 2024-04-30
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `revenue_drop`, `shipping_delay_spike`, `supplier_delay`, `warehouse_backlog_spike`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2024-04-27 to 2024-04-30.
- Lost sales units reached 128.00 during the incident.

### Affected KPIs

- `stockout_units`: min 0.0, max 544.0, average 381.5 (3 anomaly event(s))
- `net_revenue`: min 33197.66, max 55778.57, average 41760.9175 (3 anomaly event(s))
- `incident_signal`: min 0.0, max 1.0, average 0.75 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.0538, max 0.0769, average 0.0655 (1 anomaly event(s))
- `warehouse_backlog`: min 465.0, max 582.0, average 512.25 (1 anomaly event(s))
- `lost_sales_units`: min 0.0, max 128.0, average 80.25 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-026: Logistics disruption incident

- **Date range:** 2024-05-02 to 2024-05-03
- **Severity:** critical
- **Affected region:** Midwest
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `refund_spike`, `support_ticket_spike`, `warehouse_backlog_spike`, `warehouse_staffing_shortage`

### Evidence

- Shipping delay anomalies occurred from 2024-05-02 to 2024-05-03.
- Delivery complaints reached 106.00 versus a prior average of 27.07.

### Affected KPIs

- `shipping_delay_rate`: min 0.1267, max 0.1351, average 0.1309 (2 anomaly event(s))
- `support_ticket_count`: min 254.0, max 262.0, average 258.0 (2 anomaly event(s))
- `warehouse_backlog`: min 881.0, max 943.0, average 912.0 (2 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0367, max 0.0573, average 0.047 (1 anomaly event(s))
- `delivery_complaints`: min 103.0, max 106.0, average 104.5 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-027: Logistics disruption incident

- **Date range:** 2024-05-07 to 2024-05-10
- **Severity:** critical
- **Affected region:** West
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `carrier_outage`, `latency_spike`, `refund_spike`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2024-05-07 to 2024-05-10.
- Delivery complaints reached 135.00 versus a prior average of 40.21.

### Affected KPIs

- `incident_signal`: min 0.0, max 1.0, average 0.75 (1 anomaly event(s))
- `refund_rate`: min 0.0309, max 0.0582, average 0.048 (3 anomaly event(s))
- `shipping_delay_rate`: min 0.0538, max 0.1364, average 0.1085 (2 anomaly event(s))
- `support_ticket_count`: min 135.0, max 282.0, average 229.25 (3 anomaly event(s))
- `warehouse_backlog`: min 457.0, max 1029.0, average 847.0 (3 anomaly event(s))
- `avg_api_latency_ms`: min 203.16, max 214.59, average 208.725 (1 anomaly event(s))
- `delivery_complaints`: min 19.0, max 135.0, average 94.5 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-028: Refund spike incident

- **Date range:** 2024-05-12 to 2024-05-13
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success True, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** None

### Evidence

- Refund anomalies occurred from 2024-05-12 to 2024-05-13.
- Refund rate reached 0.1368 versus a prior average of 0.0369.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.1028, max 0.1368, average 0.1198 (2 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-029: Checkout Failure Spike Incident

- **Date range:** 2024-05-17 to 2024-05-19
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely platform reliability incident
- **Root cause category:** platform reliability
- **Business impact:** Checkout failures reduced conversion and increased customer contacts.
- **Resolution:** Rolled back the risky checkout change and added checkout health checks.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `api_degradation`, `latency_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- 11 event(s) for checkout_failure_spike were grouped within 2024-05-17 to 2024-05-19.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `checkout_failure_rate`: min 0.0931, max 0.0957, average 0.0944 (3 anomaly event(s))
- `avg_api_latency_ms`: min 471.44, max 480.6, average 475.9467 (3 anomaly event(s))
- `net_revenue`: min 38264.76, max 39956.07, average 38847.5933 (2 anomaly event(s))
- `support_ticket_count`: min 237.0, max 255.0, average 248.0 (2 anomaly event(s))

### Recommended Next Steps

- Rolled back the risky checkout change and added checkout health checks.
- Compare the current incident with similar historical incidents before finalizing recommendations.
- Monitor affected metrics until recovery is confirmed.

## INC-030: Demand surge incident

- **Date range:** 2024-05-22 to 2024-05-23
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely marketing campaign or holiday demand surge
- **Root cause category:** demand surge
- **Business impact:** Traffic increased quickly, creating capacity and support pressure.
- **Resolution:** Added support coverage and monitored checkout capacity during the traffic surge.
- **Outcome:** success True, recovery 2 day(s)
- **Main anomaly:** `visitor_surge`
- **Related anomalies:** `marketing_campaign_surge`

### Evidence

- Visitor surge anomalies occurred from 2024-05-22 to 2024-05-23.
- Website visitors reached 19539.00 versus a prior average of 15055.14.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `website_visitors`: min 18374.0, max 19539.0, average 18956.5 (2 anomaly event(s))

### Recommended Next Steps

- Confirm whether a campaign, holiday event, or promotion drove the traffic increase.
- Add support coverage and monitor checkout, inventory, and fulfillment capacity.
- Keep successful demand actions active only while service levels remain healthy.

## INC-031: Logistics disruption incident

- **Date range:** 2024-05-27 to 2024-05-29
- **Severity:** critical
- **Affected region:** West
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `holiday_demand_surge`, `support_ticket_spike`, `visitor_surge`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2024-05-27 to 2024-05-29.
- Delivery complaints reached 58.00 versus a prior average of 26.79.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.1162, max 0.1191, average 0.1179 (3 anomaly event(s))
- `warehouse_backlog`: min 886.0, max 967.0, average 924.3333 (3 anomaly event(s))
- `support_ticket_count`: min 199.0, max 259.0, average 223.0 (1 anomaly event(s))
- `website_visitors`: min 18100.0, max 20559.0, average 19482.6667 (2 anomaly event(s))
- `delivery_complaints`: min 47.0, max 58.0, average 53.6667 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-032: Logistics disruption incident

- **Date range:** 2024-05-31 to 2024-06-02
- **Severity:** critical
- **Affected region:** Northeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `refund_spike`, `regional_weather_disruption`, `revenue_drop`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2024-05-31 to 2024-06-02.
- Delivery complaints reached 128.00 versus a prior average of 33.36.

### Affected KPIs

- `refund_rate`: min 0.0365, max 0.0498, average 0.0436 (3 anomaly event(s))
- `net_revenue`: min 40422.98, max 45098.53, average 43163.8367 (3 anomaly event(s))
- `incident_signal`: min 0.0, max 1.0, average 0.6667 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.0698, max 0.1542, average 0.1237 (2 anomaly event(s))
- `support_ticket_count`: min 160.0, max 262.0, average 228.0 (2 anomaly event(s))
- `warehouse_backlog`: min 569.0, max 1010.0, average 844.3333 (2 anomaly event(s))
- `delivery_complaints`: min 21.0, max 128.0, average 90.0 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-033: Refund spike incident

- **Date range:** 2024-06-06 to 2024-06-08
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** `checkout_failure_spike`, `fraud_spike`, `latency_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Refund anomalies occurred from 2024-06-06 to 2024-06-08.
- Refund rate reached 0.1496 versus a prior average of 0.0279.

### Affected KPIs

- `checkout_failure_rate`: min 0.0886, max 0.0946, average 0.0919 (3 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.1205, max 0.1496, average 0.1328 (3 anomaly event(s))
- `net_revenue`: min 36372.16, max 43017.98, average 40531.6767 (3 anomaly event(s))
- `support_ticket_count`: min 216.0, max 274.0, average 250.6667 (2 anomaly event(s))
- `avg_api_latency_ms`: min 202.11, max 217.92, average 208.7833 (1 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-034: Inventory Shortage Period Incident

- **Date range:** 2024-06-11 to 2024-06-12
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely inventory planning incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `inventory_shortage`

### Evidence

- 3 event(s) for inventory_shortage_period were grouped within 2024-06-11 to 2024-06-12.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `stockout_units`: min 410.0, max 449.0, average 429.5 (2 anomaly event(s))

### Recommended Next Steps

- Transferred inventory from another warehouse and expedited replenishment.
- Compare the current incident with similar historical incidents before finalizing recommendations.
- Monitor affected metrics until recovery is confirmed.

## INC-035: Inventory shortage incident

- **Date range:** 2024-06-16 to 2024-06-18
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `revenue_drop`, `shipping_delay_spike`, `supplier_delay`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2024-06-16 to 2024-06-18.
- Lost sales units reached 133.00 during the incident.

### Affected KPIs

- `stockout_units`: min 447.0, max 521.0, average 485.6667 (3 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `net_revenue`: min 36927.1, max 45813.54, average 41635.0867 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.0626, max 0.0715, average 0.0679 (1 anomaly event(s))
- `lost_sales_units`: min 79.0, max 133.0, average 114.3333 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-036: Logistics disruption incident

- **Date range:** 2024-06-21 to 2024-06-22
- **Severity:** critical
- **Affected region:** Northeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `refund_spike`, `support_ticket_spike`, `warehouse_backlog_spike`, `warehouse_staffing_shortage`

### Evidence

- Shipping delay anomalies occurred from 2024-06-21 to 2024-06-22.
- Delivery complaints reached 111.00 versus a prior average of 27.64.

### Affected KPIs

- `refund_rate`: min 0.0441, max 0.0549, average 0.0495 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.1232, max 0.1251, average 0.1241 (2 anomaly event(s))
- `support_ticket_count`: min 228.0, max 255.0, average 241.5 (2 anomaly event(s))
- `warehouse_backlog`: min 954.0, max 975.0, average 964.5 (2 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `delivery_complaints`: min 108.0, max 111.0, average 109.5 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-037: Logistics disruption incident

- **Date range:** 2024-06-26 to 2024-06-28
- **Severity:** critical
- **Affected region:** Southeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `carrier_outage`, `refund_spike`, `revenue_drop`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2024-06-26 to 2024-06-28.
- Delivery complaints reached 120.00 versus a prior average of 39.00.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0489, max 0.0624, average 0.0539 (3 anomaly event(s))
- `shipping_delay_rate`: min 0.1347, max 0.1474, average 0.1409 (3 anomaly event(s))
- `support_ticket_count`: min 256.0, max 266.0, average 260.3333 (3 anomaly event(s))
- `warehouse_backlog`: min 947.0, max 983.0, average 959.3333 (3 anomaly event(s))
- `net_revenue`: min 36116.08, max 49607.53, average 41688.0467 (2 anomaly event(s))
- `delivery_complaints`: min 117.0, max 120.0, average 119.0 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-038: Refund spike incident

- **Date range:** 2024-07-01 to 2024-07-02
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** `checkout_failure_spike`, `latency_spike`, `revenue_drop`

### Evidence

- Refund anomalies occurred from 2024-07-01 to 2024-07-02.
- Refund rate reached 0.1498 versus a prior average of 0.0376.

### Affected KPIs

- `avg_api_latency_ms`: min 197.0, max 215.06, average 206.03 (1 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0943, max 0.1498, average 0.122 (2 anomaly event(s))
- `net_revenue`: min 34758.11, max 52544.12, average 43651.115 (1 anomaly event(s))
- `checkout_failure_rate`: min 0.0187, max 0.0202, average 0.0195 (1 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-039: Checkout Failure Spike Incident

- **Date range:** 2024-07-05 to 2024-07-08
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely platform reliability incident
- **Root cause category:** platform reliability
- **Business impact:** Checkout failures reduced conversion and increased customer contacts.
- **Resolution:** Rolled back the risky checkout change and added checkout health checks.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `api_degradation`, `latency_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- 13 event(s) for checkout_failure_spike were grouped within 2024-07-05 to 2024-07-08.

### Affected KPIs

- `net_revenue`: min 35385.72, max 41459.86, average 38576.0575 (4 anomaly event(s))
- `incident_signal`: min 0.0, max 1.0, average 0.75 (1 anomaly event(s))
- `checkout_failure_rate`: min 0.0184, max 0.0939, average 0.0733 (3 anomaly event(s))
- `avg_api_latency_ms`: min 206.34, max 479.64, average 409.2775 (3 anomaly event(s))
- `support_ticket_count`: min 170.0, max 263.0, average 233.25 (2 anomaly event(s))

### Recommended Next Steps

- Rolled back the risky checkout change and added checkout health checks.
- Compare the current incident with similar historical incidents before finalizing recommendations.
- Monitor affected metrics until recovery is confirmed.

## INC-040: Demand surge incident

- **Date range:** 2024-07-11 to 2024-07-11
- **Severity:** medium
- **Affected region:** All regions
- **Likely cause:** Likely marketing campaign or holiday demand surge
- **Root cause category:** demand surge
- **Business impact:** Traffic increased quickly, creating capacity and support pressure.
- **Resolution:** Added support coverage and monitored checkout capacity during the traffic surge.
- **Outcome:** success True, recovery 1 day(s)
- **Main anomaly:** `visitor_surge`
- **Related anomalies:** `marketing_campaign_surge`

### Evidence

- Visitor surge anomalies occurred from 2024-07-11 to 2024-07-11.
- Website visitors reached 18153.00 versus a prior average of 15104.07.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `website_visitors`: min 18153.0, max 18153.0, average 18153.0 (1 anomaly event(s))

### Recommended Next Steps

- Confirm whether a campaign, holiday event, or promotion drove the traffic increase.
- Add support coverage and monitor checkout, inventory, and fulfillment capacity.
- Keep successful demand actions active only while service levels remain healthy.

## INC-041: Revenue Drop Incident

- **Date range:** 2024-07-13 to 2024-07-13
- **Severity:** low
- **Affected region:** All regions
- **Likely cause:** Likely sales impact incident
- **Root cause category:** sales impact
- **Business impact:** Net revenue fell below its normal range during the incident.
- **Resolution:** Reviewed conversion, stockout, refund, and logistics signals before selecting remediation.
- **Outcome:** success True, recovery 3 day(s)
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 event(s) for revenue_drop were grouped within 2024-07-13 to 2024-07-13.

### Affected KPIs

- `net_revenue`: min 42464.08, max 42464.08, average 42464.08 (1 anomaly event(s))

### Recommended Next Steps

- Reviewed conversion, stockout, refund, and logistics signals before selecting remediation.
- Compare the current incident with similar historical incidents before finalizing recommendations.
- Monitor affected metrics until recovery is confirmed.

## INC-042: Logistics disruption incident

- **Date range:** 2024-07-16 to 2024-07-19
- **Severity:** critical
- **Affected region:** Southeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `holiday_demand_surge`, `revenue_drop`, `support_ticket_spike`, `visitor_surge`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2024-07-16 to 2024-07-19.
- Delivery complaints reached 79.00 versus a prior average of 29.36.

### Affected KPIs

- `incident_signal`: min 0.0, max 1.0, average 0.75 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.0733, max 0.1461, average 0.1227 (3 anomaly event(s))
- `support_ticket_count`: min 133.0, max 254.0, average 213.25 (2 anomaly event(s))
- `website_visitors`: min 13497.0, max 20404.0, average 18096.75 (3 anomaly event(s))
- `warehouse_backlog`: min 526.0, max 1036.0, average 874.75 (3 anomaly event(s))
- `net_revenue`: min 43184.69, max 73424.83, average 59990.245 (1 anomaly event(s))
- `delivery_complaints`: min 26.0, max 79.0, average 64.5 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-043: Logistics disruption incident

- **Date range:** 2024-07-21 to 2024-07-22
- **Severity:** high
- **Affected region:** Midwest
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `refund_spike`, `regional_weather_disruption`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2024-07-21 to 2024-07-22.
- Delivery complaints reached 124.00 versus a prior average of 40.00.

### Affected KPIs

- `refund_rate`: min 0.0429, max 0.0457, average 0.0443 (2 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.1382, max 0.1413, average 0.1397 (2 anomaly event(s))
- `support_ticket_count`: min 260.0, max 278.0, average 269.0 (2 anomaly event(s))
- `warehouse_backlog`: min 960.0, max 1058.0, average 1009.0 (2 anomaly event(s))
- `delivery_complaints`: min 114.0, max 124.0, average 119.0 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-044: Refund spike incident

- **Date range:** 2024-07-26 to 2024-07-28
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** `checkout_failure_spike`, `fraud_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Refund anomalies occurred from 2024-07-26 to 2024-07-28.
- Refund rate reached 0.1322 versus a prior average of 0.0283.

### Affected KPIs

- `checkout_failure_rate`: min 0.0902, max 0.0987, average 0.095 (3 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.1059, max 0.1322, average 0.1218 (3 anomaly event(s))
- `net_revenue`: min 37176.41, max 44468.43, average 40981.0033 (3 anomaly event(s))
- `support_ticket_count`: min 211.0, max 297.0, average 266.3333 (2 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-045: Inventory shortage incident

- **Date range:** 2024-07-31 to 2024-08-01
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `inventory_shortage`, `revenue_drop`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2024-07-31 to 2024-08-01.
- Lost sales units reached 61.00 during the incident.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `stockout_units`: min 381.0, max 438.0, average 409.5 (2 anomaly event(s))
- `net_revenue`: min 38650.38, max 45344.91, average 41997.645 (1 anomaly event(s))
- `lost_sales_units`: min 52.0, max 61.0, average 56.5 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-046: Inventory shortage incident

- **Date range:** 2024-08-05 to 2024-08-07
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `revenue_drop`, `supplier_delay`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2024-08-05 to 2024-08-07.
- Lost sales units reached 121.00 during the incident.

### Affected KPIs

- `stockout_units`: min 473.0, max 484.0, average 476.6667 (3 anomaly event(s))
- `net_revenue`: min 38390.89, max 39891.03, average 39061.1267 (3 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `lost_sales_units`: min 81.0, max 121.0, average 98.3333 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-047: Logistics disruption incident

- **Date range:** 2024-08-09 to 2024-08-11
- **Severity:** critical
- **Affected region:** Midwest
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `refund_spike`, `support_ticket_spike`, `warehouse_backlog_spike`, `warehouse_staffing_shortage`

### Evidence

- Shipping delay anomalies occurred from 2024-08-09 to 2024-08-11.
- Delivery complaints reached 111.00 versus a prior average of 32.29.

### Affected KPIs

- `shipping_delay_rate`: min 0.0731, max 0.1234, average 0.1054 (3 anomaly event(s))
- `support_ticket_count`: min 141.0, max 253.0, average 214.0 (2 anomaly event(s))
- `warehouse_backlog`: min 476.0, max 955.0, average 780.0 (2 anomaly event(s))
- `incident_signal`: min 0.0, max 1.0, average 0.6667 (1 anomaly event(s))
- `refund_rate`: min 0.0294, max 0.0517, average 0.0413 (1 anomaly event(s))
- `delivery_complaints`: min 30.0, max 111.0, average 79.3333 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-048: Logistics disruption incident

- **Date range:** 2024-08-15 to 2024-08-17
- **Severity:** critical
- **Affected region:** West
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `carrier_outage`, `refund_spike`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2024-08-15 to 2024-08-17.
- Delivery complaints reached 122.00 versus a prior average of 42.00.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0495, max 0.0563, average 0.0537 (3 anomaly event(s))
- `shipping_delay_rate`: min 0.1255, max 0.1384, average 0.1303 (3 anomaly event(s))
- `support_ticket_count`: min 225.0, max 273.0, average 249.6667 (2 anomaly event(s))
- `warehouse_backlog`: min 893.0, max 986.0, average 941.3333 (3 anomaly event(s))
- `delivery_complaints`: min 98.0, max 122.0, average 110.0 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-049: Refund spike incident

- **Date range:** 2024-08-20 to 2024-08-21
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success True, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** None

### Evidence

- Refund anomalies occurred from 2024-08-20 to 2024-08-21.
- Refund rate reached 0.1033 versus a prior average of 0.0385.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0979, max 0.1033, average 0.1006 (2 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-050: Revenue Drop Incident

- **Date range:** 2024-08-23 to 2024-08-23
- **Severity:** low
- **Affected region:** All regions
- **Likely cause:** Likely sales impact incident
- **Root cause category:** sales impact
- **Business impact:** Net revenue fell below its normal range during the incident.
- **Resolution:** Reviewed conversion, stockout, refund, and logistics signals before selecting remediation.
- **Outcome:** success True, recovery 3 day(s)
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 event(s) for revenue_drop were grouped within 2024-08-23 to 2024-08-23.

### Affected KPIs

- `net_revenue`: min 41679.26, max 41679.26, average 41679.26 (1 anomaly event(s))

### Recommended Next Steps

- Reviewed conversion, stockout, refund, and logistics signals before selecting remediation.
- Compare the current incident with similar historical incidents before finalizing recommendations.
- Monitor affected metrics until recovery is confirmed.

## INC-051: Checkout Failure Spike Incident

- **Date range:** 2024-08-25 to 2024-08-27
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely platform reliability incident
- **Root cause category:** platform reliability
- **Business impact:** Checkout failures reduced conversion and increased customer contacts.
- **Resolution:** Rolled back the risky checkout change and added checkout health checks.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `api_degradation`, `latency_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- 12 event(s) for checkout_failure_spike were grouped within 2024-08-25 to 2024-08-27.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `checkout_failure_rate`: min 0.0937, max 0.0949, average 0.0943 (3 anomaly event(s))
- `avg_api_latency_ms`: min 474.21, max 478.34, average 476.7 (3 anomaly event(s))
- `net_revenue`: min 31602.73, max 38753.02, average 35483.9133 (3 anomaly event(s))
- `support_ticket_count`: min 247.0, max 267.0, average 255.0 (2 anomaly event(s))

### Recommended Next Steps

- Rolled back the risky checkout change and added checkout health checks.
- Compare the current incident with similar historical incidents before finalizing recommendations.
- Monitor affected metrics until recovery is confirmed.

## INC-052: Demand surge incident

- **Date range:** 2024-08-30 to 2024-08-31
- **Severity:** medium
- **Affected region:** All regions
- **Likely cause:** Likely marketing campaign or holiday demand surge
- **Root cause category:** demand surge
- **Business impact:** Traffic increased quickly, creating capacity and support pressure.
- **Resolution:** Added support coverage and monitored checkout capacity during the traffic surge.
- **Outcome:** success True, recovery 1 day(s)
- **Main anomaly:** `visitor_surge`
- **Related anomalies:** `marketing_campaign_surge`

### Evidence

- Visitor surge anomalies occurred from 2024-08-30 to 2024-08-31.
- Website visitors reached 18407.00 versus a prior average of 15147.64.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `website_visitors`: min 16839.0, max 18407.0, average 17623.0 (2 anomaly event(s))

### Recommended Next Steps

- Confirm whether a campaign, holiday event, or promotion drove the traffic increase.
- Add support coverage and monitor checkout, inventory, and fulfillment capacity.
- Keep successful demand actions active only while service levels remain healthy.

## INC-053: Logistics disruption incident

- **Date range:** 2024-09-04 to 2024-09-06
- **Severity:** critical
- **Affected region:** West
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `holiday_demand_surge`, `visitor_surge`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2024-09-04 to 2024-09-06.
- Delivery complaints reached 72.00 versus a prior average of 30.07.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.1142, max 0.1344, average 0.122 (3 anomaly event(s))
- `website_visitors`: min 16838.0, max 19768.0, average 18464.0 (2 anomaly event(s))
- `warehouse_backlog`: min 820.0, max 1005.0, average 889.3333 (3 anomaly event(s))
- `delivery_complaints`: min 58.0, max 72.0, average 65.0 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-054: Logistics disruption incident

- **Date range:** 2024-09-09 to 2024-09-10
- **Severity:** critical
- **Affected region:** Northeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `refund_spike`, `regional_weather_disruption`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2024-09-09 to 2024-09-10.
- Delivery complaints reached 144.00 versus a prior average of 35.57.

### Affected KPIs

- `refund_rate`: min 0.0389, max 0.0644, average 0.0517 (1 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.1385, max 0.1434, average 0.141 (2 anomaly event(s))
- `support_ticket_count`: min 239.0, max 295.0, average 267.0 (2 anomaly event(s))
- `warehouse_backlog`: min 1011.0, max 1047.0, average 1029.0 (2 anomaly event(s))
- `delivery_complaints`: min 112.0, max 144.0, average 128.0 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-055: Refund spike incident

- **Date range:** 2024-09-14 to 2024-09-16
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** `checkout_failure_spike`, `fraud_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Refund anomalies occurred from 2024-09-14 to 2024-09-16.
- Refund rate reached 0.1312 versus a prior average of 0.0296.

### Affected KPIs

- `checkout_failure_rate`: min 0.0913, max 0.0956, average 0.0941 (3 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.1154, max 0.1312, average 0.1227 (3 anomaly event(s))
- `net_revenue`: min 42638.19, max 43663.95, average 43034.9167 (3 anomaly event(s))
- `support_ticket_count`: min 242.0, max 275.0, average 256.3333 (3 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-056: Inventory shortage incident

- **Date range:** 2024-09-19 to 2024-09-20
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `inventory_shortage`, `revenue_drop`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2024-09-19 to 2024-09-20.
- Lost sales units reached 111.00 during the incident.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `stockout_units`: min 387.0, max 463.0, average 425.0 (2 anomaly event(s))
- `net_revenue`: min 31897.81, max 40320.52, average 36109.165 (2 anomaly event(s))
- `lost_sales_units`: min 90.0, max 111.0, average 100.5 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-057: Inventory shortage incident

- **Date range:** 2024-09-24 to 2024-09-27
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `revenue_drop`, `supplier_delay`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2024-09-24 to 2024-09-27.
- Lost sales units reached 115.00 during the incident.

### Affected KPIs

- `stockout_units`: min 0.0, max 490.0, average 356.0 (3 anomaly event(s))
- `net_revenue`: min 34045.89, max 41656.99, average 37356.7125 (4 anomaly event(s))
- `incident_signal`: min 0.0, max 1.0, average 0.75 (1 anomaly event(s))
- `lost_sales_units`: min 0.0, max 115.0, average 65.0 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-058: Logistics disruption incident

- **Date range:** 2024-09-29 to 2024-10-01
- **Severity:** critical
- **Affected region:** Northeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `latency_spike`, `refund_spike`, `revenue_drop`, `support_ticket_spike`, `warehouse_backlog_spike`, `warehouse_staffing_shortage`

### Evidence

- Shipping delay anomalies occurred from 2024-09-29 to 2024-10-01.
- Delivery complaints reached 120.00 versus a prior average of 26.36.

### Affected KPIs

- `shipping_delay_rate`: min 0.0625, max 0.1328, average 0.1079 (2 anomaly event(s))
- `support_ticket_count`: min 154.0, max 267.0, average 227.0 (2 anomaly event(s))
- `warehouse_backlog`: min 514.0, max 964.0, average 781.6667 (2 anomaly event(s))
- `incident_signal`: min 0.0, max 1.0, average 0.6667 (1 anomaly event(s))
- `refund_rate`: min 0.0365, max 0.0645, average 0.0472 (1 anomaly event(s))
- `net_revenue`: min 34181.76, max 46441.95, average 41311.7933 (1 anomaly event(s))
- `avg_api_latency_ms`: min 208.92, max 217.73, average 212.55 (1 anomaly event(s))
- `delivery_complaints`: min 32.0, max 120.0, average 86.3333 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-059: Logistics disruption incident

- **Date range:** 2024-10-04 to 2024-10-06
- **Severity:** critical
- **Affected region:** Southeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `carrier_outage`, `refund_spike`, `revenue_drop`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2024-10-04 to 2024-10-06.
- Delivery complaints reached 146.00 versus a prior average of 40.21.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.041, max 0.0579, average 0.0514 (2 anomaly event(s))
- `net_revenue`: min 35665.12, max 53053.35, average 46078.32 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.1361, max 0.1408, average 0.138 (3 anomaly event(s))
- `support_ticket_count`: min 282.0, max 290.0, average 286.6667 (3 anomaly event(s))
- `warehouse_backlog`: min 934.0, max 978.0, average 963.0 (3 anomaly event(s))
- `delivery_complaints`: min 114.0, max 146.0, average 130.3333 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-060: Refund spike incident

- **Date range:** 2024-10-09 to 2024-10-10
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success True, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** `support_ticket_spike`

### Evidence

- Refund anomalies occurred from 2024-10-09 to 2024-10-10.
- Refund rate reached 0.1135 versus a prior average of 0.0390.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.1127, max 0.1135, average 0.1131 (2 anomaly event(s))
- `support_ticket_count`: min 196.0, max 267.0, average 231.5 (1 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-061: Checkout Failure Spike Incident

- **Date range:** 2024-10-14 to 2024-10-16
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely platform reliability incident
- **Root cause category:** platform reliability
- **Business impact:** Checkout failures reduced conversion and increased customer contacts.
- **Resolution:** Rolled back the risky checkout change and added checkout health checks.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `api_degradation`, `latency_spike`, `revenue_drop`

### Evidence

- 10 event(s) for checkout_failure_spike were grouped within 2024-10-14 to 2024-10-16.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `checkout_failure_rate`: min 0.094, max 0.0976, average 0.0954 (3 anomaly event(s))
- `avg_api_latency_ms`: min 478.87, max 482.82, average 480.5233 (3 anomaly event(s))
- `net_revenue`: min 37707.92, max 42284.35, average 40699.9967 (3 anomaly event(s))

### Recommended Next Steps

- Rolled back the risky checkout change and added checkout health checks.
- Compare the current incident with similar historical incidents before finalizing recommendations.
- Monitor affected metrics until recovery is confirmed.

## INC-062: Demand surge incident

- **Date range:** 2024-10-18 to 2024-10-20
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely marketing campaign or holiday demand surge
- **Root cause category:** demand surge
- **Business impact:** Traffic increased quickly, creating capacity and support pressure.
- **Resolution:** Added support coverage and monitored checkout capacity during the traffic surge.
- **Outcome:** success True, recovery 2 day(s)
- **Main anomaly:** `visitor_surge`
- **Related anomalies:** `marketing_campaign_surge`, `revenue_drop`

### Evidence

- Visitor surge anomalies occurred from 2024-10-18 to 2024-10-20.
- Website visitors reached 19213.00 versus a prior average of 15308.64.

### Affected KPIs

- `net_revenue`: min 39879.24, max 82854.95, average 64435.6633 (1 anomaly event(s))
- `incident_signal`: min 0.0, max 1.0, average 0.6667 (1 anomaly event(s))
- `website_visitors`: min 14092.0, max 19213.0, average 17300.3333 (2 anomaly event(s))

### Recommended Next Steps

- Confirm whether a campaign, holiday event, or promotion drove the traffic increase.
- Add support coverage and monitor checkout, inventory, and fulfillment capacity.
- Keep successful demand actions active only while service levels remain healthy.

## INC-063: Logistics disruption incident

- **Date range:** 2024-10-24 to 2024-10-26
- **Severity:** critical
- **Affected region:** Southeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `holiday_demand_surge`, `refund_spike`, `support_ticket_spike`, `visitor_surge`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2024-10-24 to 2024-10-26.
- Delivery complaints reached 69.00 versus a prior average of 28.57.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.1335, max 0.1365, average 0.1345 (3 anomaly event(s))
- `website_visitors`: min 17414.0, max 19360.0, average 18672.3333 (1 anomaly event(s))
- `warehouse_backlog`: min 884.0, max 941.0, average 907.6667 (3 anomaly event(s))
- `refund_rate`: min 0.0185, max 0.0382, average 0.0274 (1 anomaly event(s))
- `support_ticket_count`: min 220.0, max 244.0, average 236.0 (2 anomaly event(s))
- `delivery_complaints`: min 63.0, max 69.0, average 65.6667 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-064: Logistics disruption incident

- **Date range:** 2024-10-29 to 2024-10-30
- **Severity:** critical
- **Affected region:** Midwest
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `refund_spike`, `regional_weather_disruption`, `revenue_drop`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2024-10-29 to 2024-10-30.
- Delivery complaints reached 136.00 versus a prior average of 37.14.

### Affected KPIs

- `refund_rate`: min 0.0484, max 0.052, average 0.0502 (2 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.1371, max 0.1537, average 0.1454 (2 anomaly event(s))
- `support_ticket_count`: min 255.0, max 310.0, average 282.5 (2 anomaly event(s))
- `warehouse_backlog`: min 917.0, max 1073.0, average 995.0 (2 anomaly event(s))
- `net_revenue`: min 42291.02, max 51014.2, average 46652.61 (1 anomaly event(s))
- `delivery_complaints`: min 107.0, max 136.0, average 121.5 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-065: Refund spike incident

- **Date range:** 2024-11-03 to 2024-11-05
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** `checkout_failure_spike`, `fraud_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Refund anomalies occurred from 2024-11-03 to 2024-11-05.
- Refund rate reached 0.1081 versus a prior average of 0.0287.

### Affected KPIs

- `checkout_failure_rate`: min 0.0921, max 0.0949, average 0.0937 (3 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.1001, max 0.1081, average 0.1045 (3 anomaly event(s))
- `support_ticket_count`: min 253.0, max 291.0, average 271.0 (3 anomaly event(s))
- `net_revenue`: min 46255.5, max 60670.53, average 55757.4167 (1 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-066: Inventory Shortage Period Incident

- **Date range:** 2024-11-08 to 2024-11-09
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely inventory planning incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `inventory_shortage`

### Evidence

- 3 event(s) for inventory_shortage_period were grouped within 2024-11-08 to 2024-11-09.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `stockout_units`: min 441.0, max 494.0, average 467.5 (2 anomaly event(s))

### Recommended Next Steps

- Transferred inventory from another warehouse and expedited replenishment.
- Compare the current incident with similar historical incidents before finalizing recommendations.
- Monitor affected metrics until recovery is confirmed.

## INC-067: Inventory shortage incident

- **Date range:** 2024-11-13 to 2024-11-15
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `latency_spike`, `revenue_drop`, `supplier_delay`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2024-11-13 to 2024-11-15.
- Lost sales units reached 130.00 during the incident.

### Affected KPIs

- `stockout_units`: min 390.0, max 479.0, average 448.0 (3 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `avg_api_latency_ms`: min 206.62, max 215.61, average 210.3233 (1 anomaly event(s))
- `net_revenue`: min 45045.21, max 58045.64, average 49616.61 (2 anomaly event(s))
- `lost_sales_units`: min 80.0, max 130.0, average 107.6667 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-068: Logistics disruption incident

- **Date range:** 2024-11-18 to 2024-11-19
- **Severity:** critical
- **Affected region:** Midwest
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `support_ticket_spike`, `warehouse_backlog_spike`, `warehouse_staffing_shortage`

### Evidence

- Shipping delay anomalies occurred from 2024-11-18 to 2024-11-19.
- Delivery complaints reached 117.00 versus a prior average of 32.71.

### Affected KPIs

- `shipping_delay_rate`: min 0.1354, max 0.1439, average 0.1396 (2 anomaly event(s))
- `support_ticket_count`: min 237.0, max 283.0, average 260.0 (2 anomaly event(s))
- `warehouse_backlog`: min 974.0, max 1036.0, average 1005.0 (2 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `delivery_complaints`: min 100.0, max 117.0, average 108.5 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-069: Logistics disruption incident

- **Date range:** 2024-11-22 to 2024-11-25
- **Severity:** high
- **Affected region:** West
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `carrier_outage`, `checkout_failure_spike`, `refund_spike`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2024-11-22 to 2024-11-25.
- Delivery complaints reached 122.00 versus a prior average of 42.86.

### Affected KPIs

- `checkout_failure_rate`: min 0.0171, max 0.0208, average 0.0184 (1 anomaly event(s))
- `incident_signal`: min 0.0, max 1.0, average 0.75 (1 anomaly event(s))
- `refund_rate`: min 0.0184, max 0.0459, average 0.0367 (3 anomaly event(s))
- `shipping_delay_rate`: min 0.073, max 0.1379, average 0.118 (3 anomaly event(s))
- `support_ticket_count`: min 163.0, max 288.0, average 240.25 (3 anomaly event(s))
- `warehouse_backlog`: min 572.0, max 1100.0, average 930.75 (3 anomaly event(s))
- `delivery_complaints`: min 33.0, max 122.0, average 94.5 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-070: Refund spike incident

- **Date range:** 2024-11-28 to 2024-11-29
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success True, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** None

### Evidence

- Refund anomalies occurred from 2024-11-28 to 2024-11-29.
- Refund rate reached 0.0928 versus a prior average of 0.0306.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0883, max 0.0928, average 0.0905 (2 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-071: Demand surge incident

- **Date range:** 2024-12-02 to 2024-12-05
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely marketing campaign or holiday demand surge
- **Root cause category:** demand surge
- **Business impact:** Traffic increased quickly, creating capacity and support pressure.
- **Resolution:** Added support coverage and monitored checkout capacity during the traffic surge.
- **Outcome:** success False, recovery 2 day(s)
- **Main anomaly:** `visitor_surge`
- **Related anomalies:** `api_degradation`, `checkout_failure_spike`, `latency_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Visitor surge anomalies occurred from 2024-12-02 to 2024-12-05.
- Website visitors reached 21073.00 versus a prior average of 18803.64.

### Affected KPIs

- `net_revenue`: min 52502.68, max 59240.1, average 56375.2075 (2 anomaly event(s))
- `incident_signal`: min 0.0, max 1.0, average 0.75 (1 anomaly event(s))
- `checkout_failure_rate`: min 0.0185, max 0.0938, average 0.0739 (3 anomaly event(s))
- `avg_api_latency_ms`: min 207.5, max 477.09, average 408.9925 (3 anomaly event(s))
- `support_ticket_count`: min 187.0, max 266.0, average 235.25 (1 anomaly event(s))
- `website_visitors`: min 18659.0, max 21073.0, average 19970.75 (1 anomaly event(s))

### Recommended Next Steps

- Confirm whether a campaign, holiday event, or promotion drove the traffic increase.
- Add support coverage and monitor checkout, inventory, and fulfillment capacity.
- Keep successful demand actions active only while service levels remain healthy.

## INC-072: Demand surge incident

- **Date range:** 2024-12-08 to 2024-12-09
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely marketing campaign or holiday demand surge
- **Root cause category:** demand surge
- **Business impact:** Traffic increased quickly, creating capacity and support pressure.
- **Resolution:** Added support coverage and monitored checkout capacity during the traffic surge.
- **Outcome:** success True, recovery 2 day(s)
- **Main anomaly:** `visitor_surge`
- **Related anomalies:** `marketing_campaign_surge`

### Evidence

- Visitor surge anomalies occurred from 2024-12-08 to 2024-12-09.
- Website visitors reached 23989.00 versus a prior average of 19206.29.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `website_visitors`: min 23057.0, max 23989.0, average 23523.0 (2 anomaly event(s))

### Recommended Next Steps

- Confirm whether a campaign, holiday event, or promotion drove the traffic increase.
- Add support coverage and monitor checkout, inventory, and fulfillment capacity.
- Keep successful demand actions active only while service levels remain healthy.

## INC-073: Logistics disruption incident

- **Date range:** 2024-12-13 to 2024-12-16
- **Severity:** critical
- **Affected region:** West
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `holiday_demand_surge`, `revenue_drop`, `visitor_surge`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2024-12-13 to 2024-12-16.
- Delivery complaints reached 71.00 versus a prior average of 35.29.

### Affected KPIs

- `incident_signal`: min 0.0, max 1.0, average 0.75 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.0734, max 0.1305, average 0.1103 (3 anomaly event(s))
- `warehouse_backlog`: min 659.0, max 960.0, average 875.25 (3 anomaly event(s))
- `website_visitors`: min 18918.0, max 25359.0, average 22810.5 (2 anomaly event(s))
- `net_revenue`: min 59333.94, max 96198.47, average 82439.355 (1 anomaly event(s))
- `delivery_complaints`: min 29.0, max 71.0, average 56.75 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-074: Logistics disruption incident

- **Date range:** 2024-12-18 to 2024-12-19
- **Severity:** critical
- **Affected region:** Northeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `refund_spike`, `regional_weather_disruption`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2024-12-18 to 2024-12-19.
- Delivery complaints reached 148.00 versus a prior average of 42.00.

### Affected KPIs

- `refund_rate`: min 0.0369, max 0.0404, average 0.0387 (2 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.1421, max 0.1499, average 0.146 (2 anomaly event(s))
- `support_ticket_count`: min 299.0, max 327.0, average 313.0 (2 anomaly event(s))
- `warehouse_backlog`: min 1013.0, max 1053.0, average 1033.0 (2 anomaly event(s))
- `delivery_complaints`: min 129.0, max 148.0, average 138.5 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-075: Refund spike incident

- **Date range:** 2024-12-23 to 2024-12-25
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** `checkout_failure_spike`, `fraud_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Refund anomalies occurred from 2024-12-23 to 2024-12-25.
- Refund rate reached 0.1133 versus a prior average of 0.0232.

### Affected KPIs

- `checkout_failure_rate`: min 0.0911, max 0.0957, average 0.0929 (3 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0886, max 0.1133, average 0.0991 (3 anomaly event(s))
- `net_revenue`: min 58103.62, max 75127.96, average 65735.2867 (2 anomaly event(s))
- `support_ticket_count`: min 263.0, max 312.0, average 288.3333 (3 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-076: Inventory shortage incident

- **Date range:** 2024-12-28 to 2024-12-29
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `inventory_shortage`, `revenue_drop`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2024-12-28 to 2024-12-29.
- Lost sales units reached 88.00 during the incident.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `stockout_units`: min 210.0, max 445.0, average 327.5 (2 anomaly event(s))
- `net_revenue`: min 44853.19, max 63202.11, average 54027.65 (2 anomaly event(s))
- `lost_sales_units`: min 84.0, max 88.0, average 86.0 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-077: Inventory shortage incident

- **Date range:** 2025-01-02 to 2025-01-04
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `revenue_drop`, `supplier_delay`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2025-01-02 to 2025-01-04.
- Lost sales units reached 104.00 during the incident.

### Affected KPIs

- `stockout_units`: min 443.0, max 480.0, average 467.6667 (3 anomaly event(s))
- `net_revenue`: min 43180.0, max 58443.31, average 49704.43 (3 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `lost_sales_units`: min 85.0, max 104.0, average 91.6667 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-078: Logistics disruption incident

- **Date range:** 2025-01-07 to 2025-01-08
- **Severity:** critical
- **Affected region:** Northeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `refund_spike`, `support_ticket_spike`, `warehouse_backlog_spike`, `warehouse_staffing_shortage`

### Evidence

- Shipping delay anomalies occurred from 2025-01-07 to 2025-01-08.
- Delivery complaints reached 103.00 versus a prior average of 31.29.

### Affected KPIs

- `refund_rate`: min 0.0398, max 0.0493, average 0.0445 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.1242, max 0.1244, average 0.1243 (2 anomaly event(s))
- `support_ticket_count`: min 256.0, max 262.0, average 259.0 (2 anomaly event(s))
- `warehouse_backlog`: min 872.0, max 964.0, average 918.0 (2 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `delivery_complaints`: min 97.0, max 103.0, average 100.0 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-079: Logistics disruption incident

- **Date range:** 2025-01-12 to 2025-01-14
- **Severity:** critical
- **Affected region:** Southeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `carrier_outage`, `checkout_failure_spike`, `refund_spike`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2025-01-12 to 2025-01-14.
- Delivery complaints reached 126.00 versus a prior average of 40.07.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0412, max 0.0476, average 0.0452 (3 anomaly event(s))
- `shipping_delay_rate`: min 0.1451, max 0.1501, average 0.1474 (3 anomaly event(s))
- `support_ticket_count`: min 266.0, max 299.0, average 284.6667 (3 anomaly event(s))
- `warehouse_backlog`: min 1004.0, max 1033.0, average 1016.6667 (3 anomaly event(s))
- `checkout_failure_rate`: min 0.0167, max 0.0206, average 0.0182 (1 anomaly event(s))
- `delivery_complaints`: min 116.0, max 126.0, average 121.0 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-080: Refund spike incident

- **Date range:** 2025-01-17 to 2025-01-18
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success True, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** None

### Evidence

- Refund anomalies occurred from 2025-01-17 to 2025-01-18.
- Refund rate reached 0.0927 versus a prior average of 0.0327.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0891, max 0.0927, average 0.0909 (2 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-081: Checkout Failure Spike Incident

- **Date range:** 2025-01-22 to 2025-01-24
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely platform reliability incident
- **Root cause category:** platform reliability
- **Business impact:** Checkout failures reduced conversion and increased customer contacts.
- **Resolution:** Rolled back the risky checkout change and added checkout health checks.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `api_degradation`, `latency_spike`, `revenue_drop`

### Evidence

- 9 event(s) for checkout_failure_spike were grouped within 2025-01-22 to 2025-01-24.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `checkout_failure_rate`: min 0.0896, max 0.0969, average 0.0931 (3 anomaly event(s))
- `avg_api_latency_ms`: min 468.85, max 482.64, average 477.0967 (3 anomaly event(s))
- `net_revenue`: min 49253.83, max 54282.66, average 51518.2033 (2 anomaly event(s))

### Recommended Next Steps

- Rolled back the risky checkout change and added checkout health checks.
- Compare the current incident with similar historical incidents before finalizing recommendations.
- Monitor affected metrics until recovery is confirmed.

## INC-082: Demand surge incident

- **Date range:** 2025-01-27 to 2025-01-29
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely marketing campaign or holiday demand surge
- **Root cause category:** demand surge
- **Business impact:** Traffic increased quickly, creating capacity and support pressure.
- **Resolution:** Added support coverage and monitored checkout capacity during the traffic surge.
- **Outcome:** success True, recovery 2 day(s)
- **Main anomaly:** `visitor_surge`
- **Related anomalies:** `marketing_campaign_surge`, `shipping_delay_spike`

### Evidence

- Visitor surge anomalies occurred from 2025-01-27 to 2025-01-29.
- Website visitors reached 23457.00 versus a prior average of 18468.64.

### Affected KPIs

- `incident_signal`: min 0.0, max 1.0, average 0.6667 (1 anomaly event(s))
- `website_visitors`: min 19747.0, max 23457.0, average 21510.0 (2 anomaly event(s))
- `shipping_delay_rate`: min 0.0561, max 0.0698, average 0.0621 (1 anomaly event(s))

### Recommended Next Steps

- Confirm whether a campaign, holiday event, or promotion drove the traffic increase.
- Add support coverage and monitor checkout, inventory, and fulfillment capacity.
- Keep successful demand actions active only while service levels remain healthy.

## INC-083: Logistics disruption incident

- **Date range:** 2025-02-01 to 2025-02-03
- **Severity:** critical
- **Affected region:** Southeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `holiday_demand_surge`, `support_ticket_spike`, `visitor_surge`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2025-02-01 to 2025-02-03.
- Delivery complaints reached 79.00 versus a prior average of 29.36.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.1343, max 0.1367, average 0.1357 (3 anomaly event(s))
- `support_ticket_count`: min 248.0, max 263.0, average 254.0 (2 anomaly event(s))
- `website_visitors`: min 22962.0, max 24590.0, average 23904.0 (2 anomaly event(s))
- `warehouse_backlog`: min 886.0, max 946.0, average 919.3333 (3 anomaly event(s))
- `delivery_complaints`: min 64.0, max 79.0, average 72.0 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-084: Logistics disruption incident

- **Date range:** 2025-02-06 to 2025-02-07
- **Severity:** high
- **Affected region:** Midwest
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `refund_spike`, `regional_weather_disruption`, `revenue_drop`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2025-02-06 to 2025-02-07.
- Delivery complaints reached 139.00 versus a prior average of 40.29.

### Affected KPIs

- `refund_rate`: min 0.0333, max 0.0378, average 0.0355 (2 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.1323, max 0.1389, average 0.1356 (2 anomaly event(s))
- `support_ticket_count`: min 287.0, max 289.0, average 288.0 (2 anomaly event(s))
- `warehouse_backlog`: min 920.0, max 921.0, average 920.5 (2 anomaly event(s))
- `net_revenue`: min 60362.18, max 69562.57, average 64962.375 (1 anomaly event(s))
- `delivery_complaints`: min 115.0, max 139.0, average 127.0 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-085: Refund spike incident

- **Date range:** 2025-02-11 to 2025-02-13
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** `checkout_failure_spike`, `fraud_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Refund anomalies occurred from 2025-02-11 to 2025-02-13.
- Refund rate reached 0.1094 versus a prior average of 0.0223.

### Affected KPIs

- `checkout_failure_rate`: min 0.0946, max 0.0985, average 0.0961 (3 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.091, max 0.1094, average 0.1018 (3 anomaly event(s))
- `net_revenue`: min 48294.4, max 52948.15, average 50904.1633 (3 anomaly event(s))
- `support_ticket_count`: min 246.0, max 273.0, average 260.6667 (1 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-086: Inventory shortage incident

- **Date range:** 2025-02-16 to 2025-02-17
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `inventory_shortage`, `revenue_drop`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2025-02-16 to 2025-02-17.
- Lost sales units reached 106.00 during the incident.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `stockout_units`: min 403.0, max 429.0, average 416.0 (2 anomaly event(s))
- `net_revenue`: min 53773.52, max 62308.45, average 58040.985 (1 anomaly event(s))
- `lost_sales_units`: min 80.0, max 106.0, average 93.0 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-087: Inventory shortage incident

- **Date range:** 2025-02-21 to 2025-02-23
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `revenue_drop`, `supplier_delay`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2025-02-21 to 2025-02-23.
- Lost sales units reached 127.00 during the incident.

### Affected KPIs

- `stockout_units`: min 460.0, max 481.0, average 469.6667 (3 anomaly event(s))
- `net_revenue`: min 46234.14, max 52291.04, average 50090.2833 (3 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `lost_sales_units`: min 76.0, max 127.0, average 103.3333 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-088: Logistics disruption incident

- **Date range:** 2025-02-26 to 2025-02-27
- **Severity:** critical
- **Affected region:** Midwest
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `support_ticket_spike`, `warehouse_backlog_spike`, `warehouse_staffing_shortage`

### Evidence

- Shipping delay anomalies occurred from 2025-02-26 to 2025-02-27.
- Delivery complaints reached 109.00 versus a prior average of 31.64.

### Affected KPIs

- `shipping_delay_rate`: min 0.1261, max 0.1288, average 0.1275 (2 anomaly event(s))
- `support_ticket_count`: min 236.0, max 284.0, average 260.0 (2 anomaly event(s))
- `warehouse_backlog`: min 844.0, max 973.0, average 908.5 (2 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `delivery_complaints`: min 91.0, max 109.0, average 100.0 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-089: Logistics disruption incident

- **Date range:** 2025-03-03 to 2025-03-05
- **Severity:** critical
- **Affected region:** West
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `carrier_outage`, `refund_spike`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2025-03-03 to 2025-03-05.
- Delivery complaints reached 116.00 versus a prior average of 41.36.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0345, max 0.048, average 0.0433 (3 anomaly event(s))
- `shipping_delay_rate`: min 0.1215, max 0.1361, average 0.1267 (3 anomaly event(s))
- `support_ticket_count`: min 252.0, max 280.0, average 264.0 (3 anomaly event(s))
- `warehouse_backlog`: min 941.0, max 1067.0, average 987.6667 (3 anomaly event(s))
- `delivery_complaints`: min 101.0, max 116.0, average 107.6667 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-090: Refund spike incident

- **Date range:** 2025-03-08 to 2025-03-09
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success True, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** None

### Evidence

- Refund anomalies occurred from 2025-03-08 to 2025-03-09.
- Refund rate reached 0.0758 versus a prior average of 0.0297.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0744, max 0.0758, average 0.0751 (2 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-091: Checkout Failure Spike Incident

- **Date range:** 2025-03-13 to 2025-03-15
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely platform reliability incident
- **Root cause category:** platform reliability
- **Business impact:** Checkout failures reduced conversion and increased customer contacts.
- **Resolution:** Rolled back the risky checkout change and added checkout health checks.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `api_degradation`, `latency_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- 11 event(s) for checkout_failure_spike were grouped within 2025-03-13 to 2025-03-15.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `checkout_failure_rate`: min 0.0911, max 0.0965, average 0.0944 (3 anomaly event(s))
- `avg_api_latency_ms`: min 475.11, max 483.84, average 479.0467 (3 anomaly event(s))
- `net_revenue`: min 54559.1, max 65118.26, average 58329.12 (2 anomaly event(s))
- `support_ticket_count`: min 252.0, max 265.0, average 260.0 (2 anomaly event(s))

### Recommended Next Steps

- Rolled back the risky checkout change and added checkout health checks.
- Compare the current incident with similar historical incidents before finalizing recommendations.
- Monitor affected metrics until recovery is confirmed.

## INC-092: Deployment-related checkout incident

- **Date range:** 2025-03-18 to 2025-03-20
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely deployment-related checkout incident
- **Root cause category:** platform reliability
- **Business impact:** Checkout failures reduced conversion and increased customer contacts.
- **Resolution:** Rolled back the risky checkout change and added checkout health checks.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `failed_deployment`, `latency_spike`, `refund_spike`, `revenue_drop`, `support_ticket_spike`, `visitor_surge`

### Evidence

- Latency and checkout failure anomalies occurred together from 2025-03-18 to 2025-03-20.
- 2 failed or rollback deployment event(s) occurred within the investigation window.

### Affected KPIs

- `checkout_failure_rate`: min 0.1017, max 0.1237, average 0.1153 (3 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `avg_api_latency_ms`: min 500.34, max 568.69, average 544.16 (3 anomaly event(s))
- `net_revenue`: min 38129.12, max 54194.29, average 48087.6433 (3 anomaly event(s))
- `support_ticket_count`: min 312.0, max 377.0, average 345.3333 (3 anomaly event(s))
- `website_visitors`: min 20719.0, max 26353.0, average 24255.0 (2 anomaly event(s))
- `refund_rate`: min 0.0388, max 0.0665, average 0.0497 (1 anomaly event(s))
- `conversion_rate`: min 0.0266, max 0.0336, average 0.0307 (0 anomaly event(s))

### Recommended Next Steps

- Review the failed checkout deployment, dependency changes, and rollback results.
- Validate checkout success rate, API latency, and revenue after rollback.
- Add deployment health gates for checkout latency and failure rate.

## INC-093: Logistics disruption incident

- **Date range:** 2025-03-23 to 2025-03-25
- **Severity:** critical
- **Affected region:** West
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `holiday_demand_surge`, `visitor_surge`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2025-03-23 to 2025-03-25.
- Delivery complaints reached 64.00 versus a prior average of 29.43.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.1204, max 0.1265, average 0.1243 (3 anomaly event(s))
- `website_visitors`: min 24919.0, max 27504.0, average 26256.3333 (2 anomaly event(s))
- `warehouse_backlog`: min 914.0, max 984.0, average 954.6667 (3 anomaly event(s))
- `delivery_complaints`: min 56.0, max 64.0, average 59.3333 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-094: Logistics disruption incident

- **Date range:** 2025-03-28 to 2025-03-29
- **Severity:** critical
- **Affected region:** Northeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `refund_spike`, `regional_weather_disruption`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2025-03-28 to 2025-03-29.
- Delivery complaints reached 134.00 versus a prior average of 37.14.

### Affected KPIs

- `refund_rate`: min 0.0308, max 0.0461, average 0.0384 (1 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.1482, max 0.1512, average 0.1497 (2 anomaly event(s))
- `warehouse_backlog`: min 1005.0, max 1012.0, average 1008.5 (2 anomaly event(s))
- `delivery_complaints`: min 130.0, max 134.0, average 132.0 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-095: Refund spike incident

- **Date range:** 2025-04-02 to 2025-04-04
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** `checkout_failure_spike`, `fraud_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Refund anomalies occurred from 2025-04-02 to 2025-04-04.
- Refund rate reached 0.1190 versus a prior average of 0.0284.

### Affected KPIs

- `checkout_failure_rate`: min 0.0915, max 0.0939, average 0.0928 (3 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0846, max 0.119, average 0.0978 (3 anomaly event(s))
- `net_revenue`: min 45973.83, max 72491.98, average 59728.0133 (2 anomaly event(s))
- `support_ticket_count`: min 275.0, max 277.0, average 276.0 (2 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-096: Inventory shortage incident

- **Date range:** 2025-04-07 to 2025-04-08
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `inventory_shortage`, `revenue_drop`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2025-04-07 to 2025-04-08.
- Lost sales units reached 106.00 during the incident.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `stockout_units`: min 441.0, max 455.0, average 448.0 (2 anomaly event(s))
- `net_revenue`: min 54957.88, max 56638.99, average 55798.435 (2 anomaly event(s))
- `lost_sales_units`: min 58.0, max 106.0, average 82.0 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-097: Inventory shortage incident

- **Date range:** 2025-04-10 to 2025-04-20
- **Severity:** critical
- **Affected region:** Northeast
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `inventory_shortage`, `latency_spike`, `refund_spike`, `revenue_drop`, `shipping_delay_spike`, `supplier_delay`, `support_ticket_spike`, `warehouse_backlog_spike`, `warehouse_staffing_shortage`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2025-04-10 to 2025-04-20.
- Lost sales units reached 253.00 during the incident.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (5 anomaly event(s))
- `stockout_units`: min 70.0, max 552.0, average 215.2727 (11 anomaly event(s))
- `net_revenue`: min 33506.1, max 69020.87, average 51450.8864 (6 anomaly event(s))
- `shipping_delay_rate`: min 0.057, max 0.1221, average 0.0724 (2 anomaly event(s))
- `warehouse_backlog`: min 425.0, max 937.0, average 562.2727 (2 anomaly event(s))
- `refund_rate`: min 0.0185, max 0.0479, average 0.0308 (1 anomaly event(s))
- `support_ticket_count`: min 164.0, max 285.0, average 191.9091 (1 anomaly event(s))
- `avg_api_latency_ms`: min 200.09, max 215.95, average 207.0755 (1 anomaly event(s))
- `lost_sales_units`: min 90.0, max 253.0, average 137.4545 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-098: Logistics disruption incident

- **Date range:** 2025-04-22 to 2025-04-24
- **Severity:** critical
- **Affected region:** Southeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `carrier_outage`, `refund_spike`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2025-04-22 to 2025-04-24.
- Delivery complaints reached 124.00 versus a prior average of 39.64.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.1303, max 0.1398, average 0.135 (3 anomaly event(s))
- `support_ticket_count`: min 258.0, max 270.0, average 262.3333 (3 anomaly event(s))
- `warehouse_backlog`: min 912.0, max 947.0, average 930.6667 (3 anomaly event(s))
- `refund_rate`: min 0.0251, max 0.0399, average 0.0324 (1 anomaly event(s))
- `delivery_complaints`: min 99.0, max 124.0, average 113.3333 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-099: Refund spike incident

- **Date range:** 2025-04-27 to 2025-04-28
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success True, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** None

### Evidence

- Refund anomalies occurred from 2025-04-27 to 2025-04-28.
- Refund rate reached 0.0859 versus a prior average of 0.0293.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0809, max 0.0859, average 0.0834 (2 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-100: Logistics disruption incident

- **Date range:** 2025-05-02 to 2025-05-14
- **Severity:** critical
- **Affected region:** Midwest
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `api_degradation`, `checkout_failure_spike`, `holiday_demand_surge`, `latency_spike`, `marketing_campaign_surge`, `revenue_drop`, `shipping_disruption`, `support_ticket_spike`, `visitor_surge`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2025-05-02 to 2025-05-14.
- Delivery complaints reached 176.00 versus a prior average of 53.00.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (5 anomaly event(s))
- `checkout_failure_rate`: min 0.0169, max 0.0979, average 0.036 (3 anomaly event(s))
- `avg_api_latency_ms`: min 204.61, max 482.1, average 269.5138 (3 anomaly event(s))
- `net_revenue`: min 49234.63, max 100695.89, average 71733.6838 (3 anomaly event(s))
- `support_ticket_count`: min 221.0, max 358.0, average 293.0769 (8 anomaly event(s))
- `shipping_delay_rate`: min 0.0562, max 0.2264, average 0.1442 (10 anomaly event(s))
- `warehouse_backlog`: min 417.0, max 1541.0, average 993.3077 (9 anomaly event(s))
- `website_visitors`: min 19429.0, max 28969.0, average 23550.4615 (4 anomaly event(s))
- `delivery_complaints`: min 26.0, max 176.0, average 112.6923 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-101: Refund spike incident

- **Date range:** 2025-05-17 to 2025-05-17
- **Severity:** high
- **Affected region:** Midwest
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success True, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** `regional_weather_disruption`, `revenue_drop`

### Evidence

- Refund anomalies occurred from 2025-05-17 to 2025-05-17.
- Refund rate reached 0.0477 versus a prior average of 0.0256.

### Affected KPIs

- `refund_rate`: min 0.0477, max 0.0477, average 0.0477 (1 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `net_revenue`: min 63625.32, max 63625.32, average 63625.32 (1 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-102: Revenue Drop Incident

- **Date range:** 2025-05-19 to 2025-05-19
- **Severity:** low
- **Affected region:** All regions
- **Likely cause:** Likely sales impact incident
- **Root cause category:** sales impact
- **Business impact:** Net revenue fell below its normal range during the incident.
- **Resolution:** Reviewed conversion, stockout, refund, and logistics signals before selecting remediation.
- **Outcome:** success True, recovery 3 day(s)
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 event(s) for revenue_drop were grouped within 2025-05-19 to 2025-05-19.

### Affected KPIs

- `net_revenue`: min 65676.31, max 65676.31, average 65676.31 (1 anomaly event(s))

### Recommended Next Steps

- Reviewed conversion, stockout, refund, and logistics signals before selecting remediation.
- Compare the current incident with similar historical incidents before finalizing recommendations.
- Monitor affected metrics until recovery is confirmed.

## INC-103: Refund spike incident

- **Date range:** 2025-05-22 to 2025-05-24
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** `checkout_failure_spike`, `fraud_spike`, `revenue_drop`

### Evidence

- Refund anomalies occurred from 2025-05-22 to 2025-05-24.
- Refund rate reached 0.0970 versus a prior average of 0.0253.

### Affected KPIs

- `checkout_failure_rate`: min 0.0935, max 0.0977, average 0.096 (3 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0842, max 0.097, average 0.0923 (3 anomaly event(s))
- `net_revenue`: min 60817.3, max 66887.41, average 63195.4167 (2 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-104: Inventory shortage incident

- **Date range:** 2025-05-26 to 2025-05-28
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `inventory_shortage`, `latency_spike`, `revenue_drop`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2025-05-26 to 2025-05-28.
- Lost sales units reached 106.00 during the incident.

### Affected KPIs

- `avg_api_latency_ms`: min 201.08, max 216.03, average 209.21 (1 anomaly event(s))
- `incident_signal`: min 0.0, max 1.0, average 0.6667 (1 anomaly event(s))
- `stockout_units`: min 0.0, max 410.0, average 238.0 (2 anomaly event(s))
- `net_revenue`: min 60149.65, max 79245.88, average 68508.7267 (1 anomaly event(s))
- `lost_sales_units`: min 0.0, max 106.0, average 70.3333 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-105: Latency Spike Incident

- **Date range:** 2025-05-30 to 2025-05-30
- **Severity:** medium
- **Affected region:** All regions
- **Likely cause:** Likely platform reliability incident
- **Root cause category:** platform reliability
- **Business impact:** API latency slowed checkout and increased support volume.
- **Resolution:** Reduced API latency by rolling back the slow dependency and scaling checkout workers.
- **Outcome:** success True, recovery 2 day(s)
- **Main anomaly:** `latency_spike`
- **Related anomalies:** None

### Evidence

- 1 event(s) for latency_spike were grouped within 2025-05-30 to 2025-05-30.

### Affected KPIs

- `avg_api_latency_ms`: min 217.24, max 217.24, average 217.24 (1 anomaly event(s))

### Recommended Next Steps

- Reduced API latency by rolling back the slow dependency and scaling checkout workers.
- Compare the current incident with similar historical incidents before finalizing recommendations.
- Monitor affected metrics until recovery is confirmed.

## INC-106: Inventory shortage incident

- **Date range:** 2025-06-01 to 2025-06-03
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `revenue_drop`, `supplier_delay`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2025-06-01 to 2025-06-03.
- Lost sales units reached 121.00 during the incident.

### Affected KPIs

- `stockout_units`: min 449.0, max 523.0, average 481.3333 (3 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `net_revenue`: min 45009.21, max 63716.84, average 53468.2667 (2 anomaly event(s))
- `lost_sales_units`: min 72.0, max 121.0, average 102.6667 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-107: Logistics disruption incident

- **Date range:** 2025-06-06 to 2025-06-07
- **Severity:** critical
- **Affected region:** Midwest
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `support_ticket_spike`, `warehouse_backlog_spike`, `warehouse_staffing_shortage`

### Evidence

- Shipping delay anomalies occurred from 2025-06-06 to 2025-06-07.
- Delivery complaints reached 121.00 versus a prior average of 31.14.

### Affected KPIs

- `shipping_delay_rate`: min 0.12, max 0.1266, average 0.1233 (2 anomaly event(s))
- `support_ticket_count`: min 266.0, max 284.0, average 275.0 (2 anomaly event(s))
- `warehouse_backlog`: min 737.0, max 907.0, average 822.0 (2 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `delivery_complaints`: min 117.0, max 121.0, average 119.0 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-108: Logistics disruption incident

- **Date range:** 2025-06-11 to 2025-06-13
- **Severity:** high
- **Affected region:** West
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `carrier_outage`, `refund_spike`, `revenue_drop`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2025-06-11 to 2025-06-13.
- Delivery complaints reached 128.00 versus a prior average of 41.29.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0392, max 0.0442, average 0.0414 (3 anomaly event(s))
- `shipping_delay_rate`: min 0.1185, max 0.1217, average 0.1202 (3 anomaly event(s))
- `support_ticket_count`: min 252.0, max 293.0, average 278.3333 (3 anomaly event(s))
- `warehouse_backlog`: min 890.0, max 941.0, average 912.3333 (3 anomaly event(s))
- `net_revenue`: min 56158.29, max 69859.48, average 64048.97 (1 anomaly event(s))
- `delivery_complaints`: min 101.0, max 128.0, average 119.0 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-109: Refund spike incident

- **Date range:** 2025-06-16 to 2025-06-17
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success True, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** None

### Evidence

- Refund anomalies occurred from 2025-06-16 to 2025-06-17.
- Refund rate reached 0.0735 versus a prior average of 0.0285.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0668, max 0.0735, average 0.0701 (2 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-110: Checkout Failure Spike Incident

- **Date range:** 2025-06-21 to 2025-06-23
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely platform reliability incident
- **Root cause category:** platform reliability
- **Business impact:** Checkout failures reduced conversion and increased customer contacts.
- **Resolution:** Rolled back the risky checkout change and added checkout health checks.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `api_degradation`, `latency_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- 11 event(s) for checkout_failure_spike were grouped within 2025-06-21 to 2025-06-23.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `checkout_failure_rate`: min 0.0875, max 0.0986, average 0.0927 (3 anomaly event(s))
- `avg_api_latency_ms`: min 472.4, max 478.6, average 475.3733 (3 anomaly event(s))
- `net_revenue`: min 43662.18, max 49739.22, average 47008.3333 (3 anomaly event(s))
- `support_ticket_count`: min 236.0, max 263.0, average 247.3333 (1 anomaly event(s))

### Recommended Next Steps

- Rolled back the risky checkout change and added checkout health checks.
- Compare the current incident with similar historical incidents before finalizing recommendations.
- Monitor affected metrics until recovery is confirmed.

## INC-111: Demand surge incident

- **Date range:** 2025-06-26 to 2025-06-26
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely marketing campaign or holiday demand surge
- **Root cause category:** demand surge
- **Business impact:** Traffic increased quickly, creating capacity and support pressure.
- **Resolution:** Added support coverage and monitored checkout capacity during the traffic surge.
- **Outcome:** success True, recovery 2 day(s)
- **Main anomaly:** `visitor_surge`
- **Related anomalies:** `marketing_campaign_surge`

### Evidence

- Visitor surge anomalies occurred from 2025-06-26 to 2025-06-26.
- Website visitors reached 26901.00 versus a prior average of 21874.86.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `website_visitors`: min 26901.0, max 26901.0, average 26901.0 (1 anomaly event(s))

### Recommended Next Steps

- Confirm whether a campaign, holiday event, or promotion drove the traffic increase.
- Add support coverage and monitor checkout, inventory, and fulfillment capacity.
- Keep successful demand actions active only while service levels remain healthy.

## INC-112: Logistics disruption incident

- **Date range:** 2025-07-01 to 2025-07-03
- **Severity:** critical
- **Affected region:** West
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `holiday_demand_surge`, `visitor_surge`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2025-07-01 to 2025-07-03.
- Delivery complaints reached 77.00 versus a prior average of 31.57.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.1093, max 0.1311, average 0.1172 (3 anomaly event(s))
- `website_visitors`: min 26530.0, max 28136.0, average 27402.3333 (2 anomaly event(s))
- `warehouse_backlog`: min 814.0, max 943.0, average 864.3333 (3 anomaly event(s))
- `delivery_complaints`: min 44.0, max 77.0, average 59.3333 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-113: Logistics disruption incident

- **Date range:** 2025-07-06 to 2025-07-07
- **Severity:** critical
- **Affected region:** Northeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `refund_spike`, `regional_weather_disruption`, `revenue_drop`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2025-07-06 to 2025-07-07.
- Delivery complaints reached 115.00 versus a prior average of 35.64.

### Affected KPIs

- `refund_rate`: min 0.0284, max 0.0309, average 0.0297 (2 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.1336, max 0.1428, average 0.1382 (2 anomaly event(s))
- `support_ticket_count`: min 246.0, max 278.0, average 262.0 (2 anomaly event(s))
- `warehouse_backlog`: min 982.0, max 1048.0, average 1015.0 (2 anomaly event(s))
- `net_revenue`: min 58070.76, max 75668.7, average 66869.73 (1 anomaly event(s))
- `delivery_complaints`: min 105.0, max 115.0, average 110.0 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-114: Refund spike incident

- **Date range:** 2025-07-11 to 2025-07-13
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** `checkout_failure_spike`, `fraud_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Refund anomalies occurred from 2025-07-11 to 2025-07-13.
- Refund rate reached 0.1071 versus a prior average of 0.0213.

### Affected KPIs

- `checkout_failure_rate`: min 0.0908, max 0.0998, average 0.0965 (3 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0827, max 0.1071, average 0.0916 (3 anomaly event(s))
- `net_revenue`: min 42956.18, max 63026.86, average 55177.1833 (3 anomaly event(s))
- `support_ticket_count`: min 246.0, max 276.0, average 262.6667 (2 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-115: Inventory Shortage Period Incident

- **Date range:** 2025-07-16 to 2025-07-17
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely inventory planning incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `inventory_shortage`

### Evidence

- 3 event(s) for inventory_shortage_period were grouped within 2025-07-16 to 2025-07-17.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `stockout_units`: min 409.0, max 444.0, average 426.5 (2 anomaly event(s))

### Recommended Next Steps

- Transferred inventory from another warehouse and expedited replenishment.
- Compare the current incident with similar historical incidents before finalizing recommendations.
- Monitor affected metrics until recovery is confirmed.

## INC-116: Latency Spike Incident

- **Date range:** 2025-07-19 to 2025-07-19
- **Severity:** medium
- **Affected region:** All regions
- **Likely cause:** Likely platform reliability incident
- **Root cause category:** platform reliability
- **Business impact:** API latency slowed checkout and increased support volume.
- **Resolution:** Reduced API latency by rolling back the slow dependency and scaling checkout workers.
- **Outcome:** success True, recovery 2 day(s)
- **Main anomaly:** `latency_spike`
- **Related anomalies:** None

### Evidence

- 1 event(s) for latency_spike were grouped within 2025-07-19 to 2025-07-19.

### Affected KPIs

- `avg_api_latency_ms`: min 214.33, max 214.33, average 214.33 (1 anomaly event(s))

### Recommended Next Steps

- Reduced API latency by rolling back the slow dependency and scaling checkout workers.
- Compare the current incident with similar historical incidents before finalizing recommendations.
- Monitor affected metrics until recovery is confirmed.

## INC-117: Inventory shortage incident

- **Date range:** 2025-07-21 to 2025-07-23
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `failed_deployment`, `latency_spike`, `refund_spike`, `revenue_drop`, `supplier_delay`, `support_ticket_spike`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2025-07-21 to 2025-07-23.
- Lost sales units reached 125.00 during the incident.

### Affected KPIs

- `stockout_units`: min 445.0, max 512.0, average 474.6667 (3 anomaly event(s))
- `net_revenue`: min 33031.98, max 45656.65, average 38329.6167 (3 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (2 anomaly event(s))
- `avg_api_latency_ms`: min 206.72, max 310.91, average 250.51 (1 anomaly event(s))
- `refund_rate`: min 0.0341, max 0.0558, average 0.0414 (1 anomaly event(s))
- `support_ticket_count`: min 159.0, max 257.0, average 208.0 (1 anomaly event(s))
- `lost_sales_units`: min 94.0, max 125.0, average 113.0 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-118: Logistics disruption incident

- **Date range:** 2025-07-26 to 2025-07-27
- **Severity:** critical
- **Affected region:** Northeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `support_ticket_spike`, `warehouse_backlog_spike`, `warehouse_staffing_shortage`

### Evidence

- Shipping delay anomalies occurred from 2025-07-26 to 2025-07-27.
- Delivery complaints reached 116.00 versus a prior average of 27.79.

### Affected KPIs

- `shipping_delay_rate`: min 0.1207, max 0.1228, average 0.1217 (2 anomaly event(s))
- `support_ticket_count`: min 254.0, max 286.0, average 270.0 (2 anomaly event(s))
- `warehouse_backlog`: min 803.0, max 868.0, average 835.5 (2 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `delivery_complaints`: min 92.0, max 116.0, average 104.0 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-119: Logistics disruption incident

- **Date range:** 2025-07-31 to 2025-08-02
- **Severity:** critical
- **Affected region:** Southeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `carrier_outage`, `refund_spike`, `revenue_drop`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2025-07-31 to 2025-08-02.
- Delivery complaints reached 134.00 versus a prior average of 39.43.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.1336, max 0.1391, average 0.1359 (3 anomaly event(s))
- `support_ticket_count`: min 263.0, max 299.0, average 283.6667 (3 anomaly event(s))
- `warehouse_backlog`: min 868.0, max 968.0, average 917.3333 (3 anomaly event(s))
- `refund_rate`: min 0.0303, max 0.0463, average 0.0388 (2 anomaly event(s))
- `net_revenue`: min 54774.11, max 73647.55, average 62699.5867 (1 anomaly event(s))
- `delivery_complaints`: min 115.0, max 134.0, average 124.0 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-120: Refund spike incident

- **Date range:** 2025-08-05 to 2025-08-06
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success True, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** None

### Evidence

- Refund anomalies occurred from 2025-08-05 to 2025-08-06.
- Refund rate reached 0.0811 versus a prior average of 0.0287.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0677, max 0.0811, average 0.0744 (2 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-121: Inventory shortage incident

- **Date range:** 2025-08-10 to 2025-08-18
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `api_degradation`, `checkout_failure_spike`, `inventory_shortage`, `latency_spike`, `marketing_campaign_surge`, `revenue_drop`, `support_ticket_spike`, `visitor_surge`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2025-08-10 to 2025-08-18.
- Lost sales units reached 97.00 during the incident.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (4 anomaly event(s))
- `checkout_failure_rate`: min 0.0156, max 0.1009, average 0.044 (3 anomaly event(s))
- `avg_api_latency_ms`: min 205.15, max 475.69, average 295.9956 (3 anomaly event(s))
- `net_revenue`: min 43471.16, max 73461.58, average 57435.6478 (5 anomaly event(s))
- `stockout_units`: min 0.0, max 71.0, average 43.8889 (7 anomaly event(s))
- `support_ticket_count`: min 167.0, max 263.0, average 203.7778 (1 anomaly event(s))
- `website_visitors`: min 19804.0, max 24976.0, average 21781.6667 (1 anomaly event(s))
- `lost_sales_units`: min 0.0, max 97.0, average 63.2222 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-122: Logistics disruption incident

- **Date range:** 2025-08-20 to 2025-08-22
- **Severity:** critical
- **Affected region:** Southeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `holiday_demand_surge`, `visitor_surge`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2025-08-20 to 2025-08-22.
- Delivery complaints reached 70.00 versus a prior average of 31.57.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.1182, max 0.132, average 0.1252 (3 anomaly event(s))
- `website_visitors`: min 24167.0, max 28227.0, average 26332.3333 (2 anomaly event(s))
- `warehouse_backlog`: min 889.0, max 974.0, average 923.3333 (3 anomaly event(s))
- `delivery_complaints`: min 52.0, max 70.0, average 61.3333 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-123: Logistics disruption incident

- **Date range:** 2025-08-25 to 2025-08-26
- **Severity:** critical
- **Affected region:** Midwest
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `refund_spike`, `regional_weather_disruption`, `revenue_drop`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2025-08-25 to 2025-08-26.
- Delivery complaints reached 145.00 versus a prior average of 37.93.

### Affected KPIs

- `refund_rate`: min 0.0333, max 0.0415, average 0.0374 (2 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.1368, max 0.1424, average 0.1396 (2 anomaly event(s))
- `warehouse_backlog`: min 968.0, max 1017.0, average 992.5 (2 anomaly event(s))
- `net_revenue`: min 52906.19, max 68660.61, average 60783.4 (1 anomaly event(s))
- `support_ticket_count`: min 235.0, max 305.0, average 270.0 (1 anomaly event(s))
- `delivery_complaints`: min 106.0, max 145.0, average 125.5 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-124: Refund spike incident

- **Date range:** 2025-08-30 to 2025-09-01
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** `checkout_failure_spike`, `fraud_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Refund anomalies occurred from 2025-08-30 to 2025-09-01.
- Refund rate reached 0.1077 versus a prior average of 0.0227.

### Affected KPIs

- `checkout_failure_rate`: min 0.0934, max 0.0989, average 0.096 (3 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0916, max 0.1077, average 0.0984 (3 anomaly event(s))
- `net_revenue`: min 52517.38, max 61934.71, average 56568.8967 (2 anomaly event(s))
- `support_ticket_count`: min 271.0, max 288.0, average 277.3333 (3 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-125: Inventory shortage incident

- **Date range:** 2025-09-04 to 2025-09-05
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `inventory_shortage`, `revenue_drop`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2025-09-04 to 2025-09-05.
- Lost sales units reached 80.00 during the incident.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `stockout_units`: min 337.0, max 417.0, average 377.0 (2 anomaly event(s))
- `net_revenue`: min 55058.25, max 56604.01, average 55831.13 (2 anomaly event(s))
- `lost_sales_units`: min 63.0, max 80.0, average 71.5 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-126: Inventory shortage incident

- **Date range:** 2025-09-09 to 2025-09-11
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `revenue_drop`, `supplier_delay`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2025-09-09 to 2025-09-11.
- Lost sales units reached 112.00 during the incident.

### Affected KPIs

- `stockout_units`: min 444.0, max 484.0, average 469.0 (3 anomaly event(s))
- `net_revenue`: min 55215.29, max 68456.69, average 60228.0033 (2 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `lost_sales_units`: min 68.0, max 112.0, average 92.0 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-127: Logistics disruption incident

- **Date range:** 2025-09-14 to 2025-09-17
- **Severity:** critical
- **Affected region:** West
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `refund_spike`, `revenue_drop`, `shipping_disruption`, `support_ticket_spike`, `warehouse_backlog_spike`, `warehouse_staffing_shortage`

### Evidence

- Shipping delay anomalies occurred from 2025-09-14 to 2025-09-17.
- Delivery complaints reached 138.00 versus a prior average of 30.00.

### Affected KPIs

- `shipping_delay_rate`: min 0.0709, max 0.1468, average 0.1044 (2 anomaly event(s))
- `support_ticket_count`: min 197.0, max 311.0, average 255.25 (2 anomaly event(s))
- `warehouse_backlog`: min 570.0, max 961.0, average 763.0 (2 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (2 anomaly event(s))
- `refund_rate`: min 0.0222, max 0.0518, average 0.0364 (2 anomaly event(s))
- `net_revenue`: min 56961.75, max 82506.58, average 66840.2625 (1 anomaly event(s))
- `delivery_complaints`: min 66.0, max 138.0, average 99.0 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-128: Logistics disruption incident

- **Date range:** 2025-09-19 to 2025-09-21
- **Severity:** critical
- **Affected region:** West
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `carrier_outage`, `latency_spike`, `refund_spike`, `revenue_drop`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2025-09-19 to 2025-09-21.
- Delivery complaints reached 138.00 versus a prior average of 51.43.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0369, max 0.0597, average 0.0461 (2 anomaly event(s))
- `net_revenue`: min 56379.8, max 69362.7, average 62440.6367 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.1201, max 0.1284, average 0.1233 (3 anomaly event(s))
- `support_ticket_count`: min 292.0, max 315.0, average 302.6667 (3 anomaly event(s))
- `warehouse_backlog`: min 909.0, max 947.0, average 930.6667 (3 anomaly event(s))
- `avg_api_latency_ms`: min 202.08, max 218.52, average 210.7933 (1 anomaly event(s))
- `delivery_complaints`: min 132.0, max 138.0, average 134.3333 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-129: Refund spike incident

- **Date range:** 2025-09-24 to 2025-09-25
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success True, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** None

### Evidence

- Refund anomalies occurred from 2025-09-24 to 2025-09-25.
- Refund rate reached 0.0716 versus a prior average of 0.0314.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0707, max 0.0716, average 0.0711 (2 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-130: Checkout Failure Spike Incident

- **Date range:** 2025-09-29 to 2025-10-01
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely platform reliability incident
- **Root cause category:** platform reliability
- **Business impact:** Checkout failures reduced conversion and increased customer contacts.
- **Resolution:** Rolled back the risky checkout change and added checkout health checks.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `api_degradation`, `latency_spike`, `revenue_drop`

### Evidence

- 9 event(s) for checkout_failure_spike were grouped within 2025-09-29 to 2025-10-01.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `checkout_failure_rate`: min 0.0947, max 0.0956, average 0.0952 (3 anomaly event(s))
- `avg_api_latency_ms`: min 472.45, max 484.06, average 478.8567 (3 anomaly event(s))
- `net_revenue`: min 47486.1, max 57499.27, average 51975.0933 (2 anomaly event(s))

### Recommended Next Steps

- Rolled back the risky checkout change and added checkout health checks.
- Compare the current incident with similar historical incidents before finalizing recommendations.
- Monitor affected metrics until recovery is confirmed.

## INC-131: Demand surge incident

- **Date range:** 2025-10-04 to 2025-10-05
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely marketing campaign or holiday demand surge
- **Root cause category:** demand surge
- **Business impact:** Traffic increased quickly, creating capacity and support pressure.
- **Resolution:** Added support coverage and monitored checkout capacity during the traffic surge.
- **Outcome:** success True, recovery 2 day(s)
- **Main anomaly:** `visitor_surge`
- **Related anomalies:** `marketing_campaign_surge`

### Evidence

- Visitor surge anomalies occurred from 2025-10-04 to 2025-10-05.
- Website visitors reached 26279.00 versus a prior average of 21171.36.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `website_visitors`: min 25495.0, max 26279.0, average 25887.0 (2 anomaly event(s))

### Recommended Next Steps

- Confirm whether a campaign, holiday event, or promotion drove the traffic increase.
- Add support coverage and monitor checkout, inventory, and fulfillment capacity.
- Keep successful demand actions active only while service levels remain healthy.

## INC-132: Deployment-related checkout incident

- **Date range:** 2025-10-08 to 2025-10-11
- **Severity:** critical
- **Affected region:** West
- **Likely cause:** Likely deployment-related checkout incident
- **Root cause category:** platform reliability
- **Business impact:** Checkout failures reduced conversion and increased customer contacts.
- **Resolution:** Rolled back the risky checkout change and added checkout health checks.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `failed_deployment`, `latency_spike`, `refund_spike`, `revenue_drop`, `shipping_delay_spike`, `support_ticket_spike`, `visitor_surge`, `warehouse_backlog_spike`

### Evidence

- Latency and checkout failure anomalies occurred together from 2025-10-08 to 2025-10-11.
- 2 failed or rollback deployment event(s) occurred within the investigation window.

### Affected KPIs

- `checkout_failure_rate`: min 0.0241, max 0.1513, average 0.1079 (3 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `avg_api_latency_ms`: min 232.25, max 662.52, average 519.5025 (3 anomaly event(s))
- `refund_rate`: min 0.0461, max 0.0622, average 0.052 (4 anomaly event(s))
- `net_revenue`: min 33118.28, max 47066.78, average 43031.7125 (4 anomaly event(s))
- `support_ticket_count`: min 355.0, max 459.0, average 411.0 (4 anomaly event(s))
- `shipping_delay_rate`: min 0.0547, max 0.1284, average 0.1077 (3 anomaly event(s))
- `website_visitors`: min 22274.0, max 25825.0, average 24165.75 (1 anomaly event(s))
- `warehouse_backlog`: min 449.0, max 972.0, average 811.25 (3 anomaly event(s))
- `conversion_rate`: min 0.0271, max 0.0354, average 0.0297 (0 anomaly event(s))

### Recommended Next Steps

- Review the failed checkout deployment, dependency changes, and rollback results.
- Validate checkout success rate, API latency, and revenue after rollback.
- Add deployment health gates for checkout latency and failure rate.

## INC-133: Logistics disruption incident

- **Date range:** 2025-10-14 to 2025-10-15
- **Severity:** critical
- **Affected region:** Northeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `refund_spike`, `regional_weather_disruption`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2025-10-14 to 2025-10-15.
- Delivery complaints reached 127.00 versus a prior average of 40.00.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.1368, max 0.147, average 0.1419 (2 anomaly event(s))
- `warehouse_backlog`: min 944.0, max 1019.0, average 981.5 (2 anomaly event(s))
- `refund_rate`: min 0.0259, max 0.0398, average 0.0329 (1 anomaly event(s))
- `delivery_complaints`: min 125.0, max 127.0, average 126.0 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-134: Refund spike incident

- **Date range:** 2025-10-19 to 2025-10-21
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** `checkout_failure_spike`, `fraud_spike`, `revenue_drop`

### Evidence

- Refund anomalies occurred from 2025-10-19 to 2025-10-21.
- Refund rate reached 0.0906 versus a prior average of 0.0311.

### Affected KPIs

- `checkout_failure_rate`: min 0.086, max 0.0947, average 0.0905 (3 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0755, max 0.0906, average 0.0843 (3 anomaly event(s))
- `net_revenue`: min 52214.04, max 67588.7, average 61727.3333 (1 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-135: Inventory shortage incident

- **Date range:** 2025-10-24 to 2025-10-25
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `inventory_shortage`, `revenue_drop`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2025-10-24 to 2025-10-25.
- Lost sales units reached 110.00 during the incident.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `stockout_units`: min 450.0, max 492.0, average 471.0 (2 anomaly event(s))
- `net_revenue`: min 54257.34, max 67822.05, average 61039.695 (1 anomaly event(s))
- `lost_sales_units`: min 54.0, max 110.0, average 82.0 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-136: Inventory shortage incident

- **Date range:** 2025-10-29 to 2025-11-05
- **Severity:** critical
- **Affected region:** Northeast
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `revenue_drop`, `shipping_delay_spike`, `supplier_delay`, `support_ticket_spike`, `visitor_surge`, `warehouse_backlog_spike`, `warehouse_staffing_shortage`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2025-10-29 to 2025-11-05.
- Lost sales units reached 132.00 during the incident.

### Affected KPIs

- `stockout_units`: min 0.0, max 486.0, average 180.25 (3 anomaly event(s))
- `incident_signal`: min 0.0, max 1.0, average 0.625 (2 anomaly event(s))
- `net_revenue`: min 44652.33, max 113860.65, average 78319.5675 (2 anomaly event(s))
- `website_visitors`: min 19227.0, max 26926.0, average 23938.375 (4 anomaly event(s))
- `warehouse_backlog`: min 408.0, max 1036.0, average 646.5 (3 anomaly event(s))
- `shipping_delay_rate`: min 0.0578, max 0.1436, average 0.0845 (2 anomaly event(s))
- `support_ticket_count`: min 134.0, max 286.0, average 193.375 (2 anomaly event(s))
- `lost_sales_units`: min 0.0, max 132.0, average 37.375 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-137: Logistics disruption incident

- **Date range:** 2025-11-08 to 2025-11-10
- **Severity:** critical
- **Affected region:** Southeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `carrier_outage`, `refund_spike`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2025-11-08 to 2025-11-10.
- Delivery complaints reached 131.00 versus a prior average of 41.93.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0292, max 0.0361, average 0.0331 (3 anomaly event(s))
- `shipping_delay_rate`: min 0.1373, max 0.1499, average 0.1446 (3 anomaly event(s))
- `support_ticket_count`: min 271.0, max 297.0, average 287.0 (3 anomaly event(s))
- `warehouse_backlog`: min 1042.0, max 1109.0, average 1077.0 (3 anomaly event(s))
- `delivery_complaints`: min 125.0, max 131.0, average 127.6667 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-138: Refund spike incident

- **Date range:** 2025-11-13 to 2025-11-14
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success True, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** `support_ticket_spike`

### Evidence

- Refund anomalies occurred from 2025-11-13 to 2025-11-14.
- Refund rate reached 0.0657 versus a prior average of 0.0233.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.056, max 0.0657, average 0.0609 (2 anomaly event(s))
- `support_ticket_count`: min 242.0, max 262.0, average 252.0 (1 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-139: Checkout Failure Spike Incident

- **Date range:** 2025-11-18 to 2025-11-20
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely platform reliability incident
- **Root cause category:** platform reliability
- **Business impact:** Checkout failures reduced conversion and increased customer contacts.
- **Resolution:** Rolled back the risky checkout change and added checkout health checks.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `api_degradation`, `latency_spike`, `revenue_drop`

### Evidence

- 9 event(s) for checkout_failure_spike were grouped within 2025-11-18 to 2025-11-20.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `checkout_failure_rate`: min 0.0932, max 0.095, average 0.0942 (3 anomaly event(s))
- `avg_api_latency_ms`: min 468.09, max 475.94, average 471.2067 (3 anomaly event(s))
- `net_revenue`: min 76346.24, max 80707.57, average 78855.0033 (2 anomaly event(s))

### Recommended Next Steps

- Rolled back the risky checkout change and added checkout health checks.
- Compare the current incident with similar historical incidents before finalizing recommendations.
- Monitor affected metrics until recovery is confirmed.

## INC-140: Demand surge incident

- **Date range:** 2025-11-23 to 2025-11-23
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely marketing campaign or holiday demand surge
- **Root cause category:** demand surge
- **Business impact:** Traffic increased quickly, creating capacity and support pressure.
- **Resolution:** Added support coverage and monitored checkout capacity during the traffic surge.
- **Outcome:** success True, recovery 2 day(s)
- **Main anomaly:** `visitor_surge`
- **Related anomalies:** `marketing_campaign_surge`

### Evidence

- Visitor surge anomalies occurred from 2025-11-23 to 2025-11-23.
- Website visitors reached 31702.00 versus a prior average of 25557.29.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `website_visitors`: min 31702.0, max 31702.0, average 31702.0 (1 anomaly event(s))

### Recommended Next Steps

- Confirm whether a campaign, holiday event, or promotion drove the traffic increase.
- Add support coverage and monitor checkout, inventory, and fulfillment capacity.
- Keep successful demand actions active only while service levels remain healthy.

## INC-141: Warehouse backlog incident

- **Date range:** 2025-11-26 to 2025-11-26
- **Severity:** medium
- **Affected region:** All regions
- **Likely cause:** Likely warehouse staffing or fulfillment capacity incident
- **Root cause category:** warehouse labor
- **Business impact:** Warehouse backlog slowed fulfillment and increased logistics pressure.
- **Resolution:** Added temporary warehouse shifts and cleared aged outbound orders first.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `warehouse_backlog_spike`
- **Related anomalies:** `shipping_delay_spike`

### Evidence

- Warehouse backlog anomalies occurred from 2025-11-26 to 2025-11-26.
- Warehouse backlog reached 644.00 versus a prior average of 540.07.

### Affected KPIs

- `shipping_delay_rate`: min 0.0751, max 0.0751, average 0.0751 (1 anomaly event(s))
- `warehouse_backlog`: min 644.0, max 644.0, average 644.0 (1 anomaly event(s))

### Recommended Next Steps

- Add temporary warehouse coverage and clear the oldest outbound orders first.
- Review carrier handoff capacity and staffing schedule gaps.
- Monitor backlog, shipping delay rate, and delivery complaints until recovery.

## INC-142: Logistics disruption incident

- **Date range:** 2025-11-28 to 2025-11-30
- **Severity:** critical
- **Affected region:** Southeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `holiday_demand_surge`, `support_ticket_spike`, `visitor_surge`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2025-11-28 to 2025-11-30.
- Delivery complaints reached 87.00 versus a prior average of 32.21.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.134, max 0.1436, average 0.1375 (3 anomaly event(s))
- `warehouse_backlog`: min 954.0, max 1052.0, average 997.0 (3 anomaly event(s))
- `support_ticket_count`: min 218.0, max 243.0, average 233.0 (1 anomaly event(s))
- `website_visitors`: min 29264.0, max 32872.0, average 31283.0 (2 anomaly event(s))
- `delivery_complaints`: min 66.0, max 87.0, average 74.3333 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-143: Inventory shortage incident

- **Date range:** 2025-12-03 to 2025-12-20
- **Severity:** critical
- **Affected region:** Midwest
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `checkout_failure_spike`, `fraud_spike`, `inventory_shortage`, `latency_spike`, `refund_spike`, `regional_weather_disruption`, `revenue_drop`, `shipping_delay_spike`, `supplier_delay`, `support_ticket_spike`, `visitor_surge`, `warehouse_backlog_spike`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2025-12-03 to 2025-12-20.
- Lost sales units reached 252.00 during the incident.

### Affected KPIs

- `stockout_units`: min 0.0, max 470.0, average 196.5 (17 anomaly event(s))
- `refund_rate`: min 0.0141, max 0.101, average 0.0405 (7 anomaly event(s))
- `incident_signal`: min 0.0, max 1.0, average 0.9444 (5 anomaly event(s))
- `net_revenue`: min 42227.85, max 108794.53, average 61642.6894 (12 anomaly event(s))
- `shipping_delay_rate`: min 0.0579, max 0.1508, average 0.0779 (2 anomaly event(s))
- `support_ticket_count`: min 166.0, max 316.0, average 219.1667 (4 anomaly event(s))
- `warehouse_backlog`: min 476.0, max 1080.0, average 607.0556 (2 anomaly event(s))
- `checkout_failure_rate`: min 0.0166, max 0.098, average 0.031 (4 anomaly event(s))
- `avg_api_latency_ms`: min 201.15, max 214.37, average 206.6861 (1 anomaly event(s))
- `website_visitors`: min 23707.0, max 28756.0, average 26067.0556 (1 anomaly event(s))
- `lost_sales_units`: min 0.0, max 252.0, average 132.6111 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-144: Logistics disruption incident

- **Date range:** 2025-12-23 to 2025-12-24
- **Severity:** critical
- **Affected region:** Midwest
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `support_ticket_spike`, `warehouse_backlog_spike`, `warehouse_staffing_shortage`

### Evidence

- Shipping delay anomalies occurred from 2025-12-23 to 2025-12-24.
- Delivery complaints reached 124.00 versus a prior average of 35.43.

### Affected KPIs

- `shipping_delay_rate`: min 0.1348, max 0.149, average 0.1419 (2 anomaly event(s))
- `support_ticket_count`: min 258.0, max 284.0, average 271.0 (2 anomaly event(s))
- `warehouse_backlog`: min 1003.0, max 1032.0, average 1017.5 (2 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `delivery_complaints`: min 108.0, max 124.0, average 116.0 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-145: Logistics disruption incident

- **Date range:** 2025-12-28 to 2025-12-30
- **Severity:** critical
- **Affected region:** West
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `carrier_outage`, `refund_spike`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2025-12-28 to 2025-12-30.
- Delivery complaints reached 144.00 versus a prior average of 47.07.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0286, max 0.0302, average 0.0292 (3 anomaly event(s))
- `shipping_delay_rate`: min 0.1269, max 0.1517, average 0.1395 (3 anomaly event(s))
- `support_ticket_count`: min 272.0, max 302.0, average 290.0 (3 anomaly event(s))
- `warehouse_backlog`: min 993.0, max 1104.0, average 1064.3333 (3 anomaly event(s))
- `delivery_complaints`: min 122.0, max 144.0, average 129.6667 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-146: Refund spike incident

- **Date range:** 2026-01-02 to 2026-01-03
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success True, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** `latency_spike`

### Evidence

- Refund anomalies occurred from 2026-01-02 to 2026-01-03.
- Refund rate reached 0.0664 versus a prior average of 0.0206.

### Affected KPIs

- `avg_api_latency_ms`: min 208.73, max 211.18, average 209.955 (1 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0636, max 0.0664, average 0.065 (2 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-147: Checkout Failure Spike Incident

- **Date range:** 2026-01-06 to 2026-01-09
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely platform reliability incident
- **Root cause category:** platform reliability
- **Business impact:** Checkout failures reduced conversion and increased customer contacts.
- **Resolution:** Rolled back the risky checkout change and added checkout health checks.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `api_degradation`, `latency_spike`, `revenue_drop`

### Evidence

- 11 event(s) for checkout_failure_spike were grouped within 2026-01-06 to 2026-01-09.

### Affected KPIs

- `checkout_failure_rate`: min 0.0201, max 0.0985, average 0.0761 (4 anomaly event(s))
- `incident_signal`: min 0.0, max 1.0, average 0.75 (1 anomaly event(s))
- `avg_api_latency_ms`: min 199.39, max 481.31, average 409.85 (3 anomaly event(s))
- `net_revenue`: min 50993.38, max 94857.47, average 68348.19 (3 anomaly event(s))

### Recommended Next Steps

- Rolled back the risky checkout change and added checkout health checks.
- Compare the current incident with similar historical incidents before finalizing recommendations.
- Monitor affected metrics until recovery is confirmed.

## INC-148: Demand surge incident

- **Date range:** 2026-01-12 to 2026-01-13
- **Severity:** medium
- **Affected region:** All regions
- **Likely cause:** Likely marketing campaign or holiday demand surge
- **Root cause category:** demand surge
- **Business impact:** Traffic increased quickly, creating capacity and support pressure.
- **Resolution:** Added support coverage and monitored checkout capacity during the traffic surge.
- **Outcome:** success True, recovery 1 day(s)
- **Main anomaly:** `visitor_surge`
- **Related anomalies:** `marketing_campaign_surge`

### Evidence

- Visitor surge anomalies occurred from 2026-01-12 to 2026-01-13.
- Website visitors reached 31565.00 versus a prior average of 25173.14.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `website_visitors`: min 28713.0, max 31565.0, average 30139.0 (1 anomaly event(s))

### Recommended Next Steps

- Confirm whether a campaign, holiday event, or promotion drove the traffic increase.
- Add support coverage and monitor checkout, inventory, and fulfillment capacity.
- Keep successful demand actions active only while service levels remain healthy.

## INC-149: Logistics disruption incident

- **Date range:** 2026-01-17 to 2026-01-19
- **Severity:** critical
- **Affected region:** West
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `holiday_demand_surge`, `visitor_surge`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2026-01-17 to 2026-01-19.
- Delivery complaints reached 61.00 versus a prior average of 32.86.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.1157, max 0.1183, average 0.1169 (3 anomaly event(s))
- `website_visitors`: min 29654.0, max 31788.0, average 30761.3333 (2 anomaly event(s))
- `warehouse_backlog`: min 884.0, max 899.0, average 889.3333 (3 anomaly event(s))
- `delivery_complaints`: min 59.0, max 61.0, average 60.0 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-150: Logistics disruption incident

- **Date range:** 2026-01-22 to 2026-01-23
- **Severity:** critical
- **Affected region:** Northeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `refund_spike`, `regional_weather_disruption`, `revenue_drop`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2026-01-22 to 2026-01-23.
- Delivery complaints reached 130.00 versus a prior average of 38.14.

### Affected KPIs

- `refund_rate`: min 0.0293, max 0.0518, average 0.0406 (2 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `net_revenue`: min 60619.95, max 71747.16, average 66183.555 (2 anomaly event(s))
- `shipping_delay_rate`: min 0.1383, max 0.1441, average 0.1412 (2 anomaly event(s))
- `support_ticket_count`: min 272.0, max 274.0, average 273.0 (2 anomaly event(s))
- `warehouse_backlog`: min 955.0, max 995.0, average 975.0 (2 anomaly event(s))
- `delivery_complaints`: min 118.0, max 130.0, average 124.0 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-151: Deployment-related checkout incident

- **Date range:** 2026-01-27 to 2026-01-29
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely deployment-related checkout incident
- **Root cause category:** platform reliability
- **Business impact:** Checkout failures reduced conversion and increased customer contacts.
- **Resolution:** Rolled back the risky checkout change and added checkout health checks.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `failed_deployment`, `fraud_spike`, `latency_spike`, `refund_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Latency and checkout failure anomalies occurred together from 2026-01-27 to 2026-01-29.
- 2 failed or rollback deployment event(s) occurred within the investigation window.

### Affected KPIs

- `checkout_failure_rate`: min 0.0976, max 0.1491, average 0.1286 (3 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (2 anomaly event(s))
- `avg_api_latency_ms`: min 203.49, max 409.08, average 333.9567 (2 anomaly event(s))
- `refund_rate`: min 0.0787, max 0.1091, average 0.0973 (3 anomaly event(s))
- `net_revenue`: min 48711.3, max 61525.17, average 55634.4433 (3 anomaly event(s))
- `support_ticket_count`: min 257.0, max 385.0, average 332.3333 (2 anomaly event(s))
- `conversion_rate`: min 0.0307, max 0.0337, average 0.0324 (0 anomaly event(s))

### Recommended Next Steps

- Review the failed checkout deployment, dependency changes, and rollback results.
- Validate checkout success rate, API latency, and revenue after rollback.
- Add deployment health gates for checkout latency and failure rate.

## INC-152: Inventory Shortage Period Incident

- **Date range:** 2026-02-01 to 2026-02-02
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely inventory planning incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `inventory_shortage`

### Evidence

- 3 event(s) for inventory_shortage_period were grouped within 2026-02-01 to 2026-02-02.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `stockout_units`: min 372.0, max 445.0, average 408.5 (2 anomaly event(s))

### Recommended Next Steps

- Transferred inventory from another warehouse and expedited replenishment.
- Compare the current incident with similar historical incidents before finalizing recommendations.
- Monitor affected metrics until recovery is confirmed.

## INC-153: Demand surge incident

- **Date range:** 2026-02-04 to 2026-02-04
- **Severity:** low
- **Affected region:** All regions
- **Likely cause:** Likely marketing campaign or holiday demand surge
- **Root cause category:** demand surge
- **Business impact:** Traffic increased quickly, creating capacity and support pressure.
- **Resolution:** Added support coverage and monitored checkout capacity during the traffic surge.
- **Outcome:** success True, recovery 1 day(s)
- **Main anomaly:** `visitor_surge`
- **Related anomalies:** None

### Evidence

- Visitor surge anomalies occurred from 2026-02-04 to 2026-02-04.
- Website visitors reached 27861.00 versus a prior average of 25069.57.

### Affected KPIs

- `website_visitors`: min 27861.0, max 27861.0, average 27861.0 (1 anomaly event(s))

### Recommended Next Steps

- Confirm whether a campaign, holiday event, or promotion drove the traffic increase.
- Add support coverage and monitor checkout, inventory, and fulfillment capacity.
- Keep successful demand actions active only while service levels remain healthy.

## INC-154: Inventory shortage incident

- **Date range:** 2026-02-06 to 2026-02-13
- **Severity:** critical
- **Affected region:** Midwest
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `refund_spike`, `revenue_drop`, `shipping_delay_spike`, `shipping_disruption`, `supplier_delay`, `support_ticket_spike`, `warehouse_backlog_spike`, `warehouse_staffing_shortage`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2026-02-06 to 2026-02-13.
- Lost sales units reached 130.00 during the incident.

### Affected KPIs

- `stockout_units`: min 0.0, max 516.0, average 175.375 (3 anomaly event(s))
- `net_revenue`: min 58116.87, max 75956.0, average 66907.5213 (4 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (4 anomaly event(s))
- `shipping_delay_rate`: min 0.0506, max 0.1899, average 0.1125 (4 anomaly event(s))
- `support_ticket_count`: min 164.0, max 380.0, average 261.75 (4 anomaly event(s))
- `warehouse_backlog`: min 426.0, max 1287.0, average 806.125 (4 anomaly event(s))
- `refund_rate`: min 0.0163, max 0.0567, average 0.0358 (3 anomaly event(s))
- `lost_sales_units`: min 0.0, max 130.0, average 40.25 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-155: Logistics disruption incident

- **Date range:** 2026-02-16 to 2026-02-19
- **Severity:** critical
- **Affected region:** Midwest
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `carrier_outage`, `refund_spike`, `revenue_drop`, `shipping_disruption`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2026-02-16 to 2026-02-19.
- Delivery complaints reached 211.00 versus a prior average of 83.43.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (2 anomaly event(s))
- `refund_rate`: min 0.0418, max 0.0562, average 0.0486 (2 anomaly event(s))
- `net_revenue`: min 58255.31, max 76618.38, average 66297.6275 (2 anomaly event(s))
- `shipping_delay_rate`: min 0.1305, max 0.1864, average 0.168 (3 anomaly event(s))
- `support_ticket_count`: min 300.0, max 404.0, average 365.25 (3 anomaly event(s))
- `warehouse_backlog`: min 878.0, max 1342.0, average 1197.75 (3 anomaly event(s))
- `delivery_complaints`: min 148.0, max 211.0, average 189.5 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-156: Refund spike incident

- **Date range:** 2026-02-21 to 2026-02-22
- **Severity:** medium
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success True, recovery 2 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** None

### Evidence

- Refund anomalies occurred from 2026-02-21 to 2026-02-22.
- Refund rate reached 0.0610 versus a prior average of 0.0384.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0586, max 0.061, average 0.0598 (2 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-157: Checkout Failure Spike Incident

- **Date range:** 2026-02-26 to 2026-02-28
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely platform reliability incident
- **Root cause category:** platform reliability
- **Business impact:** Checkout failures reduced conversion and increased customer contacts.
- **Resolution:** Rolled back the risky checkout change and added checkout health checks.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `api_degradation`, `latency_spike`, `revenue_drop`

### Evidence

- 8 event(s) for checkout_failure_spike were grouped within 2026-02-26 to 2026-02-28.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `checkout_failure_rate`: min 0.0902, max 0.0955, average 0.093 (3 anomaly event(s))
- `avg_api_latency_ms`: min 473.02, max 478.66, average 474.9733 (3 anomaly event(s))
- `net_revenue`: min 64157.9, max 77393.35, average 71201.2067 (1 anomaly event(s))

### Recommended Next Steps

- Rolled back the risky checkout change and added checkout health checks.
- Compare the current incident with similar historical incidents before finalizing recommendations.
- Monitor affected metrics until recovery is confirmed.

## INC-158: Demand surge incident

- **Date range:** 2026-03-03 to 2026-03-04
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely marketing campaign or holiday demand surge
- **Root cause category:** demand surge
- **Business impact:** Traffic increased quickly, creating capacity and support pressure.
- **Resolution:** Added support coverage and monitored checkout capacity during the traffic surge.
- **Outcome:** success True, recovery 2 day(s)
- **Main anomaly:** `visitor_surge`
- **Related anomalies:** `marketing_campaign_surge`

### Evidence

- Visitor surge anomalies occurred from 2026-03-03 to 2026-03-04.
- Website visitors reached 35216.00 versus a prior average of 26517.14.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `website_visitors`: min 34394.0, max 35216.0, average 34805.0 (2 anomaly event(s))

### Recommended Next Steps

- Confirm whether a campaign, holiday event, or promotion drove the traffic increase.
- Add support coverage and monitor checkout, inventory, and fulfillment capacity.
- Keep successful demand actions active only while service levels remain healthy.

## INC-159: Shipping Delay Spike Incident

- **Date range:** 2026-03-06 to 2026-03-06
- **Severity:** medium
- **Affected region:** All regions
- **Likely cause:** Likely logistics incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success True, recovery 3 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** None

### Evidence

- 1 event(s) for shipping_delay_spike were grouped within 2026-03-06 to 2026-03-06.

### Affected KPIs

- `shipping_delay_rate`: min 0.0697, max 0.0697, average 0.0697 (1 anomaly event(s))

### Recommended Next Steps

- Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- Compare the current incident with similar historical incidents before finalizing recommendations.
- Monitor affected metrics until recovery is confirmed.

## INC-160: Logistics disruption incident

- **Date range:** 2026-03-08 to 2026-03-10
- **Severity:** critical
- **Affected region:** Southeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `holiday_demand_surge`, `support_ticket_spike`, `visitor_surge`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2026-03-08 to 2026-03-10.
- Delivery complaints reached 69.00 versus a prior average of 28.64.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.1232, max 0.136, average 0.1313 (3 anomaly event(s))
- `website_visitors`: min 32506.0, max 36058.0, average 34540.3333 (2 anomaly event(s))
- `warehouse_backlog`: min 867.0, max 969.0, average 923.6667 (3 anomaly event(s))
- `support_ticket_count`: min 209.0, max 244.0, average 222.0 (1 anomaly event(s))
- `delivery_complaints`: min 59.0, max 69.0, average 64.6667 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-161: Logistics disruption incident

- **Date range:** 2026-03-13 to 2026-03-14
- **Severity:** high
- **Affected region:** Midwest
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `refund_spike`, `regional_weather_disruption`, `revenue_drop`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2026-03-13 to 2026-03-14.
- Delivery complaints reached 118.00 versus a prior average of 38.00.

### Affected KPIs

- `refund_rate`: min 0.026, max 0.0279, average 0.027 (2 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `net_revenue`: min 85370.24, max 87231.37, average 86300.805 (2 anomaly event(s))
- `shipping_delay_rate`: min 0.1248, max 0.1376, average 0.1312 (2 anomaly event(s))
- `support_ticket_count`: min 266.0, max 286.0, average 276.0 (2 anomaly event(s))
- `warehouse_backlog`: min 893.0, max 927.0, average 910.0 (2 anomaly event(s))
- `delivery_complaints`: min 117.0, max 118.0, average 117.5 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-162: Refund spike incident

- **Date range:** 2026-03-18 to 2026-03-20
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** `checkout_failure_spike`, `fraud_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Refund anomalies occurred from 2026-03-18 to 2026-03-20.
- Refund rate reached 0.0798 versus a prior average of 0.0164.

### Affected KPIs

- `checkout_failure_rate`: min 0.0915, max 0.0959, average 0.093 (3 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0653, max 0.0798, average 0.0722 (3 anomaly event(s))
- `net_revenue`: min 62140.52, max 84241.91, average 74197.4833 (3 anomaly event(s))
- `support_ticket_count`: min 259.0, max 285.0, average 272.0 (3 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-163: Inventory shortage incident

- **Date range:** 2026-03-23 to 2026-03-24
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `inventory_shortage`, `latency_spike`, `revenue_drop`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2026-03-23 to 2026-03-24.
- Lost sales units reached 89.00 during the incident.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `stockout_units`: min 444.0, max 464.0, average 454.0 (2 anomaly event(s))
- `avg_api_latency_ms`: min 204.29, max 212.96, average 208.625 (1 anomaly event(s))
- `net_revenue`: min 65656.64, max 77839.93, average 71748.285 (2 anomaly event(s))
- `lost_sales_units`: min 70.0, max 89.0, average 79.5 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-164: Inventory shortage incident

- **Date range:** 2026-03-28 to 2026-03-30
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `revenue_drop`, `supplier_delay`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2026-03-28 to 2026-03-30.
- Lost sales units reached 79.00 during the incident.

### Affected KPIs

- `stockout_units`: min 437.0, max 492.0, average 466.3333 (3 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `net_revenue`: min 70396.87, max 83604.37, average 77690.4033 (1 anomaly event(s))
- `lost_sales_units`: min 65.0, max 79.0, average 72.0 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-165: Logistics disruption incident

- **Date range:** 2026-04-02 to 2026-04-03
- **Severity:** critical
- **Affected region:** Midwest
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `refund_spike`, `support_ticket_spike`, `warehouse_backlog_spike`, `warehouse_staffing_shortage`

### Evidence

- Shipping delay anomalies occurred from 2026-04-02 to 2026-04-03.
- Delivery complaints reached 112.00 versus a prior average of 32.43.

### Affected KPIs

- `shipping_delay_rate`: min 0.1246, max 0.1282, average 0.1264 (2 anomaly event(s))
- `support_ticket_count`: min 235.0, max 256.0, average 245.5 (2 anomaly event(s))
- `warehouse_backlog`: min 821.0, max 903.0, average 862.0 (2 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0257, max 0.0298, average 0.0278 (1 anomaly event(s))
- `delivery_complaints`: min 107.0, max 112.0, average 109.5 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-166: Logistics disruption incident

- **Date range:** 2026-04-07 to 2026-04-09
- **Severity:** high
- **Affected region:** West
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `carrier_outage`, `refund_spike`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2026-04-07 to 2026-04-09.
- Delivery complaints reached 119.00 versus a prior average of 44.43.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.121, max 0.128, average 0.1254 (3 anomaly event(s))
- `support_ticket_count`: min 258.0, max 285.0, average 267.0 (3 anomaly event(s))
- `warehouse_backlog`: min 898.0, max 966.0, average 924.3333 (3 anomaly event(s))
- `refund_rate`: min 0.0234, max 0.0267, average 0.0254 (2 anomaly event(s))
- `delivery_complaints`: min 105.0, max 119.0, average 110.6667 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-167: Deployment-related checkout incident

- **Date range:** 2026-04-12 to 2026-04-19
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely deployment-related checkout incident
- **Root cause category:** platform reliability
- **Business impact:** Checkout failures reduced conversion and increased customer contacts.
- **Resolution:** Rolled back the risky checkout change and added checkout health checks.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `api_degradation`, `failed_deployment`, `latency_spike`, `refund_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Latency and checkout failure anomalies occurred together from 2026-04-12 to 2026-04-19.
- 2 failed or rollback deployment event(s) occurred within the investigation window.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (3 anomaly event(s))
- `refund_rate`: min 0.0233, max 0.0872, average 0.0557 (7 anomaly event(s))
- `net_revenue`: min 26140.55, max 103679.04, average 56992.1762 (6 anomaly event(s))
- `checkout_failure_rate`: min 0.0183, max 0.2255, average 0.1308 (5 anomaly event(s))
- `avg_api_latency_ms`: min 201.76, max 998.37, average 623.8163 (5 anomaly event(s))
- `support_ticket_count`: min 222.0, max 457.0, average 356.0 (5 anomaly event(s))
- `conversion_rate`: min 0.0155, max 0.0456, average 0.0294 (0 anomaly event(s))

### Recommended Next Steps

- Review the failed checkout deployment, dependency changes, and rollback results.
- Validate checkout success rate, API latency, and revenue after rollback.
- Add deployment health gates for checkout latency and failure rate.

## INC-168: Demand surge incident

- **Date range:** 2026-04-22 to 2026-04-23
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely marketing campaign or holiday demand surge
- **Root cause category:** demand surge
- **Business impact:** Traffic increased quickly, creating capacity and support pressure.
- **Resolution:** Added support coverage and monitored checkout capacity during the traffic surge.
- **Outcome:** success True, recovery 2 day(s)
- **Main anomaly:** `visitor_surge`
- **Related anomalies:** `marketing_campaign_surge`

### Evidence

- Visitor surge anomalies occurred from 2026-04-22 to 2026-04-23.
- Website visitors reached 36934.00 versus a prior average of 28089.29.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `website_visitors`: min 34682.0, max 36934.0, average 35808.0 (2 anomaly event(s))

### Recommended Next Steps

- Confirm whether a campaign, holiday event, or promotion drove the traffic increase.
- Add support coverage and monitor checkout, inventory, and fulfillment capacity.
- Keep successful demand actions active only while service levels remain healthy.

## INC-169: Logistics disruption incident

- **Date range:** 2026-04-27 to 2026-05-03
- **Severity:** critical
- **Affected region:** West
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `holiday_demand_surge`, `refund_spike`, `regional_weather_disruption`, `revenue_drop`, `support_ticket_spike`, `visitor_surge`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2026-04-27 to 2026-05-03.
- Delivery complaints reached 110.00 versus a prior average of 31.43.

### Affected KPIs

- `incident_signal`: min 0.0, max 1.0, average 0.7143 (2 anomaly event(s))
- `shipping_delay_rate`: min 0.0644, max 0.1388, average 0.1089 (5 anomaly event(s))
- `website_visitors`: min 26093.0, max 38104.0, average 31699.2857 (3 anomaly event(s))
- `warehouse_backlog`: min 497.0, max 988.0, average 777.5714 (5 anomaly event(s))
- `net_revenue`: min 79655.36, max 138882.64, average 104285.0371 (3 anomaly event(s))
- `refund_rate`: min 0.0095, max 0.0268, average 0.0187 (1 anomaly event(s))
- `support_ticket_count`: min 171.0, max 254.0, average 218.8571 (1 anomaly event(s))
- `delivery_complaints`: min 39.0, max 110.0, average 69.8571 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-170: Refund spike incident

- **Date range:** 2026-05-07 to 2026-05-10
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** `checkout_failure_spike`, `fraud_spike`, `latency_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Refund anomalies occurred from 2026-05-07 to 2026-05-10.
- Refund rate reached 0.0871 versus a prior average of 0.0171.

### Affected KPIs

- `checkout_failure_rate`: min 0.0185, max 0.1026, average 0.0782 (3 anomaly event(s))
- `incident_signal`: min 0.0, max 1.0, average 0.75 (1 anomaly event(s))
- `refund_rate`: min 0.0131, max 0.0871, average 0.0618 (3 anomaly event(s))
- `net_revenue`: min 58956.71, max 126664.09, average 84064.4325 (3 anomaly event(s))
- `support_ticket_count`: min 177.0, max 259.0, average 231.5 (2 anomaly event(s))
- `avg_api_latency_ms`: min 199.26, max 216.31, average 206.48 (1 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-171: Inventory shortage incident

- **Date range:** 2026-05-12 to 2026-05-13
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `inventory_shortage`, `revenue_drop`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2026-05-12 to 2026-05-13.
- Lost sales units reached 96.00 during the incident.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `stockout_units`: min 356.0, max 423.0, average 389.5 (2 anomaly event(s))
- `net_revenue`: min 72384.05, max 78361.39, average 75372.72 (1 anomaly event(s))
- `lost_sales_units`: min 88.0, max 96.0, average 92.0 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-172: Inventory shortage incident

- **Date range:** 2026-05-17 to 2026-05-30
- **Severity:** critical
- **Affected region:** Southeast
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `carrier_outage`, `checkout_failure_spike`, `inventory_shortage`, `refund_spike`, `revenue_drop`, `shipping_delay_spike`, `supplier_delay`, `support_ticket_spike`, `warehouse_backlog_spike`, `warehouse_staffing_shortage`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2026-05-17 to 2026-05-30.
- Lost sales units reached 133.00 during the incident.

### Affected KPIs

- `stockout_units`: min 87.0, max 474.0, average 182.9286 (14 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (6 anomaly event(s))
- `net_revenue`: min 57487.09, max 89469.0, average 74543.6721 (6 anomaly event(s))
- `shipping_delay_rate`: min 0.0564, max 0.1456, average 0.0903 (6 anomaly event(s))
- `refund_rate`: min 0.0103, max 0.0352, average 0.0237 (5 anomaly event(s))
- `support_ticket_count`: min 166.0, max 296.0, average 219.8571 (5 anomaly event(s))
- `warehouse_backlog`: min 429.0, max 1046.0, average 663.0714 (5 anomaly event(s))
- `checkout_failure_rate`: min 0.0164, max 0.02, average 0.0181 (1 anomaly event(s))
- `lost_sales_units`: min 63.0, max 133.0, average 96.5714 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-173: Refund spike incident

- **Date range:** 2026-06-01 to 2026-06-02
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success True, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** None

### Evidence

- Refund anomalies occurred from 2026-06-01 to 2026-06-02.
- Refund rate reached 0.0663 versus a prior average of 0.0238.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0563, max 0.0663, average 0.0613 (2 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-174: Checkout Failure Spike Incident

- **Date range:** 2026-06-06 to 2026-06-08
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely platform reliability incident
- **Root cause category:** platform reliability
- **Business impact:** Checkout failures reduced conversion and increased customer contacts.
- **Resolution:** Rolled back the risky checkout change and added checkout health checks.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `api_degradation`, `latency_spike`, `revenue_drop`

### Evidence

- 8 event(s) for checkout_failure_spike were grouped within 2026-06-06 to 2026-06-08.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `checkout_failure_rate`: min 0.0957, max 0.0965, average 0.096 (3 anomaly event(s))
- `avg_api_latency_ms`: min 471.08, max 474.97, average 472.43 (3 anomaly event(s))
- `net_revenue`: min 73341.28, max 91849.28, average 82558.1333 (1 anomaly event(s))

### Recommended Next Steps

- Rolled back the risky checkout change and added checkout health checks.
- Compare the current incident with similar historical incidents before finalizing recommendations.
- Monitor affected metrics until recovery is confirmed.

## INC-175: Demand surge incident

- **Date range:** 2026-06-11 to 2026-06-11
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely marketing campaign or holiday demand surge
- **Root cause category:** demand surge
- **Business impact:** Traffic increased quickly, creating capacity and support pressure.
- **Resolution:** Added support coverage and monitored checkout capacity during the traffic surge.
- **Outcome:** success True, recovery 2 day(s)
- **Main anomaly:** `visitor_surge`
- **Related anomalies:** `marketing_campaign_surge`

### Evidence

- Visitor surge anomalies occurred from 2026-06-11 to 2026-06-11.
- Website visitors reached 34576.00 versus a prior average of 28432.21.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `website_visitors`: min 34576.0, max 34576.0, average 34576.0 (1 anomaly event(s))

### Recommended Next Steps

- Confirm whether a campaign, holiday event, or promotion drove the traffic increase.
- Add support coverage and monitor checkout, inventory, and fulfillment capacity.
- Keep successful demand actions active only while service levels remain healthy.

## INC-176: Logistics disruption incident

- **Date range:** 2026-06-15 to 2026-06-19
- **Severity:** critical
- **Affected region:** Southeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `holiday_demand_surge`, `revenue_drop`, `support_ticket_spike`, `visitor_surge`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2026-06-15 to 2026-06-19.
- Delivery complaints reached 78.00 versus a prior average of 30.07.

### Affected KPIs

- `shipping_delay_rate`: min 0.0664, max 0.134, average 0.1046 (4 anomaly event(s))
- `incident_signal`: min 0.0, max 1.0, average 0.6 (1 anomaly event(s))
- `support_ticket_count`: min 155.0, max 242.0, average 208.8 (1 anomaly event(s))
- `website_visitors`: min 25928.0, max 37974.0, average 32790.4 (3 anomaly event(s))
- `warehouse_backlog`: min 519.0, max 946.0, average 753.4 (3 anomaly event(s))
- `net_revenue`: min 88809.38, max 152157.23, average 118777.5 (1 anomaly event(s))
- `delivery_complaints`: min 33.0, max 78.0, average 54.0 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-177: Logistics disruption incident

- **Date range:** 2026-06-21 to 2026-06-28
- **Severity:** critical
- **Affected region:** Northeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `checkout_failure_spike`, `fraud_spike`, `refund_spike`, `regional_weather_disruption`, `revenue_drop`, `shipping_disruption`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2026-06-21 to 2026-06-28.
- Delivery complaints reached 193.00 versus a prior average of 38.00.

### Affected KPIs

- `refund_rate`: min 0.0225, max 0.0887, average 0.047 (7 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (3 anomaly event(s))
- `shipping_delay_rate`: min 0.1091, max 0.2069, average 0.1348 (3 anomaly event(s))
- `support_ticket_count`: min 227.0, max 402.0, average 306.5 (5 anomaly event(s))
- `warehouse_backlog`: min 767.0, max 1383.0, average 958.625 (2 anomaly event(s))
- `net_revenue`: min 72131.12, max 98428.6, average 84614.0363 (6 anomaly event(s))
- `checkout_failure_rate`: min 0.0148, max 0.0981, average 0.0463 (3 anomaly event(s))
- `delivery_complaints`: min 79.0, max 193.0, average 113.625 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-178: Inventory shortage incident

- **Date range:** 2026-07-01 to 2026-07-02
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `inventory_shortage`, `revenue_drop`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2026-07-01 to 2026-07-02.
- Lost sales units reached 99.00 during the incident.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `stockout_units`: min 296.0, max 463.0, average 379.5 (2 anomaly event(s))
- `net_revenue`: min 76910.65, max 88635.26, average 82772.955 (1 anomaly event(s))
- `lost_sales_units`: min 71.0, max 99.0, average 85.0 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-179: Inventory shortage incident

- **Date range:** 2026-07-06 to 2026-07-08
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `revenue_drop`, `supplier_delay`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2026-07-06 to 2026-07-08.
- Lost sales units reached 132.00 during the incident.

### Affected KPIs

- `stockout_units`: min 426.0, max 474.0, average 453.3333 (3 anomaly event(s))
- `net_revenue`: min 66787.01, max 80911.72, average 72803.43 (2 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `lost_sales_units`: min 123.0, max 132.0, average 128.3333 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-180: Logistics disruption incident

- **Date range:** 2026-07-11 to 2026-07-12
- **Severity:** critical
- **Affected region:** Midwest
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `refund_spike`, `support_ticket_spike`, `warehouse_backlog_spike`, `warehouse_staffing_shortage`

### Evidence

- Shipping delay anomalies occurred from 2026-07-11 to 2026-07-12.
- Delivery complaints reached 119.00 versus a prior average of 41.21.

### Affected KPIs

- `shipping_delay_rate`: min 0.1228, max 0.1313, average 0.127 (2 anomaly event(s))
- `support_ticket_count`: min 274.0, max 282.0, average 278.0 (2 anomaly event(s))
- `warehouse_backlog`: min 874.0, max 900.0, average 887.0 (2 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.028, max 0.0315, average 0.0297 (1 anomaly event(s))
- `delivery_complaints`: min 115.0, max 119.0, average 117.0 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-181: Logistics disruption incident

- **Date range:** 2026-07-16 to 2026-07-18
- **Severity:** critical
- **Affected region:** West
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `carrier_outage`, `refund_spike`, `revenue_drop`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2026-07-16 to 2026-07-18.
- Delivery complaints reached 120.00 versus a prior average of 42.71.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0273, max 0.0382, average 0.031 (3 anomaly event(s))
- `shipping_delay_rate`: min 0.1221, max 0.126, average 0.1242 (3 anomaly event(s))
- `support_ticket_count`: min 263.0, max 281.0, average 271.6667 (3 anomaly event(s))
- `warehouse_backlog`: min 907.0, max 974.0, average 947.0 (3 anomaly event(s))
- `net_revenue`: min 71583.94, max 93634.33, average 86248.8767 (1 anomaly event(s))
- `delivery_complaints`: min 111.0, max 120.0, average 114.3333 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-182: Refund spike incident

- **Date range:** 2026-07-21 to 2026-07-22
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success True, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** None

### Evidence

- Refund anomalies occurred from 2026-07-21 to 2026-07-22.
- Refund rate reached 0.0647 versus a prior average of 0.0209.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0489, max 0.0647, average 0.0568 (2 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-183: Checkout Failure Spike Incident

- **Date range:** 2026-07-26 to 2026-07-28
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely platform reliability incident
- **Root cause category:** platform reliability
- **Business impact:** Checkout failures reduced conversion and increased customer contacts.
- **Resolution:** Rolled back the risky checkout change and added checkout health checks.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `api_degradation`, `latency_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- 11 event(s) for checkout_failure_spike were grouped within 2026-07-26 to 2026-07-28.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `checkout_failure_rate`: min 0.0907, max 0.0959, average 0.094 (3 anomaly event(s))
- `avg_api_latency_ms`: min 478.18, max 482.44, average 480.56 (3 anomaly event(s))
- `net_revenue`: min 61622.85, max 79595.19, average 70418.3233 (3 anomaly event(s))
- `support_ticket_count`: min 228.0, max 250.0, average 241.6667 (1 anomaly event(s))

### Recommended Next Steps

- Rolled back the risky checkout change and added checkout health checks.
- Compare the current incident with similar historical incidents before finalizing recommendations.
- Monitor affected metrics until recovery is confirmed.

## INC-184: Demand surge incident

- **Date range:** 2026-07-31 to 2026-08-01
- **Severity:** medium
- **Affected region:** All regions
- **Likely cause:** Likely marketing campaign or holiday demand surge
- **Root cause category:** demand surge
- **Business impact:** Traffic increased quickly, creating capacity and support pressure.
- **Resolution:** Added support coverage and monitored checkout capacity during the traffic surge.
- **Outcome:** success True, recovery 1 day(s)
- **Main anomaly:** `visitor_surge`
- **Related anomalies:** `marketing_campaign_surge`

### Evidence

- Visitor surge anomalies occurred from 2026-07-31 to 2026-08-01.
- Website visitors reached 32358.00 versus a prior average of 28048.07.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `website_visitors`: min 30839.0, max 32358.0, average 31598.5 (1 anomaly event(s))

### Recommended Next Steps

- Confirm whether a campaign, holiday event, or promotion drove the traffic increase.
- Add support coverage and monitor checkout, inventory, and fulfillment capacity.
- Keep successful demand actions active only while service levels remain healthy.

## INC-185: Deployment-related checkout incident

- **Date range:** 2026-08-03 to 2026-08-07
- **Severity:** critical
- **Affected region:** West
- **Likely cause:** Likely deployment-related checkout incident
- **Root cause category:** platform reliability
- **Business impact:** Checkout failures reduced conversion and increased customer contacts.
- **Resolution:** Rolled back the risky checkout change and added checkout health checks.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `failed_deployment`, `holiday_demand_surge`, `latency_spike`, `refund_spike`, `revenue_drop`, `shipping_delay_spike`, `support_ticket_spike`, `visitor_surge`, `warehouse_backlog_spike`

### Evidence

- Latency and checkout failure anomalies occurred together from 2026-08-03 to 2026-08-07.
- 2 failed or rollback deployment event(s) occurred within the investigation window.

### Affected KPIs

- `checkout_failure_rate`: min 0.0157, max 0.0998, average 0.0437 (2 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (2 anomaly event(s))
- `avg_api_latency_ms`: min 201.63, max 514.53, average 304.79 (2 anomaly event(s))
- `refund_rate`: min 0.0132, max 0.0576, average 0.0267 (1 anomaly event(s))
- `net_revenue`: min 49876.26, max 126844.16, average 94422.946 (2 anomaly event(s))
- `support_ticket_count`: min 227.0, max 306.0, average 259.0 (2 anomaly event(s))
- `shipping_delay_rate`: min 0.0551, max 0.1258, average 0.0953 (3 anomaly event(s))
- `website_visitors`: min 25442.0, max 36245.0, average 30907.4 (2 anomaly event(s))
- `warehouse_backlog`: min 465.0, max 945.0, average 733.2 (3 anomaly event(s))
- `conversion_rate`: min 0.026, max 0.0445, average 0.0367 (0 anomaly event(s))

### Recommended Next Steps

- Review the failed checkout deployment, dependency changes, and rollback results.
- Validate checkout success rate, API latency, and revenue after rollback.
- Add deployment health gates for checkout latency and failure rate.

## INC-186: Logistics disruption incident

- **Date range:** 2026-08-10 to 2026-08-11
- **Severity:** critical
- **Affected region:** Northeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `refund_spike`, `regional_weather_disruption`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2026-08-10 to 2026-08-11.
- Delivery complaints reached 129.00 versus a prior average of 36.50.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.1466, max 0.161, average 0.1538 (2 anomaly event(s))
- `warehouse_backlog`: min 1049.0, max 1096.0, average 1072.5 (2 anomaly event(s))
- `refund_rate`: min 0.0248, max 0.0289, average 0.0268 (1 anomaly event(s))
- `support_ticket_count`: min 257.0, max 287.0, average 272.0 (1 anomaly event(s))
- `delivery_complaints`: min 111.0, max 129.0, average 120.0 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-187: Refund spike incident

- **Date range:** 2026-08-14 to 2026-08-17
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** `checkout_failure_spike`, `fraud_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Refund anomalies occurred from 2026-08-14 to 2026-08-17.
- Refund rate reached 0.0718 versus a prior average of 0.0213.

### Affected KPIs

- `net_revenue`: min 72224.91, max 79020.66, average 75993.1075 (3 anomaly event(s))
- `checkout_failure_rate`: min 0.0185, max 0.0962, average 0.0764 (3 anomaly event(s))
- `incident_signal`: min 0.0, max 1.0, average 0.75 (1 anomaly event(s))
- `refund_rate`: min 0.0209, max 0.0718, average 0.0568 (3 anomaly event(s))
- `support_ticket_count`: min 175.0, max 283.0, average 246.25 (1 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-188: Inventory shortage incident

- **Date range:** 2026-08-20 to 2026-08-21
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `inventory_shortage`, `revenue_drop`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2026-08-20 to 2026-08-21.
- Lost sales units reached 102.00 during the incident.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `stockout_units`: min 404.0, max 463.0, average 433.5 (2 anomaly event(s))
- `net_revenue`: min 69357.71, max 70588.34, average 69973.025 (2 anomaly event(s))
- `lost_sales_units`: min 76.0, max 102.0, average 89.0 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-189: Inventory shortage incident

- **Date range:** 2026-08-25 to 2026-08-27
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `revenue_drop`, `supplier_delay`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2026-08-25 to 2026-08-27.
- Lost sales units reached 124.00 during the incident.

### Affected KPIs

- `stockout_units`: min 359.0, max 505.0, average 450.0 (3 anomaly event(s))
- `net_revenue`: min 71312.75, max 79807.49, average 76487.0033 (1 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `lost_sales_units`: min 83.0, max 124.0, average 101.3333 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-190: Logistics disruption incident

- **Date range:** 2026-08-30 to 2026-08-31
- **Severity:** critical
- **Affected region:** Northeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `support_ticket_spike`, `warehouse_backlog_spike`, `warehouse_staffing_shortage`

### Evidence

- Shipping delay anomalies occurred from 2026-08-30 to 2026-08-31.
- Delivery complaints reached 116.00 versus a prior average of 32.79.

### Affected KPIs

- `shipping_delay_rate`: min 0.1188, max 0.1317, average 0.1253 (2 anomaly event(s))
- `support_ticket_count`: min 232.0, max 295.0, average 263.5 (1 anomaly event(s))
- `warehouse_backlog`: min 872.0, max 946.0, average 909.0 (2 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `delivery_complaints`: min 91.0, max 116.0, average 103.5 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-191: Logistics disruption incident

- **Date range:** 2026-09-04 to 2026-09-06
- **Severity:** critical
- **Affected region:** Southeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `carrier_outage`, `refund_spike`, `revenue_drop`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2026-09-04 to 2026-09-06.
- Delivery complaints reached 125.00 versus a prior average of 43.50.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0293, max 0.0373, average 0.0326 (3 anomaly event(s))
- `net_revenue`: min 67109.62, max 94413.72, average 82427.5433 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.1343, max 0.1469, average 0.1411 (3 anomaly event(s))
- `support_ticket_count`: min 260.0, max 306.0, average 283.6667 (3 anomaly event(s))
- `warehouse_backlog`: min 941.0, max 997.0, average 962.0 (3 anomaly event(s))
- `delivery_complaints`: min 116.0, max 125.0, average 121.3333 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-192: Inventory shortage incident

- **Date range:** 2026-09-08 to 2026-09-26
- **Severity:** critical
- **Affected region:** Southeast
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `api_degradation`, `checkout_failure_spike`, `holiday_demand_surge`, `inventory_shortage`, `latency_spike`, `marketing_campaign_surge`, `refund_spike`, `revenue_drop`, `shipping_delay_spike`, `support_ticket_spike`, `visitor_surge`, `warehouse_backlog_spike`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2026-09-08 to 2026-09-26.
- Lost sales units reached 173.00 during the incident.

### Affected KPIs

- `checkout_failure_rate`: min 0.0164, max 0.0972, average 0.0303 (4 anomaly event(s))
- `stockout_units`: min 0.0, max 137.0, average 94.8421 (15 anomaly event(s))
- `incident_signal`: min 0.0, max 1.0, average 0.9474 (7 anomaly event(s))
- `refund_rate`: min 0.0126, max 0.0786, average 0.0272 (3 anomaly event(s))
- `net_revenue`: min 33889.57, max 122302.05, average 72945.0268 (9 anomaly event(s))
- `avg_api_latency_ms`: min 199.92, max 478.48, average 247.2305 (3 anomaly event(s))
- `support_ticket_count`: min 159.0, max 280.0, average 208.4211 (2 anomaly event(s))
- `website_visitors`: min 23949.0, max 33845.0, average 28064.7895 (4 anomaly event(s))
- `shipping_delay_rate`: min 0.0544, max 0.129, average 0.0714 (3 anomaly event(s))
- `warehouse_backlog`: min 423.0, max 967.0, average 547.8421 (3 anomaly event(s))
- `lost_sales_units`: min 0.0, max 173.0, average 108.0 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-193: Logistics disruption incident

- **Date range:** 2026-09-29 to 2026-09-30
- **Severity:** high
- **Affected region:** Midwest
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `refund_spike`, `regional_weather_disruption`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2026-09-29 to 2026-09-30.
- Delivery complaints reached 124.00 versus a prior average of 37.07.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.1249, max 0.1297, average 0.1273 (2 anomaly event(s))
- `support_ticket_count`: min 264.0, max 286.0, average 275.0 (2 anomaly event(s))
- `warehouse_backlog`: min 950.0, max 976.0, average 963.0 (2 anomaly event(s))
- `refund_rate`: min 0.026, max 0.0279, average 0.027 (1 anomaly event(s))
- `delivery_complaints`: min 114.0, max 124.0, average 119.0 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-194: Latency Spike Incident

- **Date range:** 2026-10-02 to 2026-10-02
- **Severity:** medium
- **Affected region:** All regions
- **Likely cause:** Likely platform reliability incident
- **Root cause category:** platform reliability
- **Business impact:** API latency slowed checkout and increased support volume.
- **Resolution:** Reduced API latency by rolling back the slow dependency and scaling checkout workers.
- **Outcome:** success True, recovery 2 day(s)
- **Main anomaly:** `latency_spike`
- **Related anomalies:** None

### Evidence

- 1 event(s) for latency_spike were grouped within 2026-10-02 to 2026-10-02.

### Affected KPIs

- `avg_api_latency_ms`: min 213.3, max 213.3, average 213.3 (1 anomaly event(s))

### Recommended Next Steps

- Reduced API latency by rolling back the slow dependency and scaling checkout workers.
- Compare the current incident with similar historical incidents before finalizing recommendations.
- Monitor affected metrics until recovery is confirmed.

## INC-195: Inventory shortage incident

- **Date range:** 2026-10-04 to 2026-10-17
- **Severity:** critical
- **Affected region:** Northeast
- **Likely cause:** Likely inventory shortage incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `checkout_failure_spike`, `fraud_spike`, `inventory_shortage`, `refund_spike`, `revenue_drop`, `shipping_delay_spike`, `shipping_disruption`, `supplier_delay`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2026-10-04 to 2026-10-17.
- Lost sales units reached 78.00 during the incident.

### Affected KPIs

- `checkout_failure_rate`: min 0.0157, max 0.0935, average 0.0334 (3 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (6 anomaly event(s))
- `refund_rate`: min 0.0232, max 0.0928, average 0.0423 (4 anomaly event(s))
- `net_revenue`: min 54237.15, max 102917.38, average 74411.2071 (9 anomaly event(s))
- `support_ticket_count`: min 271.0, max 443.0, average 322.7143 (3 anomaly event(s))
- `shipping_delay_rate`: min 0.0652, max 0.2117, average 0.1899 (9 anomaly event(s))
- `warehouse_backlog`: min 556.0, max 1451.0, average 1330.9286 (9 anomaly event(s))
- `stockout_units`: min 0.0, max 477.0, average 160.4286 (5 anomaly event(s))
- `lost_sales_units`: min 0.0, max 78.0, average 24.5 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-196: Warehouse Staffing Shortage Incident

- **Date range:** 2026-10-19 to 2026-10-19
- **Severity:** medium
- **Affected region:** Midwest
- **Likely cause:** Likely warehouse labor incident
- **Root cause category:** warehouse labor
- **Business impact:** Warehouse staffing gaps increased backlog and delayed shipments.
- **Resolution:** Added temporary warehouse shifts and cleared aged outbound orders first.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `warehouse_staffing_shortage`
- **Related anomalies:** None

### Evidence

- 1 event(s) for warehouse_staffing_shortage were grouped within 2026-10-19 to 2026-10-19.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))

### Recommended Next Steps

- Added temporary warehouse shifts and cleared aged outbound orders first.
- Compare the current incident with similar historical incidents before finalizing recommendations.
- Monitor affected metrics until recovery is confirmed.

## INC-197: Carrier Outage Incident

- **Date range:** 2026-10-24 to 2026-10-24
- **Severity:** medium
- **Affected region:** West
- **Likely cause:** Likely carrier reliability incident
- **Root cause category:** carrier reliability
- **Business impact:** Carrier capacity dropped, shipping delays increased, and delivery complaints rose.
- **Resolution:** Rerouted affected shipments to backup carriers and upgraded priority orders.
- **Outcome:** success True, recovery 3 day(s)
- **Main anomaly:** `carrier_outage`
- **Related anomalies:** None

### Evidence

- 1 event(s) for carrier_outage were grouped within 2026-10-24 to 2026-10-24.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))

### Recommended Next Steps

- Rerouted affected shipments to backup carriers and upgraded priority orders.
- Compare the current incident with similar historical incidents before finalizing recommendations.
- Monitor affected metrics until recovery is confirmed.

## INC-198: Refund spike incident

- **Date range:** 2026-10-29 to 2026-10-30
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success True, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** None

### Evidence

- Refund anomalies occurred from 2026-10-29 to 2026-10-30.
- Refund rate reached 0.0676 versus a prior average of 0.0254.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0661, max 0.0676, average 0.0668 (2 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-199: Demand surge incident

- **Date range:** 2026-11-01 to 2026-11-01
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely marketing campaign or holiday demand surge
- **Root cause category:** demand surge
- **Business impact:** Traffic increased quickly, creating capacity and support pressure.
- **Resolution:** Added support coverage and monitored checkout capacity during the traffic surge.
- **Outcome:** success True, recovery 2 day(s)
- **Main anomaly:** `visitor_surge`
- **Related anomalies:** None

### Evidence

- Visitor surge anomalies occurred from 2026-11-01 to 2026-11-01.
- Website visitors reached 32966.00 versus a prior average of 27240.86.

### Affected KPIs

- `website_visitors`: min 32966.0, max 32966.0, average 32966.0 (1 anomaly event(s))

### Recommended Next Steps

- Confirm whether a campaign, holiday event, or promotion drove the traffic increase.
- Add support coverage and monitor checkout, inventory, and fulfillment capacity.
- Keep successful demand actions active only while service levels remain healthy.

## INC-200: Demand surge incident

- **Date range:** 2026-11-03 to 2026-11-05
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely marketing campaign or holiday demand surge
- **Root cause category:** demand surge
- **Business impact:** Traffic increased quickly, creating capacity and support pressure.
- **Resolution:** Added support coverage and monitored checkout capacity during the traffic surge.
- **Outcome:** success False, recovery 2 day(s)
- **Main anomaly:** `visitor_surge`
- **Related anomalies:** `api_degradation`, `checkout_failure_spike`, `latency_spike`, `support_ticket_spike`

### Evidence

- Visitor surge anomalies occurred from 2026-11-03 to 2026-11-05.
- Website visitors reached 34336.00 versus a prior average of 27981.14.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `checkout_failure_rate`: min 0.0942, max 0.0978, average 0.0956 (3 anomaly event(s))
- `avg_api_latency_ms`: min 474.58, max 481.46, average 477.51 (3 anomaly event(s))
- `support_ticket_count`: min 232.0, max 284.0, average 253.6667 (1 anomaly event(s))
- `website_visitors`: min 32671.0, max 34336.0, average 33614.0 (2 anomaly event(s))

### Recommended Next Steps

- Confirm whether a campaign, holiday event, or promotion drove the traffic increase.
- Add support coverage and monitor checkout, inventory, and fulfillment capacity.
- Keep successful demand actions active only while service levels remain healthy.

## INC-201: Demand surge incident

- **Date range:** 2026-11-08 to 2026-11-09
- **Severity:** medium
- **Affected region:** All regions
- **Likely cause:** Likely marketing campaign or holiday demand surge
- **Root cause category:** demand surge
- **Business impact:** Traffic increased quickly, creating capacity and support pressure.
- **Resolution:** Added support coverage and monitored checkout capacity during the traffic surge.
- **Outcome:** success True, recovery 1 day(s)
- **Main anomaly:** `visitor_surge`
- **Related anomalies:** `marketing_campaign_surge`

### Evidence

- Visitor surge anomalies occurred from 2026-11-08 to 2026-11-09.
- Website visitors reached 39674.00 versus a prior average of 29856.00.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `website_visitors`: min 37271.0, max 39674.0, average 38472.5 (2 anomaly event(s))

### Recommended Next Steps

- Confirm whether a campaign, holiday event, or promotion drove the traffic increase.
- Add support coverage and monitor checkout, inventory, and fulfillment capacity.
- Keep successful demand actions active only while service levels remain healthy.

## INC-202: Deployment-related checkout incident

- **Date range:** 2026-11-12 to 2026-11-19
- **Severity:** critical
- **Affected region:** West
- **Likely cause:** Likely deployment-related checkout incident
- **Root cause category:** platform reliability
- **Business impact:** Checkout failures reduced conversion and increased customer contacts.
- **Resolution:** Rolled back the risky checkout change and added checkout health checks.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `failed_deployment`, `holiday_demand_surge`, `latency_spike`, `refund_spike`, `revenue_drop`, `shipping_delay_spike`, `support_ticket_spike`, `visitor_surge`, `warehouse_backlog_spike`

### Evidence

- Latency and checkout failure anomalies occurred together from 2026-11-12 to 2026-11-19.
- 2 failed or rollback deployment event(s) occurred within the investigation window.

### Affected KPIs

- `net_revenue`: min 49393.45, max 176087.29, average 97082.5925 (5 anomaly event(s))
- `incident_signal`: min 0.0, max 1.0, average 0.875 (2 anomaly event(s))
- `shipping_delay_rate`: min 0.0574, max 0.1525, average 0.1074 (5 anomaly event(s))
- `warehouse_backlog`: min 435.0, max 1119.0, average 815.375 (5 anomaly event(s))
- `support_ticket_count`: min 165.0, max 462.0, average 305.75 (5 anomaly event(s))
- `website_visitors`: min 30175.0, max 41166.0, average 34874.625 (2 anomaly event(s))
- `checkout_failure_rate`: min 0.015, max 0.1392, average 0.0674 (4 anomaly event(s))
- `avg_api_latency_ms`: min 204.69, max 623.27, average 383.2688 (3 anomaly event(s))
- `refund_rate`: min 0.0061, max 0.0523, average 0.0283 (4 anomaly event(s))
- `conversion_rate`: min 0.0235, max 0.0492, average 0.0355 (0 anomaly event(s))

### Recommended Next Steps

- Review the failed checkout deployment, dependency changes, and rollback results.
- Validate checkout success rate, API latency, and revenue after rollback.
- Add deployment health gates for checkout latency and failure rate.

## INC-203: Refund spike incident

- **Date range:** 2026-11-23 to 2026-11-25
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** `checkout_failure_spike`, `fraud_spike`, `revenue_drop`

### Evidence

- Refund anomalies occurred from 2026-11-23 to 2026-11-25.
- Refund rate reached 0.0666 versus a prior average of 0.0220.

### Affected KPIs

- `checkout_failure_rate`: min 0.0931, max 0.0944, average 0.0938 (3 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0522, max 0.0666, average 0.0587 (3 anomaly event(s))
- `net_revenue`: min 93780.24, max 110102.73, average 100204.2 (1 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-204: Inventory Shortage Period Incident

- **Date range:** 2026-11-28 to 2026-11-29
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely inventory planning incident
- **Root cause category:** inventory planning
- **Business impact:** Stockouts created lost sales and customer complaints.
- **Resolution:** Transferred inventory from another warehouse and expedited replenishment.
- **Outcome:** success True, recovery 4 day(s)
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `inventory_shortage`

### Evidence

- 3 event(s) for inventory_shortage_period were grouped within 2026-11-28 to 2026-11-29.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `stockout_units`: min 423.0, max 439.0, average 431.0 (2 anomaly event(s))

### Recommended Next Steps

- Transferred inventory from another warehouse and expedited replenishment.
- Compare the current incident with similar historical incidents before finalizing recommendations.
- Monitor affected metrics until recovery is confirmed.

## INC-205: Demand surge incident

- **Date range:** 2026-12-01 to 2026-12-05
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely marketing campaign or holiday demand surge
- **Root cause category:** demand surge
- **Business impact:** Traffic increased quickly, creating capacity and support pressure.
- **Resolution:** Added support coverage and monitored checkout capacity during the traffic surge.
- **Outcome:** success False, recovery 2 day(s)
- **Main anomaly:** `visitor_surge`
- **Related anomalies:** `inventory_shortage_period`, `latency_spike`, `supplier_delay`

### Evidence

- Visitor surge anomalies occurred from 2026-12-01 to 2026-12-05.
- Website visitors reached 36393.00 versus a prior average of 32336.79.

### Affected KPIs

- `website_visitors`: min 29985.0, max 36393.0, average 33674.6 (2 anomaly event(s))
- `stockout_units`: min 0.0, max 495.0, average 288.4 (3 anomaly event(s))
- `incident_signal`: min 0.0, max 1.0, average 0.6 (1 anomaly event(s))
- `avg_api_latency_ms`: min 207.1, max 217.26, average 211.174 (1 anomaly event(s))

### Recommended Next Steps

- Confirm whether a campaign, holiday event, or promotion drove the traffic increase.
- Add support coverage and monitor checkout, inventory, and fulfillment capacity.
- Keep successful demand actions active only while service levels remain healthy.

## INC-206: Logistics disruption incident

- **Date range:** 2026-12-08 to 2026-12-09
- **Severity:** critical
- **Affected region:** Northeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `refund_spike`, `support_ticket_spike`, `warehouse_backlog_spike`, `warehouse_staffing_shortage`

### Evidence

- Shipping delay anomalies occurred from 2026-12-08 to 2026-12-09.
- Delivery complaints reached 126.00 versus a prior average of 33.64.

### Affected KPIs

- `shipping_delay_rate`: min 0.139, max 0.1395, average 0.1393 (2 anomaly event(s))
- `support_ticket_count`: min 247.0, max 286.0, average 266.5 (2 anomaly event(s))
- `warehouse_backlog`: min 976.0, max 1025.0, average 1000.5 (2 anomaly event(s))
- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0229, max 0.0253, average 0.0241 (1 anomaly event(s))
- `delivery_complaints`: min 101.0, max 126.0, average 113.5 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-207: Logistics disruption incident

- **Date range:** 2026-12-13 to 2026-12-15
- **Severity:** critical
- **Affected region:** Southeast
- **Likely cause:** Likely logistics disruption incident
- **Root cause category:** logistics
- **Business impact:** Shipping delays increased delivery complaints and delayed order completion.
- **Resolution:** Rerouted affected orders through backup carriers and prioritized delayed deliveries.
- **Outcome:** success False, recovery 4 day(s)
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `carrier_outage`, `refund_spike`, `support_ticket_spike`, `warehouse_backlog_spike`

### Evidence

- Shipping delay anomalies occurred from 2026-12-13 to 2026-12-15.
- Delivery complaints reached 142.00 versus a prior average of 43.93.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0175, max 0.0232, average 0.0203 (2 anomaly event(s))
- `shipping_delay_rate`: min 0.1435, max 0.1588, average 0.1489 (3 anomaly event(s))
- `support_ticket_count`: min 274.0, max 293.0, average 285.0 (3 anomaly event(s))
- `warehouse_backlog`: min 1017.0, max 1211.0, average 1088.0 (3 anomaly event(s))
- `delivery_complaints`: min 127.0, max 142.0, average 135.6667 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-208: Refund spike incident

- **Date range:** 2026-12-18 to 2026-12-19
- **Severity:** high
- **Affected region:** All regions
- **Likely cause:** Likely refund, billing, or fraud incident
- **Root cause category:** returns and fraud
- **Business impact:** Refunds increased and reduced net revenue.
- **Resolution:** Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.
- **Outcome:** success True, recovery 3 day(s)
- **Main anomaly:** `refund_spike`
- **Related anomalies:** None

### Evidence

- Refund anomalies occurred from 2026-12-18 to 2026-12-19.
- Refund rate reached 0.0561 versus a prior average of 0.0161.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `refund_rate`: min 0.0493, max 0.0561, average 0.0527 (2 anomaly event(s))

### Recommended Next Steps

- Review refund reasons, billing changes, fraud decisions, and recent delivery problems.
- Prioritize customer outreach for confirmed billing or fraud issues.
- Monitor refund rate and net revenue until both recover.

## INC-209: Checkout Failure Spike Incident

- **Date range:** 2026-12-23 to 2026-12-25
- **Severity:** critical
- **Affected region:** All regions
- **Likely cause:** Likely platform reliability incident
- **Root cause category:** platform reliability
- **Business impact:** Checkout failures reduced conversion and increased customer contacts.
- **Resolution:** Rolled back the risky checkout change and added checkout health checks.
- **Outcome:** success False, recovery 3 day(s)
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `api_degradation`, `latency_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- 11 event(s) for checkout_failure_spike were grouped within 2026-12-23 to 2026-12-25.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `checkout_failure_rate`: min 0.0871, max 0.0943, average 0.0908 (3 anomaly event(s))
- `avg_api_latency_ms`: min 472.41, max 479.43, average 475.19 (3 anomaly event(s))
- `net_revenue`: min 76380.61, max 98929.19, average 89333.2433 (3 anomaly event(s))
- `support_ticket_count`: min 248.0, max 283.0, average 260.0 (1 anomaly event(s))

### Recommended Next Steps

- Rolled back the risky checkout change and added checkout health checks.
- Compare the current incident with similar historical incidents before finalizing recommendations.
- Monitor affected metrics until recovery is confirmed.

## INC-210: Demand surge incident

- **Date range:** 2026-12-28 to 2026-12-29
- **Severity:** medium
- **Affected region:** All regions
- **Likely cause:** Likely marketing campaign or holiday demand surge
- **Root cause category:** demand surge
- **Business impact:** Traffic increased quickly, creating capacity and support pressure.
- **Resolution:** Added support coverage and monitored checkout capacity during the traffic surge.
- **Outcome:** success True, recovery 1 day(s)
- **Main anomaly:** `visitor_surge`
- **Related anomalies:** `marketing_campaign_surge`

### Evidence

- Visitor surge anomalies occurred from 2026-12-28 to 2026-12-29.
- Website visitors reached 43128.00 versus a prior average of 34215.07.

### Affected KPIs

- `incident_signal`: min 1.0, max 1.0, average 1.0 (1 anomaly event(s))
- `website_visitors`: min 39974.0, max 43128.0, average 41551.0 (2 anomaly event(s))

### Recommended Next Steps

- Confirm whether a campaign, holiday event, or promotion drove the traffic increase.
- Add support coverage and monitor checkout, inventory, and fulfillment capacity.
- Keep successful demand actions active only while service levels remain healthy.
