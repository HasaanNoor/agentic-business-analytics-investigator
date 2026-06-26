# KPI Monitoring And Anomaly Detection

## Goal

Combine the synthetic datasets into one daily KPI table, then detect unusual changes in those KPIs.

## Inputs

From `data/synthetic/`:

- `sales_metrics_daily.csv`
- `api_latency_hourly.csv`
- `checkout_failures_hourly.csv`
- `support_tickets_daily.csv`
- `inventory_levels_daily.csv`
- `shipping_delays_daily.csv`
- `deployment_events.csv`

## Outputs

- `outputs/reports/kpi_summary_daily.csv`
- `outputs/reports/anomaly_events.csv`
- KPI figure files in `outputs/figures/`
- Anomaly figure files in `outputs/figures/`

## Main files to create

- `src/analytics/kpi_monitor.py`
- `src/anomaly_detection/detect_anomalies.py`
- `tests/test_kpi_monitor.py`
- `tests/test_anomaly_detection.py`

## Required behavior

### KPI summary

- Convert hourly API latency to daily weighted average latency.
- Convert hourly checkout data to daily checkout failure rate.
- Aggregate inventory records to daily stockouts and shortage flags.
- Aggregate shipping records to daily delay rate, carrier utilization, backlog, complaints, and regional flags.
- Combine all sources by date.
- Add calendar features:
  - `day_of_week`
  - `month`
  - `quarter`
  - `is_weekend`
- Include these important columns:
  - `date`
  - `net_revenue`
  - `website_visitors`
  - `active_customers`
  - `average_order_value`
  - `conversion_rate`
  - `refund_rate`
  - `avg_api_latency_ms`
  - `checkout_failure_rate`
  - support ticket category columns
  - `support_ticket_count`
  - `stockout_units`
  - `lost_sales_units`
  - `shipping_delay_rate`
  - `carrier_capacity_utilization`
  - `warehouse_backlog`
  - `delivery_complaints`
  - regional disruption flags
  - `deployment_event_flag`
  - `inventory_shortage_flag`
  - `shipping_disruption_flag`
  - `business_incident_flag`
  - `dominant_incident_type`
  - `incident_signal`
- Use a 14-day rolling window when calculating baseline statistics for anomaly detection.
- An anomaly should be identified using deterministic z-score thresholds that are applied consistently across all KPI calculations.

### Anomaly detection

- Use rolling statistics over prior days.
- Detect these anomaly types:
  - `revenue_drop`
  - `latency_spike`
  - `checkout_failure_spike`
  - `support_ticket_spike`
  - `inventory_shortage_period`
  - `shipping_delay_spike`
  - `refund_spike`
  - `visitor_surge`
  - `warehouse_backlog_spike`
- Include generated incident markers so smaller known incidents can still appear in the anomaly history.
- Each anomaly row should include:
  - `date`
  - `anomaly_type`
  - `metric`
  - `value`
  - `rolling_mean`
  - `rolling_std`
  - `z_score`
  - `percent_change`
  - `severity`
  - `reason`

## Acceptance criteria

- KPI output has one row per day in the generated date range.
- KPI output has all required columns.
- Support ticket total equals the sum of support ticket categories.
- Rates stay between 0 and 1.
- Anomaly output is nonempty when generated data includes incidents.
- Anomaly output includes several anomaly types.
- Tests cover aggregation math and anomaly rule behavior.

## Test commands where relevant

```bash
python3 src/analytics/kpi_monitor.py
python3 src/anomaly_detection/detect_anomalies.py
python3 -m pytest tests/test_kpi_monitor.py tests/test_anomaly_detection.py
```
