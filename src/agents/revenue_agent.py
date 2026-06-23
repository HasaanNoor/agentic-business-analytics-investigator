"""Deterministic revenue-focused incident review."""

from __future__ import annotations

import pandas as pd


REVENUE_METRICS = [
    "net_revenue",
    "conversion_rate",
    "refund_rate",
    "website_visitors",
    "average_order_value",
    "stockout_units",
    "lost_sales_units",
]


def _round(value: object) -> float:
    return round(float(value), 4)


def _window_stats(kpis: pd.DataFrame, metric: str, start_date: pd.Timestamp, end_date: pd.Timestamp) -> dict[str, object]:
    incident = kpis.loc[kpis["date"].between(start_date, end_date), metric].astype(float)
    baseline = kpis.loc[
        kpis["date"].between(start_date - pd.Timedelta(days=14), start_date - pd.Timedelta(days=1)),
        metric,
    ].astype(float)
    incident_average = _round(incident.mean()) if not incident.empty else 0.0
    baseline_average = _round(baseline.mean()) if not baseline.empty else 0.0
    change = incident_average - baseline_average
    percent_change = (change / baseline_average * 100) if baseline_average else 0.0
    return {
        "metric": metric,
        "incident_average": incident_average,
        "baseline_average": baseline_average,
        "change": _round(change),
        "percent_change": _round(percent_change),
        "minimum": _round(incident.min()) if not incident.empty else 0.0,
        "maximum": _round(incident.max()) if not incident.empty else 0.0,
    }


def _historical_context(retrieved_incidents: list[dict[str, object]] | None) -> list[dict[str, object]]:
    context: list[dict[str, object]] = []
    for item in retrieved_incidents or []:
        metadata = item.get("metadata", {}) if isinstance(item, dict) else {}
        if not isinstance(metadata, dict):
            continue
        context.append(
            {
                "incident_id": metadata.get("incident_id"),
                "incident_type": metadata.get("incident_type"),
                "similarity_score": item.get("similarity_score"),
                "root_cause": metadata.get("root_cause"),
                "recommendations": item.get("recommendations_used_previously", []),
            }
        )
    return context


def analyze_revenue(
    incident: dict[str, object],
    kpis: pd.DataFrame,
    retrieved_incidents: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    """Review whether an incident likely affected sales."""
    start_date = pd.Timestamp(incident["incident_start_date"])
    end_date = pd.Timestamp(incident["incident_end_date"])
    metrics = [_window_stats(kpis, metric, start_date, end_date) for metric in REVENUE_METRICS if metric in kpis.columns]
    by_metric = {str(metric["metric"]): metric for metric in metrics}

    revenue_change = float(by_metric.get("net_revenue", {}).get("percent_change", 0.0))
    conversion_change = float(by_metric.get("conversion_rate", {}).get("percent_change", 0.0))
    refund_change = float(by_metric.get("refund_rate", {}).get("percent_change", 0.0))
    stockout_max = float(by_metric.get("stockout_units", {}).get("maximum", 0.0))
    lost_sales_max = float(by_metric.get("lost_sales_units", {}).get("maximum", 0.0))

    sales_affected = (
        revenue_change <= -8
        or conversion_change <= -8
        or refund_change >= 15
        or stockout_max > 0
        or lost_sales_max > 0
        or "revenue_drop" in incident.get("related_anomaly_types", [])
        or incident.get("main_anomaly_type") == "revenue_drop"
    )

    evidence: list[str] = []
    if "net_revenue" in by_metric:
        evidence.append(
            "Net revenue averaged "
            f"{by_metric['net_revenue']['incident_average']} during the incident versus "
            f"{by_metric['net_revenue']['baseline_average']} before it."
        )
    if "conversion_rate" in by_metric:
        evidence.append(
            "Conversion rate changed "
            f"{by_metric['conversion_rate']['percent_change']}% versus the prior baseline."
        )
    if lost_sales_max > 0:
        evidence.append(f"Lost sales units reached {lost_sales_max} during the incident window.")
    if stockout_max > 0:
        evidence.append(f"Stockout units reached {stockout_max} during the incident window.")
    if refund_change >= 15:
        evidence.append(f"Refund rate increased {refund_change}% versus the prior baseline.")

    if sales_affected:
        summary = "Sales were likely affected during this incident."
        recommendations = [
            "Check whether conversion rate and revenue recovered after the incident.",
            "Review refunds, stockouts, and lost sales for preventable revenue leakage.",
        ]
        confidence = "high" if revenue_change <= -8 or lost_sales_max > 0 else "medium"
    else:
        summary = "Sales impact was limited based on the available revenue signals."
        recommendations = ["Keep monitoring revenue, conversion rate, refunds, and lost sales after the incident."]
        confidence = "low"

    historical_context = _historical_context(retrieved_incidents)
    if historical_context:
        closest = historical_context[0]
        evidence.append(
            "Historical context: similar incident "
            f"{closest['incident_id']} had root cause '{closest['root_cause']}' "
            f"with similarity score {closest['similarity_score']}."
        )
        recommendations.append("Compare revenue recovery against the closest retrieved historical incident.")

    return {
        "agent": "Revenue Agent",
        "finding_type": "revenue",
        "summary": summary,
        "sales_affected": sales_affected,
        "metrics": metrics,
        "historical_incident_context": historical_context,
        "supporting_evidence": evidence,
        "recommended_next_steps": recommendations,
        "confidence": confidence,
    }
