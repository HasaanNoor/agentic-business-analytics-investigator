"""Compact evidence bundles for optional LLM agents."""

from __future__ import annotations

from typing import Any

import pandas as pd


COMMON_FIELDS = [
    "incident_id",
    "title",
    "incident_start_date",
    "incident_end_date",
    "main_anomaly_type",
    "related_anomaly_types",
    "incident_severity",
    "affected_region",
    "likely_cause",
    "root_cause_category",
    "business_impact_summary",
    "affected_metrics",
    "supporting_evidence",
    "recommended_next_steps",
]

DOMAIN_METRICS = {
    "revenue": [
        "net_revenue",
        "website_visitors",
        "active_customers",
        "conversion_rate",
        "average_order_value",
        "refund_rate",
        "checkout_failure_rate",
        "stockout_units",
        "lost_sales_units",
    ],
    "support": [
        "support_ticket_count",
        "shipping_complaint_tickets",
        "checkout_issue_tickets",
        "billing_issue_tickets",
        "account_access_tickets",
        "delivery_complaints",
    ],
    "logistics": [
        "shipping_delay_rate",
        "carrier_capacity_utilization",
        "warehouse_backlog",
        "delivery_complaints",
        "east_region_disruption",
        "west_region_disruption",
        "south_region_disruption",
        "central_region_disruption",
        "stockout_units",
    ],
    "platform": [
        "avg_api_latency_ms",
        "checkout_failure_rate",
        "deployment_event_flag",
        "checkout_issue_tickets",
        "support_ticket_count",
    ],
}

DOMAIN_FORECASTS = {
    "revenue": {"net_revenue"},
    "support": {"support_ticket_count"},
    "logistics": {"shipping_delay_rate"},
    "platform": {"net_revenue", "support_ticket_count"},
}


def _clean(value: Any) -> Any:
    if pd.isna(value):
        return None
    if hasattr(value, "item"):
        return value.item()
    if isinstance(value, pd.Timestamp):
        return value.date().isoformat()
    return value


def _records(frame: pd.DataFrame, max_rows: int = 20) -> list[dict[str, Any]]:
    return [{key: _clean(value) for key, value in row.items()} for row in frame.head(max_rows).to_dict("records")]


def _window(kpis: pd.DataFrame, incident: dict[str, Any]) -> pd.DataFrame:
    start = pd.Timestamp(incident["incident_start_date"])
    end = pd.Timestamp(incident["incident_end_date"])
    return kpis.loc[kpis["date"].between(start - pd.Timedelta(days=14), end + pd.Timedelta(days=7))].copy()


def _metric_summary(kpis: pd.DataFrame, incident: dict[str, Any], metrics: list[str]) -> list[dict[str, Any]]:
    start = pd.Timestamp(incident["incident_start_date"])
    end = pd.Timestamp(incident["incident_end_date"])
    rows: list[dict[str, Any]] = []
    for metric in metrics:
        if metric not in kpis.columns:
            continue
        incident_values = kpis.loc[kpis["date"].between(start, end), metric].astype(float)
        baseline_values = kpis.loc[kpis["date"].between(start - pd.Timedelta(days=14), start - pd.Timedelta(days=1)), metric].astype(float)
        incident_avg = round(float(incident_values.mean()), 6) if not incident_values.empty else 0.0
        baseline_avg = round(float(baseline_values.mean()), 6) if not baseline_values.empty else 0.0
        change = incident_avg - baseline_avg
        rows.append(
            {
                "metric": metric,
                "incident_average": incident_avg,
                "baseline_average": baseline_avg,
                "change": round(change, 6),
                "percent_change": round((change / baseline_avg * 100), 6) if baseline_avg else 0.0,
                "minimum": round(float(incident_values.min()), 6) if not incident_values.empty else 0.0,
                "maximum": round(float(incident_values.max()), 6) if not incident_values.empty else 0.0,
            }
        )
    return rows


def _forecast_context(forecasts: pd.DataFrame, domain: str) -> list[dict[str, Any]]:
    if forecasts.empty:
        return []
    allowed = DOMAIN_FORECASTS[domain]
    subset = forecasts[forecasts["kpi"].isin(allowed)].sort_values(["kpi", "forecast_day"])
    return _records(subset, max_rows=14)


