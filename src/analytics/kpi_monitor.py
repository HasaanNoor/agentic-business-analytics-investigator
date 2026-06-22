"""Build deterministic daily KPI summaries from synthetic operations data."""

from __future__ import annotations

import argparse
import logging
import os
from pathlib import Path
from typing import Iterable

os.environ.setdefault("MPLCONFIGDIR", str(Path("outputs/.matplotlib")))
os.environ.setdefault("XDG_CACHE_HOME", str(Path("outputs/.cache")))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


LOGGER = logging.getLogger(__name__)


REQUIRED_FILES = {
    "sales": "sales_metrics_daily.csv",
    "latency": "api_latency_hourly.csv",
    "checkout": "checkout_failures_hourly.csv",
    "support": "support_tickets_daily.csv",
    "inventory": "inventory_levels_daily.csv",
    "shipping": "shipping_delays_daily.csv",
    "deployment": "deployment_events.csv",
}


KPI_COLUMNS = [
    "date",
    "net_revenue",
    "website_visitors",
    "active_customers",
    "average_order_value",
    "conversion_rate",
    "refund_rate",
    "day_of_week",
    "month",
    "quarter",
    "is_weekend",
    "avg_api_latency_ms",
    "checkout_failure_rate",
    "support_ticket_count",
    "stockout_units",
    "lost_sales_units",
    "shipping_delay_rate",
    "delivery_complaints",
    "deployment_event_flag",
    "inventory_shortage_flag",
    "shipping_disruption_flag",
]


class KPIMonitorError(RuntimeError):
    """Raised when KPI summary generation cannot complete."""


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s - %(message)s")


