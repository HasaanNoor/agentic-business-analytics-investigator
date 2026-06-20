# Deterministic Investigation Summary

Generated from anomaly events grouped with a maximum consecutive-event gap of 3 days.
Total incidents: **73**

## INC-001: Checkout Failure Spike

- **Date range:** 2025-01-13 to 2025-01-14
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `revenue_drop`

### Evidence

- 2 anomaly event(s) across 2 anomaly type(s) were grouped within 2025-01-13 to 2025-01-14.

### Affected KPIs

- `net_revenue`: min 33287.06, max 33841.42, average 33564.24 (1 anomaly event(s))
- `checkout_failure_rate`: min 0.0168, max 0.0193, average 0.0181 (1 anomaly event(s))

### Recommended Next Steps

- Inspect checkout errors and dependency health for the incident window.
- Confirm checkout failure rate and revenue have returned to baseline.

## INC-002: Latency Spike

- **Date range:** 2025-01-19 to 2025-01-23
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `latency_spike`
- **Related anomalies:** `revenue_drop`

### Evidence

- 3 anomaly event(s) across 2 anomaly type(s) were grouped within 2025-01-19 to 2025-01-23.

### Affected KPIs

- `avg_api_latency_ms`: min 200.26, max 217.63, average 208.364 (2 anomaly event(s))
- `net_revenue`: min 33487.56, max 44872.66, average 38936.93 (1 anomaly event(s))

### Recommended Next Steps

- Inspect service latency by endpoint and dependency.
- Confirm latency has returned to its rolling baseline.

## INC-003: Revenue Drop

- **Date range:** 2025-02-03 to 2025-02-05
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** `support_ticket_spike`

### Evidence

- 3 anomaly event(s) across 2 anomaly type(s) were grouped within 2025-02-03 to 2025-02-05.

### Affected KPIs

- `net_revenue`: min 28278.3, max 40761.57, average 34540.5133 (2 anomaly event(s))
- `support_ticket_count`: min 200.0, max 251.0, average 223.6667 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-004: Revenue Drop

- **Date range:** 2025-02-10 to 2025-02-10
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-02-10 to 2025-02-10.

### Affected KPIs

- `net_revenue`: min 29305.58, max 29305.58, average 29305.58 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-005: Shipping Delay Spike

- **Date range:** 2025-02-16 to 2025-02-16
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-02-16 to 2025-02-16.

### Affected KPIs

- `shipping_delay_rate`: min 0.0639, max 0.0639, average 0.0639 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-006: Shipping Delay Spike

- **Date range:** 2025-02-20 to 2025-02-20
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-02-20 to 2025-02-20.

### Affected KPIs

- `shipping_delay_rate`: min 0.0653, max 0.0653, average 0.0653 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-007: Latency Spike

- **Date range:** 2025-02-24 to 2025-02-25
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `latency_spike`
- **Related anomalies:** `revenue_drop`

### Evidence

- 3 anomaly event(s) across 2 anomaly type(s) were grouped within 2025-02-24 to 2025-02-25.

### Affected KPIs

- `avg_api_latency_ms`: min 208.72, max 214.95, average 211.835 (1 anomaly event(s))
- `net_revenue`: min 30915.47, max 33807.57, average 32361.52 (2 anomaly event(s))

### Recommended Next Steps

- Inspect service latency by endpoint and dependency.
- Confirm latency has returned to its rolling baseline.

## INC-008: Deployment-related checkout incident

