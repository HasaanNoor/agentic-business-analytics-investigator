# Deterministic Investigation Summary

Generated from anomaly events grouped with a maximum consecutive-event gap of 3 days.
Total incidents: **69**

## INC-001: Revenue Drop

- **Date range:** 2025-01-12 to 2025-01-16
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** `shipping_delay_spike`

### Evidence

- 3 anomaly event(s) across 2 anomaly type(s) were grouped within 2025-01-12 to 2025-01-16.

### Affected KPIs

- `shipping_delay_rate`: min 0.0594, max 0.0711, average 0.0642 (1 anomaly event(s))
- `net_revenue`: min 36361.73, max 48284.24, average 41500.266 (2 anomaly event(s))

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
- **Related anomalies:** `revenue_drop`

### Evidence

- 3 anomaly event(s) across 2 anomaly type(s) were grouped within 2025-01-25 to 2025-01-29.

### Affected KPIs

- `net_revenue`: min 36094.97, max 50883.67, average 41147.874 (2 anomaly event(s))
- `checkout_failure_rate`: min 0.018, max 0.0207, average 0.0189 (1 anomaly event(s))

### Recommended Next Steps

- Inspect checkout errors and dependency health for the incident window.
- Confirm checkout failure rate and revenue have returned to baseline.

## INC-004: Latency Spike

- **Date range:** 2025-02-03 to 2025-02-05
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `latency_spike`
- **Related anomalies:** None

### Evidence

- 2 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-02-03 to 2025-02-05.

### Affected KPIs

- `avg_api_latency_ms`: min 208.69, max 214.73, average 212.3533 (2 anomaly event(s))

### Recommended Next Steps

- Inspect service latency by endpoint and dependency.
- Confirm latency has returned to its rolling baseline.

## INC-005: Support Ticket Spike

- **Date range:** 2025-02-09 to 2025-02-10
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `support_ticket_spike`
- **Related anomalies:** `revenue_drop`

### Evidence

- 3 anomaly event(s) across 2 anomaly type(s) were grouped within 2025-02-09 to 2025-02-10.

### Affected KPIs

- `support_ticket_count`: min 128.0, max 143.0, average 135.5 (2 anomaly event(s))
- `net_revenue`: min 33602.53, max 59906.98, average 46754.755 (1 anomaly event(s))

### Recommended Next Steps

- Review support ticket categories to identify the dominant customer issue.
- Confirm ticket volume returns to baseline after remediation.

## INC-006: Shipping Delay Spike

- **Date range:** 2025-02-17 to 2025-02-25
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `revenue_drop`

### Evidence

- 6 anomaly event(s) across 2 anomaly type(s) were grouped within 2025-02-17 to 2025-02-25.

### Affected KPIs

- `net_revenue`: min 34381.33, max 54944.34, average 43858.8433 (5 anomaly event(s))
- `shipping_delay_rate`: min 0.0532, max 0.0761, average 0.063 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-007: Latency Spike

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

## INC-008: Deployment-related checkout incident

- **Date range:** 2025-03-17 to 2025-03-23
- **Likely cause:** Likely deployment-related checkout incident
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `latency_spike`, `revenue_drop`, `shipping_delay_spike`, `support_ticket_spike`

### Evidence

- Latency and checkout failure anomalies occurred together from 2025-03-17 to 2025-03-23.
- 2 failed or rollback deployment event(s) occurred within the investigation window.

### Affected KPIs

- `net_revenue`: min 25906.11, max 64146.35, average 41113.6943 (4 anomaly event(s))
- `checkout_failure_rate`: min 0.0156, max 0.1239, average 0.059 (3 anomaly event(s))
- `avg_api_latency_ms`: min 205.94, max 564.89, average 353.22 (3 anomaly event(s))
- `support_ticket_count`: min 136.0, max 310.0, average 212.7143 (3 anomaly event(s))
- `shipping_delay_rate`: min 0.06, max 0.0712, average 0.065 (1 anomaly event(s))
- `conversion_rate`: min 0.0265, max 0.0467, average 0.0368 (0 anomaly event(s))

### Recommended Next Steps

