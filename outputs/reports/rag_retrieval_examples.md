# RAG Retrieval Examples

These examples show which past incidents were retrieved before agents made recommendations.

## Current incident: INC-001 - Shipping Delay Spike Incident

- **Date range:** 2024-01-08 to 2024-01-08
- **Anomaly type:** shipping_delay_spike

### Retrieved incidents

- **INC-159 - Shipping Delay Spike Incident**
  Similarity score: `0.9819`
  Root cause: Likely logistics incident
  Resolution: Rerouted affected orders through backup carriers and prioritized delayed deliveries.
  Outcome: success=True, recovery_days=3
  Retrieved recommendations:
  - Rerouted affected orders through backup carriers and prioritized delayed deliveries.
  - Compare the current incident with similar historical incidents before finalizing recommendations.
  - Monitor affected metrics until recovery is confirmed.
- **INC-159 - Shipping Delay Spike Incident**
  Similarity score: `0.9396`
  Root cause: Likely logistics incident
  Resolution: Rerouted affected orders through backup carriers and prioritized delayed deliveries.
  Outcome: success=True, recovery_days=3
  Retrieved recommendations:
  - Rerouted affected orders through backup carriers and prioritized delayed deliveries.
  - Compare the current incident with similar historical incidents before finalizing recommendations.
  - Monitor affected metrics until recovery is confirmed.
  - Check whether conversion rate and revenue recovered after the incident.
  - Review refunds, stockouts, and lost sales for preventable revenue leakage.
- **INC-010 - Logistics disruption incident**
  Similarity score: `0.9331`
  Root cause: Likely logistics disruption incident
  Resolution: Rerouted affected orders through backup carriers and prioritized delayed deliveries.
  Outcome: success=False, recovery_days=4
  Retrieved recommendations:
  - Review carrier performance and delayed shipment queues.
  - Notify affected customers and prioritize delayed deliveries.
  - Monitor shipping delay rate and delivery complaints until both return to baseline.

## Current incident: INC-002 - Latency Spike Incident

- **Date range:** 2024-01-10 to 2024-01-11
- **Anomaly type:** latency_spike

### Retrieved incidents

- **INC-116 - Latency Spike Incident**
  Similarity score: `0.9611`
  Root cause: Likely platform reliability incident
  Resolution: Reduced API latency by rolling back the slow dependency and scaling checkout workers.
  Outcome: success=True, recovery_days=2
  Retrieved recommendations:
  - Reduced API latency by rolling back the slow dependency and scaling checkout workers.
  - Compare the current incident with similar historical incidents before finalizing recommendations.
  - Monitor affected metrics until recovery is confirmed.
- **INC-194 - Latency Spike Incident**
  Similarity score: `0.9607`
  Root cause: Likely platform reliability incident
  Resolution: Reduced API latency by rolling back the slow dependency and scaling checkout workers.
  Outcome: success=True, recovery_days=2
  Retrieved recommendations:
  - Reduced API latency by rolling back the slow dependency and scaling checkout workers.
  - Compare the current incident with similar historical incidents before finalizing recommendations.
  - Monitor affected metrics until recovery is confirmed.
- **INC-105 - Latency Spike Incident**
  Similarity score: `0.959`
  Root cause: Likely platform reliability incident
  Resolution: Reduced API latency by rolling back the slow dependency and scaling checkout workers.
  Outcome: success=True, recovery_days=2
  Retrieved recommendations:
  - Reduced API latency by rolling back the slow dependency and scaling checkout workers.
  - Compare the current incident with similar historical incidents before finalizing recommendations.
  - Monitor affected metrics until recovery is confirmed.

## Current incident: INC-003 - Inventory shortage incident

- **Date range:** 2024-01-13 to 2024-01-16
- **Anomaly type:** inventory_shortage_period

### Retrieved incidents

- **INC-117 - Inventory shortage incident**
  Similarity score: `0.9804`
  Root cause: Likely inventory shortage incident
  Resolution: Transferred inventory from another warehouse and expedited replenishment.
  Outcome: success=False, recovery_days=4
  Retrieved recommendations:
  - Prioritize replenishment for stocked-out products.
  - Review demand forecasts, reorder points, and supplier lead times.
  - Track lost sales and net revenue until inventory availability recovers.