- **Date range:** 2025-03-18 to 2025-03-20
- **Likely cause:** Likely deployment-related checkout incident
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `latency_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Latency and checkout failure anomalies occurred together from 2025-03-18 to 2025-03-20.
- 2 failed or rollback deployment event(s) occurred within the investigation window.

### Affected KPIs

- `checkout_failure_rate`: min 0.1025, max 0.1225, average 0.1155 (3 anomaly event(s))
- `avg_api_latency_ms`: min 501.8, max 567.73, average 545.4 (3 anomaly event(s))
- `net_revenue`: min 22534.46, max 27479.75, average 24871.9033 (3 anomaly event(s))
- `support_ticket_count`: min 279.0, max 316.0, average 294.3333 (3 anomaly event(s))
- `conversion_rate`: min 0.0265, max 0.0302, average 0.0285 (0 anomaly event(s))

### Recommended Next Steps

- Review the failed checkout deployment, dependency changes, and rollback results.
- Validate checkout success rate, API latency, and revenue after rollback.
- Add deployment health gates for checkout latency and failure rate.

## INC-009: Revenue Drop

- **Date range:** 2025-03-24 to 2025-03-24
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-03-24 to 2025-03-24.

### Affected KPIs

- `net_revenue`: min 31951.38, max 31951.38, average 31951.38 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-010: Revenue Drop

- **Date range:** 2025-03-31 to 2025-03-31
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-03-31 to 2025-03-31.

### Affected KPIs

- `net_revenue`: min 32283.12, max 32283.12, average 32283.12 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-011: Inventory shortage incident

- **Date range:** 2025-04-07 to 2025-04-20
- **Likely cause:** Likely inventory shortage incident
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `revenue_drop`, `shipping_delay_spike`, `support_ticket_spike`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2025-04-07 to 2025-04-20.
- Lost sales units reached 126.00 during the incident.

### Affected KPIs

- `net_revenue`: min 32658.99, max 45561.81, average 38989.2836 (5 anomaly event(s))
- `stockout_units`: min 0.0, max 102.0, average 69.7857 (11 anomaly event(s))
- `support_ticket_count`: min 194.0, max 298.0, average 261.5 (4 anomaly event(s))
- `shipping_delay_rate`: min 0.0461, max 0.0677, average 0.0553 (2 anomaly event(s))
- `lost_sales_units`: min 0.0, max 126.0, average 79.7143 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-012: Logistics disruption incident

- **Date range:** 2025-05-05 to 2025-05-12
- **Likely cause:** Likely logistics disruption incident
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `revenue_drop`, `support_ticket_spike`

### Evidence

- Shipping delay anomalies occurred from 2025-05-05 to 2025-05-12.
- Delivery complaints reached 146.00 versus a prior average of 23.79.

### Affected KPIs

- `net_revenue`: min 33658.84, max 55220.59, average 45183.8275 (2 anomaly event(s))
- `shipping_delay_rate`: min 0.1124, max 0.1304, average 0.1192 (7 anomaly event(s))
- `support_ticket_count`: min 317.0, max 357.0, average 337.625 (6 anomaly event(s))
- `delivery_complaints`: min 113.0, max 146.0, average 122.25 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-013: Revenue Drop

- **Date range:** 2025-05-19 to 2025-05-19
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-05-19 to 2025-05-19.

### Affected KPIs

- `net_revenue`: min 36181.01, max 36181.01, average 36181.01 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-014: Revenue Drop

- **Date range:** 2025-05-26 to 2025-05-26
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-05-26 to 2025-05-26.

### Affected KPIs

- `net_revenue`: min 40662.61, max 40662.61, average 40662.61 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-015: Latency Spike

- **Date range:** 2025-06-01 to 2025-06-01
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `latency_spike`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-06-01 to 2025-06-01.

### Affected KPIs

- `avg_api_latency_ms`: min 215.23, max 215.23, average 215.23 (1 anomaly event(s))

### Recommended Next Steps

- Inspect service latency by endpoint and dependency.
- Confirm latency has returned to its rolling baseline.

## INC-016: Checkout Failure Spike

- **Date range:** 2025-06-09 to 2025-06-15
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `latency_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- 5 anomaly event(s) across 4 anomaly type(s) were grouped within 2025-06-09 to 2025-06-15.

### Affected KPIs

- `checkout_failure_rate`: min 0.0156, max 0.0201, average 0.0179 (1 anomaly event(s))
- `net_revenue`: min 40503.66, max 56096.21, average 47896.0486 (2 anomaly event(s))
- `avg_api_latency_ms`: min 201.32, max 215.9, average 206.7729 (1 anomaly event(s))
- `support_ticket_count`: min 193.0, max 240.0, average 209.4286 (1 anomaly event(s))

### Recommended Next Steps

- Inspect checkout errors and dependency health for the incident window.
- Confirm checkout failure rate and revenue have returned to baseline.

## INC-017: Shipping Delay Spike

- **Date range:** 2025-06-23 to 2025-06-24
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `revenue_drop`

### Evidence

- 2 anomaly event(s) across 2 anomaly type(s) were grouped within 2025-06-23 to 2025-06-24.

### Affected KPIs

- `shipping_delay_rate`: min 0.0521, max 0.0655, average 0.0588 (1 anomaly event(s))
- `net_revenue`: min 38051.5, max 46112.28, average 42081.89 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-018: Revenue Drop

- **Date range:** 2025-06-30 to 2025-07-01
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 2 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-06-30 to 2025-07-01.

### Affected KPIs

