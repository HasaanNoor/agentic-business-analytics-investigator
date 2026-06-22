# Deterministic Investigation Summary

Generated from anomaly events grouped with a maximum consecutive-event gap of 3 days.
Total incidents: **64**

## INC-001: Revenue Drop

- **Date range:** 2025-01-10 to 2025-01-16
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** `support_ticket_spike`

### Evidence

- 3 anomaly event(s) across 2 anomaly type(s) were grouped within 2025-01-10 to 2025-01-16.

### Affected KPIs

- `support_ticket_count`: min 110.0, max 151.0, average 127.2857 (1 anomaly event(s))
- `net_revenue`: min 36361.73, max 53094.33, average 44114.9443 (2 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-002: Revenue Drop

- **Date range:** 2025-01-20 to 2025-01-20
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-01-20 to 2025-01-20.

### Affected KPIs

- `net_revenue`: min 32182.47, max 32182.47, average 32182.47 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-003: Checkout Failure Spike

- **Date range:** 2025-01-25 to 2025-01-29
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `revenue_drop`, `support_ticket_spike`

### Evidence

- 4 anomaly event(s) across 3 anomaly type(s) were grouped within 2025-01-25 to 2025-01-29.

### Affected KPIs

- `net_revenue`: min 36094.97, max 50883.67, average 41147.874 (2 anomaly event(s))
- `support_ticket_count`: min 85.0, max 158.0, average 129.2 (1 anomaly event(s))
- `checkout_failure_rate`: min 0.018, max 0.0207, average 0.0189 (1 anomaly event(s))

### Recommended Next Steps

- Inspect checkout errors and dependency health for the incident window.
- Confirm checkout failure rate and revenue have returned to baseline.

## INC-004: Logistics disruption incident

- **Date range:** 2025-02-03 to 2025-02-10
- **Likely cause:** Likely logistics disruption incident
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `latency_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Shipping delay anomalies occurred from 2025-02-03 to 2025-02-10.
- Delivery complaints reached 39.00 versus a prior average of 24.14.

### Affected KPIs

- `avg_api_latency_ms`: min 202.98, max 214.9, average 209.5312 (2 anomaly event(s))
- `shipping_delay_rate`: min 0.0601, max 0.0761, average 0.0655 (1 anomaly event(s))
- `support_ticket_count`: min 120.0, max 173.0, average 141.0 (1 anomaly event(s))
- `net_revenue`: min 33602.53, max 59906.98, average 45844.8125 (1 anomaly event(s))
- `delivery_complaints`: min 22.0, max 39.0, average 26.75 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-005: Revenue Drop

- **Date range:** 2025-02-17 to 2025-02-18
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** `shipping_delay_spike`

### Evidence

- 3 anomaly event(s) across 2 anomaly type(s) were grouped within 2025-02-17 to 2025-02-18.

### Affected KPIs

- `net_revenue`: min 34381.33, max 37923.28, average 36152.305 (2 anomaly event(s))
- `shipping_delay_rate`: min 0.0574, max 0.0761, average 0.0668 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-006: Revenue Drop

- **Date range:** 2025-02-23 to 2025-02-25
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 3 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-02-23 to 2025-02-25.

### Affected KPIs

- `net_revenue`: min 36002.54, max 40132.99, average 38372.6833 (3 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-007: Support Ticket Spike

- **Date range:** 2025-03-02 to 2025-03-02
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `support_ticket_spike`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-03-02 to 2025-03-02.

### Affected KPIs

- `support_ticket_count`: min 180.0, max 180.0, average 180.0 (1 anomaly event(s))

### Recommended Next Steps

- Review support ticket categories to identify the dominant customer issue.
- Confirm ticket volume returns to baseline after remediation.

## INC-008: Latency Spike

- **Date range:** 2025-03-10 to 2025-03-13
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `latency_spike`
- **Related anomalies:** `revenue_drop`

### Evidence

- 2 anomaly event(s) across 2 anomaly type(s) were grouped within 2025-03-10 to 2025-03-13.

### Affected KPIs

- `net_revenue`: min 39939.44, max 61472.45, average 50259.05 (1 anomaly event(s))
- `avg_api_latency_ms`: min 197.76, max 216.44, average 207.5 (1 anomaly event(s))

### Recommended Next Steps

- Inspect service latency by endpoint and dependency.
- Confirm latency has returned to its rolling baseline.

## INC-009: Deployment-related checkout incident

- **Date range:** 2025-03-17 to 2025-03-21
- **Likely cause:** Likely deployment-related checkout incident
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `latency_spike`, `revenue_drop`, `shipping_delay_spike`, `support_ticket_spike`

### Evidence

- Latency and checkout failure anomalies occurred together from 2025-03-17 to 2025-03-21.
- 2 failed or rollback deployment event(s) occurred within the investigation window.

### Affected KPIs

- `net_revenue`: min 25906.11, max 45242.01, average 33845.644 (4 anomaly event(s))
- `checkout_failure_rate`: min 0.0156, max 0.1239, average 0.0751 (3 anomaly event(s))
- `avg_api_latency_ms`: min 207.94, max 564.89, average 411.506 (3 anomaly event(s))
- `support_ticket_count`: min 136.0, max 310.0, average 232.0 (3 anomaly event(s))
- `shipping_delay_rate`: min 0.06, max 0.0712, average 0.0644 (1 anomaly event(s))
- `conversion_rate`: min 0.0265, max 0.0441, average 0.0339 (0 anomaly event(s))

### Recommended Next Steps

- Review the failed checkout deployment, dependency changes, and rollback results.
- Validate checkout success rate, API latency, and revenue after rollback.
- Add deployment health gates for checkout latency and failure rate.

## INC-010: Revenue Drop

- **Date range:** 2025-04-01 to 2025-04-01
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-04-01 to 2025-04-01.

### Affected KPIs

- `net_revenue`: min 37943.25, max 37943.25, average 37943.25 (1 anomaly event(s))

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
- Lost sales units reached 113.00 during the incident.

### Affected KPIs

- `net_revenue`: min 28393.31, max 47473.27, average 38492.545 (8 anomaly event(s))
- `shipping_delay_rate`: min 0.0554, max 0.0692, average 0.0634 (1 anomaly event(s))
- `stockout_units`: min 0.0, max 109.0, average 68.9286 (11 anomaly event(s))
- `support_ticket_count`: min 133.0, max 187.0, average 158.5 (1 anomaly event(s))
- `lost_sales_units`: min 0.0, max 113.0, average 75.0 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-012: Logistics disruption incident

- **Date range:** 2025-04-25 to 2025-04-27
- **Likely cause:** Likely logistics disruption incident
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `latency_spike`

### Evidence

- Shipping delay anomalies occurred from 2025-04-25 to 2025-04-27.
- Delivery complaints reached 46.00 versus a prior average of 27.14.

### Affected KPIs

- `avg_api_latency_ms`: min 204.21, max 215.11, average 209.29 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.0589, max 0.0731, average 0.0643 (1 anomaly event(s))
- `delivery_complaints`: min 32.0, max 46.0, average 38.6667 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-013: Logistics disruption incident

- **Date range:** 2025-05-05 to 2025-05-14
- **Likely cause:** Likely logistics disruption incident
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `revenue_drop`, `support_ticket_spike`

### Evidence

- Shipping delay anomalies occurred from 2025-05-05 to 2025-05-14.
- Delivery complaints reached 128.00 versus a prior average of 29.21.

### Affected KPIs

- `net_revenue`: min 35003.13, max 58425.92, average 44677.321 (5 anomaly event(s))
- `shipping_delay_rate`: min 0.1408, max 0.1619, average 0.1491 (8 anomaly event(s))
- `support_ticket_count`: min 214.0, max 283.0, average 250.8 (8 anomaly event(s))
- `delivery_complaints`: min 105.0, max 128.0, average 120.1 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-014: Logistics disruption incident

- **Date range:** 2025-06-02 to 2025-06-05
- **Likely cause:** Likely logistics disruption incident
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `latency_spike`, `support_ticket_spike`

### Evidence

- Shipping delay anomalies occurred from 2025-06-02 to 2025-06-05.
- Delivery complaints reached 41.00 versus a prior average of 25.21.

### Affected KPIs

- `avg_api_latency_ms`: min 203.12, max 217.71, average 208.7825 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.0619, max 0.0744, average 0.0671 (2 anomaly event(s))
- `support_ticket_count`: min 136.0, max 185.0, average 152.25 (1 anomaly event(s))
- `delivery_complaints`: min 23.0, max 41.0, average 33.0 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-015: Revenue Drop

- **Date range:** 2025-06-09 to 2025-06-10
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 2 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-06-09 to 2025-06-10.

### Affected KPIs

- `net_revenue`: min 43326.96, max 43525.8, average 43426.38 (2 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-016: Revenue Drop

- **Date range:** 2025-06-16 to 2025-06-16
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-06-16 to 2025-06-16.

### Affected KPIs

- `net_revenue`: min 44903.32, max 44903.32, average 44903.32 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-017: Revenue Drop

- **Date range:** 2025-06-24 to 2025-06-26
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** `support_ticket_spike`

### Evidence

- 2 anomaly event(s) across 2 anomaly type(s) were grouped within 2025-06-24 to 2025-06-26.

### Affected KPIs

- `net_revenue`: min 44366.87, max 55491.3, average 49526.1367 (1 anomaly event(s))
- `support_ticket_count`: min 130.0, max 178.0, average 149.0 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-018: Revenue Drop

- **Date range:** 2025-06-30 to 2025-07-01
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** `checkout_failure_spike`, `shipping_delay_spike`

### Evidence

- 4 anomaly event(s) across 3 anomaly type(s) were grouped within 2025-06-30 to 2025-07-01.

### Affected KPIs

- `checkout_failure_rate`: min 0.0182, max 0.0214, average 0.0198 (1 anomaly event(s))
- `net_revenue`: min 35001.53, max 40409.72, average 37705.625 (2 anomaly event(s))
- `shipping_delay_rate`: min 0.0689, max 0.0723, average 0.0706 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-019: Shipping Delay Spike

- **Date range:** 2025-07-07 to 2025-07-08
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `latency_spike`, `revenue_drop`

### Evidence

- 3 anomaly event(s) across 3 anomaly type(s) were grouped within 2025-07-07 to 2025-07-08.

### Affected KPIs

- `shipping_delay_rate`: min 0.0582, max 0.0736, average 0.0659 (1 anomaly event(s))
- `avg_api_latency_ms`: min 205.89, max 215.87, average 210.88 (1 anomaly event(s))
- `net_revenue`: min 38507.13, max 54749.8, average 46628.465 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-020: Revenue Drop

- **Date range:** 2025-07-15 to 2025-07-15
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-07-15 to 2025-07-15.

### Affected KPIs

- `net_revenue`: min 42934.3, max 42934.3, average 42934.3 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-021: Deployment-related checkout incident

- **Date range:** 2025-07-19 to 2025-07-23
- **Likely cause:** Likely deployment-related checkout incident
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `latency_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Latency and checkout failure anomalies occurred together from 2025-07-19 to 2025-07-23.
- 2 failed or rollback deployment event(s) occurred within the investigation window.

### Affected KPIs

- `checkout_failure_rate`: min 0.0183, max 0.0468, average 0.027 (2 anomaly event(s))
- `net_revenue`: min 31629.44, max 60010.34, average 44112.26 (3 anomaly event(s))
- `avg_api_latency_ms`: min 201.62, max 311.17, average 233.45 (1 anomaly event(s))
- `support_ticket_count`: min 123.0, max 216.0, average 177.6 (2 anomaly event(s))
- `conversion_rate`: min 0.0306, max 0.0443, average 0.0391 (0 anomaly event(s))

### Recommended Next Steps

- Review the failed checkout deployment, dependency changes, and rollback results.
- Validate checkout success rate, API latency, and revenue after rollback.
- Add deployment health gates for checkout latency and failure rate.

## INC-022: Revenue Drop

- **Date range:** 2025-07-28 to 2025-07-31
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** `shipping_delay_spike`

### Evidence

- 3 anomaly event(s) across 2 anomaly type(s) were grouped within 2025-07-28 to 2025-07-31.

### Affected KPIs

- `net_revenue`: min 33010.03, max 54447.62, average 44177.77 (2 anomaly event(s))
- `shipping_delay_rate`: min 0.0601, max 0.0708, average 0.0647 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-023: Inventory shortage incident

- **Date range:** 2025-08-11 to 2025-08-18
- **Likely cause:** Likely inventory shortage incident
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `revenue_drop`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2025-08-11 to 2025-08-18.
- Lost sales units reached 92.00 during the incident.

### Affected KPIs

- `net_revenue`: min 33504.76, max 52797.11, average 43151.6775 (4 anomaly event(s))
- `stockout_units`: min 0.0, max 88.0, average 59.0 (7 anomaly event(s))
- `lost_sales_units`: min 0.0, max 92.0, average 58.375 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-024: Revenue Drop

- **Date range:** 2025-08-26 to 2025-08-26
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-08-26 to 2025-08-26.

### Affected KPIs

- `net_revenue`: min 38672.95, max 38672.95, average 38672.95 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-025: Revenue Drop

- **Date range:** 2025-09-01 to 2025-09-09
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** `support_ticket_spike`

### Evidence

- 5 anomaly event(s) across 2 anomaly type(s) were grouped within 2025-09-01 to 2025-09-09.

### Affected KPIs

- `net_revenue`: min 35526.8, max 64032.3, average 47907.0133 (4 anomaly event(s))
- `support_ticket_count`: min 123.0, max 186.0, average 159.7778 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-026: Logistics disruption incident

- **Date range:** 2025-09-15 to 2025-09-22
- **Likely cause:** Likely logistics disruption incident
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `latency_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Shipping delay anomalies occurred from 2025-09-15 to 2025-09-22.
- Delivery complaints reached 69.00 versus a prior average of 31.29.

### Affected KPIs

- `net_revenue`: min 33367.6, max 61618.04, average 48712.14 (3 anomaly event(s))
- `shipping_delay_rate`: min 0.0555, max 0.0784, average 0.0704 (3 anomaly event(s))
- `avg_api_latency_ms`: min 202.72, max 220.9, average 208.6412 (1 anomaly event(s))
- `support_ticket_count`: min 141.0, max 236.0, average 189.0 (3 anomaly event(s))
- `delivery_complaints`: min 25.0, max 69.0, average 48.75 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-027: Revenue Drop

- **Date range:** 2025-10-01 to 2025-10-01
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-10-01 to 2025-10-01.

### Affected KPIs

- `net_revenue`: min 40306.91, max 40306.91, average 40306.91 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-028: Deployment-related checkout incident

- **Date range:** 2025-10-05 to 2025-10-11
- **Likely cause:** Likely deployment-related checkout incident
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `latency_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Latency and checkout failure anomalies occurred together from 2025-10-05 to 2025-10-11.
- 2 failed or rollback deployment event(s) occurred within the investigation window.

### Affected KPIs

- `net_revenue`: min 22658.2, max 51908.47, average 36544.0186 (5 anomaly event(s))
- `checkout_failure_rate`: min 0.0172, max 0.1503, average 0.0688 (3 anomaly event(s))
- `avg_api_latency_ms`: min 204.75, max 655.44, average 384.2886 (3 anomaly event(s))
- `support_ticket_count`: min 144.0, max 391.0, average 262.1429 (4 anomaly event(s))
- `conversion_rate`: min 0.022, max 0.0473, average 0.0338 (0 anomaly event(s))

### Recommended Next Steps

- Review the failed checkout deployment, dependency changes, and rollback results.
- Validate checkout success rate, API latency, and revenue after rollback.
- Add deployment health gates for checkout latency and failure rate.

## INC-029: Shipping Delay Spike

- **Date range:** 2025-10-17 to 2025-10-17
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-10-17 to 2025-10-17.

### Affected KPIs

- `shipping_delay_rate`: min 0.0724, max 0.0724, average 0.0724 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-030: Shipping Delay Spike

- **Date range:** 2025-10-28 to 2025-10-28
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-10-28 to 2025-10-28.

### Affected KPIs

- `shipping_delay_rate`: min 0.0727, max 0.0727, average 0.0727 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-031: Shipping Delay Spike

- **Date range:** 2025-11-10 to 2025-11-17
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `checkout_failure_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- 5 anomaly event(s) across 4 anomaly type(s) were grouped within 2025-11-10 to 2025-11-17.

### Affected KPIs

- `net_revenue`: min 47369.5, max 78295.31, average 64691.4362 (2 anomaly event(s))
- `shipping_delay_rate`: min 0.0559, max 0.0796, average 0.0663 (1 anomaly event(s))
- `support_ticket_count`: min 151.0, max 192.0, average 168.625 (1 anomaly event(s))
- `checkout_failure_rate`: min 0.017, max 0.0192, average 0.0181 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-032: Revenue Drop

- **Date range:** 2025-11-25 to 2025-11-25
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-11-25 to 2025-11-25.

### Affected KPIs

- `net_revenue`: min 50122.48, max 50122.48, average 50122.48 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-033: Inventory shortage incident

- **Date range:** 2025-12-01 to 2025-12-16
- **Likely cause:** Likely inventory shortage incident
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `revenue_drop`, `shipping_delay_spike`, `support_ticket_spike`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2025-12-01 to 2025-12-16.
- Lost sales units reached 190.00 during the incident.

### Affected KPIs

- `net_revenue`: min 28434.33, max 62556.48, average 43789.6631 (9 anomaly event(s))
- `stockout_units`: min 0.0, max 135.0, average 97.5 (14 anomaly event(s))
- `support_ticket_count`: min 153.0, max 210.0, average 178.75 (2 anomaly event(s))
- `shipping_delay_rate`: min 0.051, max 0.0759, average 0.0661 (1 anomaly event(s))
- `lost_sales_units`: min 0.0, max 190.0, average 134.0625 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-034: Checkout Failure Spike

- **Date range:** 2025-12-30 to 2026-01-06
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `revenue_drop`

### Evidence

- 5 anomaly event(s) across 2 anomaly type(s) were grouped within 2025-12-30 to 2026-01-06.

### Affected KPIs

- `net_revenue`: min 49245.4, max 85536.12, average 66354.95 (4 anomaly event(s))
- `checkout_failure_rate`: min 0.017, max 0.0201, average 0.0183 (1 anomaly event(s))

### Recommended Next Steps

- Inspect checkout errors and dependency health for the incident window.
- Confirm checkout failure rate and revenue have returned to baseline.

## INC-035: Support Ticket Spike

- **Date range:** 2026-01-12 to 2026-01-14
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `support_ticket_spike`
- **Related anomalies:** `revenue_drop`

### Evidence

- 2 anomaly event(s) across 2 anomaly type(s) were grouped within 2026-01-12 to 2026-01-14.

### Affected KPIs

- `net_revenue`: min 55343.67, max 63433.8, average 60090.8033 (1 anomaly event(s))
- `support_ticket_count`: min 144.0, max 187.0, average 164.3333 (1 anomaly event(s))

### Recommended Next Steps

- Review support ticket categories to identify the dominant customer issue.
- Confirm ticket volume returns to baseline after remediation.

## INC-036: Revenue Drop

- **Date range:** 2026-01-19 to 2026-01-20
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** `support_ticket_spike`

### Evidence

- 2 anomaly event(s) across 2 anomaly type(s) were grouped within 2026-01-19 to 2026-01-20.

### Affected KPIs

- `net_revenue`: min 53386.07, max 58990.78, average 56188.425 (1 anomaly event(s))
- `support_ticket_count`: min 161.0, max 189.0, average 175.0 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-037: Deployment-related checkout incident

- **Date range:** 2026-01-26 to 2026-01-28
- **Likely cause:** Likely deployment-related checkout incident
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `latency_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Latency and checkout failure anomalies occurred together from 2026-01-26 to 2026-01-28.
- 2 failed or rollback deployment event(s) occurred within the investigation window.

### Affected KPIs

- `net_revenue`: min 42119.47, max 50861.94, average 45110.5667 (3 anomaly event(s))
- `checkout_failure_rate`: min 0.0186, max 0.075, average 0.0538 (2 anomaly event(s))
- `avg_api_latency_ms`: min 204.95, max 398.61, average 331.8867 (2 anomaly event(s))
- `support_ticket_count`: min 173.0, max 284.0, average 239.0 (2 anomaly event(s))
- `conversion_rate`: min 0.0349, max 0.0437, average 0.0387 (0 anomaly event(s))

### Recommended Next Steps

- Review the failed checkout deployment, dependency changes, and rollback results.
- Validate checkout success rate, API latency, and revenue after rollback.
- Add deployment health gates for checkout latency and failure rate.

## INC-038: Revenue Drop

- **Date range:** 2026-02-03 to 2026-02-03
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-02-03 to 2026-02-03.

### Affected KPIs

- `net_revenue`: min 54284.91, max 54284.91, average 54284.91 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-039: Logistics disruption incident

- **Date range:** 2026-02-09 to 2026-02-18
- **Likely cause:** Likely logistics disruption incident
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `revenue_drop`, `support_ticket_spike`

### Evidence

- Shipping delay anomalies occurred from 2026-02-09 to 2026-02-18.
- Delivery complaints reached 153.00 versus a prior average of 33.86.

### Affected KPIs

- `net_revenue`: min 45078.65, max 77069.6, average 57915.594 (4 anomaly event(s))
- `shipping_delay_rate`: min 0.1052, max 0.1281, average 0.1159 (8 anomaly event(s))
- `support_ticket_count`: min 263.0, max 328.0, average 278.8 (9 anomaly event(s))
- `delivery_complaints`: min 102.0, max 153.0, average 120.3 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-040: Revenue Drop

- **Date range:** 2026-03-02 to 2026-03-03
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 2 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-03-02 to 2026-03-03.

### Affected KPIs

- `net_revenue`: min 48293.97, max 53626.21, average 50960.09 (2 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-041: Revenue Drop

- **Date range:** 2026-03-09 to 2026-03-09
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-03-09 to 2026-03-09.

### Affected KPIs

- `net_revenue`: min 58848.77, max 58848.77, average 58848.77 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-042: Logistics disruption incident

- **Date range:** 2026-03-13 to 2026-03-17
- **Likely cause:** Likely logistics disruption incident
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `checkout_failure_spike`, `support_ticket_spike`

### Evidence

- Shipping delay anomalies occurred from 2026-03-13 to 2026-03-17.
- Delivery complaints reached 44.00 versus a prior average of 27.71.

### Affected KPIs

- `support_ticket_count`: min 141.0, max 185.0, average 171.0 (2 anomaly event(s))
- `checkout_failure_rate`: min 0.0166, max 0.0209, average 0.0184 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.0542, max 0.0698, average 0.0607 (1 anomaly event(s))
- `delivery_complaints`: min 21.0, max 44.0, average 34.6 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-043: Revenue Drop

- **Date range:** 2026-03-23 to 2026-03-23
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-03-23 to 2026-03-23.

### Affected KPIs

- `net_revenue`: min 56966.96, max 56966.96, average 56966.96 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-044: Support Ticket Spike

- **Date range:** 2026-03-30 to 2026-04-02
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `support_ticket_spike`
- **Related anomalies:** `revenue_drop`

### Evidence

- 4 anomaly event(s) across 2 anomaly type(s) were grouped within 2026-03-30 to 2026-04-02.

### Affected KPIs

- `net_revenue`: min 56332.76, max 68663.15, average 60712.6225 (3 anomaly event(s))
- `support_ticket_count`: min 164.0, max 206.0, average 179.5 (1 anomaly event(s))

### Recommended Next Steps

- Review support ticket categories to identify the dominant customer issue.
- Confirm ticket volume returns to baseline after remediation.

## INC-045: Deployment-related checkout incident

- **Date range:** 2026-04-13 to 2026-04-21
- **Likely cause:** Likely deployment-related checkout incident
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `latency_spike`, `revenue_drop`, `shipping_delay_spike`, `support_ticket_spike`

### Evidence

- Latency and checkout failure anomalies occurred together from 2026-04-13 to 2026-04-21.
- 2 failed or rollback deployment event(s) occurred within the investigation window.

### Affected KPIs

- `net_revenue`: min 22240.78, max 79260.17, average 45398.3344 (6 anomaly event(s))
- `checkout_failure_rate`: min 0.0175, max 0.1728, average 0.0985 (5 anomaly event(s))
- `avg_api_latency_ms`: min 204.56, max 733.8, average 490.3289 (5 anomaly event(s))
- `support_ticket_count`: min 139.0, max 439.0, average 293.7778 (5 anomaly event(s))
- `shipping_delay_rate`: min 0.0553, max 0.0732, average 0.0631 (1 anomaly event(s))
- `conversion_rate`: min 0.0197, max 0.0432, average 0.0315 (0 anomaly event(s))

### Recommended Next Steps

- Review the failed checkout deployment, dependency changes, and rollback results.
- Validate checkout success rate, API latency, and revenue after rollback.
- Add deployment health gates for checkout latency and failure rate.

## INC-046: Inventory shortage incident

- **Date range:** 2026-05-04 to 2026-05-30
- **Likely cause:** Likely inventory shortage incident
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `latency_spike`, `revenue_drop`, `shipping_delay_spike`, `support_ticket_spike`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2026-05-04 to 2026-05-30.
- Lost sales units reached 130.00 during the incident.

### Affected KPIs

- `net_revenue`: min 47213.13, max 95761.81, average 68093.4626 (10 anomaly event(s))
- `avg_api_latency_ms`: min 197.54, max 215.99, average 207.7707 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.0579, max 0.0738, average 0.0638 (3 anomaly event(s))
- `stockout_units`: min 0.0, max 129.0, average 43.3333 (11 anomaly event(s))
- `support_ticket_count`: min 143.0, max 191.0, average 169.1481 (2 anomaly event(s))
- `lost_sales_units`: min 0.0, max 130.0, average 40.3333 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-047: Latency Spike

- **Date range:** 2026-06-08 to 2026-06-08
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `latency_spike`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-06-08 to 2026-06-08.

### Affected KPIs

- `avg_api_latency_ms`: min 216.8, max 216.8, average 216.8 (1 anomaly event(s))

### Recommended Next Steps

- Inspect service latency by endpoint and dependency.
- Confirm latency has returned to its rolling baseline.

## INC-048: Logistics disruption incident

- **Date range:** 2026-06-15 to 2026-06-16
- **Likely cause:** Likely logistics disruption incident
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `revenue_drop`

### Evidence

- Shipping delay anomalies occurred from 2026-06-15 to 2026-06-16.
- Delivery complaints reached 48.00 versus a prior average of 29.86.

### Affected KPIs

- `net_revenue`: min 60182.65, max 68437.91, average 64310.28 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.0643, max 0.078, average 0.0711 (1 anomaly event(s))
- `delivery_complaints`: min 41.0, max 48.0, average 44.5 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-049: Logistics disruption incident

- **Date range:** 2026-06-21 to 2026-06-29
- **Likely cause:** Likely logistics disruption incident
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `checkout_failure_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Shipping delay anomalies occurred from 2026-06-21 to 2026-06-29.
- Delivery complaints reached 117.00 versus a prior average of 31.43.

### Affected KPIs

- `checkout_failure_rate`: min 0.0165, max 0.0206, average 0.0184 (1 anomaly event(s))
- `net_revenue`: min 49521.87, max 89125.02, average 72065.2167 (3 anomaly event(s))
- `shipping_delay_rate`: min 0.0636, max 0.1277, average 0.1088 (6 anomaly event(s))
- `support_ticket_count`: min 170.0, max 269.0, average 230.4444 (6 anomaly event(s))
- `delivery_complaints`: min 32.0, max 117.0, average 84.5556 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-050: Checkout Failure Spike

- **Date range:** 2026-07-11 to 2026-07-14
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `revenue_drop`

### Evidence

- 3 anomaly event(s) across 2 anomaly type(s) were grouped within 2026-07-11 to 2026-07-14.

### Affected KPIs

- `checkout_failure_rate`: min 0.0173, max 0.0205, average 0.0184 (1 anomaly event(s))
- `net_revenue`: min 57601.79, max 89511.9, average 70331.2925 (2 anomaly event(s))

### Recommended Next Steps

- Inspect checkout errors and dependency health for the incident window.
- Confirm checkout failure rate and revenue have returned to baseline.

## INC-051: Revenue Drop

- **Date range:** 2026-07-20 to 2026-07-21
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 2 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-07-20 to 2026-07-21.

### Affected KPIs

- `net_revenue`: min 55466.06, max 65717.59, average 60591.825 (2 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-052: Deployment-related checkout incident

- **Date range:** 2026-08-03 to 2026-08-04
- **Likely cause:** Likely deployment-related checkout incident
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `latency_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Latency and checkout failure anomalies occurred together from 2026-08-03 to 2026-08-04.
- 2 failed or rollback deployment event(s) occurred within the investigation window.

### Affected KPIs

- `checkout_failure_rate`: min 0.0682, max 0.1013, average 0.0847 (2 anomaly event(s))
- `avg_api_latency_ms`: min 392.15, max 509.74, average 450.945 (2 anomaly event(s))
- `net_revenue`: min 37153.12, max 38432.38, average 37792.75 (2 anomaly event(s))
- `support_ticket_count`: min 272.0, max 313.0, average 292.5 (2 anomaly event(s))
- `conversion_rate`: min 0.0272, max 0.0335, average 0.0304 (0 anomaly event(s))

### Recommended Next Steps

- Review the failed checkout deployment, dependency changes, and rollback results.
- Validate checkout success rate, API latency, and revenue after rollback.
- Add deployment health gates for checkout latency and failure rate.

## INC-053: Revenue Drop

- **Date range:** 2026-08-17 to 2026-08-18
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 2 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-08-17 to 2026-08-18.

### Affected KPIs

- `net_revenue`: min 50088.55, max 58680.46, average 54384.505 (2 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-054: Revenue Drop

- **Date range:** 2026-08-24 to 2026-08-25
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** `support_ticket_spike`

### Evidence

- 2 anomaly event(s) across 2 anomaly type(s) were grouped within 2026-08-24 to 2026-08-25.

### Affected KPIs

- `net_revenue`: min 61759.31, max 64584.09, average 63171.7 (1 anomaly event(s))
- `support_ticket_count`: min 146.0, max 184.0, average 165.0 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-055: Inventory shortage incident

- **Date range:** 2026-09-01 to 2026-09-24
- **Likely cause:** Likely inventory shortage incident
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `checkout_failure_spike`, `revenue_drop`, `shipping_delay_spike`, `support_ticket_spike`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2026-09-01 to 2026-09-24.
- Lost sales units reached 178.00 during the incident.

### Affected KPIs

- `net_revenue`: min 32242.51, max 90618.66, average 59179.59 (11 anomaly event(s))
- `support_ticket_count`: min 139.0, max 237.0, average 178.7083 (3 anomaly event(s))
- `shipping_delay_rate`: min 0.056, max 0.0746, average 0.064 (3 anomaly event(s))
- `stockout_units`: min 0.0, max 139.0, average 76.1667 (15 anomaly event(s))
- `checkout_failure_rate`: min 0.016, max 0.0201, average 0.018 (1 anomaly event(s))
- `lost_sales_units`: min 0.0, max 178.0, average 82.5833 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-056: Logistics disruption incident

- **Date range:** 2026-10-03 to 2026-10-14
- **Likely cause:** Likely logistics disruption incident
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `checkout_failure_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Shipping delay anomalies occurred from 2026-10-03 to 2026-10-14.
- Delivery complaints reached 165.00 versus a prior average of 32.29.

### Affected KPIs

- `checkout_failure_rate`: min 0.0166, max 0.0197, average 0.0182 (1 anomaly event(s))
- `net_revenue`: min 44608.19, max 95497.0, average 63679.7817 (7 anomaly event(s))
- `shipping_delay_rate`: min 0.0658, max 0.2306, average 0.1817 (9 anomaly event(s))
- `support_ticket_count`: min 159.0, max 321.0, average 277.1667 (8 anomaly event(s))
- `delivery_complaints`: min 29.0, max 165.0, average 129.25 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-057: Revenue Drop

- **Date range:** 2026-10-21 to 2026-10-21
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-10-21 to 2026-10-21.

### Affected KPIs

- `net_revenue`: min 54860.75, max 54860.75, average 54860.75 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-058: Deployment-related checkout incident

- **Date range:** 2026-11-06 to 2026-11-19
- **Likely cause:** Likely deployment-related checkout incident
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `latency_spike`, `revenue_drop`, `shipping_delay_spike`, `support_ticket_spike`

### Evidence

- Latency and checkout failure anomalies occurred together from 2026-11-06 to 2026-11-19.
- 2 failed or rollback deployment event(s) occurred within the investigation window.

### Affected KPIs

- `shipping_delay_rate`: min 0.0552, max 0.0794, average 0.0683 (3 anomaly event(s))
- `net_revenue`: min 44661.09, max 122748.38, average 85956.3293 (5 anomaly event(s))
- `support_ticket_count`: min 150.0, max 376.0, average 223.4286 (6 anomaly event(s))
- `checkout_failure_rate`: min 0.0161, max 0.148, average 0.0478 (4 anomaly event(s))
- `avg_api_latency_ms`: min 199.51, max 631.56, average 307.2371 (4 anomaly event(s))
- `conversion_rate`: min 0.0245, max 0.0487, average 0.0399 (0 anomaly event(s))

### Recommended Next Steps

- Review the failed checkout deployment, dependency changes, and rollback results.
- Validate checkout success rate, API latency, and revenue after rollback.
- Add deployment health gates for checkout latency and failure rate.

## INC-059: Shipping Delay Spike

- **Date range:** 2026-11-23 to 2026-11-23
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-11-23 to 2026-11-23.

### Affected KPIs

- `shipping_delay_rate`: min 0.0811, max 0.0811, average 0.0811 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-060: Revenue Drop

- **Date range:** 2026-12-02 to 2026-12-02
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-12-02 to 2026-12-02.

### Affected KPIs

- `net_revenue`: min 75858.75, max 75858.75, average 75858.75 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-061: Shipping Delay Spike

- **Date range:** 2026-12-07 to 2026-12-07
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-12-07 to 2026-12-07.

### Affected KPIs

- `shipping_delay_rate`: min 0.0773, max 0.0773, average 0.0773 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-062: Shipping Delay Spike

- **Date range:** 2026-12-12 to 2026-12-12
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-12-12 to 2026-12-12.

### Affected KPIs

- `shipping_delay_rate`: min 0.0849, max 0.0849, average 0.0849 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-063: Latency Spike

- **Date range:** 2026-12-16 to 2026-12-16
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `latency_spike`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-12-16 to 2026-12-16.

### Affected KPIs

- `avg_api_latency_ms`: min 212.02, max 212.02, average 212.02 (1 anomaly event(s))

### Recommended Next Steps

- Inspect service latency by endpoint and dependency.
- Confirm latency has returned to its rolling baseline.

## INC-064: Latency Spike

- **Date range:** 2026-12-21 to 2026-12-31
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `latency_spike`
- **Related anomalies:** `checkout_failure_spike`, `revenue_drop`, `shipping_delay_spike`, `support_ticket_spike`

### Evidence

- 7 anomaly event(s) across 5 anomaly type(s) were grouped within 2026-12-21 to 2026-12-31.

### Affected KPIs

- `checkout_failure_rate`: min 0.0148, max 0.0194, average 0.0182 (1 anomaly event(s))
- `net_revenue`: min 78900.95, max 116933.38, average 97061.89 (3 anomaly event(s))
- `support_ticket_count`: min 152.0, max 203.0, average 172.8182 (1 anomaly event(s))
- `avg_api_latency_ms`: min 201.76, max 218.72, average 207.2136 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.0574, max 0.082, average 0.0694 (1 anomaly event(s))

### Recommended Next Steps

- Inspect service latency by endpoint and dependency.
- Confirm latency has returned to its rolling baseline.
