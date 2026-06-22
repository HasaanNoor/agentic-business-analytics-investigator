"""Deterministic customer-support incident review."""

from __future__ import annotations

import pandas as pd


TICKET_METRICS = [
    "support_ticket_count",
    "shipping_complaint_tickets",
    "checkout_issue_tickets",
    "billing_issue_tickets",
    "account_access_tickets",
    "general_support_tickets",
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
        "maximum": _round(incident.max()) if not incident.empty else 0.0,
    }


def analyze_support(incident: dict[str, object], kpis: pd.DataFrame) -> dict[str, object]:
    """Review whether customer complaints increased and which categories changed most."""
    start_date = pd.Timestamp(incident["incident_start_date"])
    end_date = pd.Timestamp(incident["incident_end_date"])
    metrics = [_window_stats(kpis, metric, start_date, end_date) for metric in TICKET_METRICS if metric in kpis.columns]
    categories = [metric for metric in metrics if metric["metric"] != "support_ticket_count"]
    increased_categories = [
        metric for metric in categories if float(metric["change"]) >= 5 or float(metric["percent_change"]) >= 15
    ]
    increased_categories = sorted(increased_categories, key=lambda metric: float(metric["change"]), reverse=True)
    total_metric = next((metric for metric in metrics if metric["metric"] == "support_ticket_count"), {})
    total_change = float(total_metric.get("percent_change", 0.0))
    complaints_increased = (
        total_change >= 15
        or bool(increased_categories)
        or incident.get("main_anomaly_type") == "support_ticket_spike"
        or "support_ticket_spike" in incident.get("related_anomaly_types", [])
    )

    evidence: list[str] = []
    if total_metric:
        evidence.append(
            "Support tickets averaged "
            f"{total_metric['incident_average']} during the incident versus "
            f"{total_metric['baseline_average']} before it."
        )
    for category in increased_categories[:3]:
        evidence.append(
            f"{str(category['metric']).replace('_', ' ')} increased "
            f"{category['percent_change']}% versus the prior baseline."
        )

    if complaints_increased:
        summary = "Customer complaints increased during this incident."
        recommendations = [
            "Review the fastest-growing ticket categories and tag a sample of conversations.",
            "Prepare customer messaging for the dominant complaint type.",
        ]
        confidence = "high" if total_change >= 15 else "medium"
    else:
        summary = "Support volume did not show a clear complaint spike."
        recommendations = ["Continue monitoring ticket volume and category mix after the incident."]
        confidence = "low"

    return {
        "agent": "Customer Support Agent",
        "finding_type": "support",
        "summary": summary,
        "complaints_increased": complaints_increased,
        "top_increased_categories": increased_categories[:3],
        "metrics": metrics,
        "supporting_evidence": evidence,
        "recommended_next_steps": recommendations,
        "confidence": confidence,
    }
