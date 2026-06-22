from pathlib import Path

import pandas as pd

from src.analytics.kpi_monitor import (
    KPI_COLUMNS,
    build_daily_kpi_summary,
    load_synthetic_datasets,
    run_kpi_monitor,
)
from src.ingestion.generate_synthetic_data import generate_all_datasets, write_datasets


def write_default_synthetic_data(output_dir: Path) -> None:
    datasets = generate_all_datasets(seed=42)
    write_datasets(datasets, output_dir)


def test_build_daily_kpi_summary_has_expected_columns_and_dates(tmp_path):
    data_dir = tmp_path / "synthetic"
    write_default_synthetic_data(data_dir)

    summary = build_daily_kpi_summary(load_synthetic_datasets(data_dir))

    assert list(summary.columns) == KPI_COLUMNS
    assert len(summary) == 730
    assert summary["date"].min() == pd.Timestamp("2025-01-01")
    assert summary["date"].max() == pd.Timestamp("2026-12-31")
    assert summary["date"].is_monotonic_increasing
    assert summary["net_revenue"].gt(0).all()
    assert summary["website_visitors"].gt(0).all()
    assert summary["active_customers"].gt(0).all()
    assert summary["average_order_value"].gt(0).all()
    assert summary["conversion_rate"].between(0, 1).all()
    assert summary["refund_rate"].between(0, 1).all()
    assert summary["checkout_failure_rate"].between(0, 1).all()
    assert summary["shipping_delay_rate"].between(0, 1).all()
    assert summary["carrier_capacity_utilization"].between(0, 1).all()
    assert summary["warehouse_backlog"].ge(0).all()
    assert summary["day_of_week"].between(0, 6).all()
    assert summary["month"].between(1, 12).all()
    assert summary["quarter"].between(1, 4).all()
    assert summary["is_weekend"].isin([0, 1]).all()
    assert summary["deployment_event_flag"].isin([0, 1]).all()
    assert summary["inventory_shortage_flag"].isin([0, 1]).all()
    assert summary["shipping_disruption_flag"].isin([0, 1]).all()
    assert summary["east_region_disruption"].isin([0, 1]).all()
    assert summary["west_region_disruption"].isin([0, 1]).all()
    assert summary["south_region_disruption"].isin([0, 1]).all()
    assert summary["central_region_disruption"].isin([0, 1]).all()
    category_columns = [
        "shipping_complaint_tickets",
        "checkout_issue_tickets",
        "billing_issue_tickets",
        "account_access_tickets",
        "general_support_tickets",
    ]
    assert summary["support_ticket_count"].equals(summary[category_columns].sum(axis=1))
    assert summary["deployment_event_flag"].sum() == 14
    assert summary["inventory_shortage_flag"].sum() > 0
    assert summary["shipping_disruption_flag"].sum() > 0


def test_kpi_summary_aggregates_hourly_and_entity_data_correctly(tmp_path):
    data_dir = tmp_path / "synthetic"
    write_default_synthetic_data(data_dir)
    datasets = load_synthetic_datasets(data_dir)

    summary = build_daily_kpi_summary(datasets)
    first_day = summary.loc[summary["date"] == pd.Timestamp("2025-01-01")].iloc[0]

    latency = datasets["latency"].copy()
    latency["date"] = pd.to_datetime(latency["timestamp"]).dt.normalize()
    latency_day = latency[latency["date"] == pd.Timestamp("2025-01-01")]
    expected_latency = (latency_day["avg_latency_ms"] * latency_day["request_count"]).sum() / latency_day["request_count"].sum()

    checkout = datasets["checkout"].copy()
    checkout["date"] = pd.to_datetime(checkout["timestamp"]).dt.normalize()
    checkout_day = checkout[checkout["date"] == pd.Timestamp("2025-01-01")]
    expected_checkout_rate = checkout_day["failed_checkouts"].sum() / checkout_day["checkout_attempts"].sum()

    inventory = datasets["inventory"].copy()
    inventory["date"] = pd.to_datetime(inventory["date"])
    expected_stockouts = inventory.loc[inventory["date"] == pd.Timestamp("2025-01-01"), "stockout_units"].sum()

    assert first_day["avg_api_latency_ms"] == round(expected_latency, 2)
    assert first_day["checkout_failure_rate"] == round(expected_checkout_rate, 4)
    assert first_day["stockout_units"] == expected_stockouts
    assert first_day["website_visitors"] == datasets["sales"].loc[0, "website_visitors"]
    assert first_day["active_customers"] == datasets["sales"].loc[0, "active_customers"]
    assert first_day["average_order_value"] == datasets["sales"].loc[0, "average_order_value"]

    support = datasets["support"].copy()
    support["date"] = pd.to_datetime(support["date"])
    support_day = support[support["date"] == pd.Timestamp("2025-01-01")].iloc[0]
    support_categories = [
        "shipping_complaint_tickets",
        "checkout_issue_tickets",
        "billing_issue_tickets",
        "account_access_tickets",
        "general_support_tickets",
    ]
    assert first_day["support_ticket_count"] == support_day[support_categories].sum()

    shipping = datasets["shipping"].copy()
    shipping["date"] = pd.to_datetime(shipping["date"])
    shipping_day = shipping[shipping["date"] == pd.Timestamp("2025-01-01")]
    expected_utilization = shipping_day["carrier_capacity_utilization"].mean()
    expected_backlog = shipping_day["warehouse_backlog"].sum()
    assert first_day["carrier_capacity_utilization"] == round(expected_utilization, 4)
    assert first_day["warehouse_backlog"] == expected_backlog


def test_run_kpi_monitor_writes_csv_and_plots(tmp_path):
    data_dir = tmp_path / "synthetic"
    output_path = tmp_path / "reports" / "kpi_summary_daily.csv"
    figures_dir = tmp_path / "figures"
    write_default_synthetic_data(data_dir)

    summary = run_kpi_monitor(data_dir, output_path, figures_dir)

    assert output_path.exists()
    assert len(pd.read_csv(output_path)) == len(summary)
    assert (figures_dir / "kpi_net_revenue.png").exists()
    assert (figures_dir / "kpi_api_latency.png").exists()
    assert (figures_dir / "kpi_support_ticket_count.png").exists()
    assert (figures_dir / "kpi_carrier_capacity_utilization.png").exists()
