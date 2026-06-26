"""Read-only FastAPI app for generated analytics outputs."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

import pandas as pd
from fastapi import FastAPI, HTTPException, Query

from src.rag.retrieve_incidents import IncidentRetrievalError, load_embedding_model, retrieve_similar_incidents


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"
RAG_DIR = PROJECT_ROOT / "outputs" / "rag"

KPI_SUMMARY_PATH = REPORTS_DIR / "kpi_summary_daily.csv"
INCIDENT_REPORTS_PATH = REPORTS_DIR / "multi_agent_investigation_reports.json"
FORECAST_SUMMARY_PATH = REPORTS_DIR / "forecast_summary.csv"
SHAP_FEATURE_IMPORTANCE_PATH = REPORTS_DIR / "shap_feature_importance.csv"
ACTIONABLE_REPORT_PATH = REPORTS_DIR / "executive_operations_report.md"
KNOWLEDGE_BASE_PATH = RAG_DIR / "incident_knowledge_base.pkl"

RECENT_KPI_ROWS = 30
TOP_EXPLANATION_ROWS = 20

app = FastAPI(
    title="Agentic Business Analytics Investigator API",
    version="0.1.0",
    description="Read-only API for generated analytics, incident, forecast, explanation, and report outputs.",
)


def _missing_file_error(path: Path) -> HTTPException:
    return HTTPException(
        status_code=404,
        detail=f"Required output file is missing: {path}. Run the local pipeline first, then retry this endpoint.",
    )


def _load_csv_records(path: Path, limit: int | None = None, tail: bool = False) -> list[dict[str, Any]]:
    if not path.exists():
        raise _missing_file_error(path)
    frame = pd.read_csv(path)
    if limit is not None:
        frame = frame.tail(limit) if tail else frame.head(limit)
    return frame.where(pd.notna(frame), None).to_dict(orient="records")


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise _missing_file_error(path)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=500, detail=f"Could not parse JSON output file: {path}") from exc
    if not isinstance(payload, dict):
        raise HTTPException(status_code=500, detail=f"JSON output file should contain an object: {path}")
    return payload


def _load_markdown(path: Path) -> str:
    if not path.exists():
        raise _missing_file_error(path)
    return path.read_text(encoding="utf-8")


def _incident_list() -> list[dict[str, Any]]:
    payload = _load_json(INCIDENT_REPORTS_PATH)
    incidents = payload.get("incidents")
    if not isinstance(incidents, list):
        raise HTTPException(status_code=500, detail=f"Incident report file is missing an incidents list: {INCIDENT_REPORTS_PATH}")
    return [incident for incident in incidents if isinstance(incident, dict)]


@lru_cache(maxsize=1)
def _get_rag_model() -> object:
    try:
        return load_embedding_model(_load_rag_model_name(), local_files_only=True)
    except IncidentRetrievalError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


def _load_rag_model_name() -> str:
    if not KNOWLEDGE_BASE_PATH.exists():
        raise _missing_file_error(KNOWLEDGE_BASE_PATH)
    from src.rag.retrieve_incidents import load_knowledge_base

    try:
        knowledge_base = load_knowledge_base(KNOWLEDGE_BASE_PATH)
    except IncidentRetrievalError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return str(knowledge_base.get("model_name") or "sentence-transformers/all-MiniLM-L6-v2")


def _query_to_incident(query: str) -> dict[str, Any]:
    return {
        "incident_id": "API-QUERY",
        "title": query,
        "incident_start_date": None,
        "incident_end_date": None,
        "main_anomaly_type": query,
        "related_anomaly_types": [],
        "likely_cause": query,
        "recommended_next_steps": [],
    }


@app.get("/health")
def health() -> dict[str, Any]:
    output_paths = {
        "kpis": KPI_SUMMARY_PATH,
        "incidents": INCIDENT_REPORTS_PATH,
        "forecasts": FORECAST_SUMMARY_PATH,
        "explanations": SHAP_FEATURE_IMPORTANCE_PATH,
        "actionable_report": ACTIONABLE_REPORT_PATH,
        "rag_knowledge_base": KNOWLEDGE_BASE_PATH,
    }
    files = {name: {"path": str(path), "exists": path.exists()} for name, path in output_paths.items()}
    missing = [name for name, info in files.items() if not info["exists"]]
    return {
        "status": "ready" if not missing else "degraded",
        "project": "Agentic Business Analytics Investigator",
        "read_only": True,
        "files": files,
        "missing_outputs": missing,
    }


@app.get("/kpis")
def get_kpis(limit: int = Query(RECENT_KPI_ROWS, ge=1, le=500)) -> dict[str, Any]:
    rows = _load_csv_records(KPI_SUMMARY_PATH, limit=limit, tail=True)
    return {"count": len(rows), "rows": rows}


@app.get("/incidents")
def get_incidents() -> dict[str, Any]:
    incidents = _incident_list()
    return {"count": len(incidents), "incidents": incidents}


@app.get("/incidents/{incident_id}")
def get_incident(incident_id: str) -> dict[str, Any]:
    for incident in _incident_list():
        if str(incident.get("incident_id")) == incident_id:
            return {"incident": incident}
    raise HTTPException(status_code=404, detail=f"Incident not found: {incident_id}")


@app.get("/forecasts")
def get_forecasts() -> dict[str, Any]:
    rows = _load_csv_records(FORECAST_SUMMARY_PATH)
    return {"count": len(rows), "rows": rows}


@app.get("/explanations")
def get_explanations(limit: int = Query(TOP_EXPLANATION_ROWS, ge=1, le=500)) -> dict[str, Any]:
    rows = _load_csv_records(SHAP_FEATURE_IMPORTANCE_PATH, limit=limit)
    return {"count": len(rows), "rows": rows}


@app.get("/reports/actionable")
def get_actionable_report() -> dict[str, Any]:
    return {"format": "markdown", "content": _load_markdown(ACTIONABLE_REPORT_PATH)}


@app.get("/rag/search")
def search_rag(query: str = Query(..., min_length=1), top_k: int = Query(3, ge=1, le=10)) -> dict[str, Any]:
    if not KNOWLEDGE_BASE_PATH.exists():
        raise _missing_file_error(KNOWLEDGE_BASE_PATH)
    try:
        results = retrieve_similar_incidents(
            _query_to_incident(query),
            knowledge_base_path=KNOWLEDGE_BASE_PATH,
            top_k=top_k,
            model=_get_rag_model(),
        )
    except IncidentRetrievalError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return {"query": query, "count": len(results), "results": results}
