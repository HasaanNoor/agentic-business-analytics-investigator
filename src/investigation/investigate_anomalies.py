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
    "latency_spike": 3,
    "revenue_drop": 2,
    "support_ticket_spike": 1,
}

SEVERITY_PRIORITY = {"low": 1, "medium": 2, "high": 3}

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

    main_type = _main_anomaly_type(events)
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
    window_days: int = 3,
) -> list[dict[str, object]]:
    reports: list[dict[str, object]] = []
    for incident_number, events in enumerate(group_anomalies_into_incidents(anomalies, window_days), start=1):
        start_date = events["date"].min()
        end_date = events["date"].max()
        kpi_slice = kpis[kpis["date"].between(start_date, end_date)]
        deployment_records = _deployment_records(deployments, start_date, end_date)
        classification = classify_incident(events, kpis, deployment_records)
        main_type = str(classification["main_anomaly_type"])
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
                f"- **Likely cause:** {report['likely_cause']}",
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
    window_days: int = 3,
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
    parser.add_argument("--window-days", type=int, default=3, help="Maximum gap between consecutive incident events.")
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
