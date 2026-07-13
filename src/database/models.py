"""SQLAlchemy models for persisted analytics outputs."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from sqlalchemy import Boolean, Date, DateTime, Float, Index, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class DailyKPI(TimestampMixin, Base):
    __tablename__ = "daily_kpis"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[date] = mapped_column(Date, nullable=False, unique=True, index=True)
    metrics: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    dominant_incident_type: Mapped[str | None] = mapped_column(String(100), index=True)
    business_incident_flag: Mapped[bool | None] = mapped_column(Boolean)
    incident_signal: Mapped[bool | None] = mapped_column(Boolean)


class AnomalyEvent(TimestampMixin, Base):
    __tablename__ = "anomaly_events"
    __table_args__ = (
        UniqueConstraint("date", "anomaly_type", "metric", name="uq_anomaly_event_natural_key"),
        Index("ix_anomaly_events_type_date", "anomaly_type", "date"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    anomaly_type: Mapped[str] = mapped_column(String(100), nullable=False)
    metric: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    value: Mapped[float | None] = mapped_column(Float)
    rolling_mean: Mapped[float | None] = mapped_column(Float)
    rolling_std: Mapped[float | None] = mapped_column(Float)
    z_score: Mapped[float | None] = mapped_column(Float)
    percent_change: Mapped[float | None] = mapped_column(Float)
    severity: Mapped[str | None] = mapped_column(String(50), index=True)
    reason: Mapped[str | None] = mapped_column(Text)


class Incident(TimestampMixin, Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    incident_id: Mapped[str] = mapped_column(String(80), nullable=False, unique=True, index=True)
    title: Mapped[str | None] = mapped_column(String(255))
    incident_start_date: Mapped[date | None] = mapped_column(Date, index=True)
    incident_end_date: Mapped[date | None] = mapped_column(Date, index=True)
    main_anomaly_type: Mapped[str | None] = mapped_column(String(100), index=True)
    severity: Mapped[str | None] = mapped_column(String(50), index=True)
    affected_region: Mapped[str | None] = mapped_column(String(100))
    root_cause_category: Mapped[str | None] = mapped_column(String(100), index=True)
    likely_cause: Mapped[str | None] = mapped_column(Text)
    business_impact_summary: Mapped[str | None] = mapped_column(Text)
    resolution_action: Mapped[str | None] = mapped_column(Text)
    resolution_success: Mapped[bool | None] = mapped_column(Boolean)
    recovery_days: Mapped[int | None] = mapped_column(Integer)
    affected_metrics: Mapped[list[Any] | None] = mapped_column(JSON)
    recommendations: Mapped[list[Any] | None] = mapped_column(JSON)
    supporting_evidence: Mapped[list[Any] | None] = mapped_column(JSON)
    retrieved_incidents: Mapped[list[Any] | None] = mapped_column(JSON)
    agent_findings: Mapped[list[Any] | None] = mapped_column(JSON)
    execution_mode: Mapped[str | None] = mapped_column(String(50), index=True)
    model_name: Mapped[str | None] = mapped_column(String(120))
    fallback_used: Mapped[bool | None] = mapped_column(Boolean, index=True)
    fallback_reason: Mapped[str | None] = mapped_column(Text)
    provenance: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    prompt_version: Mapped[str | None] = mapped_column(String(120))
    schema_version: Mapped[str | None] = mapped_column(String(120))
    raw_report: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)


class Forecast(TimestampMixin, Base):
    __tablename__ = "forecasts"
    __table_args__ = (
        UniqueConstraint("date", "kpi", "forecast_day", "model_name", name="uq_forecast_natural_key"),
        Index("ix_forecasts_kpi_date", "kpi", "date"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    kpi: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    forecast_day: Mapped[int] = mapped_column(Integer, nullable=False)
    prediction: Mapped[float | None] = mapped_column(Float)
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    metadata_: Mapped[dict[str, Any] | None] = mapped_column("metadata", JSON)


class ModelMetric(TimestampMixin, Base):
    __tablename__ = "model_metrics"
    __table_args__ = (UniqueConstraint("kpi", "model_name", name="uq_model_metric_natural_key"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    kpi: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    mae: Mapped[float | None] = mapped_column(Float)
    rmse: Mapped[float | None] = mapped_column(Float)
    r2: Mapped[float | None] = mapped_column(Float)
    train_rows: Mapped[int | None] = mapped_column(Integer)
    test_rows: Mapped[int | None] = mapped_column(Integer)
    selected_model: Mapped[bool | None] = mapped_column(Boolean, index=True)
    metadata_: Mapped[dict[str, Any] | None] = mapped_column("metadata", JSON)


class ShapExplanation(TimestampMixin, Base):
    __tablename__ = "shap_explanations"
    __table_args__ = (
        UniqueConstraint("kpi", "model_name", "feature", name="uq_shap_explanation_natural_key"),
        Index("ix_shap_kpi_rank", "kpi", "rank"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    kpi: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    feature: Mapped[str] = mapped_column(String(150), nullable=False)
    mean_abs_attribution: Mapped[float | None] = mapped_column(Float)
    rank: Mapped[int | None] = mapped_column(Integer)
    explanation_method: Mapped[str | None] = mapped_column(String(150))
    metadata_: Mapped[dict[str, Any] | None] = mapped_column("metadata", JSON)


class RagRecord(TimestampMixin, Base):
    __tablename__ = "rag_records"
    __table_args__ = (UniqueConstraint("incident_id", "chunk_index", name="uq_rag_record_natural_key"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    incident_id: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    incident_type: Mapped[str | None] = mapped_column(String(255))
    text_chunk: Mapped[str | None] = mapped_column(Text)
    model_name: Mapped[str | None] = mapped_column(String(255))
    metadata_: Mapped[dict[str, Any] | None] = mapped_column("metadata", JSON)


class ActionableReport(TimestampMixin, Base):
    __tablename__ = "actionable_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    report_name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True, index=True)
    format: Mapped[str] = mapped_column(String(50), nullable=False, default="markdown")
    content: Mapped[str] = mapped_column(Text, nullable=False)
    metadata_: Mapped[dict[str, Any] | None] = mapped_column("metadata", JSON)


class PipelineRun(TimestampMixin, Base):
    __tablename__ = "pipeline_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    run_id: Mapped[str] = mapped_column(String(120), nullable=False, unique=True, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime)
    source: Mapped[str | None] = mapped_column(String(120))
    metadata_: Mapped[dict[str, Any] | None] = mapped_column("metadata", JSON)