- **INC-015 - Inventory shortage incident**
  Similarity score: `0.9799`
  Root cause: Likely inventory shortage incident
  Resolution: Transferred inventory from another warehouse and expedited replenishment.
  Outcome: success=False, recovery_days=4
  Retrieved recommendations:
  - Prioritize replenishment for stocked-out products.
  - Review demand forecasts, reorder points, and supplier lead times.
  - Track lost sales and net revenue until inventory availability recovers.
- **INC-104 - Inventory shortage incident**
  Similarity score: `0.9768`
  Root cause: Likely inventory shortage incident
  Resolution: Transferred inventory from another warehouse and expedited replenishment.
  Outcome: success=False, recovery_days=4
  Retrieved recommendations:
  - Prioritize replenishment for stocked-out products.
  - Review demand forecasts, reorder points, and supplier lead times.
  - Track lost sales and net revenue until inventory availability recovers.

## Current incident: INC-004 - Inventory shortage incident

- **Date range:** 2024-01-18 to 2024-01-20
- **Anomaly type:** inventory_shortage_period

### Retrieved incidents

- **INC-024 - Inventory shortage incident**
  Similarity score: `0.9934`
  Root cause: Likely inventory shortage incident
  Resolution: Transferred inventory from another warehouse and expedited replenishment.
  Outcome: success=True, recovery_days=4
  Retrieved recommendations:
  - Prioritize replenishment for stocked-out products.
  - Review demand forecasts, reorder points, and supplier lead times.
  - Track lost sales and net revenue until inventory availability recovers.
- **INC-013 - Inventory shortage incident**
  Similarity score: `0.9861`
  Root cause: Likely inventory shortage incident
  Resolution: Transferred inventory from another warehouse and expedited replenishment.
  Outcome: success=True, recovery_days=4
  Retrieved recommendations:
  - Prioritize replenishment for stocked-out products.
  - Review demand forecasts, reorder points, and supplier lead times.
  - Track lost sales and net revenue until inventory availability recovers.
- **INC-076 - Inventory shortage incident**
  Similarity score: `0.9851`
  Root cause: Likely inventory shortage incident
  Resolution: Transferred inventory from another warehouse and expedited replenishment.
  Outcome: success=True, recovery_days=4
  Retrieved recommendations:
  - Prioritize replenishment for stocked-out products.
  - Review demand forecasts, reorder points, and supplier lead times.
  - Track lost sales and net revenue until inventory availability recovers.

## Current incident: INC-005 - Logistics disruption incident

- **Date range:** 2024-01-23 to 2024-01-24
- **Anomaly type:** shipping_delay_spike

### Retrieved incidents

- **INC-026 - Logistics disruption incident**
  Similarity score: `0.9862`
  Root cause: Likely logistics disruption incident
  Resolution: Rerouted affected orders through backup carriers and prioritized delayed deliveries.
  Outcome: success=False, recovery_days=4
  Retrieved recommendations:
  - Review carrier performance and delayed shipment queues.
  - Notify affected customers and prioritize delayed deliveries.
  - Monitor shipping delay rate and delivery complaints until both return to baseline.
- **INC-180 - Logistics disruption incident**
  Similarity score: `0.9843`
  Root cause: Likely logistics disruption incident
  Resolution: Rerouted affected orders through backup carriers and prioritized delayed deliveries.
  Outcome: success=False, recovery_days=4
  Retrieved recommendations:
  - Review carrier performance and delayed shipment queues.
  - Notify affected customers and prioritize delayed deliveries.
  - Monitor shipping delay rate and delivery complaints until both return to baseline.
- **INC-043 - Logistics disruption incident**
  Similarity score: `0.9827`
  Root cause: Likely logistics disruption incident
  Resolution: Rerouted affected orders through backup carriers and prioritized delayed deliveries.
  Outcome: success=True, recovery_days=4
  Retrieved recommendations:
  - Review carrier performance and delayed shipment queues.
  - Notify affected customers and prioritize delayed deliveries.
  - Monitor shipping delay rate and delivery complaints until both return to baseline.
