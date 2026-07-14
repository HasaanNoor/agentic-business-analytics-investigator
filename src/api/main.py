"""Read-only FastAPI app for generated analytics outputs."""

from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from src.database import crud
from src.database.config import get_database_url, is_database_configured
from src.database.session import SessionLocal, create_database_engine
from src.llm.config import load_agent_mode, load_fallback_enabled, load_llm_config
from src.llm.errors import LLMConfigurationError
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


def _parse_cors_allowed_origins() -> list[str]:
    raw_origins = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:5173")
    return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]


app.add_middleware(
    CORSMiddleware,
    allow_origins=_parse_cors_allowed_origins(),
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)


def _missing_file_error(path: Path) -> HTTPException:
    return HTTPException(
        status_code=404,
        detail=f"Required output file is missing: {path}. Run the local pipeline first, then retry this endpoint.",
    )


def _database_status() -> dict[str, Any]:
    configured = is_database_configured()
    if not configured:
        return {"configured": False, "available": False, "error": None}
    try:
        with _runtime_session_factory()() as session:
            session.execute(text("SELECT 1"))
        return {"configured": True, "available": True, "error": None}
    except SQLAlchemyError as exc:
        return {"configured": True, "available": False, "error": str(exc)}


def _load_from_database(loader):
    if not is_database_configured():
        return None
    try:
        with _runtime_session_factory()() as session:
            session.execute(text("SELECT 1"))
            return loader(session)
    except SQLAlchemyError:
        return None


def _file_fallback(load_file):
    try:
        return load_file()
    except HTTPException as exc:
        if exc.status_code == 404 and is_database_configured():
            raise HTTPException(
                status_code=503,
                detail=(
                    "Neither PostgreSQL nor file fallback data is available for this endpoint. "
                    f"{exc.detail}"
                ),
            ) from exc
        raise


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


def _public_llm_status() -> dict[str, Any]:
    try:
        config = load_llm_config()
        config_error = None
    except LLMConfigurationError as exc:
        config = None
        config_error = str(exc)
    try:
        agent_mode = load_agent_mode()
    except LLMConfigurationError:
        agent_mode = "invalid"
    try:
        fallback_enabled = load_fallback_enabled()
    except LLMConfigurationError:
        fallback_enabled = True
    return {
        "enabled": bool(config.enabled) if config else False,
        "configured": bool(config.configured) if config else False,
        "selected_model": config.model if config and config.model else None,
        "agent_mode": agent_mode,
        "fallback_enabled": fallback_enabled,
        "configuration_error": config_error,
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
    database = _database_status()
    file_fallback_available = not missing
    ready = database["available"] or file_fallback_available
    return {
        "status": "ready" if ready else "degraded",
        "project": "Agentic Business Analytics Investigator",
        "read_only": True,
        "api": {"status": "ok"},
        "database": database,
        "llm": _public_llm_status(),
        "file_fallback": {"available": file_fallback_available, "missing_outputs": missing},
        "ready": ready,
        "files": files,
        "missing_outputs": missing,
    }


@app.get("/llm/status")
def get_llm_status() -> dict[str, Any]:
    return _public_llm_status()


@app.get("/kpis")
def get_kpis(limit: int = Query(RECENT_KPI_ROWS, ge=1, le=500)) -> dict[str, Any]:
    rows = _load_from_database(lambda session: crud.list_kpis(session, limit=limit))
    if rows is None:
        rows = _file_fallback(lambda: _load_csv_records(KPI_SUMMARY_PATH, limit=limit, tail=True))
    return {"count": len(rows), "rows": rows}


@app.get("/incidents")
def get_incidents() -> dict[str, Any]:
    incidents = _load_from_database(crud.list_incidents)
    if incidents is None:
        incidents = _file_fallback(_incident_list)
    return {"count": len(incidents), "incidents": incidents}


@app.get("/incidents/{incident_id}")
def get_incident(incident_id: str) -> dict[str, Any]:
    if is_database_configured():
        try:
            with _runtime_session_factory()() as session:
                session.execute(text("SELECT 1"))
                incident = crud.get_incident(session, incident_id)
                if incident is not None:
                    return {"incident": incident}
                raise HTTPException(status_code=404, detail=f"Incident not found: {incident_id}")
        except SQLAlchemyError:
            pass
    incidents = _file_fallback(_incident_list)
    for incident_record in incidents:
        if str(incident_record.get("incident_id")) == incident_id:
            return {"incident": incident_record}
    raise HTTPException(status_code=404, detail=f"Incident not found: {incident_id}")


@app.get("/forecasts")
def get_forecasts() -> dict[str, Any]:
    rows = _load_from_database(crud.list_forecasts)
    if rows is None:
        rows = _file_fallback(lambda: _load_csv_records(FORECAST_SUMMARY_PATH))
    return {"count": len(rows), "rows": rows}


@app.get("/explanations")
def get_explanations(limit: int = Query(TOP_EXPLANATION_ROWS, ge=1, le=500)) -> dict[str, Any]:
    rows = _load_from_database(lambda session: crud.list_shap_explanations(session, limit=limit))
    if rows is None:
        rows = _file_fallback(lambda: _load_csv_records(SHAP_FEATURE_IMPORTANCE_PATH, limit=limit))
    return {"count": len(rows), "rows": rows}


@app.get("/reports/actionable")
def get_actionable_report() -> dict[str, Any]:
    report = _load_from_database(crud.get_actionable_report)
    if report is not None:
        return report
    return {"format": "markdown", "content": _file_fallback(lambda: _load_markdown(ACTIONABLE_REPORT_PATH))}


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


def _runtime_session_factory():
    configured_url = get_database_url()
    try:
        bind = SessionLocal.kw.get("bind")
        current_url = str(bind.url) if bind is not None else None
    except AttributeError:
        current_url = None
    if is_database_configured() and current_url != configured_url:
        engine = create_database_engine(configured_url)
        return sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, future=True)
    return SessionLocal