def _shap_context(shap_importance: pd.DataFrame, metrics: list[str], top_n: int = 3) -> list[dict[str, Any]]:
    if shap_importance.empty:
        return []
    subset = shap_importance[shap_importance["kpi"].isin(metrics)].sort_values(["kpi", "rank"])
    rows: list[dict[str, Any]] = []
    for kpi, group in subset.groupby("kpi"):
        rows.append({"kpi": str(kpi), "top_drivers": _records(group, max_rows=top_n)})
    return rows


def _retrieved_context(retrieved_incidents: list[dict[str, Any]] | None, top_k: int = 3) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in (retrieved_incidents or [])[:top_k]:
        metadata = item.get("metadata", {}) if isinstance(item, dict) else {}
        if not isinstance(metadata, dict):
            continue
        rows.append(
            {
                "incident_id": metadata.get("incident_id"),
                "incident_type": metadata.get("incident_type"),
                "root_cause": metadata.get("root_cause"),
                "resolution": metadata.get("resolution"),
                "outcome": metadata.get("outcome"),
                "similarity_score": item.get("similarity_score"),
                "recommendations_used_previously": item.get("recommendations_used_previously", []),
            }
        )
    return rows


def _deployment_context(deployments: pd.DataFrame, incident: dict[str, Any]) -> list[dict[str, Any]]:
    if deployments.empty:
        return []
    start = pd.Timestamp(incident["incident_start_date"])
    end = pd.Timestamp(incident["incident_end_date"])
    subset = deployments[deployments["timestamp"].between(start - pd.Timedelta(days=3), end + pd.Timedelta(days=1))]
    return _records(subset.sort_values("timestamp"), max_rows=12)


def _truncate_text(value: Any, max_chars: int) -> Any:
    if isinstance(value, str) and len(value) > max_chars:
        return value[: max_chars - 16].rstrip() + " [truncated]"
    if isinstance(value, list):
        return [_truncate_text(item, max_chars) for item in value]
    if isinstance(value, dict):
        return {key: _truncate_text(item, max_chars) for key, item in value.items()}
    return value


def build_evidence_bundle(
    domain: str,
    incident: dict[str, Any],
    kpis: pd.DataFrame,
    forecasts: pd.DataFrame,
    shap_importance: pd.DataFrame,
    retrieved_incidents: list[dict[str, Any]] | None = None,
    deployments: pd.DataFrame | None = None,
    max_input_characters: int = 24000,
) -> dict[str, Any]:
    metrics = DOMAIN_METRICS[domain]
    window = _window(kpis, incident)
    available_metrics = [metric for metric in metrics if metric in window.columns]
    common_context = {field: incident.get(field) for field in COMMON_FIELDS if field in incident}
    retrieved = _retrieved_context(retrieved_incidents)
    bundle: dict[str, Any] = {
        "incident_id": incident.get("incident_id"),
        "domain": domain,
        "common_context": common_context,
        "metric_summary": _metric_summary(window, incident, available_metrics),
        "daily_metric_window": _records(window[["date", *available_metrics]], max_rows=28),
        "forecast_context": _forecast_context(forecasts, domain),
        "shap_driver_context": _shap_context(shap_importance, available_metrics),
        "retrieved_historical_incidents": retrieved,
        "allowed_metric_names": sorted(set(available_metrics) | set(incident.get("affected_metrics", []) or [])),
        "historical_incident_ids": [str(item["incident_id"]) for item in retrieved if item.get("incident_id")],
        "allowed_dates": [str(item)[:10] for item in window["date"].dt.date.astype(str).tolist()],
        "evidence_sources": ["KPI summary", "forecast summary", "SHAP explanations", "retrieved historical incidents"],
        "context_truncated": False,
        "max_output_characters": 16000,
    }
    if domain == "platform" and deployments is not None:
        bundle["deployment_events"] = _deployment_context(deployments, incident)
        bundle["evidence_sources"].append("deployment events")

    encoded = str(bundle)
    if len(encoded) > max_input_characters:
        bundle = _truncate_text(bundle, max_chars=700)
        bundle["context_truncated"] = True
    return bundle

