# Deterministic Investigation Summary

Generated from anomaly events grouped with a maximum consecutive-event gap of 3 days.
Total incidents: **22**

## INC-001: Revenue Drop

- **Date range:** 2025-01-11 to 2025-01-13
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** `support_ticket_spike`

### Evidence

- 2 anomaly event(s) across 2 anomaly type(s) were grouped within 2025-01-11 to 2025-01-13.

### Affected KPIs

- `support_ticket_count`: min 207.0, max 245.0, average 226.3333 (1 anomaly event(s))
- `net_revenue`: min 29037.88, max 44616.21, average 37991.8067 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-002: Shipping Delay Spike

- **Date range:** 2025-01-18 to 2025-01-18
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-01-18 to 2025-01-18.

### Affected KPIs

- `shipping_delay_rate`: min 0.0625, max 0.0625, average 0.0625 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-003: Shipping Delay Spike

- **Date range:** 2025-01-28 to 2025-01-29
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `latency_spike`, `revenue_drop`

### Evidence

- 3 anomaly event(s) across 3 anomaly type(s) were grouped within 2025-01-28 to 2025-01-29.

### Affected KPIs

- `net_revenue`: min 30984.02, max 39783.46, average 35383.74 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.0586, max 0.0668, average 0.0627 (1 anomaly event(s))
- `avg_api_latency_ms`: min 203.34, max 217.04, average 210.19 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-004: Revenue Drop

- **Date range:** 2025-02-03 to 2025-02-06
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 3 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-02-03 to 2025-02-06.

### Affected KPIs

