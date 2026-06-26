# Data Generation

## Goal

Generate deterministic synthetic ecommerce data for Northstar Commerce.

The data should cover daily and hourly business activity, including known incidents that later phases can detect and investigate.

## Inputs

- A start date and end date.
- A fixed random seed.
- Default date range should cover `2024-01-01` through `2026-12-31`.

## Outputs

Write these files to `data/synthetic/`:

- `sales_metrics_daily.csv`
- `api_latency_hourly.csv`
- `checkout_failures_hourly.csv`
- `support_tickets_daily.csv`
- `inventory_levels_daily.csv`
- `shipping_delays_daily.csv`
- `deployment_events.csv`

Write this validation report:

- `outputs/reports/synthetic_data_profile.md`

## Main files to create

- `src/ingestion/generate_synthetic_data.py`
- `src/ingestion/validate_synthetic_data.py`
- `tests/test_synthetic_data_validation.py`

## Incident Generation

The synthetic data generator should create incidents from a deterministic incident catalog.

The catalog defines:

- Incident type
- Start date
- Duration
- Severity
- Region
- Root cause category
- Business impact
- Resolution
- Recovery time

The generator should not create incidents at fixed intervals. Instead, incident frequency and timing should be determined by the catalog while producing approximately 210 enriched incidents across the full three-year dataset.

## Required behavior

- Generate repeatable data for a given seed.
- Include these business areas:
  - Sales and revenue.
  - Website visitors and active customers.
  - Conversion rate and refund rate.
  - API latency.
  - Checkout attempts and failed checkouts.
  - Support tickets by category.
  - Inventory stockouts and lost sales.
  - Shipping delays, carrier utilization, warehouse backlog, delivery complaints, and regional disruption flags.
  - Deployment events.
- Include incident records for:
  - Failed deployments.
  - Inventory shortages.
  - Supplier delays.
  - Warehouse staffing shortages.
  - Carrier outages.
  - Refund spikes.
  - API degradation.
  - Marketing campaign surges.
  - Holiday demand surges.
  - Regional weather disruptions.
  - Fraud spikes.
- Incident effects must appear in related metrics. For example:
  - API degradation should raise latency and checkout failures.
  - Inventory shortage should raise stockouts and lost sales and reduce revenue.
  - Carrier outage should raise shipping delays and delivery complaints.
- Each generated dataset should include required date or timestamp columns.
- Validation should check:
  - Required files exist.
  - Required columns exist.
  - Dates parse correctly.
  - Numeric counts are nonnegative.
  - Rates are between 0 and 1 where appropriate.
  - Duplicate rows are not present for expected keys.
  - Expected incident windows exist.

## Acceptance criteria

- Running the generator creates all seven synthetic CSV files.
- Running the validator creates `outputs/reports/synthetic_data_profile.md`.
- The generated data contains more than one year of records and covers the default full date range.
- Validation passes on freshly generated data.
- Tests confirm expected files, columns, date ranges, and basic numeric rules.

## Test commands where relevant

```bash
python3 src/ingestion/generate_synthetic_data.py
python3 src/ingestion/validate_synthetic_data.py
python3 -m pytest tests/test_synthetic_data_validation.py
```
