"""Generate synthetic Northstar Commerce operational datasets.

The generator is deterministic for a given seed and intentionally injects
cross-domain incidents so downstream anomaly detection and investigation
workflows have known ground truth.
"""

from __future__ import annotations

import argparse
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable

import numpy as np
import pandas as pd


LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class IncidentWindows:
    failed_deployment_start: pd.Timestamp = pd.Timestamp("2025-03-18 09:00")
    failed_deployment_end: pd.Timestamp = pd.Timestamp("2025-03-20 23:00")
    inventory_shortage_start: pd.Timestamp = pd.Timestamp("2025-04-10")
    inventory_shortage_end: pd.Timestamp = pd.Timestamp("2025-04-20")
    shipping_disruption_start: pd.Timestamp = pd.Timestamp("2025-05-05")
    shipping_disruption_end: pd.Timestamp = pd.Timestamp("2025-05-14")


SKUS = (
    "NSC-CORE-TEE",
    "NSC-TRAVEL-MUG",
    "NSC-WIRELESS-CHARGER",
    "NSC-DESK-LAMP",
    "NSC-CARRY-ALL",
)

REGIONS = ("Northeast", "Southeast", "Midwest", "West")
CARRIERS = ("ShipFast", "ParcelPro", "Northline")


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )


def daily_dates(start_date: str, end_date: str) -> pd.DatetimeIndex:
    return pd.date_range(start=start_date, end=end_date, freq="D")


def hourly_dates(start_date: str, end_date: str) -> pd.DatetimeIndex:
    start = pd.Timestamp(start_date)
    end = pd.Timestamp(end_date) + pd.Timedelta(days=1) - pd.Timedelta(hours=1)
    return pd.date_range(start=start, end=end, freq="h")


def in_window(values: pd.Series | pd.DatetimeIndex, start: pd.Timestamp, end: pd.Timestamp) -> np.ndarray:
    return (values >= start) & (values <= end)


def date_features(dates: pd.DatetimeIndex) -> pd.DataFrame:
    day_of_week = dates.dayofweek.to_numpy()
    day_index = np.arange(len(dates))
    weekend = day_of_week >= 5
    weekly_seasonality = 1.0 + 0.12 * np.sin(2 * np.pi * day_index / 7)
    trend = 1.0 + 0.0015 * day_index

    return pd.DataFrame(
        {
            "date": dates.date,
            "day_of_week": day_of_week,
            "is_weekend": weekend,
            "weekly_seasonality": weekly_seasonality,
            "trend": trend,
        }
    )


def generate_sales_metrics(
    dates: pd.DatetimeIndex,
    rng: np.random.Generator,
    incidents: IncidentWindows,
) -> pd.DataFrame:
    features = date_features(dates)
    deployment_days = in_window(dates, incidents.failed_deployment_start.normalize(), incidents.failed_deployment_end.normalize())
    shortage_days = in_window(dates, incidents.inventory_shortage_start, incidents.inventory_shortage_end)

    expected_sessions = 10_500 * features["trend"] * features["weekly_seasonality"]
    expected_sessions *= np.where(features["is_weekend"], 1.18, 1.0)
    sessions = rng.poisson(expected_sessions).astype(int)

    conversion_rate = rng.normal(0.043, 0.003, len(dates))
    conversion_rate -= np.where(deployment_days, 0.012, 0.0)
    conversion_rate -= np.where(shortage_days, 0.006, 0.0)
    conversion_rate = np.clip(conversion_rate, 0.015, 0.07)

    orders = rng.poisson(sessions * conversion_rate).astype(int)
    average_order_value = rng.normal(86.0, 5.5, len(dates))
    average_order_value -= np.where(deployment_days, 7.0, 0.0)
    average_order_value = np.clip(average_order_value, 45.0, None)

    units_per_order = rng.normal(1.75, 0.12, len(dates))
    units_sold = np.maximum(np.round(orders * units_per_order), 0).astype(int)
    lost_sales_units = np.where(shortage_days, rng.integers(70, 150, len(dates)), 0)
    gross_revenue = orders * average_order_value
    net_revenue = gross_revenue * rng.normal(0.972, 0.006, len(dates))

    incident_type = np.full(len(dates), "normal", dtype=object)
    incident_type[deployment_days] = "failed_deployment"
    incident_type[shortage_days] = "inventory_shortage"

    return pd.DataFrame(
        {
            "date": dates.date,
            "sessions": sessions,
            "orders": orders,
            "units_sold": units_sold,
            "gross_revenue": np.round(gross_revenue, 2),
            "net_revenue": np.round(net_revenue, 2),
            "conversion_rate": np.round(conversion_rate, 4),
            "average_order_value": np.round(average_order_value, 2),
            "lost_sales_units": lost_sales_units,
            "incident_flag": incident_type != "normal",
            "incident_type": incident_type,
        }
    )


