"""Small CRUD helpers for persisted analytics outputs."""

from __future__ import annotations

from collections.abc import Iterable
from datetime import date, datetime
from typing import Any, TypeVar

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from src.database import models


ModelT = TypeVar("ModelT")


def _upsert(session: Session, model: type[ModelT], lookup: dict[str, Any], values: dict[str, Any]) -> tuple[ModelT, bool]:
    instance = None
    for pending in session.new:
        if isinstance(pending, model) and all(getattr(pending, key) == value for key, value in lookup.items()):
            instance = pending
            break
    if instance is None:
        instance = session.execute(select(model).filter_by(**lookup)).scalar_one_or_none()
    created = instance is None
    if created:
        instance = model(**lookup)  # type: ignore[call-arg]
        session.add(instance)
    for key, value in values.items():
        setattr(instance, key, value)
    if hasattr(instance, "updated_at"):
        setattr(instance, "updated_at", datetime.utcnow())
    return instance, created


def _all(session: Session, statement: Select[tuple[ModelT]]) -> list[ModelT]:
    return list(session.execute(statement).scalars().all())


def _coerce_date(value: Any) -> date | None:
    if value is None or isinstance(value, date):
        return value
    return date.fromisoformat(str(value)[:10])


def upsert_daily_kpi(session: Session, row: dict[str, Any]) -> tuple[models.DailyKPI, bool]:
    metrics = {key: value for key, value in row.items() if key != "date"}
    return _upsert(
        session,
        models.DailyKPI,
        {"date": row["date"]},
        {
            "metrics": metrics,
            "dominant_incident_type": row.get("dominant_incident_type"),
            "business_incident_flag": row.get("business_incident_flag"),
            "incident_signal": row.get("incident_signal"),
        },
    )


def upsert_anomaly_event(session: Session, row: dict[str, Any]) -> tuple[models.AnomalyEvent, bool]:
    lookup = {"date": row["date"], "anomaly_type": row["anomaly_type"], "metric": row["metric"]}
    values = {key: row.get(key) for key in ("value", "rolling_mean", "rolling_std", "z_score", "percent_change", "severity", "reason")}
    return _upsert(session, models.AnomalyEvent, lookup, values)


def upsert_incident(session: Session, incident: dict[str, Any]) -> tuple[models.Incident, bool]:
    date_range = incident.get("date_range") if isinstance(incident.get("date_range"), dict) else {}
    start_date = _coerce_date(incident.get("incident_start_date") or date_range.get("start"))
    end_date = _coerce_date(incident.get("incident_end_date") or date_range.get("end"))
    provenance = incident.get("provenance") if isinstance(incident.get("provenance"), dict) else {}
    return _upsert(
        session,
        models.Incident,
        {"incident_id": str(incident["incident_id"])},
        {
            "title": incident.get("incident_title") or incident.get("title"),
            "incident_start_date": start_date,
            "incident_end_date": end_date,
            "main_anomaly_type": incident.get("main_anomaly_type"),
            "severity": incident.get("incident_severity") or incident.get("severity"),
            "affected_region": incident.get("affected_region"),
            "root_cause_category": incident.get("root_cause_category"),
            "likely_cause": incident.get("likely_cause"),
            "business_impact_summary": incident.get("business_impact_summary"),
            "resolution_action": incident.get("resolution_action"),
            "resolution_success": incident.get("resolution_success"),
            "recovery_days": incident.get("recovery_days"),
            "affected_metrics": incident.get("affected_metrics"),
            "recommendations": incident.get("recommended_next_steps") or incident.get("recommendations"),
            "supporting_evidence": incident.get("supporting_evidence"),
            "retrieved_incidents": incident.get("retrieved_incidents"),
            "agent_findings": incident.get("agent_findings"),
            "execution_mode": incident.get("execution_mode") or provenance.get("execution_mode"),
            "model_name": incident.get("model_name") or provenance.get("model_name"),
            "fallback_used": incident.get("fallback_used") if "fallback_used" in incident else provenance.get("fallback_used"),
            "fallback_reason": incident.get("fallback_reason") or provenance.get("fallback_reason"),
            "provenance": provenance or None,
            "prompt_version": incident.get("prompt_version") or provenance.get("prompt_version"),
            "schema_version": incident.get("schema_version") or provenance.get("schema_version"),
            "raw_report": incident,
        },
    )


def upsert_forecast(session: Session, row: dict[str, Any]) -> tuple[models.Forecast, bool]:
    lookup = {"date": row["date"], "kpi": row["kpi"], "forecast_day": row["forecast_day"], "model_name": row["model_name"]}
    return _upsert(session, models.Forecast, lookup, {"prediction": row.get("prediction"), "metadata_": row.get("metadata")})


def upsert_model_metric(session: Session, row: dict[str, Any]) -> tuple[models.ModelMetric, bool]:
    lookup = {"kpi": row["kpi"], "model_name": row["model_name"]}
    values = {
        "mae": row.get("mae"),
        "rmse": row.get("rmse"),
        "r2": row.get("r2"),
        "train_rows": row.get("train_rows"),
        "test_rows": row.get("test_rows"),
        "selected_model": row.get("selected_model"),
        "metadata_": row.get("metadata"),
    }
    return _upsert(session, models.ModelMetric, lookup, values)


