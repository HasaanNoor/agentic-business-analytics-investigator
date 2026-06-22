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

- `net_revenue`: min 36361.73, max 40917.99, average 38639.86 (1 anomaly event(s))
- `checkout_failure_rate`: min 0.018, max 0.0181, average 0.0181 (1 anomaly event(s))

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

- `avg_api_latency_ms`: min 199.13, max 209.01, average 204.57 (2 anomaly event(s))
- `net_revenue`: min 32182.47, max 44506.34, average 40173.03 (1 anomaly event(s))

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

- `net_revenue`: min 38518.7, max 50563.99, average 43732.84 (2 anomaly event(s))
- `support_ticket_count`: min 195.0, max 206.0, average 200.3333 (1 anomaly event(s))

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

- `net_revenue`: min 33602.53, max 33602.53, average 33602.53 (1 anomaly event(s))

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

- `shipping_delay_rate`: min 0.0584, max 0.0584, average 0.0584 (1 anomaly event(s))

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

- `shipping_delay_rate`: min 0.0722, max 0.0722, average 0.0722 (1 anomaly event(s))

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

- `avg_api_latency_ms`: min 202.76, max 212.48, average 207.62 (1 anomaly event(s))
- `net_revenue`: min 36002.54, max 38982.52, average 37492.53 (2 anomaly event(s))

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

- `checkout_failure_rate`: min 0.0995, max 0.1239, average 0.1139 (3 anomaly event(s))
- `avg_api_latency_ms`: min 510.83, max 564.89, average 546.1333 (3 anomaly event(s))
- `net_revenue`: min 25906.11, max 27830.67, average 26772.3333 (3 anomaly event(s))
- `support_ticket_count`: min 310.0, max 353.0, average 332.0 (3 anomaly event(s))
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

- `net_revenue`: min 43282.0, max 43282.0, average 43282.0 (1 anomaly event(s))

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

- `net_revenue`: min 41310.21, max 41310.21, average 41310.21 (1 anomaly event(s))

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

- `net_revenue`: min 28393.31, max 47473.27, average 38492.545 (5 anomaly event(s))
- `stockout_units`: min 0.0, max 112.0, average 77.1429 (11 anomaly event(s))
- `support_ticket_count`: min 214.0, max 291.0, average 255.6429 (4 anomaly event(s))
- `shipping_delay_rate`: min 0.045, max 0.0641, average 0.0539 (2 anomaly event(s))
- `lost_sales_units`: min 0.0, max 113.0, average 75.0 (0 anomaly event(s))

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
- Delivery complaints reached 132.00 versus a prior average of 24.36.

### Affected KPIs

- `net_revenue`: min 35003.13, max 58425.92, average 45275.75 (2 anomaly event(s))
- `shipping_delay_rate`: min 0.1074, max 0.1211, average 0.1161 (7 anomaly event(s))
- `support_ticket_count`: min 328.0, max 357.0, average 342.625 (6 anomaly event(s))
- `delivery_complaints`: min 105.0, max 132.0, average 119.125 (0 anomaly event(s))

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

- `net_revenue`: min 42263.43, max 42263.43, average 42263.43 (1 anomaly event(s))

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

- `net_revenue`: min 44380.12, max 44380.12, average 44380.12 (1 anomaly event(s))

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

- `avg_api_latency_ms`: min 205.77, max 205.77, average 205.77 (1 anomaly event(s))

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

- `checkout_failure_rate`: min 0.0153, max 0.0193, average 0.0176 (1 anomaly event(s))
- `net_revenue`: min 43326.96, max 63378.89, average 51359.3886 (2 anomaly event(s))
- `avg_api_latency_ms`: min 201.36, max 211.68, average 206.9543 (1 anomaly event(s))
- `support_ticket_count`: min 201.0, max 238.0, average 216.1429 (1 anomaly event(s))

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

- `shipping_delay_rate`: min 0.0517, max 0.0623, average 0.057 (1 anomaly event(s))
- `net_revenue`: min 44366.87, max 50159.3, average 47263.085 (1 anomaly event(s))

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

- `net_revenue`: min 35001.53, max 40409.72, average 37705.625 (2 anomaly event(s))

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

- `support_ticket_count`: min 196.0, max 223.0, average 209.5 (1 anomaly event(s))
- `net_revenue`: min 38507.13, max 54749.8, average 46628.465 (1 anomaly event(s))

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

- `shipping_delay_rate`: min 0.0508, max 0.0508, average 0.0508 (1 anomaly event(s))

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

- `checkout_failure_rate`: min 0.0303, max 0.0468, average 0.0386 (1 anomaly event(s))
- `avg_api_latency_ms`: min 234.99, max 311.17, average 273.08 (1 anomaly event(s))
- `net_revenue`: min 31629.44, max 33624.5, average 32626.97 (2 anomaly event(s))
- `support_ticket_count`: min 274.0, max 284.0, average 279.0 (2 anomaly event(s))
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

