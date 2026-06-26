import json
from pathlib import Path

from fastapi.testclient import TestClient

import src.api.main as api


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    headers = list(rows[0])
    lines = [",".join(headers)]
    for row in rows:
        lines.append(",".join(str(row[header]) for header in headers))
    path.write_text("\n".join(lines), encoding="utf-8")


def configure_paths(monkeypatch, tmp_path: Path) -> dict[str, Path]:
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
    api._get_rag_model.cache_clear()
    return paths


def write_outputs(paths: dict[str, Path]) -> None:
    write_csv(
        paths["kpis"],
        [
            {"date": "2026-01-01", "net_revenue": 100},
            {"date": "2026-01-02", "net_revenue": 110},
            {"date": "2026-01-03", "net_revenue": 120},
        ],
    )
    paths["incidents"].parent.mkdir(parents=True, exist_ok=True)
    paths["incidents"].write_text(
        json.dumps(
            {
                "incident_count": 2,
                "incidents": [
                    {"incident_id": "INC-001", "incident_title": "Checkout issue"},
                    {"incident_id": "INC-002", "incident_title": "Shipping issue"},
                ],
            }
        ),
        encoding="utf-8",
    )
    write_csv(paths["forecasts"], [{"date": "2026-01-04", "kpi": "net_revenue", "prediction": 130}])
    write_csv(
        paths["explanations"],
        [
            {"kpi": "net_revenue", "feature": "website_visitors", "rank": 1},
            {"kpi": "net_revenue", "feature": "conversion_rate", "rank": 2},
        ],
    )
    paths["actionable"].write_text("# Executive Operations Report\n\nReview checkout recovery.", encoding="utf-8")
    paths["knowledge_base"].parent.mkdir(parents=True, exist_ok=True)
    paths["knowledge_base"].write_bytes(b"placeholder")


def test_health_reports_ready_when_outputs_exist(monkeypatch, tmp_path):
    paths = configure_paths(monkeypatch, tmp_path)
    write_outputs(paths)
    client = TestClient(api.app)

    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ready"
    assert payload["read_only"] is True
    assert payload["missing_outputs"] == []


def test_health_reports_degraded_when_outputs_are_missing(monkeypatch, tmp_path):
    configure_paths(monkeypatch, tmp_path)
    client = TestClient(api.app)

    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "degraded"
    assert "kpis" in payload["missing_outputs"]


def test_kpis_returns_recent_rows(monkeypatch, tmp_path):
    paths = configure_paths(monkeypatch, tmp_path)
    write_outputs(paths)
    client = TestClient(api.app)

    response = client.get("/kpis?limit=2")

    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] == 2
    assert [row["date"] for row in payload["rows"]] == ["2026-01-02", "2026-01-03"]


def test_kpis_returns_friendly_missing_file_error(monkeypatch, tmp_path):
    configure_paths(monkeypatch, tmp_path)
    client = TestClient(api.app)

    response = client.get("/kpis")

    assert response.status_code == 404
    assert "Required output file is missing" in response.json()["detail"]


def test_incidents_and_single_incident_endpoints(monkeypatch, tmp_path):
    paths = configure_paths(monkeypatch, tmp_path)
    write_outputs(paths)
    client = TestClient(api.app)

    incidents_response = client.get("/incidents")
    single_response = client.get("/incidents/INC-001")
    missing_response = client.get("/incidents/INC-404")

    assert incidents_response.status_code == 200
    assert incidents_response.json()["count"] == 2
    assert single_response.status_code == 200
    assert single_response.json()["incident"]["incident_title"] == "Checkout issue"
    assert missing_response.status_code == 404
    assert missing_response.json()["detail"] == "Incident not found: INC-404"


def test_forecasts_explanations_and_actionable_report(monkeypatch, tmp_path):
    paths = configure_paths(monkeypatch, tmp_path)
    write_outputs(paths)
    client = TestClient(api.app)

    forecasts_response = client.get("/forecasts")
    explanations_response = client.get("/explanations?limit=1")
    report_response = client.get("/reports/actionable")

    assert forecasts_response.status_code == 200
    assert forecasts_response.json()["rows"][0]["kpi"] == "net_revenue"
    assert explanations_response.status_code == 200
    assert explanations_response.json()["rows"][0]["feature"] == "website_visitors"
    assert report_response.status_code == 200
    assert report_response.json()["format"] == "markdown"
    assert "Executive Operations Report" in report_response.json()["content"]


def test_rag_search_uses_existing_retrieval_code(monkeypatch, tmp_path):
    paths = configure_paths(monkeypatch, tmp_path)
    write_outputs(paths)

    def fake_get_model():
        return object()

    def fake_retrieve(current_incident, knowledge_base_path, top_k, model):
        assert current_incident["title"] == "checkout failures"
        assert knowledge_base_path == paths["knowledge_base"]
        assert top_k == 2
        assert model is not None
        return [{"similarity_score": 0.91, "metadata": {"incident_id": "INC-001"}}]

    monkeypatch.setattr(api, "_get_rag_model", fake_get_model)
    monkeypatch.setattr(api, "retrieve_similar_incidents", fake_retrieve)
    client = TestClient(api.app)

    response = client.get("/rag/search?query=checkout%20failures&top_k=2")

    assert response.status_code == 200
    payload = response.json()
    assert payload["query"] == "checkout failures"
    assert payload["count"] == 1
    assert payload["results"][0]["metadata"]["incident_id"] == "INC-001"


def test_rag_search_requires_knowledge_base_file(monkeypatch, tmp_path):
    paths = configure_paths(monkeypatch, tmp_path)
    write_outputs(paths)
    paths["knowledge_base"].unlink()
    client = TestClient(api.app)

    response = client.get("/rag/search?query=checkout")

    assert response.status_code == 404
    assert "incident_knowledge_base.pkl" in response.json()["detail"]
