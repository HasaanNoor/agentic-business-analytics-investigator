"""Synchronize generated pipeline outputs into the database."""

from __future__ import annotations

import argparse
import json
import pickle
import sys
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any

import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.database import crud
from src.database.models import Base
from src.database.session import SessionLocal, create_database_engine


PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"
RAG_DIR = PROJECT_ROOT / "outputs" / "rag"

KPI_SUMMARY_PATH = REPORTS_DIR / "kpi_summary_daily.csv"
ANOMALY_EVENTS_PATH = REPORTS_DIR / "anomaly_events.csv"
INVESTIGATION_REPORTS_PATH = REPORTS_DIR / "investigation_reports.json"
MULTI_AGENT_REPORTS_PATH = REPORTS_DIR / "multi_agent_investigation_reports.json"
FORECAST_SUMMARY_PATH = REPORTS_DIR / "forecast_summary.csv"
MODEL_METRICS_PATH = REPORTS_DIR / "model_metrics.csv"
SHAP_FEATURE_IMPORTANCE_PATH = REPORTS_DIR / "shap_feature_importance.csv"
ACTIONABLE_REPORT_PATH = REPORTS_DIR / "executive_operations_report.md"
KNOWLEDGE_BASE_PATH = RAG_DIR / "incident_knowledge_base.pkl"

REQUIRED_FILES = {
    "kpis": KPI_SUMMARY_PATH,
    "anomalies": ANOMALY_EVENTS_PATH,
    "incidents": MULTI_AGENT_REPORTS_PATH,
    "forecasts": FORECAST_SUMMARY_PATH,
    "model_metrics": MODEL_METRICS_PATH,
    "shap_explanations": SHAP_FEATURE_IMPORTANCE_PATH,
}

OPTIONAL_FILES = {
    "first_pass_incidents": INVESTIGATION_REPORTS_PATH,
    "actionable_report": ACTIONABLE_REPORT_PATH,
    "rag_knowledge_base": KNOWLEDGE_BASE_PATH,
}


class SyncError(RuntimeError):
    """Raised when output synchronization cannot complete."""


@dataclass
class SyncSummary:
    inserted: int = 0
    updated: int = 0
    skipped: int = 0
    failed: int = 0
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def record(self, created: bool) -> None:
        if created:
            self.inserted += 1
        else:
            self.updated += 1

    def as_dict(self) -> dict[str, Any]:
        return {
            "inserted": self.inserted,
            "updated": self.updated,
            "skipped": self.skipped,
            "failed": self.failed,
            "warnings": self.warnings,
            "errors": self.errors,
        }


def _require_files() -> None:
    missing = [f"{name}: {path}" for name, path in REQUIRED_FILES.items() if not path.exists()]
    if missing:
        raise SyncError("Missing required output file(s): " + "; ".join(missing))


def _warn_optional(summary: SyncSummary) -> None:
    for name, path in OPTIONAL_FILES.items():
        if not path.exists():
            summary.warnings.append(f"Optional output file is missing and was skipped: {name}: {path}")


def _clean_value(value: Any) -> Any:
    if pd.isna(value):
        return None
    if hasattr(value, "item"):
        return value.item()
    return value


def _to_date(value: Any) -> date | None:
    value = _clean_value(value)
    if value is None or isinstance(value, date):
        return value
    return date.fromisoformat(str(value)[:10])


def _to_bool(value: Any) -> bool | None:
    value = _clean_value(value)
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    text = str(value).strip().lower()
    if text in {"true", "1", "yes"}:
        return True
    if text in {"false", "0", "no"}:
        return False
    return None


def _read_csv(path: Path) -> list[dict[str, Any]]:
    frame = pd.read_csv(path)
    records = frame.where(pd.notna(frame), None).to_dict(orient="records")
    return [{key: _clean_value(value) for key, value in row.items()} for row in records]