- `net_revenue`: min 33010.03, max 35349.82, average 34179.925 (2 anomaly event(s))

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
- Lost sales units reached 92.00 during the incident.

### Affected KPIs

- `net_revenue`: min 33504.76, max 55208.18, average 44440.761 (4 anomaly event(s))
- `stockout_units`: min 0.0, max 75.0, average 42.8 (7 anomaly event(s))
- `support_ticket_count`: min 197.0, max 272.0, average 239.5 (2 anomaly event(s))
- `shipping_delay_rate`: min 0.0506, max 0.0637, average 0.0545 (1 anomaly event(s))
- `lost_sales_units`: min 0.0, max 92.0, average 46.7 (0 anomaly event(s))

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

- `checkout_failure_rate`: min 0.0186, max 0.0187, average 0.0186 (1 anomaly event(s))
- `net_revenue`: min 38672.95, max 50847.77, average 44760.36 (1 anomaly event(s))

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

- `net_revenue`: min 35711.86, max 35711.86, average 35711.86 (1 anomaly event(s))

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

- `shipping_delay_rate`: min 0.0487, max 0.06, average 0.0565 (1 anomaly event(s))
- `avg_api_latency_ms`: min 200.01, max 210.6, average 207.194 (2 anomaly event(s))
- `net_revenue`: min 38084.11, max 64032.3, average 49364.292 (1 anomaly event(s))
- `support_ticket_count`: min 201.0, max 223.0, average 213.8 (2 anomaly event(s))

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
- Delivery complaints reached 101.00 versus a prior average of 21.36.

### Affected KPIs

- `net_revenue`: min 33367.6, max 60787.09, average 46044.42 (2 anomaly event(s))
- `support_ticket_count`: min 259.0, max 329.0, average 298.75 (3 anomaly event(s))
- `shipping_delay_rate`: min 0.0545, max 0.0675, average 0.064 (2 anomaly event(s))
- `delivery_complaints`: min 79.0, max 101.0, average 85.75 (0 anomaly event(s))

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

## INC-029: Deployment-related checkout incident

- **Date range:** 2025-09-29 to 2025-10-14
- **Likely cause:** Likely deployment-related checkout incident
- **Main anomaly:** `checkout_failure_spike`
- **Related anomalies:** `latency_spike`, `revenue_drop`, `shipping_delay_spike`, `support_ticket_spike`

### Evidence

- Latency and checkout failure anomalies occurred together from 2025-09-29 to 2025-10-14.
- 2 failed or rollback deployment event(s) occurred within the investigation window.

### Affected KPIs

- `net_revenue`: min 22658.2, max 75335.86, average 45825.9219 (10 anomaly event(s))
- `avg_api_latency_ms`: min 201.16, max 655.44, average 284.4656 (4 anomaly event(s))
- `checkout_failure_rate`: min 0.0152, max 0.1503, average 0.04 (4 anomaly event(s))
- `shipping_delay_rate`: min 0.0461, max 0.0629, average 0.0529 (1 anomaly event(s))
- `support_ticket_count`: min 190.0, max 401.0, average 253.375 (4 anomaly event(s))
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

- `net_revenue`: min 55520.37, max 65719.68, average 60620.025 (2 anomaly event(s))

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

- `shipping_delay_rate`: min 0.0509, max 0.0675, average 0.0566 (1 anomaly event(s))
- `net_revenue`: min 47369.5, max 78295.31, average 66125.218 (4 anomaly event(s))
- `support_ticket_count`: min 196.0, max 228.0, average 213.0 (2 anomaly event(s))

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

- `net_revenue`: min 50122.48, max 79838.69, average 66519.652 (2 anomaly event(s))
- `shipping_delay_rate`: min 0.0515, max 0.0584, average 0.0552 (1 anomaly event(s))
- `avg_api_latency_ms`: min 208.31, max 212.57, average 211.05 (1 anomaly event(s))

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
- Lost sales units reached 190.00 during the incident.

### Affected KPIs

- `stockout_units`: min 92.0, max 134.0, average 117.0 (14 anomaly event(s))
- `net_revenue`: min 28434.33, max 61170.31, average 41587.5243 (6 anomaly event(s))
- `support_ticket_count`: min 263.0, max 306.0, average 287.1429 (5 anomaly event(s))
- `lost_sales_units`: min 100.0, max 190.0, average 153.2143 (0 anomaly event(s))

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

- `shipping_delay_rate`: min 0.0497, max 0.0497, average 0.0497 (1 anomaly event(s))

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

- `avg_api_latency_ms`: min 210.96, max 210.96, average 210.96 (1 anomaly event(s))
- `net_revenue`: min 58149.45, max 58149.45, average 58149.45 (1 anomaly event(s))

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

