"""Deterministic platform-reliability incident review."""

from __future__ import annotations

import pandas as pd


PLATFORM_METRICS = ["avg_api_latency_ms", "checkout_failure_rate", "deployment_event_flag"]


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


def _nearby_deployments(deployments: pd.DataFrame, start_date: pd.Timestamp, end_date: pd.Timestamp) -> list[dict[str, object]]:
    if deployments.empty:
        return []
    timestamp_column = "timestamp"
    recent = deployments[
        deployments[timestamp_column].between(start_date - pd.Timedelta(days=3), end_date + pd.Timedelta(days=1))
    ]
    records: list[dict[str, object]] = []
    for row in recent.to_dict("records"):
        records.append(
            {
                "timestamp": pd.Timestamp(row["timestamp"]).isoformat(sep=" "),
                "service": row.get("service"),
                "version": row.get("version"),
                "status": row.get("status"),
                "change_type": row.get("change_type"),
                "incident_type": row.get("incident_type"),
            }
        )
    return records


def _failed_or_rollback(deployment: dict[str, object]) -> bool:
    return deployment.get("status") in {"failed", "rollback_success"} or deployment.get("incident_type") == "failed_deployment"


def analyze_platform(incident: dict[str, object], kpis: pd.DataFrame, deployments: pd.DataFrame) -> dict[str, object]:
    """Review whether a release or platform problem contributed to an incident."""
    start_date = pd.Timestamp(incident["incident_start_date"])
    end_date = pd.Timestamp(incident["incident_end_date"])
    metrics = [_window_stats(kpis, metric, start_date, end_date) for metric in PLATFORM_METRICS if metric in kpis.columns]
    by_metric = {str(metric["metric"]): metric for metric in metrics}
    deployment_records = _nearby_deployments(deployments, start_date, end_date)
    failed_deployments = [deployment for deployment in deployment_records if _failed_or_rollback(deployment)]

    latency_change = float(by_metric.get("avg_api_latency_ms", {}).get("percent_change", 0.0))
    failure_change = float(by_metric.get("checkout_failure_rate", {}).get("percent_change", 0.0))
    platform_contributed = (
        latency_change >= 20
        or failure_change >= 20
        or bool(failed_deployments)
        or incident.get("main_anomaly_type") in {"latency_spike", "checkout_failure_spike"}
        or bool({"latency_spike", "checkout_failure_spike"}.intersection(incident.get("related_anomaly_types", [])))
    )

    evidence: list[str] = []
    if "avg_api_latency_ms" in by_metric:
        evidence.append(
            "API latency averaged "
            f"{by_metric['avg_api_latency_ms']['incident_average']} ms during the incident versus "
            f"{by_metric['avg_api_latency_ms']['baseline_average']} ms before it."
        )
    if "checkout_failure_rate" in by_metric:
        evidence.append(f"Checkout failure rate changed {failure_change}% versus the prior baseline.")
    if failed_deployments:
        services = sorted({str(deployment.get("service")) for deployment in failed_deployments})
        evidence.append(
            f"{len(failed_deployments)} failed or rollback deployment event(s) occurred near the incident "
            f"for {', '.join(services)}."
        )

    if platform_contributed:
        summary = "A software release or platform issue likely contributed to this incident."
        recommendations = [
            "Review failed deployments, rollback timing, API latency, and checkout errors.",
            "Add release checks for checkout failure rate and API latency before full rollout.",
        ]
        confidence = "high" if failed_deployments else "medium"
    else:
        summary = "Platform signals did not show a clear software or reliability contribution."
        recommendations = ["Continue monitoring API latency, checkout failures, and deployment events."]
        confidence = "low"

    return {
        "agent": "Platform Reliability Agent",
        "finding_type": "platform",
        "summary": summary,
        "platform_contributed": platform_contributed,
        "deployment_events": deployment_records,
        "metrics": metrics,
        "supporting_evidence": evidence,
        "recommended_next_steps": recommendations,
        "confidence": confidence,
    }
