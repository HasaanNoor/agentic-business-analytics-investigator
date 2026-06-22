"""Deterministic logistics-focused incident review."""

from __future__ import annotations

import pandas as pd


LOGISTICS_METRICS = [
    "shipping_delay_rate",
    "carrier_capacity_utilization",
    "warehouse_backlog",
    "delivery_complaints",
    "east_region_disruption",
    "west_region_disruption",
    "south_region_disruption",
    "central_region_disruption",
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


def analyze_logistics(incident: dict[str, object], kpis: pd.DataFrame) -> dict[str, object]:
    """Review whether shipping or fulfillment problems contributed to an incident."""
    start_date = pd.Timestamp(incident["incident_start_date"])
    end_date = pd.Timestamp(incident["incident_end_date"])
    metrics = [_window_stats(kpis, metric, start_date, end_date) for metric in LOGISTICS_METRICS if metric in kpis.columns]
    by_metric = {str(metric["metric"]): metric for metric in metrics}

    delay_change = float(by_metric.get("shipping_delay_rate", {}).get("percent_change", 0.0))
    utilization_change = float(by_metric.get("carrier_capacity_utilization", {}).get("percent_change", 0.0))
    backlog_change = float(by_metric.get("warehouse_backlog", {}).get("percent_change", 0.0))
    complaint_change = float(by_metric.get("delivery_complaints", {}).get("percent_change", 0.0))
    active_regions = [
        metric for metric in metrics if str(metric["metric"]).endswith("_region_disruption") and float(metric["maximum"]) > 0
    ]
    logistics_contributed = (
        delay_change >= 20
        or utilization_change >= 10
        or backlog_change >= 20
        or complaint_change >= 20
        or bool(active_regions)
        or incident.get("main_anomaly_type") == "shipping_delay_spike"
        or "shipping_delay_spike" in incident.get("related_anomaly_types", [])
    )

    evidence: list[str] = []
    if "shipping_delay_rate" in by_metric:
        evidence.append(
            "Shipping delay rate averaged "
            f"{by_metric['shipping_delay_rate']['incident_average']} during the incident versus "
            f"{by_metric['shipping_delay_rate']['baseline_average']} before it."
        )
    if "warehouse_backlog" in by_metric:
        evidence.append(f"Warehouse backlog changed {backlog_change}% versus the prior baseline.")
    if "delivery_complaints" in by_metric:
        evidence.append(f"Delivery complaints changed {complaint_change}% versus the prior baseline.")
    if active_regions:
        regions = ", ".join(str(metric["metric"]).replace("_region_disruption", "") for metric in active_regions)
        evidence.append(f"Regional disruption flags were active for: {regions}.")

    if logistics_contributed:
        summary = "Shipping or fulfillment problems likely contributed to this incident."
        recommendations = [
            "Review delayed orders by carrier, warehouse, and affected region.",
            "Reduce warehouse backlog and contact customers with delayed deliveries.",
        ]
        confidence = "high" if delay_change >= 20 or active_regions else "medium"
    else:
        summary = "Logistics signals did not show a clear contribution."
        recommendations = ["Keep monitoring delay rate, backlog, carrier utilization, and delivery complaints."]
        confidence = "low"

    return {
        "agent": "Logistics Agent",
        "finding_type": "logistics",
        "summary": summary,
        "logistics_contributed": logistics_contributed,
        "active_region_flags": [metric["metric"] for metric in active_regions],
        "metrics": metrics,
        "supporting_evidence": evidence,
        "recommended_next_steps": recommendations,
        "confidence": confidence,
    }
