"""Build deterministic incident investigations from KPI anomaly events."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Iterable

import pandas as pd


LOGGER = logging.getLogger(__name__)

ANOMALY_PRIORITY = {
    "checkout_failure_spike": 6,
    "inventory_shortage_period": 5,
    "shipping_delay_spike": 4,
    "warehouse_backlog_spike": 4,
    "latency_spike": 3,
    "refund_spike": 3,
    "visitor_surge": 3,
    "revenue_drop": 2,
    "support_ticket_spike": 1,
    "inventory_shortage": 5,
    "supplier_delay": 5,
    "warehouse_staffing_shortage": 4,
    "carrier_outage": 4,
    "regional_weather_disruption": 4,
    "refund_spike": 3,
    "api_degradation": 6,
    "marketing_campaign_surge": 3,
    "holiday_demand_surge": 3,
    "fraud_spike": 3,
    "failed_deployment": 6,
    "shipping_disruption": 4,
}

SEVERITY_PRIORITY = {"low": 1, "medium": 2, "high": 3, "critical": 4}
SEVERITY_LABELS = {1: "low", 2: "medium", 3: "high", 4: "critical"}

GENERIC_RECOMMENDATIONS = {
    "checkout_failure_spike": [
        "Inspect checkout errors and dependency health for the incident window.",
        "Confirm checkout failure rate and revenue have returned to baseline.",
    ],
    "inventory_shortage_period": [
        "Review replenishment timing and inventory forecasts for affected products.",
        "Prioritize restocking and monitor lost sales until stockouts clear.",
    ],
    "shipping_delay_spike": [
        "Review carrier performance and delayed shipment queues.",
        "Notify affected customers and monitor delivery complaints.",
    ],
    "latency_spike": [
        "Inspect service latency by endpoint and dependency.",
        "Confirm latency has returned to its rolling baseline.",
    ],
    "revenue_drop": [
        "Review conversion, checkout, inventory, and logistics signals for revenue impact.",
        "Monitor net revenue against its rolling baseline.",
    ],
    "support_ticket_spike": [
        "Review support ticket categories to identify the dominant customer issue.",
        "Confirm ticket volume returns to baseline after remediation.",
    ],
    "refund_spike": [
        "Review refund reasons and recent billing, fraud, and delivery changes.",
        "Confirm refund rate and net revenue return to baseline.",
    ],
    "visitor_surge": [
        "Review campaign, holiday, and capacity signals for demand pressure.",
        "Confirm conversion rate and support coverage can handle the traffic increase.",
    ],
    "warehouse_backlog_spike": [
        "Review staffing, picking queues, and carrier handoff capacity.",
        "Prioritize aged orders until backlog returns to baseline.",
    ],
}

ENRICHMENT_BY_ANOMALY = {
    "failed_deployment": {
        "root_cause_category": "platform release",
        "business_impact_summary": "A failed deployment increased reliability risk and customer impact.",
        "resolution_action": "Rolled back the failed deployment and validated checkout health after rollback.",
        "recovery_days": 2,
    },
    "api_degradation": {
        "root_cause_category": "platform reliability",
        "business_impact_summary": "API latency rose, checkout failures increased, and conversion rate declined.",
        "resolution_action": "Rolled back the slow dependency and added latency alerts for the checkout path.",
        "recovery_days": 2,
    },
    "checkout_failure_spike": {
        "root_cause_category": "platform reliability",
        "business_impact_summary": "Checkout failures reduced conversion and increased customer contacts.",
        "resolution_action": "Rolled back the risky checkout change and added checkout health checks.",
        "recovery_days": 2,
    },
    "latency_spike": {
        "root_cause_category": "platform reliability",
        "business_impact_summary": "API latency slowed checkout and increased support volume.",
        "resolution_action": "Reduced API latency by rolling back the slow dependency and scaling checkout workers.",
        "recovery_days": 2,
    },
    "inventory_shortage": {
        "root_cause_category": "inventory planning",
        "business_impact_summary": "Stockouts created lost sales and customer complaints.",
        "resolution_action": "Transferred inventory from another warehouse and expedited replenishment.",
        "recovery_days": 3,
    },
    "inventory_shortage_period": {
        "root_cause_category": "inventory planning",
        "business_impact_summary": "Stockouts created lost sales and customer complaints.",
        "resolution_action": "Transferred inventory from another warehouse and expedited replenishment.",
        "recovery_days": 3,
    },
    "supplier_delay": {
        "root_cause_category": "supplier operations",
        "business_impact_summary": "Late inbound replenishment increased stockouts and lost sales.",
        "resolution_action": "Expedited inbound freight and split the delayed order across receiving docks.",
        "recovery_days": 5,
    },
    "shipping_disruption": {
        "root_cause_category": "logistics",
        "business_impact_summary": "Shipping disruption increased delivery delays and customer complaints.",
        "resolution_action": "Rerouted affected orders through backup carriers and prioritized delayed deliveries.",
        "recovery_days": 3,
    },
    "shipping_delay_spike": {
        "root_cause_category": "logistics",
        "business_impact_summary": "Shipping delays increased delivery complaints and delayed order completion.",
        "resolution_action": "Rerouted affected orders through backup carriers and prioritized delayed deliveries.",
        "recovery_days": 3,
    },
    "warehouse_backlog_spike": {
        "root_cause_category": "warehouse labor",
        "business_impact_summary": "Warehouse backlog slowed fulfillment and increased logistics pressure.",
        "resolution_action": "Added temporary warehouse shifts and cleared aged outbound orders first.",
        "recovery_days": 4,
    },
    "warehouse_staffing_shortage": {
        "root_cause_category": "warehouse labor",
        "business_impact_summary": "Warehouse staffing gaps increased backlog and delayed shipments.",
        "resolution_action": "Added temporary warehouse shifts and cleared aged outbound orders first.",
        "recovery_days": 4,
    },
    "carrier_outage": {
        "root_cause_category": "carrier reliability",
        "business_impact_summary": "Carrier capacity dropped, shipping delays increased, and delivery complaints rose.",
        "resolution_action": "Rerouted affected shipments to backup carriers and upgraded priority orders.",
        "recovery_days": 3,
    },
    "regional_weather_disruption": {
        "root_cause_category": "weather",
        "business_impact_summary": "Regional weather slowed deliveries and increased logistics complaints.",
        "resolution_action": "Paused delivery promises in the affected region and rerouted shipments through nearby hubs.",
        "recovery_days": 3,
    },
    "refund_spike": {
        "root_cause_category": "returns and fraud",
        "business_impact_summary": "Refunds increased and reduced net revenue.",
        "resolution_action": "Audited refund reasons, fixed the highest-volume cause, and reviewed suspected fraud.",
        "recovery_days": 2,
    },
    "visitor_surge": {
        "root_cause_category": "demand surge",
        "business_impact_summary": "Traffic increased quickly, creating capacity and support pressure.",
        "resolution_action": "Added support coverage and monitored checkout capacity during the traffic surge.",
        "recovery_days": 1,
    },
    "marketing_campaign_surge": {
        "root_cause_category": "demand generation",
        "business_impact_summary": "Marketing traffic increased quickly and raised support and capacity pressure.",
        "resolution_action": "Kept the campaign active while adding support coverage and checkout monitoring.",
        "recovery_days": 1,
    },
    "holiday_demand_surge": {
        "root_cause_category": "seasonal demand",
        "business_impact_summary": "Holiday demand increased orders, backlog, and support contacts.",
        "resolution_action": "Opened holiday fulfillment lanes and moved high-demand SKUs closer to customers.",
        "recovery_days": 4,
    },
    "fraud_spike": {
        "root_cause_category": "fraud controls",
        "business_impact_summary": "Fraud reviews and refund requests increased, reducing completed revenue.",
        "resolution_action": "Tightened fraud rules, manually reviewed held orders, and refunded confirmed fraud cases.",
        "recovery_days": 3,
    },
    "support_ticket_spike": {
        "root_cause_category": "customer experience",
        "business_impact_summary": "Customer contacts increased and required additional support review.",
        "resolution_action": "Triaged the largest ticket category and published customer-facing updates.",
        "recovery_days": 2,
    },
    "revenue_drop": {
        "root_cause_category": "sales impact",
        "business_impact_summary": "Net revenue fell below its normal range during the incident.",
        "resolution_action": "Reviewed conversion, stockout, refund, and logistics signals before selecting remediation.",
        "recovery_days": 3,
    },
}


class InvestigationError(RuntimeError):
    """Raised when deterministic investigation cannot complete."""


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s - %(message)s")


def load_inputs(
    kpi_path: Path,
    anomaly_path: Path,
    deployment_path: Path,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    for path in (kpi_path, anomaly_path, deployment_path):
        if not path.exists():
            raise InvestigationError(f"Missing required input file: {path}")

    kpis = pd.read_csv(kpi_path)
    anomalies = pd.read_csv(anomaly_path)
    deployments = pd.read_csv(deployment_path)

    required_anomaly_columns = {"date", "anomaly_type", "metric", "value", "severity", "reason"}
    missing_anomaly_columns = required_anomaly_columns - set(anomalies.columns)
    if "date" not in kpis.columns:
        raise InvestigationError(f"KPI summary missing required date column: {kpi_path}")
    if missing_anomaly_columns:
        raise InvestigationError(
            f"Anomaly events missing required columns: {', '.join(sorted(missing_anomaly_columns))}"
        )
    if "timestamp" not in deployments.columns:
        raise InvestigationError(f"Deployment events missing required timestamp column: {deployment_path}")

    kpis["date"] = pd.to_datetime(kpis["date"], errors="raise").dt.normalize()
    anomalies["date"] = pd.to_datetime(anomalies["date"], errors="raise").dt.normalize()
    deployments["timestamp"] = pd.to_datetime(deployments["timestamp"], errors="raise")

    return (
        kpis.sort_values("date").reset_index(drop=True),
        anomalies.sort_values(["date", "anomaly_type"]).reset_index(drop=True),
        deployments.sort_values("timestamp").reset_index(drop=True),
    )


def group_anomalies_into_incidents(anomalies: pd.DataFrame, window_days: int = 3) -> list[pd.DataFrame]:
    """Group anomalies transitively when consecutive event dates are within the window."""
    if window_days < 0:
        raise InvestigationError("Incident window must be zero or greater.")
    if anomalies.empty:
        return []

    ordered = anomalies.sort_values(["date", "anomaly_type"]).reset_index(drop=True)
    groups: list[list[int]] = [[0]]
    previous_date = ordered.loc[0, "date"]

    for index in range(1, len(ordered)):
        event_date = ordered.loc[index, "date"]
        if (event_date - previous_date).days <= window_days:
            groups[-1].append(index)
        else:
            groups.append([index])
        previous_date = event_date

    return [ordered.loc[indexes].reset_index(drop=True) for indexes in groups]


def _float(value: object) -> float:
    return round(float(value), 4)


def _summarize_affected_kpis(
    events: pd.DataFrame,
    kpi_slice: pd.DataFrame,
    contextual_metrics: Iterable[str] = (),
) -> list[dict[str, object]]:
    summaries: list[dict[str, object]] = []
    metrics = list(events["metric"].drop_duplicates())
    metrics.extend(metric for metric in contextual_metrics if metric not in metrics)
    for metric in metrics:
        metric_events = events[events["metric"] == metric]
        values = kpi_slice[metric].astype(float) if metric in kpi_slice.columns else metric_events["value"].astype(float)
        summaries.append(
            {
                "metric": metric,
                "anomaly_types": sorted(metric_events["anomaly_type"].unique().tolist()),
                "event_count": int(len(metric_events)),
                "minimum": _float(values.min()),
                "maximum": _float(values.max()),
                "average": _float(values.mean()),
                "largest_absolute_percent_change": _float(metric_events["percent_change"].abs().max())
                if not metric_events.empty and "percent_change" in metric_events
                else None,
            }
        )
    return summaries


def _kpi_signal(
    kpis: pd.DataFrame,
    metric: str,
    start_date: pd.Timestamp,
    end_date: pd.Timestamp,
    baseline_days: int = 14,
) -> dict[str, float]:
    incident_values = kpis.loc[kpis["date"].between(start_date, end_date), metric].astype(float)
    baseline_values = kpis.loc[
        kpis["date"].between(start_date - pd.Timedelta(days=baseline_days), start_date - pd.Timedelta(days=1)),
        metric,
    ].astype(float)
    return {
        "minimum": _float(incident_values.min()),
        "maximum": _float(incident_values.max()),
        "average": _float(incident_values.mean()),
        "baseline_average": _float(baseline_values.mean()) if not baseline_values.empty else 0.0,
    }


def _deployment_records(deployments: pd.DataFrame, start_date: pd.Timestamp, end_date: pd.Timestamp) -> list[dict[str, object]]:
    recent = deployments[
        deployments["timestamp"].between(start_date - pd.Timedelta(days=3), end_date + pd.Timedelta(days=1))
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


def _main_anomaly_type(events: pd.DataFrame) -> str:
    ranked = (
        events.assign(
            severity_rank=events["severity"].map(SEVERITY_PRIORITY).fillna(0),
            type_rank=events["anomaly_type"].map(ANOMALY_PRIORITY).fillna(0),
        )
        .groupby("anomaly_type", as_index=False)
        .agg(max_severity=("severity_rank", "max"), event_count=("anomaly_type", "size"), type_rank=("type_rank", "max"))
        .sort_values(["max_severity", "event_count", "type_rank", "anomaly_type"], ascending=[False, False, False, True])
    )
    return str(ranked.iloc[0]["anomaly_type"])


def _incident_severity(events: pd.DataFrame) -> str:
    rank = int(events["severity"].map(SEVERITY_PRIORITY).fillna(1).max())
    distinct_types = int(events["anomaly_type"].nunique())
    event_count = int(len(events))
    if rank >= 3 and (event_count >= 8 or distinct_types >= 4):
        return "critical"
    if rank >= 3 or event_count >= 5 or distinct_types >= 3:
        return "high"
    if rank >= 2 or event_count >= 3:
        return "medium"
    return "low"


def _affected_region(kpi_slice: pd.DataFrame) -> str:
    region_columns = {
        "east_region_disruption": "Northeast",
        "west_region_disruption": "West",
        "south_region_disruption": "Southeast",
        "central_region_disruption": "Midwest",
    }
    scores = {
        region: int(kpi_slice[column].sum())
        for column, region in region_columns.items()
        if column in kpi_slice.columns
    }
    if not scores or max(scores.values()) == 0:
        return "All regions"
    return sorted(scores, key=lambda region: (-scores[region], region))[0]


def _enrichment_for_incident(
    main_type: str,
    events: pd.DataFrame,
    kpi_slice: pd.DataFrame,
    classification: dict[str, object],
) -> dict[str, object]:
    template = dict(ENRICHMENT_BY_ANOMALY.get(main_type, ENRICHMENT_BY_ANOMALY["support_ticket_spike"]))
    affected_metrics = sorted(set(events["metric"].astype(str).tolist()))
    for metric in ("net_revenue", "support_ticket_count", "refund_rate", "lost_sales_units", "delivery_complaints"):
        if metric in kpi_slice.columns and metric not in affected_metrics:
            affected_metrics.append(metric)
    severity = _incident_severity(events)
    recovery_days = int(template["recovery_days"]) + (1 if severity in {"high", "critical"} else 0)
    return {
        "incident_severity": severity,
        "affected_region": _affected_region(kpi_slice),
        "root_cause_category": template["root_cause_category"],
        "business_impact_summary": template["business_impact_summary"],
        "resolution_action": template["resolution_action"],
        "resolution_success": severity != "critical",
        "recovery_days": recovery_days,
        "affected_metrics": affected_metrics,
    }


def _is_failed_deployment(deployment: dict[str, object]) -> bool:
    return deployment.get("status") in {"failed", "rollback_success"} or deployment.get("incident_type") == "failed_deployment"


def classify_incident(
    events: pd.DataFrame,
    kpis: pd.DataFrame,
    deployment_records: list[dict[str, object]],
) -> dict[str, object]:
    types = set(events["anomaly_type"])
    start_date = events["date"].min()
    end_date = events["date"].max()
    failed_deployments = [deployment for deployment in deployment_records if _is_failed_deployment(deployment)]

    if {"latency_spike", "checkout_failure_spike"}.issubset(types) and failed_deployments:
        services = sorted({str(deployment["service"]) for deployment in failed_deployments})
        return {
            "main_anomaly_type": "checkout_failure_spike",
            "title": "Deployment-related checkout incident",
            "likely_cause": "Likely deployment-related checkout incident",
            "possible_contributing_factors": [
                f"Failed or rolled-back deployment affecting {', '.join(services)}",
                "Elevated API latency",
                "Elevated checkout failure rate",
            ],
            "supporting_evidence": [
                f"Latency and checkout failure anomalies occurred together from {start_date.date()} to {end_date.date()}.",
                f"{len(failed_deployments)} failed or rollback deployment event(s) occurred within the investigation window.",
            ],
            "recommended_next_steps": [
                "Review the failed checkout deployment, dependency changes, and rollback results.",
                "Validate checkout success rate, API latency, and revenue after rollback.",
                "Add deployment health gates for checkout latency and failure rate.",
            ],
        }

    lost_sales = _kpi_signal(kpis, "lost_sales_units", start_date, end_date)
    if {"inventory_shortage_period", "revenue_drop"}.issubset(types) and lost_sales["maximum"] > 0:
        return {
            "main_anomaly_type": "inventory_shortage_period",
            "title": "Inventory shortage incident",
            "likely_cause": "Likely inventory shortage incident",
            "possible_contributing_factors": [
                "Stockout units were reported",
                "Lost sales occurred during the shortage",
                "Net revenue dropped during the incident window",
            ],
            "supporting_evidence": [
                f"Inventory shortage and revenue drop anomalies overlapped from {start_date.date()} to {end_date.date()}.",
                f"Lost sales units reached {lost_sales['maximum']:.2f} during the incident.",
            ],
            "recommended_next_steps": [
                "Prioritize replenishment for stocked-out products.",
                "Review demand forecasts, reorder points, and supplier lead times.",
                "Track lost sales and net revenue until inventory availability recovers.",
            ],
        }

    complaints = _kpi_signal(kpis, "delivery_complaints", start_date, end_date)
    complaints_elevated = complaints["maximum"] > max(complaints["baseline_average"] * 1.5, complaints["baseline_average"] + 5)
    if "shipping_delay_spike" in types and complaints_elevated:
        return {
            "main_anomaly_type": "shipping_delay_spike",
            "title": "Logistics disruption incident",
            "likely_cause": "Likely logistics disruption incident",
            "possible_contributing_factors": [
                "Shipping delay rate increased",
                "Delivery complaints rose above the prior baseline",
            ],
            "supporting_evidence": [
                f"Shipping delay anomalies occurred from {start_date.date()} to {end_date.date()}.",
                f"Delivery complaints reached {complaints['maximum']:.2f} versus a prior average of "
                f"{complaints['baseline_average']:.2f}.",
            ],
            "recommended_next_steps": [
                "Review carrier performance and delayed shipment queues.",
                "Notify affected customers and prioritize delayed deliveries.",
                "Monitor shipping delay rate and delivery complaints until both return to baseline.",
            ],
        }

    refunds = _kpi_signal(kpis, "refund_rate", start_date, end_date)
    if "refund_spike" in types and refunds["maximum"] > max(refunds["baseline_average"] * 1.25, refunds["baseline_average"] + 0.01):
        return {
            "main_anomaly_type": "refund_spike",
            "title": "Refund spike incident",
            "likely_cause": "Likely refund, billing, or fraud incident",
            "possible_contributing_factors": [
                "Refund rate rose above baseline",
                "Billing or fraud-related support contacts may have increased",
                "Net revenue may be reduced by higher refunds",
            ],
            "supporting_evidence": [
                f"Refund anomalies occurred from {start_date.date()} to {end_date.date()}.",
                f"Refund rate reached {refunds['maximum']:.4f} versus a prior average of {refunds['baseline_average']:.4f}.",
            ],
            "recommended_next_steps": [
                "Review refund reasons, billing changes, fraud decisions, and recent delivery problems.",
                "Prioritize customer outreach for confirmed billing or fraud issues.",
                "Monitor refund rate and net revenue until both recover.",
            ],
        }

    visitors = _kpi_signal(kpis, "website_visitors", start_date, end_date)
    if "visitor_surge" in types:
        return {
            "main_anomaly_type": "visitor_surge",
            "title": "Demand surge incident",
            "likely_cause": "Likely marketing campaign or holiday demand surge",
            "possible_contributing_factors": [
                "Website visitors rose above baseline",
                "Support volume or fulfillment pressure may have increased",
            ],
            "supporting_evidence": [
                f"Visitor surge anomalies occurred from {start_date.date()} to {end_date.date()}.",
                f"Website visitors reached {visitors['maximum']:.2f} versus a prior average of "
                f"{visitors['baseline_average']:.2f}.",
            ],
            "recommended_next_steps": [
                "Confirm whether a campaign, holiday event, or promotion drove the traffic increase.",
                "Add support coverage and monitor checkout, inventory, and fulfillment capacity.",
                "Keep successful demand actions active only while service levels remain healthy.",
            ],
        }

    backlog = _kpi_signal(kpis, "warehouse_backlog", start_date, end_date)
    if "warehouse_backlog_spike" in types:
        return {
            "main_anomaly_type": "warehouse_backlog_spike",
            "title": "Warehouse backlog incident",
            "likely_cause": "Likely warehouse staffing or fulfillment capacity incident",
            "possible_contributing_factors": [
                "Warehouse backlog rose above baseline",
                "Shipping delays or delivery complaints may have followed",
            ],
            "supporting_evidence": [
                f"Warehouse backlog anomalies occurred from {start_date.date()} to {end_date.date()}.",
                f"Warehouse backlog reached {backlog['maximum']:.2f} versus a prior average of "
                f"{backlog['baseline_average']:.2f}.",
            ],
            "recommended_next_steps": [
                "Add temporary warehouse coverage and clear the oldest outbound orders first.",
                "Review carrier handoff capacity and staffing schedule gaps.",
                "Monitor backlog, shipping delay rate, and delivery complaints until recovery.",
            ],
        }

    main_type = _main_anomaly_type(events)
    if main_type in ENRICHMENT_BY_ANOMALY:
        template = ENRICHMENT_BY_ANOMALY[main_type]
        return {
            "main_anomaly_type": main_type,
            "title": main_type.replace("_", " ").title() + " Incident",
            "likely_cause": f"Likely {template['root_cause_category']} incident",
            "possible_contributing_factors": sorted(types),
            "supporting_evidence": [
                f"{len(events)} event(s) for {main_type} were grouped within {start_date.date()} to {end_date.date()}."
            ],
            "recommended_next_steps": [
                str(template["resolution_action"]),
                "Compare the current incident with similar historical incidents before finalizing recommendations.",
                "Monitor affected metrics until recovery is confirmed.",
            ],
        }
    return {
        "main_anomaly_type": main_type,
        "title": main_type.replace("_", " ").title(),
        "likely_cause": "No known deterministic root-cause pattern matched",
        "possible_contributing_factors": sorted(types),
        "supporting_evidence": [
            f"{len(events)} anomaly event(s) across {len(types)} anomaly type(s) were grouped within "
            f"{start_date.date()} to {end_date.date()}."
        ],
        "recommended_next_steps": GENERIC_RECOMMENDATIONS.get(
            main_type, ["Review the grouped anomaly evidence and monitor affected KPIs."]
        ),
    }


def build_incident_reports(
    kpis: pd.DataFrame,
    anomalies: pd.DataFrame,
    deployments: pd.DataFrame,
    window_days: int = 1,
) -> list[dict[str, object]]:
    reports: list[dict[str, object]] = []
    for incident_number, events in enumerate(group_anomalies_into_incidents(anomalies, window_days), start=1):
        start_date = events["date"].min()
        end_date = events["date"].max()
        kpi_slice = kpis[kpis["date"].between(start_date, end_date)]
        deployment_records = _deployment_records(deployments, start_date, end_date)
        classification = classify_incident(events, kpis, deployment_records)
        main_type = str(classification["main_anomaly_type"])
        enrichment = _enrichment_for_incident(main_type, events, kpi_slice, classification)
        related_types = sorted(set(events["anomaly_type"]) - {main_type})
        contextual_metrics: list[str] = []
        if classification["likely_cause"] == "Likely deployment-related checkout incident":
            contextual_metrics.append("conversion_rate")
        if classification["likely_cause"] == "Likely inventory shortage incident":
            contextual_metrics.append("lost_sales_units")
        if classification["likely_cause"] == "Likely logistics disruption incident":
            contextual_metrics.append("delivery_complaints")

        event_records: list[dict[str, object]] = []
        for event in events.to_dict("records"):
            event_records.append(
                {
                    "date": pd.Timestamp(event["date"]).strftime("%Y-%m-%d"),
                    "anomaly_type": event["anomaly_type"],
                    "metric": event["metric"],
                    "value": _float(event["value"]),
                    "severity": event["severity"],
                    "reason": event["reason"],
                }
            )

        reports.append(
            {
                "incident_id": f"INC-{incident_number:03d}",
                "title": classification["title"],
                "incident_start_date": start_date.strftime("%Y-%m-%d"),
                "incident_end_date": end_date.strftime("%Y-%m-%d"),
                "main_anomaly_type": main_type,
                "related_anomaly_types": related_types,
                "likely_cause": classification["likely_cause"],
                **enrichment,
                "affected_kpis": _summarize_affected_kpis(events, kpi_slice, contextual_metrics),
                "possible_contributing_factors": classification["possible_contributing_factors"],
                "supporting_evidence": classification["supporting_evidence"],
                "deployment_events": deployment_records,
                "anomaly_events": event_records,
                "recommended_next_steps": classification["recommended_next_steps"],
            }
        )
    return reports


def write_json_report(reports: list[dict[str, object]], output_path: Path, window_days: int) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "method": "Deterministic anomaly grouping and root-cause rules",
        "incident_window_days": window_days,
        "incident_count": len(reports),
        "incidents": reports,
    }
    output_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    LOGGER.info("Wrote %s incident reports to %s", len(reports), output_path)


def write_markdown_summary(reports: list[dict[str, object]], output_path: Path, window_days: int) -> None:
    lines = [
        "# Deterministic Investigation Summary",
        "",
        f"Generated from anomaly events grouped with a maximum consecutive-event gap of {window_days} days.",
        f"Total incidents: **{len(reports)}**",
        "",
    ]
    for report in reports:
        lines.extend(
            [
                f"## {report['incident_id']}: {report['title']}",
                "",
                f"- **Date range:** {report['incident_start_date']} to {report['incident_end_date']}",
                f"- **Severity:** {report['incident_severity']}",
                f"- **Affected region:** {report['affected_region']}",
                f"- **Likely cause:** {report['likely_cause']}",
                f"- **Root cause category:** {report['root_cause_category']}",
                f"- **Business impact:** {report['business_impact_summary']}",
                f"- **Resolution:** {report['resolution_action']}",
                f"- **Outcome:** success {report['resolution_success']}, recovery {report['recovery_days']} day(s)",
                f"- **Main anomaly:** `{report['main_anomaly_type']}`",
                f"- **Related anomalies:** "
                + (", ".join(f"`{item}`" for item in report["related_anomaly_types"]) or "None"),
                "",
                "### Evidence",
                "",
            ]
        )
        lines.extend(f"- {evidence}" for evidence in report["supporting_evidence"])
        lines.extend(["", "### Affected KPIs", ""])
        for kpi in report["affected_kpis"]:
            lines.append(
                f"- `{kpi['metric']}`: min {kpi['minimum']}, max {kpi['maximum']}, "
                f"average {kpi['average']} ({kpi['event_count']} anomaly event(s))"
            )
        lines.extend(["", "### Recommended Next Steps", ""])
        lines.extend(f"- {recommendation}" for recommendation in report["recommended_next_steps"])
        lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    LOGGER.info("Wrote investigation summary to %s", output_path)


def run_investigation(
    kpi_path: Path,
    anomaly_path: Path,
    deployment_path: Path,
    json_output_path: Path,
    markdown_output_path: Path,
    window_days: int = 1,
) -> list[dict[str, object]]:
    kpis, anomalies, deployments = load_inputs(kpi_path, anomaly_path, deployment_path)
    reports = build_incident_reports(kpis, anomalies, deployments, window_days=window_days)
    write_json_report(reports, json_output_path, window_days)
    write_markdown_summary(reports, markdown_output_path, window_days)
    return reports


def parse_args(args: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build deterministic incident investigations from anomaly events.")
    parser.add_argument("--kpi-path", type=Path, default=Path("outputs/reports/kpi_summary_daily.csv"))
    parser.add_argument("--anomaly-path", type=Path, default=Path("outputs/reports/anomaly_events.csv"))
    parser.add_argument("--deployment-path", type=Path, default=Path("data/synthetic/deployment_events.csv"))
    parser.add_argument("--json-output-path", type=Path, default=Path("outputs/reports/investigation_reports.json"))
    parser.add_argument("--markdown-output-path", type=Path, default=Path("outputs/reports/investigation_summary.md"))
    parser.add_argument("--window-days", type=int, default=1, help="Maximum gap between consecutive incident events.")
    return parser.parse_args(args)


def main(args: Iterable[str] | None = None) -> None:
    configure_logging()
    parsed = parse_args(args)
    run_investigation(
        kpi_path=parsed.kpi_path,
        anomaly_path=parsed.anomaly_path,
        deployment_path=parsed.deployment_path,
        json_output_path=parsed.json_output_path,
        markdown_output_path=parsed.markdown_output_path,
        window_days=parsed.window_days,
    )


if __name__ == "__main__":
    main()
