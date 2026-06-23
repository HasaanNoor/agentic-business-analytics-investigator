import json
from pathlib import Path

import pandas as pd
import pytest

from src.analytics.kpi_monitor import run_kpi_monitor
from src.anomaly_detection.detect_anomalies import run_anomaly_detection
from src.ingestion.generate_synthetic_data import generate_all_datasets, write_datasets
from src.investigation.investigate_anomalies import group_anomalies_into_incidents, run_investigation


@pytest.fixture(scope="module")
def investigation_result(tmp_path_factory):
    root = tmp_path_factory.mktemp("investigation")
    data_dir = root / "synthetic"
    reports_dir = root / "reports"
    figures_dir = root / "figures"
    kpi_path = reports_dir / "kpi_summary_daily.csv"
    anomaly_path = reports_dir / "anomaly_events.csv"
    json_path = reports_dir / "investigation_reports.json"
    markdown_path = reports_dir / "investigation_summary.md"

    write_datasets(generate_all_datasets(seed=42), data_dir)
    run_kpi_monitor(data_dir, kpi_path, figures_dir, create_plots=False)
    run_anomaly_detection(kpi_path, anomaly_path, figures_dir, create_plots=False)
    reports = run_investigation(
        kpi_path=kpi_path,
        anomaly_path=anomaly_path,
        deployment_path=data_dir / "deployment_events.csv",
        json_output_path=json_path,
        markdown_output_path=markdown_path,
    )
    return reports, json_path, markdown_path


def find_report(reports: list[dict[str, object]], likely_cause: str) -> dict[str, object]:
    return next(report for report in reports if report["likely_cause"] == likely_cause)


def test_investigation_report_files_are_created(investigation_result):
    reports, json_path, markdown_path = investigation_result

    assert json_path.exists()
    assert markdown_path.exists()
    assert json.loads(json_path.read_text(encoding="utf-8"))["incident_count"] == len(reports)


def test_incidents_are_grouped_by_consecutive_date_window():
    anomalies = pd.DataFrame(
        {
            "date": pd.to_datetime(["2025-01-01", "2025-01-03", "2025-01-06", "2025-01-10"]),
            "anomaly_type": ["latency_spike", "revenue_drop", "support_ticket_spike", "shipping_delay_spike"],
        }
    )

    incidents = group_anomalies_into_incidents(anomalies, window_days=3)

    assert len(incidents) == 2
    assert incidents[0]["date"].min() == pd.Timestamp("2025-01-01")
    assert incidents[0]["date"].max() == pd.Timestamp("2025-01-06")
    assert incidents[1]["date"].min() == pd.Timestamp("2025-01-10")


def test_deployment_related_incident_is_detected(investigation_result):
    reports, _, _ = investigation_result

    report = find_report(reports, "Likely deployment-related checkout incident")

    assert report["incident_start_date"] <= "2025-03-18"
    assert report["incident_end_date"] >= "2025-03-20"
    assert report["main_anomaly_type"] == "checkout_failure_spike"
    assert report["deployment_events"]


def test_inventory_shortage_incident_is_detected(investigation_result):
    reports, _, _ = investigation_result

    report = find_report(reports, "Likely inventory shortage incident")

    assert report["main_anomaly_type"] == "inventory_shortage_period"
    assert "revenue_drop" in report["related_anomaly_types"]
    assert any("Lost sales units reached" in evidence for evidence in report["supporting_evidence"])
    assert "lost_sales_units" in {kpi["metric"] for kpi in report["affected_kpis"]}


def test_shipping_disruption_incident_is_detected(investigation_result):
    reports, _, _ = investigation_result

    report = find_report(reports, "Likely logistics disruption incident")

    assert report["main_anomaly_type"] == "shipping_delay_spike"
    assert any("Delivery complaints reached" in evidence for evidence in report["supporting_evidence"])
    assert "delivery_complaints" in {kpi["metric"] for kpi in report["affected_kpis"]}


def test_reports_include_evidence_and_recommendations(investigation_result):
    reports, _, markdown_path = investigation_result
    markdown = markdown_path.read_text(encoding="utf-8")

    assert reports
    assert all(report["supporting_evidence"] for report in reports)
    assert all(report["recommended_next_steps"] for report in reports)
    assert "### Evidence" in markdown
    assert "### Affected KPIs" in markdown
    assert "### Recommended Next Steps" in markdown


def test_phase_11_reports_include_enriched_incident_metadata(investigation_result):
    reports, _, markdown_path = investigation_result
    markdown = markdown_path.read_text(encoding="utf-8")

    assert len(reports) >= 200
    assert all(report["incident_severity"] in {"low", "medium", "high", "critical"} for report in reports)
    assert all(report["affected_region"] for report in reports)
    assert all(report["root_cause_category"] for report in reports)
    assert all(report["business_impact_summary"] for report in reports)
    assert all(report["resolution_action"] for report in reports)
    assert all(isinstance(report["resolution_success"], bool) for report in reports)
    assert all(isinstance(report["recovery_days"], int) and report["recovery_days"] > 0 for report in reports)
    assert all(report["affected_metrics"] for report in reports)
    assert "**Severity:**" in markdown
    assert "**Business impact:**" in markdown
    assert "**Resolution:**" in markdown
