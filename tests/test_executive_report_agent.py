import json
from pathlib import Path

import pandas as pd

from src.agents import executive_report_agent
from src.agents.executive_report_agent import build_evidence_bundle, build_prompt, run_executive_report


def write_phase8_inputs(root: Path) -> dict[str, Path]:
    reports_dir = root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    investigation_payload = {
        "method": "Deterministic anomaly grouping and root-cause rules",
        "incident_window_days": 3,
        "incident_count": 1,
        "incidents": [
            {
                "incident_id": "INC-001",
                "title": "Logistics disruption incident",
                "incident_start_date": "2026-03-01",
                "incident_end_date": "2026-03-03",
                "main_anomaly_type": "shipping_delay_spike",
                "related_anomaly_types": ["support_ticket_spike"],
                "likely_cause": "Likely logistics disruption incident",
                "affected_kpis": [
                    {
                        "metric": "shipping_delay_rate",
                        "minimum": 0.11,
                        "maximum": 0.22,
                        "average": 0.17,
                        "event_count": 2,
                    },
                    {
                        "metric": "delivery_complaints",
                        "minimum": 50,
                        "maximum": 88,
                        "average": 72,
                        "event_count": 0,
                    },
                ],
                "supporting_evidence": ["Shipping delay anomalies occurred from 2026-03-01 to 2026-03-03."],
                "recommended_next_steps": [
                    "Review carrier performance and delayed shipment queues.",
                    "Notify affected customers and prioritize delayed deliveries.",
                ],
            }
        ],
    }
    investigation_reports_path = reports_dir / "investigation_reports.json"
    investigation_reports_path.write_text(json.dumps(investigation_payload), encoding="utf-8")

    investigation_summary_path = reports_dir / "investigation_summary.md"
    investigation_summary_path.write_text("# Deterministic Investigation Summary\n", encoding="utf-8")

    forecast_summary_path = reports_dir / "forecast_summary.csv"
    pd.DataFrame(
        [
            {
                "date": "2027-01-01",
                "kpi": "shipping_delay_rate",
                "forecast_day": 1,
                "prediction": 0.071,
                "model_name": "linear_regression",
            },
            {
                "date": "2027-01-07",
                "kpi": "shipping_delay_rate",
                "forecast_day": 7,
                "prediction": 0.081,
                "model_name": "linear_regression",
            },
            {
                "date": "2027-01-01",
                "kpi": "support_ticket_count",
                "forecast_day": 1,
                "prediction": 180,
                "model_name": "xgboost",
            },
            {
                "date": "2027-01-07",
                "kpi": "support_ticket_count",
                "forecast_day": 7,
                "prediction": 190,
                "model_name": "xgboost",
            },
        ]
    ).to_csv(forecast_summary_path, index=False)

    forecast_explanations_path = reports_dir / "forecast_explanations.md"
    forecast_explanations_path.write_text("# Forecast Explainability Report\n", encoding="utf-8")

    shap_feature_importance_path = reports_dir / "shap_feature_importance.csv"
    pd.DataFrame(
        [
            {
                "kpi": "shipping_delay_rate",
                "model_name": "linear_regression",
                "feature": "warehouse_backlog",
                "mean_abs_attribution": 0.004,
                "rank": 1,
                "explanation_method": "SHAP LinearExplainer",
            },
            {
                "kpi": "shipping_delay_rate",
                "model_name": "linear_regression",
                "feature": "carrier_capacity_utilization",
                "mean_abs_attribution": 0.003,
                "rank": 2,
                "explanation_method": "SHAP LinearExplainer",
            },
            {
                "kpi": "support_ticket_count",
                "model_name": "xgboost",
                "feature": "shipping_delay_rate",
                "mean_abs_attribution": 12.0,
                "rank": 1,
                "explanation_method": "SHAP TreeExplainer",
            },
        ]
    ).to_csv(shap_feature_importance_path, index=False)

    model_metrics_path = reports_dir / "model_metrics.csv"
    pd.DataFrame(
        [
            {
                "kpi": "shipping_delay_rate",
                "model_name": "linear_regression",
                "mae": 0.007,
                "rmse": 0.015,
                "r2": 0.86,
                "selected_model": True,
            },
            {
                "kpi": "support_ticket_count",
                "model_name": "xgboost",
                "mae": 13.68,
                "rmse": 18.57,
                "r2": 0.86,
                "selected_model": True,
            },
        ]
    ).to_csv(model_metrics_path, index=False)

    return {
        "investigation_reports_path": investigation_reports_path,
        "investigation_summary_path": investigation_summary_path,
        "forecast_summary_path": forecast_summary_path,
        "forecast_explanations_path": forecast_explanations_path,
        "shap_feature_importance_path": shap_feature_importance_path,
        "model_metrics_path": model_metrics_path,
        "output_path": reports_dir / "executive_operations_report.md",
    }


def test_executive_report_file_is_created_in_fallback_mode(tmp_path, monkeypatch):
    paths = write_phase8_inputs(tmp_path)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    report = run_executive_report(**paths)

    assert paths["output_path"].exists()
    assert paths["output_path"].read_text(encoding="utf-8") == report
    assert "## Executive Summary" in report
    assert "## Limitations" in report


def test_fallback_mode_does_not_call_openai_without_api_key(tmp_path, monkeypatch):
    paths = write_phase8_inputs(tmp_path)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    def fail_if_called(prompt, model):
        raise AssertionError("OpenAI should not be called without OPENAI_API_KEY")

    monkeypatch.setattr(executive_report_agent, "generate_llm_report", fail_if_called)

    report = run_executive_report(**paths)

    assert "deterministic pipeline" in report
    assert "OPENAI_API_KEY" not in report


def test_report_includes_incidents_forecasts_shap_drivers_and_recommendations(tmp_path, monkeypatch):
    paths = write_phase8_inputs(tmp_path)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    report = run_executive_report(**paths)

    assert "Logistics disruption incident" in report
    assert "shipping_delay_rate" in report
    assert "support_ticket_count" in report
    assert "warehouse_backlog" in report
    assert "shipping_delay_rate" in report
    assert "Review carrier performance and delayed shipment queues." in report
    assert "Recommended Actions" in report


def test_prompt_uses_evidence_bundle_without_requiring_raw_hallucinated_fields(tmp_path):
    paths = write_phase8_inputs(tmp_path)
    investigation_payload = json.loads(paths["investigation_reports_path"].read_text(encoding="utf-8"))
    evidence = build_evidence_bundle(
        investigation_payload=investigation_payload,
        investigation_summary=paths["investigation_summary_path"].read_text(encoding="utf-8"),
        forecasts=pd.read_csv(paths["forecast_summary_path"]),
        forecast_explanations=paths["forecast_explanations_path"].read_text(encoding="utf-8"),
        shap_importance=pd.read_csv(paths["shap_feature_importance_path"]),
        model_metrics=pd.read_csv(paths["model_metrics_path"]),
    )

    prompt = build_prompt(evidence)
    prompt_text = "\n".join(message["content"] for message in prompt)

    assert "Evidence bundle" in prompt_text
    assert "raw_transactions" not in prompt_text
    assert "customer_email" not in prompt_text
    assert "Use only the evidence provided" in prompt_text