def _read_incidents(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    incidents = payload.get("incidents") if isinstance(payload, dict) else None
    if not isinstance(incidents, list):
        raise SyncError(f"Incident file is missing an incidents list: {path}")
    return [incident for incident in incidents if isinstance(incident, dict)]


def _sync_kpis(session: Session, summary: SyncSummary) -> None:
    for row in _read_csv(KPI_SUMMARY_PATH):
        row["date"] = _to_date(row["date"])
        row["business_incident_flag"] = _to_bool(row.get("business_incident_flag"))
        row["incident_signal"] = _to_bool(row.get("incident_signal"))
        _, created = crud.upsert_daily_kpi(session, row)
        summary.record(created)


def _sync_anomalies(session: Session, summary: SyncSummary) -> None:
    for row in _read_csv(ANOMALY_EVENTS_PATH):
        row["date"] = _to_date(row["date"])
        _, created = crud.upsert_anomaly_event(session, row)
        summary.record(created)


def _sync_incidents(session: Session, summary: SyncSummary) -> None:
    incidents = _read_incidents(MULTI_AGENT_REPORTS_PATH)
    for incident in incidents:
        _, created = crud.upsert_incident(session, incident)
        summary.record(created)


def _sync_forecasts(session: Session, summary: SyncSummary) -> None:
    for row in _read_csv(FORECAST_SUMMARY_PATH):
        row["date"] = _to_date(row["date"])
        row["forecast_day"] = int(row["forecast_day"])
        _, created = crud.upsert_forecast(session, row)
        summary.record(created)


def _sync_model_metrics(session: Session, summary: SyncSummary) -> None:
    for row in _read_csv(MODEL_METRICS_PATH):
        row["train_rows"] = int(row["train_rows"]) if row.get("train_rows") is not None else None
        row["test_rows"] = int(row["test_rows"]) if row.get("test_rows") is not None else None
        row["selected_model"] = _to_bool(row.get("selected_model"))
        _, created = crud.upsert_model_metric(session, row)
        summary.record(created)


def _sync_shap_explanations(session: Session, summary: SyncSummary) -> None:
    for row in _read_csv(SHAP_FEATURE_IMPORTANCE_PATH):
        row["rank"] = int(row["rank"]) if row.get("rank") is not None else None
        _, created = crud.upsert_shap_explanation(session, row)
        summary.record(created)


def _sync_actionable_report(session: Session, summary: SyncSummary) -> None:
    if not ACTIONABLE_REPORT_PATH.exists():
        summary.skipped += 1
        return
    row = {
        "report_name": "executive_operations_report",
        "format": "markdown",
        "content": ACTIONABLE_REPORT_PATH.read_text(encoding="utf-8"),
        "metadata": {"source_path": str(ACTIONABLE_REPORT_PATH)},
    }
    _, created = crud.upsert_actionable_report(session, row)
    summary.record(created)


def _sync_rag_metadata(session: Session, summary: SyncSummary) -> None:
    if not KNOWLEDGE_BASE_PATH.exists():
        summary.skipped += 1
        return
    with KNOWLEDGE_BASE_PATH.open("rb") as handle:
        payload = pickle.load(handle)
    text_chunks = payload.get("text_chunks", []) if isinstance(payload, dict) else []
    metadata_rows = payload.get("metadata", []) if isinstance(payload, dict) else []
    model_name = payload.get("model_name") if isinstance(payload, dict) else None
    if not isinstance(text_chunks, list) or not isinstance(metadata_rows, list):
        raise SyncError(f"RAG knowledge base has unexpected shape: {KNOWLEDGE_BASE_PATH}")
    for index, metadata in enumerate(metadata_rows):
        if not isinstance(metadata, dict):
            summary.skipped += 1
            continue
        incident_id = str(metadata.get("incident_id") or f"unknown-{index}")
        row = {
            "incident_id": incident_id,
            "chunk_index": index,
            "incident_type": metadata.get("incident_type"),
            "text_chunk": text_chunks[index] if index < len(text_chunks) else None,
            "model_name": model_name,
            "metadata": metadata,
        }
        _, created = crud.upsert_rag_record(session, row)
        summary.record(created)


def _record_sync_run(session: Session, summary: SyncSummary) -> None:
    _, created = crud.record_pipeline_run(
        session,
        {
            "run_id": "sync_outputs_latest",
            "status": "success" if summary.failed == 0 else "failed",
            "started_at": None,
            "finished_at": datetime.utcnow(),
            "source": "sync_outputs.py",
            "metadata": summary.as_dict(),
        },
    )
    summary.record(created)


def sync_outputs(session: Session | None = None, create_tables: bool = False) -> SyncSummary:
    summary = SyncSummary()
    _require_files()
    _warn_optional(summary)

    owns_session = session is None
    if owns_session:
        session = SessionLocal()
    assert session is not None

    try:
        if create_tables:
            Base.metadata.create_all(bind=session.get_bind())
        with session.begin():
            _sync_kpis(session, summary)
            _sync_anomalies(session, summary)
            _sync_incidents(session, summary)
            _sync_forecasts(session, summary)
            _sync_model_metrics(session, summary)
            _sync_shap_explanations(session, summary)
            _sync_actionable_report(session, summary)
            _sync_rag_metadata(session, summary)
            _record_sync_run(session, summary)
    except Exception as exc:
        summary.failed += 1
        summary.errors.append(str(exc))
        session.rollback()
        raise
    finally:
        if owns_session:
            session.close()
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Synchronize generated outputs into the configured database.")
    parser.add_argument("--database-url", default=None, help="Optional database URL. Defaults to DATABASE_URL or local SQLite.")
    parser.add_argument("--create-tables", action="store_true", help="Create tables before syncing. Use Alembic in production.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.database_url:
        engine = create_database_engine(args.database_url)
        session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, future=True)
        session = session_factory()
        try:
            summary = sync_outputs(session=session, create_tables=args.create_tables)
        finally:
            session.close()
    else:
        summary = sync_outputs(create_tables=args.create_tables)
    print("Synchronization summary:")
    for key, value in summary.as_dict().items():
        print(f"- {key}: {value}")


if __name__ == "__main__":
    main()