def upsert_shap_explanation(session: Session, row: dict[str, Any]) -> tuple[models.ShapExplanation, bool]:
    lookup = {"kpi": row["kpi"], "model_name": row["model_name"], "feature": row["feature"]}
    values = {
        "mean_abs_attribution": row.get("mean_abs_attribution"),
        "rank": row.get("rank"),
        "explanation_method": row.get("explanation_method"),
        "metadata_": row.get("metadata"),
    }
    return _upsert(session, models.ShapExplanation, lookup, values)


def upsert_rag_record(session: Session, row: dict[str, Any]) -> tuple[models.RagRecord, bool]:
    lookup = {"incident_id": row["incident_id"], "chunk_index": row["chunk_index"]}
    values = {
        "incident_type": row.get("incident_type"),
        "text_chunk": row.get("text_chunk"),
        "model_name": row.get("model_name"),
        "metadata_": row.get("metadata"),
    }
    return _upsert(session, models.RagRecord, lookup, values)


def upsert_actionable_report(session: Session, row: dict[str, Any]) -> tuple[models.ActionableReport, bool]:
    lookup = {"report_name": row["report_name"]}
    values = {"format": row.get("format", "markdown"), "content": row["content"], "metadata_": row.get("metadata")}
    return _upsert(session, models.ActionableReport, lookup, values)


def record_pipeline_run(session: Session, row: dict[str, Any]) -> tuple[models.PipelineRun, bool]:
    lookup = {"run_id": row["run_id"]}
    values = {
        "status": row.get("status"),
        "started_at": row.get("started_at"),
        "finished_at": row.get("finished_at"),
        "source": row.get("source"),
        "metadata_": row.get("metadata"),
    }
    return _upsert(session, models.PipelineRun, lookup, values)


def list_kpis(session: Session, limit: int = 30) -> list[dict[str, Any]]:
    rows = _all(session, select(models.DailyKPI).order_by(models.DailyKPI.date.desc()).limit(limit))
    return [_daily_kpi_to_record(row) for row in reversed(rows)]


def list_incidents(session: Session) -> list[dict[str, Any]]:
    rows = _all(session, select(models.Incident).order_by(models.Incident.incident_start_date, models.Incident.incident_id))
    return [_incident_to_record(row) for row in rows]


def get_incident(session: Session, incident_id: str) -> dict[str, Any] | None:
    row = session.execute(select(models.Incident).where(models.Incident.incident_id == incident_id)).scalar_one_or_none()
    return _incident_to_record(row) if row else None


def list_forecasts(session: Session) -> list[dict[str, Any]]:
    rows = _all(session, select(models.Forecast).order_by(models.Forecast.kpi, models.Forecast.date, models.Forecast.forecast_day))
    return [_forecast_to_record(row) for row in rows]


def list_shap_explanations(session: Session, limit: int = 20) -> list[dict[str, Any]]:
    rows = _all(session, select(models.ShapExplanation).order_by(models.ShapExplanation.kpi, models.ShapExplanation.rank).limit(limit))
    return [_shap_to_record(row) for row in rows]


def get_actionable_report(session: Session, report_name: str = "executive_operations_report") -> dict[str, Any] | None:
    row = session.execute(select(models.ActionableReport).where(models.ActionableReport.report_name == report_name)).scalar_one_or_none()
    if not row:
        return None
    return {"format": row.format, "content": row.content}


def count_records(session: Session, model: type[Any]) -> int:
    return int(session.execute(select(func.count()).select_from(model)).scalar_one())


def _date_to_text(value: date | None) -> str | None:
    return value.isoformat() if value else None


def _daily_kpi_to_record(row: models.DailyKPI) -> dict[str, Any]:
    return {"date": _date_to_text(row.date), **(row.metrics or {})}


def _incident_to_record(row: models.Incident) -> dict[str, Any]:
    if row.raw_report:
        return row.raw_report
    return {
        "incident_id": row.incident_id,
        "incident_title": row.title,
        "date_range": {"start": _date_to_text(row.incident_start_date), "end": _date_to_text(row.incident_end_date)},
        "main_anomaly_type": row.main_anomaly_type,
        "incident_severity": row.severity,
        "affected_region": row.affected_region,
        "root_cause_category": row.root_cause_category,
        "likely_cause": row.likely_cause,
        "business_impact_summary": row.business_impact_summary,
        "resolution_action": row.resolution_action,
        "resolution_success": row.resolution_success,
        "recovery_days": row.recovery_days,
        "affected_metrics": row.affected_metrics or [],
        "recommended_next_steps": row.recommendations or [],
        "supporting_evidence": row.supporting_evidence or [],
        "retrieved_incidents": row.retrieved_incidents or [],
        "agent_findings": row.agent_findings or [],
        "execution_mode": row.execution_mode,
        "model_name": row.model_name,
        "fallback_used": row.fallback_used,
        "fallback_reason": row.fallback_reason,
        "provenance": row.provenance or {},
        "prompt_version": row.prompt_version,
        "schema_version": row.schema_version,
    }


def _forecast_to_record(row: models.Forecast) -> dict[str, Any]:
    return {
        "date": _date_to_text(row.date),
        "kpi": row.kpi,
        "forecast_day": row.forecast_day,
        "prediction": row.prediction,
        "model_name": row.model_name,
    }


def _shap_to_record(row: models.ShapExplanation) -> dict[str, Any]:
    return {
        "kpi": row.kpi,
        "model_name": row.model_name,
        "feature": row.feature,
        "mean_abs_attribution": row.mean_abs_attribution,
        "rank": row.rank,
        "explanation_method": row.explanation_method,
    }