def generate_api_latency(
    hours: pd.DatetimeIndex,
    rng: np.random.Generator,
    incidents: IncidentWindows,
) -> pd.DataFrame:
    hour = hours.hour.to_numpy()
    business_hours = (hour >= 9) & (hour <= 22)
    deployment_hours = in_window(hours, incidents.failed_deployment_start, incidents.failed_deployment_end)

    base_latency = rng.normal(185, 18, len(hours)) + np.where(business_hours, 32, 0)
    base_latency += 18 * np.sin(2 * np.pi * hour / 24)
    p95_latency = base_latency + rng.normal(95, 16, len(hours))
    p99_latency = p95_latency + rng.normal(130, 30, len(hours))

    p95_latency += np.where(deployment_hours, rng.normal(520, 90, len(hours)), 0)
    p99_latency += np.where(deployment_hours, rng.normal(1_150, 180, len(hours)), 0)
    error_rate = rng.beta(1.4, 180, len(hours))
    error_rate += np.where(deployment_hours, rng.uniform(0.025, 0.065, len(hours)), 0)

    return pd.DataFrame(
        {
            "timestamp": hours,
            "service": "checkout-api",
            "request_count": rng.poisson(np.where(business_hours, 8_000, 2_500)).astype(int),
            "avg_latency_ms": np.round(np.clip(base_latency + np.where(deployment_hours, 360, 0), 80, None), 1),
            "p95_latency_ms": np.round(np.clip(p95_latency, 120, None), 1),
            "p99_latency_ms": np.round(np.clip(p99_latency, 160, None), 1),
            "error_rate": np.round(np.clip(error_rate, 0, 0.25), 4),
            "incident_flag": deployment_hours,
            "incident_type": np.where(deployment_hours, "failed_deployment", "normal"),
        }
    )


def generate_checkout_failures(
    hours: pd.DatetimeIndex,
    rng: np.random.Generator,
    incidents: IncidentWindows,
) -> pd.DataFrame:
    hour = hours.hour.to_numpy()
    business_hours = (hour >= 8) & (hour <= 23)
    deployment_hours = in_window(hours, incidents.failed_deployment_start, incidents.failed_deployment_end)

    checkout_attempts = rng.poisson(np.where(business_hours, 1_850, 620)).astype(int)
    failure_rate = rng.normal(0.018, 0.004, len(hours))
    failure_rate += np.where(deployment_hours, rng.uniform(0.075, 0.13, len(hours)), 0)
    failure_rate = np.clip(failure_rate, 0.002, 0.24)
    failed_checkouts = rng.binomial(checkout_attempts, failure_rate)

    payment_gateway_errors = np.round(failed_checkouts * rng.uniform(0.18, 0.32, len(hours))).astype(int)
    api_timeout_errors = np.round(failed_checkouts * np.where(deployment_hours, rng.uniform(0.45, 0.62, len(hours)), rng.uniform(0.08, 0.16, len(hours)))).astype(int)

    return pd.DataFrame(
        {
            "timestamp": hours,
            "checkout_attempts": checkout_attempts,
            "failed_checkouts": failed_checkouts,
            "failure_rate": np.round(failure_rate, 4),
            "payment_gateway_errors": payment_gateway_errors,
            "api_timeout_errors": api_timeout_errors,
            "incident_flag": deployment_hours,
            "incident_type": np.where(deployment_hours, "failed_deployment", "normal"),
        }
    )


