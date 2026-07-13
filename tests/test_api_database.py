from datetime import date

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import src.api.main as api
from src.database import crud, models


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    headers = list(rows[0])
    lines = [",".join(headers)]
    for row in rows:
        lines.append(",".join(str(row[header]) for header in headers))
    path.write_text("\n".join(lines), encoding="utf-8")


def configure_paths(monkeypatch, tmp_path):
    reports_dir = tmp_path / "outputs" / "reports"
    rag_dir = tmp_path / "outputs" / "rag"
    paths = {
        "kpis": reports_dir / "kpi_summary_daily.csv",
        "incidents": reports_dir / "multi_agent_investigation_reports.json",
        "forecasts": reports_dir / "forecast_summary.csv",
        "explanations": reports_dir / "shap_feature_importance.csv",
        "actionable": reports_dir / "executive_operations_report.md",
        "knowledge_base": rag_dir / "incident_knowledge_base.pkl",
    }
    monkeypatch.setattr(api, "KPI_SUMMARY_PATH", paths["kpis"])
    monkeypatch.setattr(api, "INCIDENT_REPORTS_PATH", paths["incidents"])
    monkeypatch.setattr(api, "FORECAST_SUMMARY_PATH", paths["forecasts"])
    monkeypatch.setattr(api, "SHAP_FEATURE_IMPORTANCE_PATH", paths["explanations"])
    monkeypatch.setattr(api, "ACTIONABLE_REPORT_PATH", paths["actionable"])
    monkeypatch.setattr(api, "KNOWLEDGE_BASE_PATH", paths["knowledge_base"])
    return paths


def write_outputs(paths):
    import json

    write_csv(paths["kpis"], [{"date": "2026-01-01", "net_revenue": 100}, {"date": "2026-01-03", "net_revenue": 130}])
    paths["incidents"].parent.mkdir(parents=True, exist_ok=True)
    paths["incidents"].write_text(
        json.dumps({"incidents": [{"incident_id": "INC-001", "incident_title": "File incident"}]}),
        encoding="utf-8",
    )
    write_csv(paths["forecasts"], [{"date": "2026-01-04", "kpi": "net_revenue", "prediction": 140}])
    write_csv(paths["explanations"], [{"kpi": "net_revenue", "feature": "website_visitors", "rank": 1}])
    paths["actionable"].write_text("# File Report", encoding="utf-8")
    paths["knowledge_base"].parent.mkdir(parents=True, exist_ok=True)
    paths["knowledge_base"].write_bytes(b"placeholder")


def make_session_factory():
    engine = create_engine(
        "sqlite:///:memory:",
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    models.Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, future=True)


def test_api_reads_from_database_when_configured(monkeypatch, tmp_path):
    Session = make_session_factory()
    with Session() as session:
        crud.upsert_daily_kpi(session, {"date": date(2026, 1, 1), "net_revenue": 100})
        crud.upsert_incident(session, {"incident_id": "INC-001", "incident_title": "DB incident"})
        crud.upsert_forecast(session, {"date": date(2026, 1, 2), "kpi": "net_revenue", "forecast_day": 1, "prediction": 110, "model_name": "linear_regression"})
        crud.upsert_shap_explanation(session, {"kpi": "net_revenue", "model_name": "linear_regression", "feature": "visitors", "rank": 1})
        crud.upsert_actionable_report(session, {"report_name": "executive_operations_report", "content": "# DB Report"})
        session.commit()

    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    monkeypatch.setattr(api, "SessionLocal", Session)
    monkeypatch.setattr(api, "KPI_SUMMARY_PATH", tmp_path / "missing_kpis.csv")
    client = TestClient(api.app)

    assert client.get("/kpis").json()["rows"][0]["net_revenue"] == 100
    assert client.get("/incidents").json()["incidents"][0]["incident_title"] == "DB incident"
    assert client.get("/incidents/INC-001").json()["incident"]["incident_title"] == "DB incident"
    assert client.get("/forecasts").json()["rows"][0]["prediction"] == 110
    assert client.get("/explanations").json()["rows"][0]["feature"] == "visitors"
    assert "DB Report" in client.get("/reports/actionable").json()["content"]


def test_api_falls_back_to_files_when_database_unavailable(monkeypatch, tmp_path):
    paths = configure_paths(monkeypatch, tmp_path)
    write_outputs(paths)
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg2://placeholder:placeholder@127.0.0.1:1/placeholder")

    client = TestClient(api.app)

    response = client.get("/kpis?limit=1")

    assert response.status_code == 200
    assert response.json()["rows"][0]["date"] == "2026-01-03"


def test_health_reports_database_available(monkeypatch, tmp_path):
    configure_paths(monkeypatch, tmp_path)
    Session = make_session_factory()
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    monkeypatch.setattr(api, "SessionLocal", Session)

    response = TestClient(api.app).get("/health")
    payload = response.json()

    assert response.status_code == 200
    assert payload["database"]["configured"] is True
    assert payload["database"]["available"] is True
    assert payload["ready"] is True


def test_health_reports_database_unavailable_and_missing_files(monkeypatch, tmp_path):
    configure_paths(monkeypatch, tmp_path)
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg2://placeholder:placeholder@127.0.0.1:1/placeholder")

    response = TestClient(api.app).get("/health")
    payload = response.json()

    assert response.status_code == 200
    assert payload["database"]["available"] is False
    assert payload["file_fallback"]["available"] is False
    assert payload["status"] == "degraded"
