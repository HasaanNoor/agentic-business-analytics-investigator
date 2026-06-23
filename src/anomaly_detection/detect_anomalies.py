"""Detect deterministic KPI anomalies using rolling statistics."""

from __future__ import annotations

import argparse
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

os.environ.setdefault("MPLCONFIGDIR", str(Path("outputs/.matplotlib")))
os.environ.setdefault("XDG_CACHE_HOME", str(Path("outputs/.cache")))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class AnomalyRule:
    anomaly_type: str
    metric: str
    direction: str
    z_threshold: float
    pct_change_threshold: float
    minimum_value: float | None = None


ANOMALY_RULES = (
    AnomalyRule("revenue_drop", "net_revenue", "drop", 2.0, 0.15),
    AnomalyRule("latency_spike", "avg_api_latency_ms", "spike", 2.5, 0.45),
    AnomalyRule("checkout_failure_spike", "checkout_failure_rate", "spike", 2.5, 0.50),
    AnomalyRule("support_ticket_spike", "support_ticket_count", "spike", 2.0, 0.25),
    AnomalyRule("inventory_shortage_period", "stockout_units", "spike", 1.5, 0.25, minimum_value=1.0),
    AnomalyRule("shipping_delay_spike", "shipping_delay_rate", "spike", 2.0, 0.35),
    AnomalyRule("refund_spike", "refund_rate", "spike", 2.0, 0.30),
    AnomalyRule("visitor_surge", "website_visitors", "spike", 2.0, 0.18),
    AnomalyRule("warehouse_backlog_spike", "warehouse_backlog", "spike", 2.0, 0.35),
)

INCIDENT_MARKER_TYPES = {
    "inventory_shortage",
    "supplier_delay",
    "warehouse_staffing_shortage",
    "carrier_outage",
    "refund_spike",
    "api_degradation",
    "marketing_campaign_surge",
    "holiday_demand_surge",
    "regional_weather_disruption",
    "fraud_spike",
    "failed_deployment",
    "shipping_disruption",
}


class AnomalyDetectionError(RuntimeError):
    """Raised when anomaly detection cannot complete."""


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s - %(message)s")