- Review the failed checkout deployment, dependency changes, and rollback results.
- Validate checkout success rate, API latency, and revenue after rollback.
- Add deployment health gates for checkout latency and failure rate.

## INC-009: Revenue Drop

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

## INC-010: Inventory shortage incident

- **Date range:** 2025-04-05 to 2025-04-20
- **Likely cause:** Likely inventory shortage incident
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `revenue_drop`, `shipping_delay_spike`, `support_ticket_spike`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2025-04-05 to 2025-04-20.
- Lost sales units reached 113.00 during the incident.

### Affected KPIs

- `shipping_delay_rate`: min 0.0554, max 0.0692, average 0.0634 (2 anomaly event(s))
- `net_revenue`: min 28393.31, max 66326.54, average 41203.9631 (8 anomaly event(s))
- `stockout_units`: min 0.0, max 109.0, average 60.3125 (11 anomaly event(s))
- `support_ticket_count`: min 133.0, max 187.0, average 159.25 (2 anomaly event(s))
- `lost_sales_units`: min 0.0, max 113.0, average 65.625 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-011: Latency Spike

- **Date range:** 2025-04-25 to 2025-04-25
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `latency_spike`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-04-25 to 2025-04-25.

### Affected KPIs

- `avg_api_latency_ms`: min 215.11, max 215.11, average 215.11 (1 anomaly event(s))

### Recommended Next Steps

- Inspect service latency by endpoint and dependency.
- Confirm latency has returned to its rolling baseline.

## INC-012: Logistics disruption incident

- **Date range:** 2025-05-05 to 2025-05-13
- **Likely cause:** Likely logistics disruption incident
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `revenue_drop`, `support_ticket_spike`

### Evidence

- Shipping delay anomalies occurred from 2025-05-05 to 2025-05-13.
- Delivery complaints reached 127.00 versus a prior average of 29.21.

### Affected KPIs

- `net_revenue`: min 35003.13, max 58425.92, average 44294.3822 (5 anomaly event(s))
- `shipping_delay_rate`: min 0.1415, max 0.1619, average 0.15 (7 anomaly event(s))
- `support_ticket_count`: min 214.0, max 281.0, average 247.2222 (6 anomaly event(s))
- `delivery_complaints`: min 105.0, max 127.0, average 119.2222 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-013: Logistics disruption incident

- **Date range:** 2025-06-02 to 2025-06-04
- **Likely cause:** Likely logistics disruption incident
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `latency_spike`

### Evidence

- Shipping delay anomalies occurred from 2025-06-02 to 2025-06-04.
- Delivery complaints reached 38.00 versus a prior average of 25.21.

### Affected KPIs

- `avg_api_latency_ms`: min 203.12, max 217.71, average 209.63 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.0619, max 0.0695, average 0.0647 (1 anomaly event(s))
- `delivery_complaints`: min 23.0, max 38.0, average 30.3333 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-014: Revenue Drop

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

## INC-015: Revenue Drop

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

## INC-016: Revenue Drop

- **Date range:** 2025-06-24 to 2025-06-24
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-06-24 to 2025-06-24.

### Affected KPIs

- `net_revenue`: min 44366.87, max 44366.87, average 44366.87 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-017: Revenue Drop

- **Date range:** 2025-06-29 to 2025-07-03
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** `checkout_failure_spike`, `shipping_delay_spike`, `support_ticket_spike`

### Evidence

- 6 anomaly event(s) across 4 anomaly type(s) were grouped within 2025-06-29 to 2025-07-03.

### Affected KPIs

- `support_ticket_count`: min 146.0, max 173.0, average 159.4 (2 anomaly event(s))
- `checkout_failure_rate`: min 0.0168, max 0.0214, average 0.0189 (1 anomaly event(s))
- `net_revenue`: min 35001.53, max 64852.2, average 50496.802 (2 anomaly event(s))
- `shipping_delay_rate`: min 0.0564, max 0.0723, average 0.0639 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-018: Latency Spike

- **Date range:** 2025-07-08 to 2025-07-08
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `latency_spike`
- **Related anomalies:** `revenue_drop`

### Evidence