- `net_revenue`: min 36484.17, max 36718.37, average 36601.27 (2 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-019: Revenue Drop

- **Date range:** 2025-07-07 to 2025-07-08
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** `support_ticket_spike`

### Evidence

- 2 anomaly event(s) across 2 anomaly type(s) were grouped within 2025-07-07 to 2025-07-08.

### Affected KPIs

- `support_ticket_count`: min 194.0, max 236.0, average 215.0 (1 anomaly event(s))
- `net_revenue`: min 39243.05, max 48569.13, average 43906.09 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-020: Shipping Delay Spike

- **Date range:** 2025-07-13 to 2025-07-13
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-07-13 to 2025-07-13.

### Affected KPIs

- `shipping_delay_rate`: min 0.0624, max 0.0624, average 0.0624 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-021: Deployment-related checkout incident

- **Date range:** 2025-07-22 to 2025-07-23
- **Likely cause:** Likely deployment-related checkout incident
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `latency_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Latency and checkout failure anomalies occurred together from 2025-07-22 to 2025-07-23.
- 2 failed or rollback deployment event(s) occurred within the investigation window.

### Affected KPIs

- `checkout_failure_rate`: min 0.0263, max 0.0482, average 0.0372 (1 anomaly event(s))
- `avg_api_latency_ms`: min 236.31, max 308.89, average 272.6 (1 anomaly event(s))
- `net_revenue`: min 30921.83, max 33015.25, average 31968.54 (2 anomaly event(s))
- `support_ticket_count`: min 264.0, max 284.0, average 274.0 (2 anomaly event(s))
- `conversion_rate`: min 0.0306, max 0.0367, average 0.0336 (0 anomaly event(s))

### Recommended Next Steps

- Review the failed checkout deployment, dependency changes, and rollback results.
- Validate checkout success rate, API latency, and revenue after rollback.
- Add deployment health gates for checkout latency and failure rate.

## INC-022: Revenue Drop

- **Date range:** 2025-07-28 to 2025-07-29
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 2 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-07-28 to 2025-07-29.

### Affected KPIs

- `net_revenue`: min 37023.04, max 37093.28, average 37058.16 (2 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-023: Inventory shortage incident

- **Date range:** 2025-08-11 to 2025-08-20
- **Likely cause:** Likely inventory shortage incident
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `revenue_drop`, `shipping_delay_spike`, `support_ticket_spike`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2025-08-11 to 2025-08-20.
- Lost sales units reached 96.00 during the incident.

### Affected KPIs

- `net_revenue`: min 39203.73, max 59389.39, average 48840.273 (4 anomaly event(s))
- `stockout_units`: min 0.0, max 74.0, average 43.8 (7 anomaly event(s))
- `support_ticket_count`: min 195.0, max 262.0, average 235.7 (2 anomaly event(s))
- `shipping_delay_rate`: min 0.0546, max 0.0691, average 0.0595 (1 anomaly event(s))
- `lost_sales_units`: min 0.0, max 96.0, average 57.7 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-024: Checkout Failure Spike

- **Date range:** 2025-08-25 to 2025-08-26
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `revenue_drop`

### Evidence

- 2 anomaly event(s) across 2 anomaly type(s) were grouped within 2025-08-25 to 2025-08-26.

### Affected KPIs

- `checkout_failure_rate`: min 0.0171, max 0.0217, average 0.0194 (1 anomaly event(s))
- `net_revenue`: min 35949.95, max 44679.89, average 40314.92 (1 anomaly event(s))

### Recommended Next Steps

- Inspect checkout errors and dependency health for the incident window.
- Confirm checkout failure rate and revenue have returned to baseline.

## INC-025: Revenue Drop

- **Date range:** 2025-09-01 to 2025-09-01
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-09-01 to 2025-09-01.

### Affected KPIs

- `net_revenue`: min 40033.92, max 40033.92, average 40033.92 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-026: Latency Spike

- **Date range:** 2025-09-06 to 2025-09-10
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `latency_spike`
- **Related anomalies:** `revenue_drop`, `shipping_delay_spike`, `support_ticket_spike`

### Evidence

- 6 anomaly event(s) across 4 anomaly type(s) were grouped within 2025-09-06 to 2025-09-10.

### Affected KPIs

- `shipping_delay_rate`: min 0.0506, max 0.0636, average 0.0564 (1 anomaly event(s))
- `avg_api_latency_ms`: min 203.91, max 213.91, average 209.27 (2 anomaly event(s))
- `net_revenue`: min 44130.03, max 65142.48, average 54397.582 (1 anomaly event(s))
- `support_ticket_count`: min 192.0, max 261.0, average 222.6 (2 anomaly event(s))

### Recommended Next Steps

- Inspect service latency by endpoint and dependency.
- Confirm latency has returned to its rolling baseline.

## INC-027: Logistics disruption incident

- **Date range:** 2025-09-15 to 2025-09-18
- **Likely cause:** Likely logistics disruption incident
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `revenue_drop`, `support_ticket_spike`

### Evidence

- Shipping delay anomalies occurred from 2025-09-15 to 2025-09-18.
- Delivery complaints reached 101.00 versus a prior average of 22.93.

### Affected KPIs

- `net_revenue`: min 43316.08, max 60344.53, average 52350.8875 (2 anomaly event(s))
- `support_ticket_count`: min 264.0, max 318.0, average 291.25 (3 anomaly event(s))
- `shipping_delay_rate`: min 0.0564, max 0.0721, average 0.0653 (2 anomaly event(s))
- `delivery_complaints`: min 82.0, max 101.0, average 92.75 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-028: Revenue Drop

- **Date range:** 2025-09-22 to 2025-09-22
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-09-22 to 2025-09-22.

### Affected KPIs

- `net_revenue`: min 42386.16, max 42386.16, average 42386.16 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-029: Deployment-related checkout incident

- **Date range:** 2025-09-29 to 2025-10-14
- **Likely cause:** Likely deployment-related checkout incident
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `latency_spike`, `revenue_drop`, `shipping_delay_spike`, `support_ticket_spike`

### Evidence

- Latency and checkout failure anomalies occurred together from 2025-09-29 to 2025-10-14.
- 2 failed or rollback deployment event(s) occurred within the investigation window.

### Affected KPIs

- `net_revenue`: min 30539.98, max 73220.04, average 48413.5694 (10 anomaly event(s))
- `avg_api_latency_ms`: min 199.8, max 660.19, average 284.495 (4 anomaly event(s))
- `checkout_failure_rate`: min 0.0149, max 0.1491, average 0.04 (4 anomaly event(s))
- `shipping_delay_rate`: min 0.0477, max 0.0645, average 0.0551 (1 anomaly event(s))
- `support_ticket_count`: min 196.0, max 387.0, average 255.0625 (4 anomaly event(s))
- `conversion_rate`: min 0.022, max 0.0484, average 0.0385 (0 anomaly event(s))

### Recommended Next Steps

- Review the failed checkout deployment, dependency changes, and rollback results.
- Validate checkout success rate, API latency, and revenue after rollback.
- Add deployment health gates for checkout latency and failure rate.

## INC-030: Revenue Drop

- **Date range:** 2025-11-03 to 2025-11-04
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 2 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-11-03 to 2025-11-04.

### Affected KPIs

- `net_revenue`: min 42294.8, max 46696.69, average 44495.745 (2 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-031: Shipping Delay Spike

- **Date range:** 2025-11-08 to 2025-11-17
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `revenue_drop`, `support_ticket_spike`

### Evidence

- 7 anomaly event(s) across 3 anomaly type(s) were grouped within 2025-11-08 to 2025-11-17.

### Affected KPIs

- `shipping_delay_rate`: min 0.0488, max 0.0666, average 0.0567 (1 anomaly event(s))
- `net_revenue`: min 36601.88, max 69079.86, average 54759.25 (4 anomaly event(s))
- `support_ticket_count`: min 198.0, max 261.0, average 228.6 (2 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-032: Latency Spike

- **Date range:** 2025-11-24 to 2025-11-28
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `latency_spike`
- **Related anomalies:** `revenue_drop`, `shipping_delay_spike`

### Evidence

- 4 anomaly event(s) across 3 anomaly type(s) were grouped within 2025-11-24 to 2025-11-28.

### Affected KPIs

- `net_revenue`: min 42869.95, max 68204.68, average 54116.458 (2 anomaly event(s))
- `shipping_delay_rate`: min 0.05, max 0.0648, average 0.0558 (1 anomaly event(s))
- `avg_api_latency_ms`: min 204.33, max 216.54, average 208.196 (1 anomaly event(s))

### Recommended Next Steps

- Inspect service latency by endpoint and dependency.
- Confirm latency has returned to its rolling baseline.

## INC-033: Inventory shortage incident

- **Date range:** 2025-12-03 to 2025-12-16
- **Likely cause:** Likely inventory shortage incident
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `revenue_drop`, `support_ticket_spike`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2025-12-03 to 2025-12-16.
- Lost sales units reached 201.00 during the incident.

### Affected KPIs

- `stockout_units`: min 90.0, max 124.0, average 111.7143 (14 anomaly event(s))
- `net_revenue`: min 32557.83, max 58574.79, average 45890.5393 (6 anomaly event(s))
- `support_ticket_count`: min 243.0, max 312.0, average 283.7857 (5 anomaly event(s))
- `lost_sales_units`: min 111.0, max 201.0, average 159.8571 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-034: Shipping Delay Spike

- **Date range:** 2025-12-31 to 2025-12-31
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-12-31 to 2025-12-31.

### Affected KPIs

- `shipping_delay_rate`: min 0.0639, max 0.0639, average 0.0639 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-035: Latency Spike

- **Date range:** 2026-01-05 to 2026-01-05
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `latency_spike`
- **Related anomalies:** `revenue_drop`

### Evidence

- 2 anomaly event(s) across 2 anomaly type(s) were grouped within 2026-01-05 to 2026-01-05.

### Affected KPIs

- `avg_api_latency_ms`: min 216.89, max 216.89, average 216.89 (1 anomaly event(s))
- `net_revenue`: min 50518.39, max 50518.39, average 50518.39 (1 anomaly event(s))

### Recommended Next Steps

- Inspect service latency by endpoint and dependency.
- Confirm latency has returned to its rolling baseline.

## INC-036: Revenue Drop

- **Date range:** 2026-01-12 to 2026-01-12
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** `support_ticket_spike`

### Evidence

- 2 anomaly event(s) across 2 anomaly type(s) were grouped within 2026-01-12 to 2026-01-12.

### Affected KPIs

- `net_revenue`: min 51703.76, max 51703.76, average 51703.76 (1 anomaly event(s))
- `support_ticket_count`: min 237.0, max 237.0, average 237.0 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-037: Revenue Drop

- **Date range:** 2026-01-19 to 2026-01-19
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-01-19 to 2026-01-19.

### Affected KPIs

- `net_revenue`: min 44396.01, max 44396.01, average 44396.01 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-038: Deployment-related checkout incident

- **Date range:** 2026-01-27 to 2026-02-03
- **Likely cause:** Likely deployment-related checkout incident
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `latency_spike`, `revenue_drop`, `shipping_delay_spike`, `support_ticket_spike`

### Evidence

- Latency and checkout failure anomalies occurred together from 2026-01-27 to 2026-02-03.
- 2 failed or rollback deployment event(s) occurred within the investigation window.

### Affected KPIs

- `checkout_failure_rate`: min 0.0157, max 0.0711, average 0.0314 (2 anomaly event(s))
- `avg_api_latency_ms`: min 202.62, max 407.37, average 255.2775 (2 anomaly event(s))
- `net_revenue`: min 43233.91, max 82763.0, average 60310.9637 (3 anomaly event(s))
- `support_ticket_count`: min 199.0, max 305.0, average 227.5 (2 anomaly event(s))
- `shipping_delay_rate`: min 0.0472, max 0.0632, average 0.0555 (2 anomaly event(s))
- `conversion_rate`: min 0.0349, max 0.0496, average 0.042 (0 anomaly event(s))

### Recommended Next Steps

- Review the failed checkout deployment, dependency changes, and rollback results.
- Validate checkout success rate, API latency, and revenue after rollback.
- Add deployment health gates for checkout latency and failure rate.

## INC-039: Logistics disruption incident

- **Date range:** 2026-02-09 to 2026-02-17
- **Likely cause:** Likely logistics disruption incident
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `revenue_drop`, `support_ticket_spike`

### Evidence

- Shipping delay anomalies occurred from 2026-02-09 to 2026-02-17.
- Delivery complaints reached 163.00 versus a prior average of 22.43.

### Affected KPIs

- `shipping_delay_rate`: min 0.0898, max 0.0989, average 0.0939 (5 anomaly event(s))
- `support_ticket_count`: min 360.0, max 409.0, average 373.0 (7 anomaly event(s))
- `net_revenue`: min 47860.47, max 93772.02, average 61222.7767 (3 anomaly event(s))
- `delivery_complaints`: min 133.0, max 163.0, average 146.3333 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-040: Revenue Drop

- **Date range:** 2026-02-24 to 2026-02-24
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-02-24 to 2026-02-24.

### Affected KPIs

- `net_revenue`: min 49075.3, max 49075.3, average 49075.3 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-041: Revenue Drop

- **Date range:** 2026-03-02 to 2026-03-02
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-03-02 to 2026-03-02.

### Affected KPIs

- `net_revenue`: min 49100.34, max 49100.34, average 49100.34 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-042: Revenue Drop

- **Date range:** 2026-03-10 to 2026-03-11
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** `support_ticket_spike`

### Evidence

- 2 anomaly event(s) across 2 anomaly type(s) were grouped within 2026-03-10 to 2026-03-11.

### Affected KPIs

- `net_revenue`: min 52828.81, max 57697.56, average 55263.185 (1 anomaly event(s))
- `support_ticket_count`: min 218.0, max 255.0, average 236.5 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-043: Revenue Drop

- **Date range:** 2026-03-24 to 2026-03-24
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-03-24 to 2026-03-24.

### Affected KPIs

- `net_revenue`: min 49153.93, max 49153.93, average 49153.93 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-044: Revenue Drop

- **Date range:** 2026-03-30 to 2026-03-30
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-03-30 to 2026-03-30.

### Affected KPIs

- `net_revenue`: min 53444.37, max 53444.37, average 53444.37 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-045: Revenue Drop

- **Date range:** 2026-04-06 to 2026-04-06
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-04-06 to 2026-04-06.

### Affected KPIs

- `net_revenue`: min 55834.78, max 55834.78, average 55834.78 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-046: Deployment-related checkout incident

- **Date range:** 2026-04-10 to 2026-04-18
- **Likely cause:** Likely deployment-related checkout incident
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `latency_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Latency and checkout failure anomalies occurred together from 2026-04-10 to 2026-04-18.
- 2 failed or rollback deployment event(s) occurred within the investigation window.

### Affected KPIs

- `avg_api_latency_ms`: min 209.79, max 725.77, average 488.5011 (6 anomaly event(s))
- `net_revenue`: min 29512.52, max 76474.18, average 50309.7833 (6 anomaly event(s))
- `checkout_failure_rate`: min 0.0166, max 0.1724, average 0.099 (5 anomaly event(s))
- `support_ticket_count`: min 184.0, max 442.0, average 304.5556 (5 anomaly event(s))
- `conversion_rate`: min 0.0197, max 0.0459, average 0.0325 (0 anomaly event(s))

### Recommended Next Steps

- Review the failed checkout deployment, dependency changes, and rollback results.
- Validate checkout success rate, API latency, and revenue after rollback.
- Add deployment health gates for checkout latency and failure rate.

## INC-047: Shipping Delay Spike

- **Date range:** 2026-04-27 to 2026-04-27
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-04-27 to 2026-04-27.

### Affected KPIs

- `shipping_delay_rate`: min 0.0676, max 0.0676, average 0.0676 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-048: Revenue Drop

- **Date range:** 2026-05-04 to 2026-05-04
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-05-04 to 2026-05-04.

### Affected KPIs

- `net_revenue`: min 48601.74, max 48601.74, average 48601.74 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-049: Inventory shortage incident

- **Date range:** 2026-05-10 to 2026-05-30
- **Likely cause:** Likely inventory shortage incident
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `checkout_failure_spike`, `revenue_drop`, `shipping_delay_spike`, `support_ticket_spike`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2026-05-10 to 2026-05-30.
- Lost sales units reached 122.00 during the incident.

### Affected KPIs

- `checkout_failure_rate`: min 0.0152, max 0.0212, average 0.0186 (3 anomaly event(s))
- `net_revenue`: min 50269.24, max 82965.41, average 66804.67 (6 anomaly event(s))
- `support_ticket_count`: min 180.0, max 296.0, average 244.4762 (4 anomaly event(s))
- `stockout_units`: min 0.0, max 116.0, average 51.381 (11 anomaly event(s))
- `shipping_delay_rate`: min 0.0463, max 0.0645, average 0.0547 (1 anomaly event(s))
- `lost_sales_units`: min 0.0, max 122.0, average 51.9048 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-050: Revenue Drop

- **Date range:** 2026-06-08 to 2026-06-08
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-06-08 to 2026-06-08.

### Affected KPIs

- `net_revenue`: min 53844.41, max 53844.41, average 53844.41 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-051: Revenue Drop

- **Date range:** 2026-06-15 to 2026-06-16
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 2 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-06-15 to 2026-06-16.

### Affected KPIs

- `net_revenue`: min 57413.57, max 60460.32, average 58936.945 (2 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-052: Logistics disruption incident

- **Date range:** 2026-06-20 to 2026-06-29
- **Likely cause:** Likely logistics disruption incident
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `checkout_failure_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Shipping delay anomalies occurred from 2026-06-20 to 2026-06-29.
- Delivery complaints reached 125.00 versus a prior average of 22.50.

### Affected KPIs

- `checkout_failure_rate`: min 0.0173, max 0.0194, average 0.0181 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.0455, max 0.1093, average 0.0859 (6 anomaly event(s))
- `support_ticket_count`: min 215.0, max 330.0, average 281.4 (4 anomaly event(s))
- `net_revenue`: min 52260.42, max 91085.28, average 73105.793 (2 anomaly event(s))
- `delivery_complaints`: min 22.0, max 125.0, average 83.3 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-053: Checkout Failure Spike

- **Date range:** 2026-07-06 to 2026-07-09
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `revenue_drop`

### Evidence

- 2 anomaly event(s) across 2 anomaly type(s) were grouped within 2026-07-06 to 2026-07-09.

### Affected KPIs

- `net_revenue`: min 57787.97, max 75655.33, average 66880.5175 (1 anomaly event(s))
- `checkout_failure_rate`: min 0.0173, max 0.0191, average 0.0181 (1 anomaly event(s))

### Recommended Next Steps

- Inspect checkout errors and dependency health for the incident window.
- Confirm checkout failure rate and revenue have returned to baseline.

## INC-054: Revenue Drop

- **Date range:** 2026-07-13 to 2026-07-13
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-07-13 to 2026-07-13.

### Affected KPIs

- `net_revenue`: min 56640.91, max 56640.91, average 56640.91 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-055: Shipping Delay Spike

- **Date range:** 2026-07-17 to 2026-07-24
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `checkout_failure_spike`, `revenue_drop`

### Evidence

- 5 anomaly event(s) across 3 anomaly type(s) were grouped within 2026-07-17 to 2026-07-24.

### Affected KPIs

- `checkout_failure_rate`: min 0.0155, max 0.0214, average 0.0183 (1 anomaly event(s))
- `net_revenue`: min 60407.31, max 95882.71, average 74447.9312 (3 anomaly event(s))
- `shipping_delay_rate`: min 0.0485, max 0.0676, average 0.0553 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-056: Deployment-related checkout incident

- **Date range:** 2026-08-03 to 2026-08-06
- **Likely cause:** Likely deployment-related checkout incident
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `latency_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Latency and checkout failure anomalies occurred together from 2026-08-03 to 2026-08-06.
- 2 failed or rollback deployment event(s) occurred within the investigation window.

### Affected KPIs

- `checkout_failure_rate`: min 0.018, max 0.1065, average 0.0524 (2 anomaly event(s))
- `avg_api_latency_ms`: min 209.36, max 512.1, average 330.6475 (2 anomaly event(s))
- `net_revenue`: min 40202.62, max 70078.59, average 53674.2875 (3 anomaly event(s))
- `support_ticket_count`: min 218.0, max 327.0, average 272.5 (2 anomaly event(s))
- `conversion_rate`: min 0.0272, max 0.04, average 0.0346 (0 anomaly event(s))

### Recommended Next Steps

- Review the failed checkout deployment, dependency changes, and rollback results.
- Validate checkout success rate, API latency, and revenue after rollback.
- Add deployment health gates for checkout latency and failure rate.

## INC-057: Revenue Drop

- **Date range:** 2026-08-11 to 2026-08-11
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-08-11 to 2026-08-11.

### Affected KPIs

- `net_revenue`: min 60843.45, max 60843.45, average 60843.45 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-058: Shipping Delay Spike

- **Date range:** 2026-08-15 to 2026-08-19
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `revenue_drop`

### Evidence

- 3 anomaly event(s) across 2 anomaly type(s) were grouped within 2026-08-15 to 2026-08-19.

### Affected KPIs

- `shipping_delay_rate`: min 0.0553, max 0.0666, average 0.0596 (1 anomaly event(s))
- `net_revenue`: min 54449.52, max 96878.63, average 73404.36 (2 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-059: Revenue Drop

- **Date range:** 2026-08-26 to 2026-08-26
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-08-26 to 2026-08-26.

### Affected KPIs

- `net_revenue`: min 59374.81, max 59374.81, average 59374.81 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-060: Inventory shortage incident

- **Date range:** 2026-09-07 to 2026-09-23
- **Likely cause:** Likely inventory shortage incident
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `latency_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2026-09-07 to 2026-09-23.
- Lost sales units reached 179.00 during the incident.

### Affected KPIs

- `net_revenue`: min 49573.3, max 93627.89, average 65170.7329 (6 anomaly event(s))
- `stockout_units`: min 0.0, max 138.0, average 105.4118 (15 anomaly event(s))
- `support_ticket_count`: min 199.0, max 301.0, average 271.1765 (4 anomaly event(s))
- `avg_api_latency_ms`: min 199.75, max 217.6, average 207.8018 (1 anomaly event(s))
- `lost_sales_units`: min 0.0, max 179.0, average 115.4706 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-061: Logistics disruption incident

- **Date range:** 2026-09-30 to 2026-10-13
- **Likely cause:** Likely logistics disruption incident
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `checkout_failure_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Shipping delay anomalies occurred from 2026-09-30 to 2026-10-13.
- Delivery complaints reached 146.00 versus a prior average of 23.14.

### Affected KPIs

- `checkout_failure_rate`: min 0.0161, max 0.0205, average 0.0178 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.0494, max 0.1631, average 0.1205 (9 anomaly event(s))
- `net_revenue`: min 61769.81, max 115107.58, average 79074.5564 (3 anomaly event(s))
- `support_ticket_count`: min 212.0, max 372.0, average 300.7143 (6 anomaly event(s))
- `delivery_complaints`: min 22.0, max 146.0, average 93.7143 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-062: Checkout Failure Spike

- **Date range:** 2026-10-17 to 2026-10-17
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-10-17 to 2026-10-17.

### Affected KPIs

- `checkout_failure_rate`: min 0.0216, max 0.0216, average 0.0216 (1 anomaly event(s))

### Recommended Next Steps

- Inspect checkout errors and dependency health for the incident window.
- Confirm checkout failure rate and revenue have returned to baseline.

## INC-063: Revenue Drop

- **Date range:** 2026-10-21 to 2026-10-21
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-10-21 to 2026-10-21.

### Affected KPIs

- `net_revenue`: min 66322.31, max 66322.31, average 66322.31 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-064: Shipping Delay Spike

- **Date range:** 2026-10-29 to 2026-11-05
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `revenue_drop`

### Evidence

- 4 anomaly event(s) across 2 anomaly type(s) were grouped within 2026-10-29 to 2026-11-05.

### Affected KPIs

- `net_revenue`: min 59463.83, max 90596.78, average 69259.525 (3 anomaly event(s))
- `shipping_delay_rate`: min 0.0449, max 0.0647, average 0.0555 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-065: Revenue Drop

- **Date range:** 2026-11-09 to 2026-11-09
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-11-09 to 2026-11-09.

### Affected KPIs

- `net_revenue`: min 53565.65, max 53565.65, average 53565.65 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-066: Deployment-related checkout incident

- **Date range:** 2026-11-16 to 2026-11-19
- **Likely cause:** Likely deployment-related checkout incident
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `latency_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Latency and checkout failure anomalies occurred together from 2026-11-16 to 2026-11-19.
- 2 failed or rollback deployment event(s) occurred within the investigation window.

### Affected KPIs

- `checkout_failure_rate`: min 0.0832, max 0.1328, average 0.1148 (4 anomaly event(s))
- `avg_api_latency_ms`: min 449.05, max 628.11, average 563.025 (4 anomaly event(s))
- `net_revenue`: min 45106.36, max 53223.63, average 48024.535 (4 anomaly event(s))
- `support_ticket_count`: min 318.0, max 374.0, average 347.5 (4 anomaly event(s))
- `conversion_rate`: min 0.0245, max 0.036, average 0.031 (0 anomaly event(s))

### Recommended Next Steps

- Review the failed checkout deployment, dependency changes, and rollback results.
- Validate checkout success rate, API latency, and revenue after rollback.
- Add deployment health gates for checkout latency and failure rate.

## INC-067: Revenue Drop

- **Date range:** 2026-11-23 to 2026-11-23
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-11-23 to 2026-11-23.

### Affected KPIs

- `net_revenue`: min 60698.91, max 60698.91, average 60698.91 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-068: Revenue Drop

- **Date range:** 2026-12-01 to 2026-12-01
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-12-01 to 2026-12-01.

### Affected KPIs

- `net_revenue`: min 61676.47, max 61676.47, average 61676.47 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-069: Checkout Failure Spike

- **Date range:** 2026-12-07 to 2026-12-08
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `latency_spike`, `revenue_drop`

### Evidence

- 4 anomaly event(s) across 3 anomaly type(s) were grouped within 2026-12-07 to 2026-12-08.

### Affected KPIs

- `net_revenue`: min 61897.73, max 64628.37, average 63263.05 (2 anomaly event(s))
- `checkout_failure_rate`: min 0.018, max 0.0211, average 0.0195 (1 anomaly event(s))
- `avg_api_latency_ms`: min 209.79, max 216.36, average 213.075 (1 anomaly event(s))

### Recommended Next Steps

- Inspect checkout errors and dependency health for the incident window.
- Confirm checkout failure rate and revenue have returned to baseline.

## INC-070: Shipping Delay Spike

- **Date range:** 2026-12-12 to 2026-12-12
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-12-12 to 2026-12-12.

### Affected KPIs

- `shipping_delay_rate`: min 0.0609, max 0.0609, average 0.0609 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-071: Shipping Delay Spike

- **Date range:** 2026-12-16 to 2026-12-16
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-12-16 to 2026-12-16.

### Affected KPIs

- `shipping_delay_rate`: min 0.0617, max 0.0617, average 0.0617 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-072: Shipping Delay Spike

- **Date range:** 2026-12-22 to 2026-12-24
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `revenue_drop`, `support_ticket_spike`

### Evidence

- 4 anomaly event(s) across 3 anomaly type(s) were grouped within 2026-12-22 to 2026-12-24.

### Affected KPIs

- `net_revenue`: min 62626.81, max 75625.24, average 70198.2167 (2 anomaly event(s))
- `shipping_delay_rate`: min 0.0447, max 0.0759, average 0.0599 (1 anomaly event(s))
- `support_ticket_count`: min 194.0, max 231.0, average 212.6667 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-073: Checkout Failure Spike

- **Date range:** 2026-12-30 to 2026-12-30
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-12-30 to 2026-12-30.

### Affected KPIs

- `checkout_failure_rate`: min 0.0211, max 0.0211, average 0.0211 (1 anomaly event(s))

### Recommended Next Steps

- Inspect checkout errors and dependency health for the incident window.
- Confirm checkout failure rate and revenue have returned to baseline.
