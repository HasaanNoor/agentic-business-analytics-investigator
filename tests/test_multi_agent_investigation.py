import json
from pathlib import Path

import pandas as pd

from src.agents.coordinator_agent import coordinate_incident_report
from src.agents.logistics_agent import analyze_logistics
from src.agents.multi_agent_investigation import run_multi_agent_investigation
from src.agents.platform_agent import analyze_platform
from src.agents.revenue_agent import analyze_revenue
from src.agents.support_agent import analyze_support


def make_kpis() -> pd.DataFrame:
    dates = pd.date_range("2026-01-01", periods=24, freq="D")
    rows = []
    for index, date in enumerate(dates):
        incident_window = pd.Timestamp("2026-01-16") <= date <= pd.Timestamp("2026-01-18")
        rows.append(
            {
                "date": date,
                "net_revenue": 90000 if incident_window else 110000,
                "website_visitors": 10000,
                "active_customers": 8000,
                "average_order_value": 86,
                "conversion_rate": 0.034 if incident_window else 0.045,
                "refund_rate": 0.04 if incident_window else 0.025,
                "stockout_units": 10 if incident_window else 0,
                "lost_sales_units": 50 if incident_window else 0,
                "support_ticket_count": 250 if incident_window else 140,
                "shipping_complaint_tickets": 80 if incident_window else 20,
                "checkout_issue_tickets": 55 if incident_window else 12,
                "billing_issue_tickets": 15,
                "account_access_tickets": 20,
                "general_support_tickets": 80 if incident_window else 73,
                "shipping_delay_rate": 0.18 if incident_window else 0.06,
                "carrier_capacity_utilization": 0.89 if incident_window else 0.67,
                "warehouse_backlog": 900 if incident_window else 450,
                "delivery_complaints": 90 if incident_window else 25,
                "east_region_disruption": 1 if incident_window else 0,
                "west_region_disruption": 0,
                "south_region_disruption": 0,
                "central_region_disruption": 0,
                "avg_api_latency_ms": 420 if incident_window else 210,
                "checkout_failure_rate": 0.09 if incident_window else 0.02,
                "deployment_event_flag": 1 if date == pd.Timestamp("2026-01-16") else 0,
            }
        )
    return pd.DataFrame(rows)


def make_deployments() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "timestamp": pd.Timestamp("2026-01-16 09:00:00"),
                "service": "checkout-api",
                "version": "2026.01.16.1",
                "environment": "production",
                "status": "failed",
                "change_type": "feature_release",
                "incident_flag": True,
                "incident_type": "failed_deployment",
            },
            {
                "timestamp": pd.Timestamp("2026-01-18 18:00:00"),
                "service": "checkout-api",
                "version": "2026.01.16.1.rollback",
                "environment": "production",
                "status": "rollback_success",
                "change_type": "rollback",
                "incident_flag": True,
                "incident_type": "failed_deployment",
            },
        ]
    )


def make_incident() -> dict[str, object]:
    return {
        "incident_id": "INC-001",
        "title": "Deployment-related checkout incident",
        "incident_start_date": "2026-01-16",
        "incident_end_date": "2026-01-18",
        "main_anomaly_type": "checkout_failure_spike",
        "related_anomaly_types": ["shipping_delay_spike", "support_ticket_spike", "revenue_drop"],
        "likely_cause": "Likely deployment-related checkout incident",
        "supporting_evidence": ["Checkout failures and latency increased together."],
        "recommended_next_steps": ["Review the failed checkout deployment."],
    }


def make_forecasts() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"date": "2026-01-19", "kpi": "net_revenue", "forecast_day": 1, "prediction": 98000, "model_name": "linear_regression"},
            {"date": "2026-01-25", "kpi": "net_revenue", "forecast_day": 7, "prediction": 104000, "model_name": "linear_regression"},
            {"date": "2026-01-19", "kpi": "support_ticket_count", "forecast_day": 1, "prediction": 220, "model_name": "xgboost"},
            {"date": "2026-01-25", "kpi": "support_ticket_count", "forecast_day": 7, "prediction": 180, "model_name": "xgboost"},
        ]
    )


def make_shap() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "kpi": "net_revenue",
                "model_name": "linear_regression",
                "feature": "conversion_rate",
                "mean_abs_attribution": 4000,
                "rank": 1,
                "explanation_method": "SHAP LinearExplainer",
            },
            {
                "kpi": "support_ticket_count",
                "model_name": "xgboost",
                "feature": "checkout_failure_rate",
                "mean_abs_attribution": 8,
                "rank": 1,
                "explanation_method": "SHAP TreeExplainer",
            },
        ]
    )