- 2 anomaly event(s) across 2 anomaly type(s) were grouped within 2025-07-08 to 2025-07-08.

### Affected KPIs

- `avg_api_latency_ms`: min 215.87, max 215.87, average 215.87 (1 anomaly event(s))
- `net_revenue`: min 38507.13, max 38507.13, average 38507.13 (1 anomaly event(s))

### Recommended Next Steps

- Inspect service latency by endpoint and dependency.
- Confirm latency has returned to its rolling baseline.

## INC-019: Revenue Drop

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

## INC-020: Deployment-related checkout incident

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

## INC-021: Revenue Drop

- **Date range:** 2025-07-28 to 2025-07-29
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 2 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-07-28 to 2025-07-29.

### Affected KPIs

- `net_revenue`: min 33010.03, max 35349.82, average 34179.925 (2 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-022: Shipping Delay Spike

- **Date range:** 2025-08-04 to 2025-08-04
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-08-04 to 2025-08-04.

### Affected KPIs

- `shipping_delay_rate`: min 0.0548, max 0.0548, average 0.0548 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-023: Inventory shortage incident

- **Date range:** 2025-08-10 to 2025-08-18
- **Likely cause:** Likely inventory shortage incident
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `revenue_drop`, `support_ticket_spike`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2025-08-10 to 2025-08-18.
- Lost sales units reached 92.00 during the incident.

### Affected KPIs

- `support_ticket_count`: min 116.0, max 186.0, average 162.1111 (4 anomaly event(s))
- `net_revenue`: min 33504.76, max 55102.91, average 44479.5922 (4 anomaly event(s))
- `stockout_units`: min 0.0, max 88.0, average 52.4444 (7 anomaly event(s))
- `lost_sales_units`: min 0.0, max 92.0, average 51.8889 (0 anomaly event(s))

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

## INC-025: Shipping Delay Spike

- **Date range:** 2025-09-01 to 2025-09-02
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `revenue_drop`

### Evidence

- 3 anomaly event(s) across 2 anomaly type(s) were grouped within 2025-09-01 to 2025-09-02.

### Affected KPIs

- `net_revenue`: min 35526.8, max 35711.86, average 35619.33 (2 anomaly event(s))
- `shipping_delay_rate`: min 0.0673, max 0.069, average 0.0682 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-026: Revenue Drop

- **Date range:** 2025-09-08 to 2025-09-09
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 2 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-09-08 to 2025-09-09.

### Affected KPIs

- `net_revenue`: min 38084.11, max 41719.83, average 39901.97 (2 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-027: Logistics disruption incident

- **Date range:** 2025-09-15 to 2025-09-18
- **Likely cause:** Likely logistics disruption incident
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `latency_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Shipping delay anomalies occurred from 2025-09-15 to 2025-09-18.
- Delivery complaints reached 69.00 versus a prior average of 31.29.

### Affected KPIs

- `net_revenue`: min 33367.6, max 60787.09, average 46044.42 (2 anomaly event(s))
- `shipping_delay_rate`: min 0.072, max 0.0784, average 0.0753 (2 anomaly event(s))
- `support_ticket_count`: min 185.0, max 218.0, average 200.0 (3 anomaly event(s))
- `avg_api_latency_ms`: min 202.72, max 220.9, average 208.205 (1 anomaly event(s))
- `delivery_complaints`: min 58.0, max 69.0, average 63.0 (0 anomaly event(s))

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

- `net_revenue`: min 40116.25, max 40116.25, average 40116.25 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-029: Revenue Drop

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

## INC-030: Deployment-related checkout incident

- **Date range:** 2025-10-05 to 2025-10-11
- **Likely cause:** Likely deployment-related checkout incident
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `latency_spike`, `revenue_drop`, `shipping_delay_spike`, `support_ticket_spike`

### Evidence

- Latency and checkout failure anomalies occurred together from 2025-10-05 to 2025-10-11.
- 2 failed or rollback deployment event(s) occurred within the investigation window.

### Affected KPIs

- `net_revenue`: min 22658.2, max 51908.47, average 36544.0186 (5 anomaly event(s))
- `shipping_delay_rate`: min 0.0585, max 0.0649, average 0.0619 (1 anomaly event(s))
- `checkout_failure_rate`: min 0.0172, max 0.1503, average 0.0688 (3 anomaly event(s))
- `avg_api_latency_ms`: min 204.75, max 655.44, average 384.2886 (3 anomaly event(s))
- `support_ticket_count`: min 144.0, max 391.0, average 262.1429 (4 anomaly event(s))
- `conversion_rate`: min 0.022, max 0.0473, average 0.0338 (0 anomaly event(s))

### Recommended Next Steps

- Review the failed checkout deployment, dependency changes, and rollback results.
- Validate checkout success rate, API latency, and revenue after rollback.
- Add deployment health gates for checkout latency and failure rate.

## INC-031: Logistics disruption incident

- **Date range:** 2025-10-18 to 2025-10-18
- **Likely cause:** Likely logistics disruption incident
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** None

### Evidence

- Shipping delay anomalies occurred from 2025-10-18 to 2025-10-18.
- Delivery complaints reached 45.00 versus a prior average of 28.79.

### Affected KPIs

- `shipping_delay_rate`: min 0.0673, max 0.0673, average 0.0673 (1 anomaly event(s))
- `delivery_complaints`: min 45.0, max 45.0, average 45.0 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-032: Support Ticket Spike

- **Date range:** 2025-10-29 to 2025-10-29
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `support_ticket_spike`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-10-29 to 2025-10-29.

### Affected KPIs

- `support_ticket_count`: min 149.0, max 149.0, average 149.0 (1 anomaly event(s))

### Recommended Next Steps

- Review support ticket categories to identify the dominant customer issue.
- Confirm ticket volume returns to baseline after remediation.

## INC-033: Revenue Drop

- **Date range:** 2025-11-10 to 2025-11-10
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-11-10 to 2025-11-10.

### Affected KPIs

- `net_revenue`: min 49538.39, max 49538.39, average 49538.39 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-034: Shipping Delay Spike

- **Date range:** 2025-11-16 to 2025-11-17
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `checkout_failure_spike`, `revenue_drop`

### Evidence

- 3 anomaly event(s) across 3 anomaly type(s) were grouped within 2025-11-16 to 2025-11-17.

### Affected KPIs

- `checkout_failure_rate`: min 0.0188, max 0.0192, average 0.019 (1 anomaly event(s))
- `net_revenue`: min 47369.5, max 75787.99, average 61578.745 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.0603, max 0.0657, average 0.063 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-035: Support Ticket Spike

- **Date range:** 2025-11-24 to 2025-11-25
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `support_ticket_spike`
- **Related anomalies:** `revenue_drop`

### Evidence

- 2 anomaly event(s) across 2 anomaly type(s) were grouped within 2025-11-24 to 2025-11-25.

### Affected KPIs

- `support_ticket_count`: min 168.0, max 174.0, average 171.0 (1 anomaly event(s))
- `net_revenue`: min 50122.48, max 60680.78, average 55401.63 (1 anomaly event(s))

### Recommended Next Steps

- Review support ticket categories to identify the dominant customer issue.
- Confirm ticket volume returns to baseline after remediation.

## INC-036: Inventory shortage incident

- **Date range:** 2025-12-01 to 2025-12-16
- **Likely cause:** Likely inventory shortage incident
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `revenue_drop`, `shipping_delay_spike`, `support_ticket_spike`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2025-12-01 to 2025-12-16.
- Lost sales units reached 190.00 during the incident.

### Affected KPIs

- `net_revenue`: min 28434.33, max 62556.48, average 43789.6631 (9 anomaly event(s))
- `shipping_delay_rate`: min 0.051, max 0.0759, average 0.0661 (1 anomaly event(s))
- `stockout_units`: min 0.0, max 135.0, average 97.5 (14 anomaly event(s))
- `support_ticket_count`: min 153.0, max 210.0, average 178.75 (5 anomaly event(s))
- `lost_sales_units`: min 0.0, max 190.0, average 134.0625 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-037: Shipping Delay Spike

- **Date range:** 2025-12-25 to 2025-12-25
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2025-12-25 to 2025-12-25.

### Affected KPIs

- `shipping_delay_rate`: min 0.0681, max 0.0681, average 0.0681 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-038: Checkout Failure Spike

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

## INC-039: Revenue Drop

- **Date range:** 2026-01-12 to 2026-01-12
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-01-12 to 2026-01-12.

### Affected KPIs

- `net_revenue`: min 55343.67, max 55343.67, average 55343.67 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-040: Revenue Drop

- **Date range:** 2026-01-19 to 2026-01-19
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-01-19 to 2026-01-19.

### Affected KPIs

- `net_revenue`: min 53386.07, max 53386.07, average 53386.07 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-041: Deployment-related checkout incident

- **Date range:** 2026-01-23 to 2026-01-28
- **Likely cause:** Likely deployment-related checkout incident
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `latency_spike`, `revenue_drop`, `shipping_delay_spike`, `support_ticket_spike`

### Evidence

- Latency and checkout failure anomalies occurred together from 2026-01-23 to 2026-01-28.
- 2 failed or rollback deployment event(s) occurred within the investigation window.

### Affected KPIs

- `shipping_delay_rate`: min 0.0534, max 0.0681, average 0.0617 (1 anomaly event(s))
- `net_revenue`: min 42119.47, max 87086.7, average 61046.4917 (3 anomaly event(s))
- `checkout_failure_rate`: min 0.0158, max 0.075, average 0.0354 (2 anomaly event(s))
- `avg_api_latency_ms`: min 202.19, max 398.61, average 269.6533 (2 anomaly event(s))
- `support_ticket_count`: min 149.0, max 284.0, average 205.8333 (1 anomaly event(s))
- `conversion_rate`: min 0.0349, max 0.0446, average 0.0406 (0 anomaly event(s))

### Recommended Next Steps

- Review the failed checkout deployment, dependency changes, and rollback results.
- Validate checkout success rate, API latency, and revenue after rollback.
- Add deployment health gates for checkout latency and failure rate.

## INC-042: Revenue Drop

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

## INC-043: Logistics disruption incident

- **Date range:** 2026-02-09 to 2026-02-17
- **Likely cause:** Likely logistics disruption incident
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `revenue_drop`, `support_ticket_spike`

### Evidence

- Shipping delay anomalies occurred from 2026-02-09 to 2026-02-17.
- Delivery complaints reached 136.00 versus a prior average of 33.86.

### Affected KPIs

- `net_revenue`: min 45078.65, max 77069.6, average 58123.1022 (4 anomaly event(s))
- `shipping_delay_rate`: min 0.1052, max 0.1281, average 0.1153 (6 anomaly event(s))
- `support_ticket_count`: min 263.0, max 287.0, average 273.3333 (8 anomaly event(s))
- `delivery_complaints`: min 102.0, max 136.0, average 116.6667 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-044: Revenue Drop

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

## INC-045: Revenue Drop

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

## INC-046: Checkout Failure Spike

- **Date range:** 2026-03-15 to 2026-03-15
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-03-15 to 2026-03-15.

### Affected KPIs

- `checkout_failure_rate`: min 0.0209, max 0.0209, average 0.0209 (1 anomaly event(s))

### Recommended Next Steps

- Inspect checkout errors and dependency health for the incident window.
- Confirm checkout failure rate and revenue have returned to baseline.

## INC-047: Shipping Delay Spike

- **Date range:** 2026-03-23 to 2026-03-24
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `revenue_drop`

### Evidence

- 2 anomaly event(s) across 2 anomaly type(s) were grouped within 2026-03-23 to 2026-03-24.

### Affected KPIs

- `net_revenue`: min 56966.96, max 64817.0, average 60891.98 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.055, max 0.0659, average 0.0605 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-048: Shipping Delay Spike

- **Date range:** 2026-03-28 to 2026-04-01
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `revenue_drop`, `support_ticket_spike`

### Evidence

- 5 anomaly event(s) across 3 anomaly type(s) were grouped within 2026-03-28 to 2026-04-01.

### Affected KPIs

- `shipping_delay_rate`: min 0.0516, max 0.07, average 0.0624 (1 anomaly event(s))
- `net_revenue`: min 56332.76, max 112430.23, average 72956.65 (3 anomaly event(s))
- `support_ticket_count`: min 164.0, max 181.0, average 171.8 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-049: Deployment-related checkout incident

- **Date range:** 2026-04-13 to 2026-04-18
- **Likely cause:** Likely deployment-related checkout incident
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `latency_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Latency and checkout failure anomalies occurred together from 2026-04-13 to 2026-04-18.
- 2 failed or rollback deployment event(s) occurred within the investigation window.

### Affected KPIs

- `net_revenue`: min 22240.78, max 59551.86, average 32951.85 (6 anomaly event(s))
- `checkout_failure_rate`: min 0.0184, max 0.1728, average 0.1385 (5 anomaly event(s))
- `avg_api_latency_ms`: min 204.56, max 733.8, average 629.99 (5 anomaly event(s))
- `support_ticket_count`: min 162.0, max 439.0, average 361.1667 (5 anomaly event(s))
- `conversion_rate`: min 0.0197, max 0.0424, average 0.0264 (0 anomaly event(s))

### Recommended Next Steps

- Review the failed checkout deployment, dependency changes, and rollback results.
- Validate checkout success rate, API latency, and revenue after rollback.
- Add deployment health gates for checkout latency and failure rate.

## INC-050: Latency Spike

- **Date range:** 2026-05-04 to 2026-05-05
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `latency_spike`
- **Related anomalies:** `revenue_drop`

### Evidence

- 2 anomaly event(s) across 2 anomaly type(s) were grouped within 2026-05-04 to 2026-05-05.

### Affected KPIs

- `net_revenue`: min 62606.93, max 70014.3, average 66310.615 (1 anomaly event(s))
- `avg_api_latency_ms`: min 209.3, max 215.99, average 212.645 (1 anomaly event(s))

### Recommended Next Steps

- Inspect service latency by endpoint and dependency.
- Confirm latency has returned to its rolling baseline.

## INC-051: Inventory shortage incident

- **Date range:** 2026-05-09 to 2026-05-30
- **Likely cause:** Likely inventory shortage incident
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `revenue_drop`, `shipping_delay_spike`, `support_ticket_spike`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2026-05-09 to 2026-05-30.
- Lost sales units reached 130.00 during the incident.

### Affected KPIs

- `shipping_delay_rate`: min 0.0579, max 0.0738, average 0.0639 (2 anomaly event(s))
- `net_revenue`: min 47213.13, max 95761.81, average 66819.1173 (9 anomaly event(s))
- `support_ticket_count`: min 148.0, max 191.0, average 170.0455 (3 anomaly event(s))
- `stockout_units`: min 0.0, max 129.0, average 53.1818 (11 anomaly event(s))
- `lost_sales_units`: min 0.0, max 130.0, average 49.5 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-052: Latency Spike

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

## INC-053: Revenue Drop

- **Date range:** 2026-06-15 to 2026-06-15
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-06-15 to 2026-06-15.

### Affected KPIs

- `net_revenue`: min 60182.65, max 60182.65, average 60182.65 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-054: Logistics disruption incident

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
- `shipping_delay_rate`: min 0.0636, max 0.1277, average 0.1088 (7 anomaly event(s))
- `support_ticket_count`: min 170.0, max 269.0, average 230.4444 (7 anomaly event(s))
- `delivery_complaints`: min 32.0, max 117.0, average 84.5556 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-055: Checkout Failure Spike

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

## INC-056: Revenue Drop

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

## INC-057: Deployment-related checkout incident

- **Date range:** 2026-08-01 to 2026-08-04
- **Likely cause:** Likely deployment-related checkout incident
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `latency_spike`, `revenue_drop`, `shipping_delay_spike`, `support_ticket_spike`

### Evidence

- Latency and checkout failure anomalies occurred together from 2026-08-01 to 2026-08-04.
- 2 failed or rollback deployment event(s) occurred within the investigation window.

### Affected KPIs

- `shipping_delay_rate`: min 0.0595, max 0.0689, average 0.066 (1 anomaly event(s))
- `support_ticket_count`: min 165.0, max 313.0, average 232.5 (3 anomaly event(s))
- `checkout_failure_rate`: min 0.0178, max 0.1013, average 0.0515 (2 anomaly event(s))
- `avg_api_latency_ms`: min 208.44, max 509.74, average 330.3675 (2 anomaly event(s))
- `net_revenue`: min 37153.12, max 91543.42, average 63852.3625 (2 anomaly event(s))
- `conversion_rate`: min 0.0272, max 0.0494, average 0.038 (0 anomaly event(s))

### Recommended Next Steps

- Review the failed checkout deployment, dependency changes, and rollback results.
- Validate checkout success rate, API latency, and revenue after rollback.
- Add deployment health gates for checkout latency and failure rate.

## INC-058: Shipping Delay Spike

- **Date range:** 2026-08-14 to 2026-08-18
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `revenue_drop`

### Evidence

- 4 anomaly event(s) across 2 anomaly type(s) were grouped within 2026-08-14 to 2026-08-18.

### Affected KPIs

- `shipping_delay_rate`: min 0.0573, max 0.0653, average 0.0614 (2 anomaly event(s))
- `net_revenue`: min 50088.55, max 88595.9, average 71360.41 (2 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-059: Support Ticket Spike

- **Date range:** 2026-08-23 to 2026-08-24
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `support_ticket_spike`
- **Related anomalies:** `revenue_drop`

### Evidence

- 2 anomaly event(s) across 2 anomaly type(s) were grouped within 2026-08-23 to 2026-08-24.

### Affected KPIs

- `support_ticket_count`: min 146.0, max 167.0, average 156.5 (1 anomaly event(s))
- `net_revenue`: min 61759.31, max 83558.15, average 72658.73 (1 anomaly event(s))

### Recommended Next Steps

- Review support ticket categories to identify the dominant customer issue.
- Confirm ticket volume returns to baseline after remediation.

## INC-060: Revenue Drop

- **Date range:** 2026-09-01 to 2026-09-01
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `revenue_drop`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-09-01 to 2026-09-01.

### Affected KPIs

- `net_revenue`: min 61040.5, max 61040.5, average 61040.5 (1 anomaly event(s))

### Recommended Next Steps

- Review conversion, checkout, inventory, and logistics signals for revenue impact.
- Monitor net revenue against its rolling baseline.

## INC-061: Inventory shortage incident

- **Date range:** 2026-09-07 to 2026-09-23
- **Likely cause:** Likely inventory shortage incident
- **Main anomaly:** `inventory_shortage_period`
- **Related anomalies:** `checkout_failure_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Inventory shortage and revenue drop anomalies overlapped from 2026-09-07 to 2026-09-23.
- Lost sales units reached 178.00 during the incident.

### Affected KPIs

- `net_revenue`: min 32242.51, max 79740.26, average 51200.4547 (10 anomaly event(s))
- `stockout_units`: min 0.0, max 139.0, average 107.5294 (15 anomaly event(s))
- `support_ticket_count`: min 155.0, max 237.0, average 182.5294 (2 anomaly event(s))
- `checkout_failure_rate`: min 0.016, max 0.0201, average 0.0181 (1 anomaly event(s))
- `lost_sales_units`: min 0.0, max 178.0, average 116.5882 (0 anomaly event(s))

### Recommended Next Steps

- Prioritize replenishment for stocked-out products.
- Review demand forecasts, reorder points, and supplier lead times.
- Track lost sales and net revenue until inventory availability recovers.

## INC-062: Shipping Delay Spike

- **Date range:** 2026-09-28 to 2026-09-28
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-09-28 to 2026-09-28.

### Affected KPIs

- `shipping_delay_rate`: min 0.0605, max 0.0605, average 0.0605 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-063: Logistics disruption incident

- **Date range:** 2026-10-02 to 2026-10-14
- **Likely cause:** Likely logistics disruption incident
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `checkout_failure_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Shipping delay anomalies occurred from 2026-10-02 to 2026-10-14.
- Delivery complaints reached 165.00 versus a prior average of 32.86.

### Affected KPIs

- `shipping_delay_rate`: min 0.0603, max 0.2306, average 0.1724 (10 anomaly event(s))
- `checkout_failure_rate`: min 0.0166, max 0.0197, average 0.0182 (1 anomaly event(s))
- `net_revenue`: min 44608.19, max 95497.0, average 64526.8038 (7 anomaly event(s))
- `support_ticket_count`: min 150.0, max 321.0, average 267.3846 (7 anomaly event(s))
- `delivery_complaints`: min 24.0, max 165.0, average 121.1538 (0 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and prioritize delayed deliveries.
- Monitor shipping delay rate and delivery complaints until both return to baseline.

## INC-064: Revenue Drop

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

## INC-065: Shipping Delay Spike

- **Date range:** 2026-11-07 to 2026-11-09
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** `revenue_drop`, `support_ticket_spike`

### Evidence

- 3 anomaly event(s) across 3 anomaly type(s) were grouped within 2026-11-07 to 2026-11-09.

### Affected KPIs

- `support_ticket_count`: min 168.0, max 190.0, average 176.0 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.0552, max 0.0689, average 0.0626 (1 anomaly event(s))
- `net_revenue`: min 67805.4, max 122748.38, average 97765.6767 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-066: Deployment-related checkout incident

- **Date range:** 2026-11-16 to 2026-11-19
- **Likely cause:** Likely deployment-related checkout incident
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `latency_spike`, `revenue_drop`, `support_ticket_spike`

### Evidence

- Latency and checkout failure anomalies occurred together from 2026-11-16 to 2026-11-19.
- 2 failed or rollback deployment event(s) occurred within the investigation window.

### Affected KPIs

- `checkout_failure_rate`: min 0.086, max 0.148, average 0.1217 (4 anomaly event(s))
- `avg_api_latency_ms`: min 445.12, max 631.56, average 561.43 (4 anomaly event(s))
- `net_revenue`: min 44661.09, max 56544.32, average 49736.84 (4 anomaly event(s))
- `support_ticket_count`: min 308.0, max 376.0, average 354.0 (4 anomaly event(s))
- `conversion_rate`: min 0.0245, max 0.036, average 0.031 (0 anomaly event(s))

### Recommended Next Steps

- Review the failed checkout deployment, dependency changes, and rollback results.
- Validate checkout success rate, API latency, and revenue after rollback.
- Add deployment health gates for checkout latency and failure rate.

## INC-067: Shipping Delay Spike

- **Date range:** 2026-11-27 to 2026-11-27
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `shipping_delay_spike`
- **Related anomalies:** None

### Evidence

- 1 anomaly event(s) across 1 anomaly type(s) were grouped within 2026-11-27 to 2026-11-27.

### Affected KPIs

- `shipping_delay_rate`: min 0.0677, max 0.0677, average 0.0677 (1 anomaly event(s))

### Recommended Next Steps

- Review carrier performance and delayed shipment queues.
- Notify affected customers and monitor delivery complaints.

## INC-068: Revenue Drop

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

## INC-069: Latency Spike

- **Date range:** 2026-12-16 to 2026-12-31
- **Likely cause:** No known deterministic root-cause pattern matched
- **Main anomaly:** `latency_spike`
- **Related anomalies:** `checkout_failure_spike`, `revenue_drop`, `shipping_delay_spike`, `support_ticket_spike`

### Evidence

- 9 anomaly event(s) across 5 anomaly type(s) were grouped within 2026-12-16 to 2026-12-31.

### Affected KPIs

- `avg_api_latency_ms`: min 201.76, max 218.72, average 207.3212 (2 anomaly event(s))
- `support_ticket_count`: min 145.0, max 203.0, average 171.25 (2 anomaly event(s))
- `checkout_failure_rate`: min 0.0148, max 0.0194, average 0.0179 (1 anomaly event(s))
- `net_revenue`: min 78900.95, max 123641.42, average 101834.2719 (3 anomaly event(s))
- `shipping_delay_rate`: min 0.0574, max 0.082, average 0.0687 (1 anomaly event(s))

### Recommended Next Steps

- Inspect service latency by endpoint and dependency.
- Confirm latency has returned to its rolling baseline.