def generate_support_tickets(
    dates: pd.DatetimeIndex,
    rng: np.random.Generator,
    incidents: IncidentWindows,
) -> pd.DataFrame:
    deployment_days = in_window(dates, incidents.failed_deployment_start.normalize(), incidents.failed_deployment_end.normalize())
    disruption_days = in_window(dates, incidents.shipping_disruption_start, incidents.shipping_disruption_end)

    base = rng.poisson(135, len(dates)).astype(int)
    checkout_complaints = rng.poisson(np.where(deployment_days, 95, 16)).astype(int)
    delivery_complaints = rng.poisson(np.where(disruption_days, 120, 24)).astype(int)
    inventory_complaints = rng.poisson(18, len(dates)).astype(int)
    refund_requests = rng.poisson(22 + np.where(deployment_days | disruption_days, 25, 0)).astype(int)
    total = base + checkout_complaints + delivery_complaints + inventory_complaints + refund_requests

    incident_type = np.full(len(dates), "normal", dtype=object)
    incident_type[deployment_days] = "failed_deployment"
    incident_type[disruption_days] = "shipping_disruption"

    return pd.DataFrame(
        {
            "date": dates.date,
            "total_tickets": total,
            "checkout_complaints": checkout_complaints,
            "delivery_complaints": delivery_complaints,
            "inventory_complaints": inventory_complaints,
            "refund_requests": refund_requests,
            "avg_first_response_minutes": np.round(rng.normal(42, 8, len(dates)) + np.where(deployment_days | disruption_days, 16, 0), 1),
            "incident_flag": incident_type != "normal",
            "incident_type": incident_type,
        }
    )


def generate_inventory_levels(
    dates: pd.DatetimeIndex,
    rng: np.random.Generator,
    incidents: IncidentWindows,
) -> pd.DataFrame:
    records = []
    shortage_days = in_window(dates, incidents.inventory_shortage_start, incidents.inventory_shortage_end)

    for sku_index, sku in enumerate(SKUS):
        starting_inventory = 1_150 + 175 * sku_index + rng.integers(-80, 90)
        daily_demand = 43 + 9 * sku_index
        on_hand = starting_inventory

        for date_index, date in enumerate(dates):
            is_shortage_sku = sku == "NSC-TRAVEL-MUG"
            is_shortage_day = bool(shortage_days[date_index] and is_shortage_sku)
            demand = max(0, int(rng.normal(daily_demand, 8)))
            received_units = 0

            if date_index % 21 == 0 and not is_shortage_day:
                received_units = int(rng.normal(760, 55))
            if is_shortage_day:
                received_units = 0
                demand += int(rng.normal(38, 8))

            on_hand = max(0, on_hand + received_units - demand)
            if is_shortage_day:
                on_hand = min(on_hand, rng.integers(0, 35))

            stockout_units = max(0, demand - on_hand) if is_shortage_day else 0
            records.append(
                {
                    "date": date.date(),
                    "sku": sku,
                    "warehouse": "WH-Northstar-01",
                    "on_hand_units": int(on_hand),
                    "units_demanded": demand,
                    "units_received": received_units,
                    "stockout_units": int(stockout_units),
                    "reorder_point": 220,
                    "incident_flag": is_shortage_day,
                    "incident_type": "inventory_shortage" if is_shortage_day else "normal",
                }
            )

    return pd.DataFrame.from_records(records)