- `net_revenue`: min 36129.82, max 41125.49, average 37628.2775 (3 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-005: Revenue Drop

- **Date range:** 2025-02-10 to 2025-02-10
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-02-10 to 2025-02-10.

### Affected KPIs

- `net_revenue`: min 34349.44, max 34349.44, average 34349.44 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-006: Shipping Delay Spike

- **Date range:** 2025-02-16 to 2025-02-16
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-02-16 to 2025-02-16.

### Affected KPIs

- `shipping_delay_rate`: min 0.0665, max 0.0665, average 0.0665 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-007: Latency Spike

- **Date range:** 2025-02-26 to 2025-02-27
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `latency_spike`
- **Related anomalies:** `revenue_drop`

### Evidence

- 2 anomaly event(s) across 2 anomaly type(s) were grouped within 2025-02-26 to 2025-02-27.

### Affected KPIs

- `net_revenue`: min 34952.84, max 40115.58, average 37534.21 (1 anomaly event(s))
- `avg_api_latency_ms`: min 207.7, max 215.53, average 211.615 (1 anomaly event(s))

### Recommended Next Steps

- Inspect service latency by endpoint and dependency.
- Confirm latency has returned to its rolling baseline.

## INC-008: Revenue Drop

- **Date range:** 2025-03-03 to 2025-03-03
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-03-03 to 2025-03-03.

### Affected KPIs

- `net_revenue`: min 31591.65, max 31591.65, average 31591.65 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-009: Revenue Drop

- **Date range:** 2025-03-10 to 2025-03-10
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-03-10 to 2025-03-10.

### Affected KPIs

- `net_revenue`: min 34297.12, max 34297.12, average 34297.12 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-010: Deployment-related checkout incident

- **Date range:** 2025-03-17 to 2025-03-20
- **Likely cause:** Likely deployment-related checkout incident
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `latency_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Latency and checkout failure anomalies occurred together from 2025-03-17 to 2025-03-20.
- 2 failed or rollback deployment event(s) occurred within the investigation window.

### Affected KPIs

- `net_revenue`: min 24647.18, max 34897.68, average 29282.99 (4 anomaly event(s))
- `checkout_failure_rate`: min 0.0183, max 0.1182, average 0.0877 (3 anomaly event(s))
- `avg_api_latency_ms`: min 208.4, max 571.63, average 465.1325 (3 anomaly event(s))
- `support_ticket_count`: min 194.0, max 327.0, average 288.25 (3 anomaly event(s))
- `conversion_rate`: min 0.0306, max 0.042, average 0.0348 (0 anomaly event(s))

### Recommended Next Steps

- Review the failed checkout deployment, dependency changes, and rollback results.
- Validate checkout success rate, API latency, and revenue after rollback.
- Add deployment health gates for checkout latency and failure rate.

## INC-011: Revenue Drop

- **Date range:** 2025-03-24 to 2025-03-24
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-03-24 to 2025-03-24.

### Affected KPIs

- `net_revenue`: min 34307.74, max 34307.74, average 34307.74 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-012: Shipping Delay Spike

- **Date range:** 2025-03-31 to 2025-04-02
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `revenue_drop`

### Evidence

- 2 anomaly event(s) across 2 anomaly type(s) were grouped within 2025-03-31 to 2025-04-02.

### Affected KPIs

- `shipping_delay_rate`: min 0.0455, max 0.0637, average 0.0531 (1 anomaly event(s))
- `net_revenue`: min 34539.62, max 37954.57, average 36803.73 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-013: Inventory shortage incident

- **Date range:** 2025-04-07 to 2025-04-20
- **Likely cause:** Likely inventory shortage incident
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `checkout_failure_spike`, `revenue_drop`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2025-04-07 to 2025-04-20.
- Lost sales units reached 147.00 during the incident.

### Affected KPIs

- `net_revenue`: min 33270.91, max 58995.53, average 41755.4057 (5 anomaly event(s))
- `stockout_units`: min 0.0, max 101.0, average 71.3571 (11 anomaly event(s))
- `checkout_failure_rate`: min 0.0165, max 0.02, average 0.0184 (1 anomaly event(s))
- `lost_sales_units`: min 0.0, max 147.0, average 89.8571 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-014: Shipping Delay Spike

- **Date range:** 2025-04-24 to 2025-04-24
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-04-24 to 2025-04-24.

### Affected KPIs

- `shipping_delay_rate`: min 0.0647, max 0.0647, average 0.0647 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-015: Logistics disruption incident

- **Date range:** 2025-05-05 to 2025-05-13
- **Likely cause:** Likely logistics disruption incident
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `latency_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Shipping delay anomalies occurred from 2025-05-05 to 2025-05-13.
- Delivery complaints reached 136.00 versus a prior average of 25.00.

### Affected KPIs

- `avg_api_latency_ms`: min 198.13, max 215.35, average 206.6178 (1 anomaly event(s))
- `net_revenue`: min 32417.94, max 62436.16, average 44318.9144 (4 anomaly event(s))
- `shipping_delay_rate`: min 0.1104, max 0.121, average 0.1154 (8 anomaly event(s))
- `support_ticket_count`: min 319.0, max 354.0, average 337.5556 (8 anomaly event(s))
- `delivery_complaints`: min 116.0, max 136.0, average 124.6667 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-016: Revenue Drop

- **Date range:** 2025-05-19 to 2025-05-19
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-05-19 to 2025-05-19.

### Affected KPIs

- `net_revenue`: min 34245.79, max 34245.79, average 34245.79 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-017: Checkout Failure Spike

- **Date range:** 2025-05-26 to 2025-05-27
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `revenue_drop`

### Evidence

- 2 anomaly event(s) across 2 anomaly type(s) were grouped within 2025-05-26 to 2025-05-27.

### Affected KPIs

- `net_revenue`: min 36336.94, max 42217.36, average 39277.15 (1 anomaly event(s))
- `checkout_failure_rate`: min 0.0184, max 0.0205, average 0.0195 (1 anomaly event(s))

### Recommended Next Steps

- Inspect checkout errors and dependency health for the incident window.
- Confirm checkout failure rate and revenue have returned to baseline.

## INC-018: Shipping Delay Spike

- **Date range:** 2025-06-02 to 2025-06-03
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `revenue_drop`

### Evidence

- 2 anomaly event(s) across 2 anomaly type(s) were grouped within 2025-06-02 to 2025-06-03.

### Affected KPIs

- `shipping_delay_rate`: min 0.0591, max 0.0623, average 0.0607 (1 anomaly event(s))
- `net_revenue`: min 37305.23, max 48238.32, average 42771.775 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-019: Revenue Drop

- **Date range:** 2025-06-09 to 2025-06-10
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 2 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-06-09 to 2025-06-10.

### Affected KPIs

- `net_revenue`: min 37135.8, max 37239.99, average 37187.895 (2 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-020: Checkout Failure Spike

- **Date range:** 2025-06-16 to 2025-06-18
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `revenue_drop`

### Evidence

- 4 anomaly event(s) across 2 anomaly type(s) were grouped within 2025-06-16 to 2025-06-18.

### Affected KPIs

- `net_revenue`: min 38313.77, max 39772.37, average 39013.12 (3 anomaly event(s))
- `checkout_failure_rate`: min 0.0183, max 0.0216, average 0.0197 (1 anomaly event(s))

### Recommended Next Steps

- Inspect checkout errors and dependency health for the incident window.
- Confirm checkout failure rate and revenue have returned to baseline.

## INC-021: Shipping Delay Spike

- **Date range:** 2025-06-23 to 2025-06-23
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `revenue_drop`

### Evidence

- 2 anomaly event(s) across 2 anomaly type(s) were grouped within 2025-06-23 to 2025-06-23.

### Affected KPIs

- `net_revenue`: min 34631.3, max 34631.3, average 34631.3 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.0628, max 0.0628, average 0.0628 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-022: Latency Spike

- **Date range:** 2025-06-28 to 2025-06-28
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `latency_spike`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-06-28 to 2025-06-28.

### Affected KPIs

- `avg_api_latency_ms`: min 220.13, max 220.13, average 220.13 (1 anomaly event(s))

### Recommended Next Steps

- Inspect service latency by endpoint and dependency.
- Confirm latency has returned to its rolling baseline.