- `net_revenue`: min 55343.67, max 55343.67, average 55343.67 (1 anomaly event(s))
- `support_ticket_count`: min 235.0, max 235.0, average 235.0 (1 anomaly event(s))

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

- `net_revenue`: min 53386.07, max 53386.07, average 53386.07 (1 anomaly event(s))

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

- `checkout_failure_rate`: min 0.0176, max 0.075, average 0.0315 (2 anomaly event(s))
- `avg_api_latency_ms`: min 204.23, max 398.61, average 254.325 (2 anomaly event(s))
- `net_revenue`: min 42119.47, max 73025.67, average 60486.2125 (3 anomaly event(s))
- `support_ticket_count`: min 195.0, max 312.0, average 234.125 (2 anomaly event(s))
- `shipping_delay_rate`: min 0.0495, max 0.0631, average 0.0552 (2 anomaly event(s))
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
- Delivery complaints reached 170.00 versus a prior average of 23.93.

### Affected KPIs

- `shipping_delay_rate`: min 0.0876, max 0.1013, average 0.0923 (5 anomaly event(s))
- `support_ticket_count`: min 349.0, max 397.0, average 375.7778 (7 anomaly event(s))
- `net_revenue`: min 45078.65, max 77069.6, average 58123.1022 (3 anomaly event(s))
- `delivery_complaints`: min 149.0, max 170.0, average 156.2222 (0 anomaly event(s))

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

- `net_revenue`: min 63766.89, max 63766.89, average 63766.89 (1 anomaly event(s))

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

- `net_revenue`: min 48293.97, max 48293.97, average 48293.97 (1 anomaly event(s))

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

- `net_revenue`: min 63140.24, max 68683.17, average 65911.705 (1 anomaly event(s))
- `support_ticket_count`: min 193.0, max 225.0, average 209.0 (1 anomaly event(s))

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

- `net_revenue`: min 64817.0, max 64817.0, average 64817.0 (1 anomaly event(s))

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

- `net_revenue`: min 56332.76, max 56332.76, average 56332.76 (1 anomaly event(s))

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

- `net_revenue`: min 66348.87, max 66348.87, average 66348.87 (1 anomaly event(s))

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

- `avg_api_latency_ms`: min 202.99, max 733.8, average 488.28 (6 anomaly event(s))
- `net_revenue`: min 22240.78, max 92473.3, average 51368.5422 (6 anomaly event(s))
- `checkout_failure_rate`: min 0.0163, max 0.1728, average 0.0982 (5 anomaly event(s))
- `support_ticket_count`: min 207.0, max 434.0, average 314.5556 (5 anomaly event(s))
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

- `shipping_delay_rate`: min 0.0578, max 0.0578, average 0.0578 (1 anomaly event(s))

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

- `net_revenue`: min 62606.93, max 62606.93, average 62606.93 (1 anomaly event(s))

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
- Lost sales units reached 130.00 during the incident.

### Affected KPIs

- `checkout_failure_rate`: min 0.0158, max 0.0202, average 0.0182 (3 anomaly event(s))
- `net_revenue`: min 47213.13, max 84665.69, average 65440.8938 (6 anomaly event(s))
- `support_ticket_count`: min 185.0, max 289.0, average 235.2857 (4 anomaly event(s))
- `stockout_units`: min 0.0, max 125.0, average 55.381 (11 anomaly event(s))
- `shipping_delay_rate`: min 0.045, max 0.0653, average 0.0547 (1 anomaly event(s))
- `lost_sales_units`: min 0.0, max 130.0, average 51.8571 (0 anomaly event(s))

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

- `net_revenue`: min 64253.64, max 64253.64, average 64253.64 (1 anomaly event(s))

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

- `net_revenue`: min 60182.65, max 68437.91, average 64310.28 (2 anomaly event(s))

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
- Delivery complaints reached 108.00 versus a prior average of 23.64.

### Affected KPIs

- `checkout_failure_rate`: min 0.0165, max 0.0206, average 0.0185 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.0491, max 0.1083, average 0.0874 (6 anomaly event(s))
- `support_ticket_count`: min 160.0, max 329.0, average 279.8 (4 anomaly event(s))
- `net_revenue`: min 49521.87, max 96140.81, average 74472.776 (2 anomaly event(s))
- `delivery_complaints`: min 17.0, max 108.0, average 76.4 (0 anomaly event(s))

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

- `net_revenue`: min 65669.1, max 102746.43, average 78326.1525 (1 anomaly event(s))
- `checkout_failure_rate`: min 0.016, max 0.0181, average 0.0175 (1 anomaly event(s))

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

- `net_revenue`: min 57601.79, max 57601.79, average 57601.79 (1 anomaly event(s))

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

