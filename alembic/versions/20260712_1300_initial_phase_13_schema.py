"""initial phase 13 schema

Revision ID: 20260712_1300
Revises:
Create Date: 2026-07-12 13:00:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260712_1300"
down_revision = None
branch_labels = None
depends_on = None


def _timestamps() -> list[sa.Column]:
    return [
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    ]


def upgrade() -> None:
    op.create_table(
        "daily_kpis",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("metrics", sa.JSON(), nullable=False),
        sa.Column("dominant_incident_type", sa.String(length=100), nullable=True),
        sa.Column("business_incident_flag", sa.Boolean(), nullable=True),
        sa.Column("incident_signal", sa.Boolean(), nullable=True),
        *_timestamps(),
        sa.UniqueConstraint("date", name="uq_daily_kpis_date"),
    )
    op.create_index("ix_daily_kpis_date", "daily_kpis", ["date"])
    op.create_index("ix_daily_kpis_dominant_incident_type", "daily_kpis", ["dominant_incident_type"])

    op.create_table(
        "anomaly_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("anomaly_type", sa.String(length=100), nullable=False),
        sa.Column("metric", sa.String(length=100), nullable=False),
        sa.Column("value", sa.Float(), nullable=True),
        sa.Column("rolling_mean", sa.Float(), nullable=True),
        sa.Column("rolling_std", sa.Float(), nullable=True),
        sa.Column("z_score", sa.Float(), nullable=True),
        sa.Column("percent_change", sa.Float(), nullable=True),
        sa.Column("severity", sa.String(length=50), nullable=True),
        sa.Column("reason", sa.Text(), nullable=True),
        *_timestamps(),
        sa.UniqueConstraint("date", "anomaly_type", "metric", name="uq_anomaly_event_natural_key"),
    )
    op.create_index("ix_anomaly_events_date", "anomaly_events", ["date"])
    op.create_index("ix_anomaly_events_metric", "anomaly_events", ["metric"])
    op.create_index("ix_anomaly_events_severity", "anomaly_events", ["severity"])
    op.create_index("ix_anomaly_events_type_date", "anomaly_events", ["anomaly_type", "date"])

    op.create_table(
        "incidents",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("incident_id", sa.String(length=80), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("incident_start_date", sa.Date(), nullable=True),
        sa.Column("incident_end_date", sa.Date(), nullable=True),
        sa.Column("main_anomaly_type", sa.String(length=100), nullable=True),
        sa.Column("severity", sa.String(length=50), nullable=True),
        sa.Column("affected_region", sa.String(length=100), nullable=True),
        sa.Column("root_cause_category", sa.String(length=100), nullable=True),
        sa.Column("likely_cause", sa.Text(), nullable=True),
        sa.Column("business_impact_summary", sa.Text(), nullable=True),
        sa.Column("resolution_action", sa.Text(), nullable=True),
        sa.Column("resolution_success", sa.Boolean(), nullable=True),
        sa.Column("recovery_days", sa.Integer(), nullable=True),
        sa.Column("affected_metrics", sa.JSON(), nullable=True),
        sa.Column("recommendations", sa.JSON(), nullable=True),
        sa.Column("supporting_evidence", sa.JSON(), nullable=True),
        sa.Column("retrieved_incidents", sa.JSON(), nullable=True),
        sa.Column("agent_findings", sa.JSON(), nullable=True),
        sa.Column("raw_report", sa.JSON(), nullable=False),
        *_timestamps(),
        sa.UniqueConstraint("incident_id", name="uq_incidents_incident_id"),
    )
    op.create_index("ix_incidents_incident_id", "incidents", ["incident_id"])
    op.create_index("ix_incidents_incident_start_date", "incidents", ["incident_start_date"])
    op.create_index("ix_incidents_incident_end_date", "incidents", ["incident_end_date"])
    op.create_index("ix_incidents_main_anomaly_type", "incidents", ["main_anomaly_type"])
    op.create_index("ix_incidents_severity", "incidents", ["severity"])
    op.create_index("ix_incidents_root_cause_category", "incidents", ["root_cause_category"])

    op.create_table(
        "forecasts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("kpi", sa.String(length=100), nullable=False),
        sa.Column("forecast_day", sa.Integer(), nullable=False),
        sa.Column("prediction", sa.Float(), nullable=True),
        sa.Column("model_name", sa.String(length=100), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=True),
        *_timestamps(),
        sa.UniqueConstraint("date", "kpi", "forecast_day", "model_name", name="uq_forecast_natural_key"),
    )
    op.create_index("ix_forecasts_date", "forecasts", ["date"])
    op.create_index("ix_forecasts_kpi", "forecasts", ["kpi"])
    op.create_index("ix_forecasts_kpi_date", "forecasts", ["kpi", "date"])

    op.create_table(
        "model_metrics",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("kpi", sa.String(length=100), nullable=False),
        sa.Column("model_name", sa.String(length=100), nullable=False),
        sa.Column("mae", sa.Float(), nullable=True),
        sa.Column("rmse", sa.Float(), nullable=True),
        sa.Column("r2", sa.Float(), nullable=True),
        sa.Column("train_rows", sa.Integer(), nullable=True),
        sa.Column("test_rows", sa.Integer(), nullable=True),
        sa.Column("selected_model", sa.Boolean(), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=True),
        *_timestamps(),
        sa.UniqueConstraint("kpi", "model_name", name="uq_model_metric_natural_key"),
    )
    op.create_index("ix_model_metrics_kpi", "model_metrics", ["kpi"])
    op.create_index("ix_model_metrics_selected_model", "model_metrics", ["selected_model"])

    op.create_table(
        "shap_explanations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("kpi", sa.String(length=100), nullable=False),
        sa.Column("model_name", sa.String(length=100), nullable=False),
        sa.Column("feature", sa.String(length=150), nullable=False),
        sa.Column("mean_abs_attribution", sa.Float(), nullable=True),
        sa.Column("rank", sa.Integer(), nullable=True),
        sa.Column("explanation_method", sa.String(length=150), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=True),
        *_timestamps(),
        sa.UniqueConstraint("kpi", "model_name", "feature", name="uq_shap_explanation_natural_key"),
    )
    op.create_index("ix_shap_explanations_kpi", "shap_explanations", ["kpi"])
    op.create_index("ix_shap_kpi_rank", "shap_explanations", ["kpi", "rank"])

    op.create_table(
        "rag_records",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("incident_id", sa.String(length=80), nullable=False),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("incident_type", sa.String(length=255), nullable=True),
        sa.Column("text_chunk", sa.Text(), nullable=True),
        sa.Column("model_name", sa.String(length=255), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=True),
        *_timestamps(),
        sa.UniqueConstraint("incident_id", "chunk_index", name="uq_rag_record_natural_key"),
    )
    op.create_index("ix_rag_records_incident_id", "rag_records", ["incident_id"])

    op.create_table(
        "actionable_reports",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("report_name", sa.String(length=120), nullable=False),
        sa.Column("format", sa.String(length=50), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=True),
        *_timestamps(),
        sa.UniqueConstraint("report_name", name="uq_actionable_reports_report_name"),
    )
    op.create_index("ix_actionable_reports_report_name", "actionable_reports", ["report_name"])

    op.create_table(
        "pipeline_runs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("run_id", sa.String(length=120), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("finished_at", sa.DateTime(), nullable=True),
        sa.Column("source", sa.String(length=120), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=True),
        *_timestamps(),
        sa.UniqueConstraint("run_id", name="uq_pipeline_runs_run_id"),
    )
    op.create_index("ix_pipeline_runs_run_id", "pipeline_runs", ["run_id"])
    op.create_index("ix_pipeline_runs_status", "pipeline_runs", ["status"])


def downgrade() -> None:
    op.drop_table("pipeline_runs")
    op.drop_table("actionable_reports")
    op.drop_table("rag_records")
    op.drop_table("shap_explanations")
    op.drop_table("model_metrics")
    op.drop_table("forecasts")
    op.drop_table("incidents")
    op.drop_table("anomaly_events")
    op.drop_table("daily_kpis")
