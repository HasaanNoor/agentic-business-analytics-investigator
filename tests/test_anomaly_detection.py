from pathlib import Path

import pandas as pd

from src.analytics.kpi_monitor import run_kpi_monitor
from src.anomaly_detection.detect_anomalies import detect_anomalies, run_anomaly_detection
from src.ingestion.generate_synthetic_data import generate_all_datasets, write_datasets


def write_default_synthetic_data(output_dir: Path) -> None:
    datasets = generate_all_datasets(seed=42)
    write_datasets(datasets, output_dir)


def build_test_kpi_summary(tmp_path) -> pd.DataFrame:
    data_dir = tmp_path / "synthetic"
    kpi_path = tmp_path / "reports" / "kpi_summary_daily.csv"
    figures_dir = tmp_path / "figures"
    write_default_synthetic_data(data_dir)
    return run_kpi_monitor(data_dir, kpi_path, figures_dir, create_plots=False)


def test_detect_anomalies_finds_expected_incident_families(tmp_path):
    summary = build_test_kpi_summary(tmp_path)

    anomalies = detect_anomalies(summary)
    anomaly_types = set(anomalies["anomaly_type"])

    assert {
        "revenue_drop",
        "latency_spike",
        "checkout_failure_spike",
        "support_ticket_spike",
        "inventory_shortage_period",
        "shipping_delay_spike",
    }.issubset(anomaly_types)


def test_detect_anomalies_covers_known_injected_windows(tmp_path):
    summary = build_test_kpi_summary(tmp_path)

    anomalies = detect_anomalies(summary)
    failed_deployment = anomalies[
        (anomalies["date"].between(pd.Timestamp("2025-03-18"), pd.Timestamp("2025-03-20")))
        & (anomalies["anomaly_type"].isin({"latency_spike", "checkout_failure_spike", "support_ticket_spike"}))
    ]
    inventory_shortage = anomalies[
        (anomalies["date"].between(pd.Timestamp("2025-04-10"), pd.Timestamp("2025-04-20")))
        & (anomalies["anomaly_type"] == "inventory_shortage_period")
    ]
    shipping_disruption = anomalies[
        (anomalies["date"].between(pd.Timestamp("2025-05-05"), pd.Timestamp("2025-05-14")))
        & (anomalies["anomaly_type"] == "shipping_delay_spike")
    ]

    assert not failed_deployment.empty
    assert not inventory_shortage.empty
    assert not shipping_disruption.empty


def test_run_anomaly_detection_writes_csv_and_plot(tmp_path):
    data_dir = tmp_path / "synthetic"
    kpi_path = tmp_path / "reports" / "kpi_summary_daily.csv"
    anomaly_path = tmp_path / "reports" / "anomaly_events.csv"
    figures_dir = tmp_path / "figures"
    write_default_synthetic_data(data_dir)
    run_kpi_monitor(data_dir, kpi_path, figures_dir, create_plots=False)

    anomalies = run_anomaly_detection(kpi_path, anomaly_path, figures_dir)

    assert anomaly_path.exists()
    assert len(pd.read_csv(anomaly_path)) == len(anomalies)
    assert (figures_dir / "anomaly_events_by_type.png").exists()
