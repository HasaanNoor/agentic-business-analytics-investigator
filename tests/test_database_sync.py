import json
import pickle
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database import models, sync_outputs


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    headers = list(rows[0])
    lines = [",".join(headers)]
    for row in rows:
        lines.append(",".join(str(row.get(header, "")) for header in headers))
    path.write_text("\n".join(lines), encoding="utf-8")


def make_session():
    engine = create_engine("sqlite:///:memory:", future=True)
    models.Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, future=True)
    return Session()


def configure_sync_paths(monkeypatch, tmp_path: Path) -> dict[str, Path]:
    reports = tmp_path / "outputs" / "reports"
    rag = tmp_path / "outputs" / "rag"
    paths = {
        "kpis": reports / "kpi_summary_daily.csv",
        "anomalies": reports / "anomaly_events.csv",
        "incidents": reports / "multi_agent_investigation_reports.json",
        "first_pass": reports / "investigation_reports.json",
        "forecasts": reports / "forecast_summary.csv",
        "model_metrics": reports / "model_metrics.csv",
        "shap": reports / "shap_feature_importance.csv",
        "report": reports / "executive_operations_report.md",
        "rag": rag / "incident_knowledge_base.pkl",
    }
    monkeypatch.setattr(sync_outputs, "KPI_SUMMARY_PATH", paths["kpis"])
    monkeypatch.setattr(sync_outputs, "ANOMALY_EVENTS_PATH", paths["anomalies"])
    monkeypatch.setattr(sync_outputs, "MULTI_AGENT_REPORTS_PATH", paths["incidents"])
    monkeypatch.setattr(sync_outputs, "INVESTIGATION_REPORTS_PATH", paths["first_pass"])
    monkeypatch.setattr(sync_outputs, "FORECAST_SUMMARY_PATH", paths["forecasts"])
    monkeypatch.setattr(sync_outputs, "MODEL_METRICS_PATH", paths["model_metrics"])
    monkeypatch.setattr(sync_outputs, "SHAP_FEATURE_IMPORTANCE_PATH", paths["shap"])
    monkeypatch.setattr(sync_outputs, "ACTIONABLE_REPORT_PATH", paths["report"])
    monkeypatch.setattr(sync_outputs, "KNOWLEDGE_BASE_PATH", paths["rag"])
    monkeypatch.setattr(
        sync_outputs,
        "REQUIRED_FILES",
        {
            "kpis": paths["kpis"],
            "anomalies": paths["anomalies"],
            "incidents": paths["incidents"],
            "forecasts": paths["forecasts"],
            "model_metrics": paths["model_metrics"],
            "shap_explanations": paths["shap"],
        },
    )
    monkeypatch.setattr(
        sync_outputs,
        "OPTIONAL_FILES",
        {
            "first_pass_incidents": paths["first_pass"],
            "actionable_report": paths["report"],
            "rag_knowledge_base": paths["rag"],
        },
    )
    return paths


def write_outputs(paths: dict[str, Path]) -> None:
    write_csv(paths["kpis"], [{"date": "2026-01-01", "net_revenue": 100, "business_incident_flag": 0, "incident_signal": 0}])
    write_csv(
        paths["anomalies"],
        [
            {
                "date": "2026-01-01",
                "anomaly_type": "latency_spike",
                "metric": "avg_api_latency_ms",
                "value": 250,
                "rolling_mean": 200,
                "rolling_std": 10,
                "z_score": 5,
                "percent_change": 0.25,
                "severity": "high",
                "reason": "latency increased",
            }
        ],
    )
    paths["incidents"].parent.mkdir(parents=True, exist_ok=True)
    paths["incidents"].write_text(
        json.dumps(
            {
                "incidents": [
                    {
                        "incident_id": "INC-001",
                        "incident_title": "Latency issue",
                        "date_range": {"start": "2026-01-01", "end": "2026-01-01"},
                        "main_anomaly_type": "latency_spike",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    write_csv(paths["forecasts"], [{"date": "2026-01-02", "kpi": "net_revenue", "forecast_day": 1, "prediction": 120, "model_name": "linear_regression"}])
    write_csv(paths["model_metrics"], [{"kpi": "net_revenue", "model_name": "linear_regression", "mae": 1, "rmse": 2, "r2": 0.9, "train_rows": 10, "test_rows": 2, "selected_model": True}])
    write_csv(paths["shap"], [{"kpi": "net_revenue", "model_name": "linear_regression", "feature": "visitors", "mean_abs_attribution": 10, "rank": 1, "explanation_method": "SHAP"}])
    paths["report"].write_text("# Executive Operations Report", encoding="utf-8")
    paths["rag"].parent.mkdir(parents=True, exist_ok=True)
    paths["rag"].write_bytes(
        pickle.dumps(
            {
                "model_name": "test-model",
                "text_chunks": ["Incident INC-001 summary"],
                "metadata": [{"incident_id": "INC-001", "incident_type": "Latency issue"}],
                "embeddings": [[0.1, 0.2]],
            }
        )
    )


def test_sync_outputs_is_idempotent(monkeypatch, tmp_path):
    paths = configure_sync_paths(monkeypatch, tmp_path)
    write_outputs(paths)
    session = make_session()

    first = sync_outputs.sync_outputs(session=session)
    second = sync_outputs.sync_outputs(session=session)

    assert first.inserted > 0
    assert second.inserted == 0
    assert models_count(session, models.DailyKPI) == 1
    assert models_count(session, models.AnomalyEvent) == 1
    assert models_count(session, models.Incident) == 1
    assert models_count(session, models.RagRecord) == 1


def test_sync_outputs_rolls_back_on_failure(monkeypatch, tmp_path):
    paths = configure_sync_paths(monkeypatch, tmp_path)
    write_outputs(paths)
    write_csv(paths["anomalies"], [{"date": "2026-01-01", "anomaly_type": "latency_spike"}])
    session = make_session()

    with pytest.raises(KeyError):
        sync_outputs.sync_outputs(session=session)

    assert models_count(session, models.DailyKPI) == 0


def test_sync_outputs_errors_when_required_file_missing(monkeypatch, tmp_path):
    paths = configure_sync_paths(monkeypatch, tmp_path)
    write_outputs(paths)
    paths["kpis"].unlink()
    session = make_session()

    with pytest.raises(sync_outputs.SyncError, match="Missing required output"):
        sync_outputs.sync_outputs(session=session)


def models_count(session, model) -> int:
    return session.query(model).count()