def safe_divide(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    result = numerator.divide(denominator.where(denominator != 0))
    return result.fillna(0.0)


def load_synthetic_datasets(data_dir: Path) -> dict[str, pd.DataFrame]:
    datasets: dict[str, pd.DataFrame] = {}
    missing_files: list[str] = []

    for dataset_name, file_name in REQUIRED_FILES.items():
        path = data_dir / file_name
        if not path.exists():
            missing_files.append(str(path))
            continue
        datasets[dataset_name] = pd.read_csv(path)

    if missing_files:
        raise KPIMonitorError(f"Missing required input files: {', '.join(missing_files)}")

    return datasets


def parse_daily_dates(dataframe: pd.DataFrame, column: str = "date") -> pd.DataFrame:
    parsed = dataframe.copy()
    parsed[column] = pd.to_datetime(parsed[column], errors="raise").dt.normalize()
    return parsed


def aggregate_hourly_latency(latency: pd.DataFrame) -> pd.DataFrame:
    parsed = latency.copy()
    parsed["date"] = pd.to_datetime(parsed["timestamp"], errors="raise").dt.normalize()
    parsed["weighted_latency"] = parsed["avg_latency_ms"] * parsed["request_count"]

    daily = parsed.groupby("date", as_index=False).agg(
        request_count=("request_count", "sum"),
        weighted_latency=("weighted_latency", "sum"),
    )
    daily["avg_api_latency_ms"] = safe_divide(daily["weighted_latency"], daily["request_count"]).round(2)
    return daily[["date", "avg_api_latency_ms"]]


def aggregate_hourly_checkout(checkout: pd.DataFrame) -> pd.DataFrame:
    parsed = checkout.copy()
    parsed["date"] = pd.to_datetime(parsed["timestamp"], errors="raise").dt.normalize()

    daily = parsed.groupby("date", as_index=False).agg(
        checkout_attempts=("checkout_attempts", "sum"),
        failed_checkouts=("failed_checkouts", "sum"),
    )
    daily["checkout_failure_rate"] = safe_divide(daily["failed_checkouts"], daily["checkout_attempts"]).round(4)
    return daily[["date", "checkout_failure_rate"]]


def aggregate_inventory(inventory: pd.DataFrame) -> pd.DataFrame:
    parsed = parse_daily_dates(inventory)
    daily = parsed.groupby("date", as_index=False).agg(
        stockout_units=("stockout_units", "sum"),
        inventory_shortage_flag=("incident_flag", "max"),
    )
    daily["inventory_shortage_flag"] = daily["inventory_shortage_flag"].astype(int)
    return daily


def aggregate_shipping(shipping: pd.DataFrame) -> pd.DataFrame:
    parsed = parse_daily_dates(shipping)
    daily = parsed.groupby("date", as_index=False).agg(
        shipments=("shipments", "sum"),
        delayed_shipments=("delayed_shipments", "sum"),
        shipping_disruption_flag=("incident_flag", "max"),
    )
    daily["shipping_delay_rate"] = safe_divide(daily["delayed_shipments"], daily["shipments"]).round(4)
    daily["shipping_disruption_flag"] = daily["shipping_disruption_flag"].astype(int)
    return daily[["date", "shipping_delay_rate", "shipping_disruption_flag"]]


def aggregate_deployment_events(deployment: pd.DataFrame) -> pd.DataFrame:
    parsed = deployment.copy()
    parsed["date"] = pd.to_datetime(parsed["timestamp"], errors="raise").dt.normalize()
    daily = parsed.groupby("date", as_index=False).agg(deployment_event_flag=("incident_flag", "max"))
    daily["deployment_event_flag"] = daily["deployment_event_flag"].astype(int)
    return daily


def build_daily_kpi_summary(datasets: dict[str, pd.DataFrame]) -> pd.DataFrame:
    sales = parse_daily_dates(datasets["sales"])
    support = parse_daily_dates(datasets["support"])

    base = sales[
        [
            "date",
            "net_revenue",
            "website_visitors",
            "active_customers",
            "average_order_value",
            "conversion_rate",
            "day_of_week",
            "month",
            "quarter",
            "is_weekend",
            "orders",
            "lost_sales_units",
        ]
    ].copy()

    support_daily = support[
        [
            "date",
            "total_tickets",
            "refund_requests",
            "delivery_complaints",
        ]
    ].rename(columns={"total_tickets": "support_ticket_count"})

    summary = (
        base.merge(aggregate_hourly_latency(datasets["latency"]), on="date", how="left")
        .merge(aggregate_hourly_checkout(datasets["checkout"]), on="date", how="left")
        .merge(support_daily, on="date", how="left")
        .merge(aggregate_inventory(datasets["inventory"]), on="date", how="left")
        .merge(aggregate_shipping(datasets["shipping"]), on="date", how="left")
        .merge(aggregate_deployment_events(datasets["deployment"]), on="date", how="left")
    )

    summary["refund_rate"] = safe_divide(summary["refund_requests"], summary["orders"]).round(4)
    summary["support_ticket_count"] = summary["support_ticket_count"].fillna(0).astype(int)
    summary["stockout_units"] = summary["stockout_units"].fillna(0).astype(int)
    summary["delivery_complaints"] = summary["delivery_complaints"].fillna(0).astype(int)
    summary["website_visitors"] = summary["website_visitors"].fillna(0).astype(int)
    summary["active_customers"] = summary["active_customers"].fillna(0).astype(int)
    summary["day_of_week"] = summary["day_of_week"].astype(int)
    summary["month"] = summary["month"].astype(int)
    summary["quarter"] = summary["quarter"].astype(int)
    summary["is_weekend"] = summary["is_weekend"].astype(int)
    summary["deployment_event_flag"] = summary["deployment_event_flag"].fillna(0).astype(int)
    summary["inventory_shortage_flag"] = summary["inventory_shortage_flag"].fillna(0).astype(int)
    summary["shipping_disruption_flag"] = summary["shipping_disruption_flag"].fillna(0).astype(int)

    return summary[KPI_COLUMNS].sort_values("date").reset_index(drop=True)


def write_kpi_summary(summary: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    export = summary.copy()
    export["date"] = export["date"].dt.strftime("%Y-%m-%d")
    export.to_csv(output_path, index=False)
    LOGGER.info("Wrote %s daily KPI rows to %s", len(export), output_path)


def plot_kpi_summary(summary: pd.DataFrame, figures_dir: Path) -> list[Path]:
    figures_dir.mkdir(parents=True, exist_ok=True)
    plot_specs = [
        ("net_revenue", "Daily Net Revenue", "kpi_net_revenue.png"),
        ("avg_api_latency_ms", "Average API Latency", "kpi_api_latency.png"),
        ("checkout_failure_rate", "Checkout Failure Rate", "kpi_checkout_failure_rate.png"),
        ("shipping_delay_rate", "Shipping Delay Rate", "kpi_shipping_delay_rate.png"),
    ]

    written_paths: list[Path] = []
    for metric, title, file_name in plot_specs:
        figure, axis = plt.subplots(figsize=(10, 4))
        axis.plot(summary["date"], summary[metric], linewidth=1.8)
        axis.set_title(title)
        axis.set_xlabel("Date")
        axis.set_ylabel(metric)
        axis.grid(True, alpha=0.3)
        figure.autofmt_xdate()
        figure.tight_layout()
        output_path = figures_dir / file_name
        figure.savefig(output_path, dpi=140)
        plt.close(figure)
        written_paths.append(output_path)

    LOGGER.info("Wrote %s KPI figure files to %s", len(written_paths), figures_dir)
    return written_paths


def run_kpi_monitor(data_dir: Path, output_path: Path, figures_dir: Path, create_plots: bool = True) -> pd.DataFrame:
    datasets = load_synthetic_datasets(data_dir)
    summary = build_daily_kpi_summary(datasets)
    write_kpi_summary(summary, output_path)
    if create_plots:
        plot_kpi_summary(summary, figures_dir)
    return summary


def parse_args(args: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build daily KPI summaries from synthetic CSV data.")
    parser.add_argument("--data-dir", type=Path, default=Path("data/synthetic"), help="Directory containing synthetic CSV files.")
    parser.add_argument(
        "--output-path",
        type=Path,
        default=Path("outputs/reports/kpi_summary_daily.csv"),
        help="CSV path for the daily KPI summary.",
    )
    parser.add_argument(
        "--figures-dir",
        type=Path,
        default=Path("outputs/figures"),
        help="Directory for KPI plot PNG files.",
    )
    parser.add_argument("--no-plots", action="store_true", help="Skip writing KPI plot files.")
    return parser.parse_args(args)


def main(args: Iterable[str] | None = None) -> None:
    configure_logging()
    parsed = parse_args(args)
    run_kpi_monitor(
        data_dir=parsed.data_dir,
        output_path=parsed.output_path,
        figures_dir=parsed.figures_dir,
        create_plots=not parsed.no_plots,
    )


if __name__ == "__main__":
    main()
