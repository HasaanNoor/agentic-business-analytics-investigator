"""Combine specialist agent findings into final incident reports."""

from __future__ import annotations

from collections import Counter

import pandas as pd


CONFIDENCE_SCORE = {"low": 1, "medium": 2, "high": 3}


def _top_forecast_rows(forecasts: pd.DataFrame) -> list[dict[str, object]]:
    if forecasts.empty:
        return []
    rows: list[dict[str, object]] = []
    for kpi, group in forecasts.sort_values("forecast_day").groupby("kpi"):
        first = group.iloc[0]
        last = group.iloc[-1]
        rows.append(
            {
                "kpi": str(kpi),
                "start_date": str(first["date"]),
                "end_date": str(last["date"]),
                "start_prediction": round(float(first["prediction"]), 4),
                "end_prediction": round(float(last["prediction"]), 4),
                "model_name": str(last["model_name"]),
            }
        )
    return sorted(rows, key=lambda row: str(row["kpi"]))


def _top_shap_features(shap_importance: pd.DataFrame, max_per_kpi: int = 3) -> list[dict[str, object]]:
    if shap_importance.empty:
        return []
    rows: list[dict[str, object]] = []
    for kpi, group in shap_importance.sort_values(["kpi", "rank"]).groupby("kpi"):
        rows.append(
            {
                "kpi": str(kpi),
                "top_features": [
                    {
                        "feature": str(row["feature"]),
                        "rank": int(row["rank"]),
                        "mean_abs_attribution": round(float(row["mean_abs_attribution"]), 6),
                    }
                    for row in group.head(max_per_kpi).to_dict("records")
                ],
            }
        )
    return rows


def _combined_confidence(findings: list[dict[str, object]]) -> str:
    if not findings:
        return "low"
    average = sum(CONFIDENCE_SCORE.get(str(finding.get("confidence")), 1) for finding in findings) / len(findings)
    if average >= 2.4:
        return "high"
    if average >= 1.6:
        return "medium"
    return "low"


def _likely_cause(incident: dict[str, object], findings: list[dict[str, object]]) -> str:
    existing_cause = str(incident.get("likely_cause", ""))
    if existing_cause and existing_cause != "No known deterministic root-cause pattern matched":
        return existing_cause

    positive_findings = [
        finding
        for finding in findings
        if finding.get("sales_affected")
        or finding.get("complaints_increased")
        or finding.get("logistics_contributed")
        or finding.get("platform_contributed")
    ]
    if not positive_findings:
        return existing_cause or "No clear cause found by deterministic agents"

    priority = ["platform", "logistics", "support", "revenue"]
    counter = Counter(str(finding.get("finding_type")) for finding in positive_findings)
    best_type = sorted(counter, key=lambda item: (-counter[item], priority.index(item) if item in priority else 99))[0]
    labels = {
        "platform": "Likely platform reliability incident",
        "logistics": "Likely logistics disruption incident",
        "support": "Likely customer-impact incident",
        "revenue": "Likely sales-impact incident",
    }
    return labels.get(best_type, "Likely operational incident")


def coordinate_incident_report(
    incident: dict[str, object],
    findings: list[dict[str, object]],
    forecasts: pd.DataFrame,
    shap_importance: pd.DataFrame,
    retrieved_incidents: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    """Build one clear report from the specialist agent findings."""
    evidence: list[str] = list(incident.get("supporting_evidence", []) or [])
    if retrieved_incidents:
        evidence.append(f"{len(retrieved_incidents)} similar historical incident(s) were retrieved for recommendation context.")
    for finding in findings:
        evidence.extend(finding.get("supporting_evidence", []) or [])

    recommendations: list[str] = []
    for recommendation in incident.get("recommended_next_steps", []) or []:
        if recommendation not in recommendations:
            recommendations.append(str(recommendation))
    for finding in findings:
        for recommendation in finding.get("recommended_next_steps", []) or []:
            if recommendation not in recommendations:
                recommendations.append(str(recommendation))
    for item in retrieved_incidents or []:
        for recommendation in item.get("recommendations_used_previously", []) or []:
            historical_recommendation = f"Historical precedent: {recommendation}"
            if historical_recommendation not in recommendations:
                recommendations.append(historical_recommendation)

    return {
        "incident_id": incident.get("incident_id"),
        "incident_title": incident.get("title"),
        "date_range": {
            "start": incident.get("incident_start_date"),
            "end": incident.get("incident_end_date"),
        },
        "main_anomaly_type": incident.get("main_anomaly_type"),
        "related_anomaly_types": incident.get("related_anomaly_types", []),
        "incident_severity": incident.get("incident_severity", "not specified"),
        "affected_region": incident.get("affected_region", "not specified"),
        "root_cause_category": incident.get("root_cause_category", "not specified"),
        "business_impact_summary": incident.get("business_impact_summary", "not specified"),
        "resolution_action": incident.get("resolution_action", "not specified"),
        "resolution_success": incident.get("resolution_success"),
        "recovery_days": incident.get("recovery_days"),
        "affected_metrics": incident.get("affected_metrics", []),
        "likely_cause": _likely_cause(incident, findings),
        "agent_findings": findings,
        "supporting_evidence": evidence,
        "retrieved_historical_incidents": retrieved_incidents or [],
        "forecast_context": _top_forecast_rows(forecasts),
        "model_driver_context": _top_shap_features(shap_importance),
        "recommended_next_steps": recommendations,
        "confidence_level": _combined_confidence(findings),
    }


def build_final_reports(
    incidents: list[dict[str, object]],
    findings_by_incident: dict[str, list[dict[str, object]]],
    forecasts: pd.DataFrame,
    shap_importance: pd.DataFrame,
    retrieved_by_incident: dict[str, list[dict[str, object]]] | None = None,
) -> list[dict[str, object]]:
    return [
        coordinate_incident_report(
            incident=incident,
            findings=findings_by_incident.get(str(incident.get("incident_id")), []),
            forecasts=forecasts,
            shap_importance=shap_importance,
            retrieved_incidents=(retrieved_by_incident or {}).get(str(incident.get("incident_id")), []),
        )
        for incident in incidents
    ]