def write_inputs(root: Path) -> dict[str, Path]:
    reports_dir = root / "reports"
    data_dir = root / "synthetic"
    reports_dir.mkdir(parents=True)
    data_dir.mkdir(parents=True)

    investigation_path = reports_dir / "investigation_reports.json"
    investigation_path.write_text(
        json.dumps({"method": "test", "incident_count": 1, "incidents": [make_incident()]}),
        encoding="utf-8",
    )
    kpi_path = reports_dir / "kpi_summary_daily.csv"
    make_kpis().to_csv(kpi_path, index=False)
    deployment_path = data_dir / "deployment_events.csv"
    make_deployments().to_csv(deployment_path, index=False)
    forecast_path = reports_dir / "forecast_summary.csv"
    make_forecasts().to_csv(forecast_path, index=False)
    shap_path = reports_dir / "shap_feature_importance.csv"
    make_shap().to_csv(shap_path, index=False)
    return {
        "investigation_path": investigation_path,
        "kpi_path": kpi_path,
        "deployment_path": deployment_path,
        "forecast_path": forecast_path,
        "shap_path": shap_path,
        "json_output_path": reports_dir / "multi_agent_investigation_reports.json",
        "markdown_output_path": reports_dir / "multi_agent_investigation_summary.md",
    }


def test_each_agent_returns_structured_finding():
    incident = make_incident()
    kpis = make_kpis()
    deployments = make_deployments()

    findings = [
        analyze_revenue(incident, kpis),
        analyze_support(incident, kpis),
        analyze_logistics(incident, kpis),
        analyze_platform(incident, kpis, deployments),
    ]

    for finding in findings:
        assert finding["agent"]
        assert finding["summary"]
        assert finding["supporting_evidence"]
        assert finding["recommended_next_steps"]
        assert finding["confidence"] in {"low", "medium", "high"}


def test_coordinator_combines_findings_correctly():
    incident = make_incident()
    kpis = make_kpis()
    deployments = make_deployments()
    findings = [
        analyze_revenue(incident, kpis),
        analyze_support(incident, kpis),
        analyze_logistics(incident, kpis),
        analyze_platform(incident, kpis, deployments),
    ]

    report = coordinate_incident_report(incident, findings, make_forecasts(), make_shap())

    assert report["incident_title"] == "Deployment-related checkout incident"
    assert report["likely_cause"] == "Likely deployment-related checkout incident"
    assert len(report["agent_findings"]) == 4
    assert report["recommended_next_steps"]
    assert report["confidence_level"] in {"medium", "high"}


def test_output_files_are_created(tmp_path):
    paths = write_inputs(tmp_path)

    reports = run_multi_agent_investigation(**paths)

    assert reports
    assert paths["json_output_path"].exists()
    assert paths["markdown_output_path"].exists()
    payload = json.loads(paths["json_output_path"].read_text(encoding="utf-8"))
    assert payload["incident_count"] == 1
    assert "Recommended Next Steps" in paths["markdown_output_path"].read_text(encoding="utf-8")


def test_deployment_incidents_include_platform_findings():
    finding = analyze_platform(make_incident(), make_kpis(), make_deployments())

    assert finding["platform_contributed"] is True
    assert finding["deployment_events"]
    assert any("deployment" in evidence for evidence in finding["supporting_evidence"])


def test_shipping_incidents_include_logistics_findings():
    finding = analyze_logistics(make_incident(), make_kpis())

    assert finding["logistics_contributed"] is True
    assert finding["active_region_flags"] == ["east_region_disruption"]
    assert any("Shipping delay rate" in evidence for evidence in finding["supporting_evidence"])


def test_support_ticket_increases_include_support_findings():
    finding = analyze_support(make_incident(), make_kpis())

    assert finding["complaints_increased"] is True
    assert finding["top_increased_categories"]
    assert any(category["metric"] == "shipping_complaint_tickets" for category in finding["top_increased_categories"])


def test_reports_include_recommendations_and_confidence_level(tmp_path):
    paths = write_inputs(tmp_path)

    reports = run_multi_agent_investigation(**paths)

    report = reports[0]
    assert report["recommended_next_steps"]
    assert report["confidence_level"] in {"low", "medium", "high"}
    assert all(finding["recommended_next_steps"] for finding in report["agent_findings"])