def generate_shipping_delays(
    dates: pd.DatetimeIndex,
    rng: np.random.Generator,
    incidents: IncidentWindows,
) -> pd.DataFrame:
    records = []
    disruption_days = in_window(dates, incidents.shipping_disruption_start, incidents.shipping_disruption_end)

    for date_index, date in enumerate(dates):
        for region in REGIONS:
            for carrier in CARRIERS:
                affected = bool(disruption_days[date_index] and region in {"Northeast", "Midwest"} and carrier != "Northline")
                shipments = int(rng.poisson(420 if region != "West" else 360))
                delay_rate = rng.normal(0.055, 0.012)
                delay_rate += 0.18 if affected else 0.0
                delay_rate = float(np.clip(delay_rate, 0.01, 0.45))
                delayed_shipments = int(rng.binomial(shipments, delay_rate))
                avg_delay_hours = rng.normal(7.5, 1.6) + (22 if affected else 0)

                records.append(
                    {
                        "date": date.date(),
                        "region": region,
                        "carrier": carrier,
                        "shipments": shipments,
                        "delayed_shipments": delayed_shipments,
                        "delay_rate": round(delay_rate, 4),
                        "avg_delay_hours": round(max(avg_delay_hours, 0.5), 1),
                        "incident_flag": affected,
                        "incident_type": "shipping_disruption" if affected else "normal",
                    }
                )

    return pd.DataFrame.from_records(records)


def generate_deployment_events(incidents: IncidentWindows) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "timestamp": pd.Timestamp("2025-02-06 10:00"),
                "service": "catalog-api",
                "version": "2025.02.06.1",
                "environment": "production",
                "status": "success",
                "change_type": "feature_release",
                "incident_flag": False,
                "incident_type": "normal",
            },
            {
                "timestamp": incidents.failed_deployment_start,
                "service": "checkout-api",
                "version": "2025.03.18.1",
                "environment": "production",
                "status": "failed",
                "change_type": "dependency_upgrade",
                "incident_flag": True,
                "incident_type": "failed_deployment",
            },
            {
                "timestamp": pd.Timestamp("2025-03-20 23:30"),
                "service": "checkout-api",
                "version": "2025.03.20.2",
                "environment": "production",
                "status": "rollback_success",
                "change_type": "rollback",
                "incident_flag": True,
                "incident_type": "failed_deployment",
            },
            {
                "timestamp": pd.Timestamp("2025-04-29 11:00"),
                "service": "recommendations-api",
                "version": "2025.04.29.1",
                "environment": "production",
                "status": "success",
                "change_type": "model_refresh",
                "incident_flag": False,
                "incident_type": "normal",
            },
        ]
    )


def generate_all_datasets(
    start_date: str = "2025-01-01",
    end_date: str = "2025-06-30",
    seed: int = 42,
) -> Dict[str, pd.DataFrame]:
    rng = np.random.default_rng(seed)
    incidents = IncidentWindows()
    days = daily_dates(start_date, end_date)
    hours = hourly_dates(start_date, end_date)

    LOGGER.info("Generating Northstar Commerce synthetic data from %s to %s with seed=%s", start_date, end_date, seed)
    return {
        "sales_metrics_daily": generate_sales_metrics(days, rng, incidents),
        "api_latency_hourly": generate_api_latency(hours, rng, incidents),
        "checkout_failures_hourly": generate_checkout_failures(hours, rng, incidents),
        "support_tickets_daily": generate_support_tickets(days, rng, incidents),
        "inventory_levels_daily": generate_inventory_levels(days, rng, incidents),
        "shipping_delays_daily": generate_shipping_delays(days, rng, incidents),
        "deployment_events": generate_deployment_events(incidents),
    }


def write_datasets(datasets: Dict[str, pd.DataFrame], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, dataframe in datasets.items():
        output_path = output_dir / f"{name}.csv"
        dataframe.to_csv(output_path, index=False)
        LOGGER.info("Wrote %s rows to %s", len(dataframe), output_path)


def parse_args(args: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate synthetic Northstar Commerce operational datasets.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducible output.")
    parser.add_argument("--start-date", default="2025-01-01", help="Inclusive start date in YYYY-MM-DD format.")
    parser.add_argument("--end-date", default="2025-06-30", help="Inclusive end date in YYYY-MM-DD format.")
    parser.add_argument("--output-dir", type=Path, default=Path("data/synthetic"), help="Directory for generated CSV files.")
    return parser.parse_args(args)


def main(args: Iterable[str] | None = None) -> None:
    configure_logging()
    parsed = parse_args(args)
    datasets = generate_all_datasets(
        start_date=parsed.start_date,
        end_date=parsed.end_date,
        seed=parsed.seed,
    )
    write_datasets(datasets, parsed.output_dir)


if __name__ == "__main__":
    main()