def load_kpi_summary(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise AnomalyDetectionError(f"Missing KPI summary file: {path}")
    summary = pd.read_csv(path)
    if "date" not in summary.columns:
        raise AnomalyDetectionError(f"KPI summary missing required date column: {path}")
    summary["date"] = pd.to_datetime(summary["date"], errors="raise").dt.normalize()
    return summary.sort_values("date").reset_index(drop=True)


def score_metric(summary: pd.DataFrame, metric: str, window: int, min_periods: int) -> pd.DataFrame:
    values = summary[metric].astype(float)
    baseline = values.rolling(window=window, min_periods=min_periods).mean().shift(1)
    rolling_std = values.rolling(window=window, min_periods=min_periods).std(ddof=0).shift(1)
    z_score = (values - baseline).divide(rolling_std.where(rolling_std > 0))
    percent_change = values.divide(baseline.where(baseline != 0)) - 1

    return pd.DataFrame(
        {
            "date": summary["date"],
            "metric": metric,
            "value": values,
            "rolling_mean": baseline,
            "rolling_std": rolling_std,
            "z_score": z_score.fillna(0.0),
            "percent_change": percent_change.fillna(0.0),
        }
    )


def rule_mask(scored: pd.DataFrame, rule: AnomalyRule) -> pd.Series:
    if rule.direction == "drop":
        mask = (scored["z_score"] <= -rule.z_threshold) | (scored["percent_change"] <= -rule.pct_change_threshold)
    else:
        mask = (scored["z_score"] >= rule.z_threshold) | (scored["percent_change"] >= rule.pct_change_threshold)

    mask &= scored["rolling_mean"].notna()
    if rule.minimum_value is not None:
        mask |= scored["value"] >= rule.minimum_value
    return mask


def classify_severity(z_score: float, percent_change: float, direction: str) -> str:
    directional_change = abs(percent_change)
    directional_z = abs(z_score)
    if directional_z >= 4.0 or directional_change >= 0.75:
        return "high"
    if directional_z >= 2.5 or directional_change >= 0.35:
        return "medium"
    return "low"


def detect_anomalies(summary: pd.DataFrame, window: int = 14, min_periods: int = 7) -> pd.DataFrame:
    missing_metrics = [rule.metric for rule in ANOMALY_RULES if rule.metric not in summary.columns]
    if missing_metrics:
        raise AnomalyDetectionError(f"KPI summary missing required metrics: {', '.join(missing_metrics)}")

    events: list[dict[str, object]] = []
    if {"dominant_incident_type", "incident_signal"} <= set(summary.columns):
        previous_type = "normal"
        for row in summary.to_dict("records"):
            incident_type = str(row.get("dominant_incident_type") or "normal")
            if incident_type in INCIDENT_MARKER_TYPES and incident_type != previous_type:
                events.append(
                    {
                        "date": row["date"],
                        "anomaly_type": incident_type,
                        "metric": "incident_signal",
                        "value": 1.0,
                        "rolling_mean": 0.0,
                        "rolling_std": 0.0,
                        "z_score": 0.0,
                        "percent_change": 1.0,
                        "severity": "medium",
                        "reason": f"Generated incident marker for {incident_type}.",
                    }
                )
            previous_type = incident_type
    for rule in ANOMALY_RULES:
        scored = score_metric(summary, rule.metric, window=window, min_periods=min_periods)
        anomalies = scored[rule_mask(scored, rule)].copy()

        for row in anomalies.to_dict("records"):
            z_score = float(row["z_score"])
            percent_change = float(row["percent_change"])
            events.append(
                {
                    "date": row["date"],
                    "anomaly_type": rule.anomaly_type,
                    "metric": rule.metric,
                    "value": round(float(row["value"]), 4),
                    "rolling_mean": round(float(row["rolling_mean"]), 4) if pd.notna(row["rolling_mean"]) else 0.0,
                    "rolling_std": round(float(row["rolling_std"]), 4) if pd.notna(row["rolling_std"]) else 0.0,
                    "z_score": round(z_score, 4),
                    "percent_change": round(percent_change, 4),
                    "severity": classify_severity(z_score, percent_change, rule.direction),
                    "reason": build_reason(rule, float(row["value"]), z_score, percent_change),
                }
            )

    anomaly_events = pd.DataFrame.from_records(events)
    if anomaly_events.empty:
        return pd.DataFrame(
            columns=[
                "date",
                "anomaly_type",
                "metric",
                "value",
                "rolling_mean",
                "rolling_std",
                "z_score",
                "percent_change",
                "severity",
                "reason",
            ]
        )
    return anomaly_events.sort_values(["date", "anomaly_type"]).reset_index(drop=True)


def build_reason(rule: AnomalyRule, value: float, z_score: float, percent_change: float) -> str:
    direction = "below" if rule.direction == "drop" else "above"
    return (
        f"{rule.metric} value {value:.4f} is {direction} its rolling baseline "
        f"(z={z_score:.2f}, pct_change={percent_change:.2%})."
    )


def write_anomalies(anomalies: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    export = anomalies.copy()
    if "date" in export.columns:
        export["date"] = pd.to_datetime(export["date"]).dt.strftime("%Y-%m-%d")
    export.to_csv(output_path, index=False)
    LOGGER.info("Wrote %s anomaly events to %s", len(export), output_path)


def plot_anomaly_counts(anomalies: pd.DataFrame, figures_dir: Path) -> Path:
    figures_dir.mkdir(parents=True, exist_ok=True)
    output_path = figures_dir / "anomaly_events_by_type.png"

    figure, axis = plt.subplots(figsize=(10, 4))
    if anomalies.empty:
        axis.text(0.5, 0.5, "No anomalies detected", ha="center", va="center")
        axis.set_axis_off()
    else:
        counts = anomalies["anomaly_type"].value_counts().sort_index()
        axis.bar(counts.index, counts.values)
        axis.set_title("Anomaly Events by Type")
        axis.set_xlabel("Anomaly Type")
        axis.set_ylabel("Event Count")
        axis.tick_params(axis="x", rotation=30)
        axis.grid(True, axis="y", alpha=0.3)
    figure.tight_layout()
    figure.savefig(output_path, dpi=140)
    plt.close(figure)
    LOGGER.info("Wrote anomaly figure to %s", output_path)
    return output_path


def run_anomaly_detection(
    input_path: Path,
    output_path: Path,
    figures_dir: Path,
    window: int = 14,
    min_periods: int = 7,
    create_plots: bool = True,
) -> pd.DataFrame:
    summary = load_kpi_summary(input_path)
    anomalies = detect_anomalies(summary, window=window, min_periods=min_periods)
    write_anomalies(anomalies, output_path)
    if create_plots:
        plot_anomaly_counts(anomalies, figures_dir)
    return anomalies


def parse_args(args: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Detect deterministic anomalies in the daily KPI summary.")
    parser.add_argument(
        "--input-path",
        type=Path,
        default=Path("outputs/reports/kpi_summary_daily.csv"),
        help="Input daily KPI summary CSV path.",
    )
    parser.add_argument(
        "--output-path",
        type=Path,
        default=Path("outputs/reports/anomaly_events.csv"),
        help="Output anomaly events CSV path.",
    )
    parser.add_argument(
        "--figures-dir",
        type=Path,
        default=Path("outputs/figures"),
        help="Directory for anomaly plot PNG files.",
    )
    parser.add_argument("--window", type=int, default=14, help="Rolling baseline window in days.")
    parser.add_argument("--min-periods", type=int, default=7, help="Minimum baseline observations before z-score checks.")
    parser.add_argument("--no-plots", action="store_true", help="Skip writing anomaly plot files.")
    return parser.parse_args(args)


def main(args: Iterable[str] | None = None) -> None:
    configure_logging()
    parsed = parse_args(args)
    run_anomaly_detection(
        input_path=parsed.input_path,
        output_path=parsed.output_path,
        figures_dir=parsed.figures_dir,
        window=parsed.window,
        min_periods=parsed.min_periods,
        create_plots=not parsed.no_plots,
    )


if __name__ == "__main__":
    main()