- `checkout_failure_rate`: min 0.0174, max 0.0191, average 0.0181 (1 anomaly event(s))
- `net_revenue`: min 55466.06, max 109564.07, average 78149.3425 (3 anomaly event(s))
- `shipping_delay_rate`: min 0.0506, max 0.0606, average 0.055 (1 anomaly event(s))

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

- `checkout_failure_rate`: min 0.0162, max 0.1013, average 0.0511 (2 anomaly event(s))
- `avg_api_latency_ms`: min 207.95, max 509.74, average 331.2825 (2 anomaly event(s))
- `net_revenue`: min 37153.12, max 65913.9, average 51430.795 (3 anomaly event(s))
- `support_ticket_count`: min 203.0, max 327.0, average 263.25 (2 anomaly event(s))
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

- `net_revenue`: min 68309.62, max 68309.62, average 68309.62 (1 anomaly event(s))

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

- `shipping_delay_rate`: min 0.0449, max 0.0647, average 0.0549 (1 anomaly event(s))
- `net_revenue`: min 50088.55, max 88595.9, average 71026.828 (2 anomaly event(s))

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

- `net_revenue`: min 81280.14, max 81280.14, average 81280.14 (1 anomaly event(s))

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
- Lost sales units reached 178.00 during the incident.

### Affected KPIs

- `net_revenue`: min 32242.51, max 79740.26, average 51200.4547 (6 anomaly event(s))
- `stockout_units`: min 0.0, max 143.0, average 108.4706 (15 anomaly event(s))
- `support_ticket_count`: min 193.0, max 307.0, average 272.5294 (4 anomaly event(s))
- `avg_api_latency_ms`: min 196.93, max 214.7, average 207.0112 (1 anomaly event(s))
- `lost_sales_units`: min 0.0, max 178.0, average 116.5882 (0 anomaly event(s))

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
- Delivery complaints reached 161.00 versus a prior average of 24.79.

### Affected KPIs

- `checkout_failure_rate`: min 0.0166, max 0.0197, average 0.0181 (1 anomaly event(s))
- `shipping_delay_rate`: min 0.0517, max 0.1682, average 0.1229 (9 anomaly event(s))
- `net_revenue`: min 44608.19, max 95497.0, average 68414.8871 (3 anomaly event(s))
- `support_ticket_count`: min 200.0, max 374.0, average 299.7143 (6 anomaly event(s))
- `delivery_complaints`: min 21.0, max 161.0, average 95.9286 (0 anomaly event(s))

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

- `checkout_failure_rate`: min 0.0175, max 0.0175, average 0.0175 (1 anomaly event(s))

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

- `net_revenue`: min 54860.75, max 54860.75, average 54860.75 (1 anomaly event(s))

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

- `net_revenue`: min 63076.86, max 94612.37, average 79272.86 (3 anomaly event(s))
- `shipping_delay_rate`: min 0.0493, max 0.059, average 0.055 (1 anomaly event(s))

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

- `net_revenue`: min 67805.4, max 67805.4, average 67805.4 (1 anomaly event(s))

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

- `checkout_failure_rate`: min 0.086, max 0.148, average 0.1217 (4 anomaly event(s))
- `avg_api_latency_ms`: min 445.12, max 631.56, average 561.43 (4 anomaly event(s))
- `net_revenue`: min 44661.09, max 56544.32, average 49736.84 (4 anomaly event(s))
- `support_ticket_count`: min 329.0, max 401.0, average 363.75 (4 anomaly event(s))
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

- `net_revenue`: min 77299.31, max 77299.31, average 77299.31 (1 anomaly event(s))

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

- `net_revenue`: min 87613.24, max 87613.24, average 87613.24 (1 anomaly event(s))

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

- `net_revenue`: min 86185.24, max 93529.71, average 89857.475 (2 anomaly event(s))
- `checkout_failure_rate`: min 0.0162, max 0.0162, average 0.0162 (1 anomaly event(s))
- `avg_api_latency_ms`: min 202.93, max 203.71, average 203.32 (1 anomaly event(s))

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

- `shipping_delay_rate`: min 0.0531, max 0.0531, average 0.0531 (1 anomaly event(s))

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

- `shipping_delay_rate`: min 0.055, max 0.055, average 0.055 (1 anomaly event(s))

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

- `net_revenue`: min 78900.95, max 93494.36, average 87524.1033 (2 anomaly event(s))
- `shipping_delay_rate`: min 0.0541, max 0.0577, average 0.0553 (1 anomaly event(s))
- `support_ticket_count`: min 217.0, max 224.0, average 219.6667 (1 anomaly event(s))

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

- `checkout_failure_rate`: min 0.0166, max 0.0166, average 0.0166 (1 anomaly event(s))

### Recommended Next Steps

- Inspect checkout errors and dependency health for the incident window.
- Confirm checkout failure rate and revenue have returned to baseline.
