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
    assert len(summary) == 181
    assert summary["date"].min() == pd.Timestamp("2025-01-01")
    assert summary["date"].max() == pd.Timestamp("2025-06-30")
    assert summary["date"].is_monotonic_increasing
    assert summary["net_revenue"].gt(0).all()
    assert summary["conversion_rate"].between(0, 1).all()
    assert summary["refund_rate"].between(0, 1).all()
    assert summary["checkout_failure_rate"].between(0, 1).all()
    assert summary["shipping_delay_rate"].between(0, 1).all()
    assert summary["deployment_event_flag"].isin([0, 1]).all()
    assert summary["inventory_shortage_flag"].isin([0, 1]).all()
    assert summary["shipping_disruption_flag"].isin([0, 1]).all()
    assert summary["deployment_event_flag"].sum() == 2
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
