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
class DeploymentIncident:
    start: pd.Timestamp
    end: pd.Timestamp
    severity: float
    service: str
    version: str
    change_type: str


@dataclass(frozen=True)
class InventoryIncident:
    start: pd.Timestamp
    end: pd.Timestamp
    severity: float
    sku: str


@dataclass(frozen=True)
class ShippingIncident:
    start: pd.Timestamp
    end: pd.Timestamp
    severity: float
    affected_regions: tuple[str, ...]
    affected_carriers: tuple[str, ...]


@dataclass(frozen=True)
class BusinessIncident:
    start: pd.Timestamp
    end: pd.Timestamp
    incident_type: str
    severity: float
    affected_region: str
    root_cause_category: str
    business_impact_summary: str
    resolution_action: str
    resolution_success: bool
    recovery_days: int
    affected_metrics: tuple[str, ...]


@dataclass(frozen=True)
class IncidentCatalog:
    deployments: tuple[DeploymentIncident, ...]
    inventory_shortages: tuple[InventoryIncident, ...]
    shipping_disruptions: tuple[ShippingIncident, ...]
    business_incidents: tuple[BusinessIncident, ...] = ()


SKUS = (
    "NSC-CORE-TEE",
    "NSC-TRAVEL-MUG",
    "NSC-WIRELESS-CHARGER",
    "NSC-DESK-LAMP",
    "NSC-CARRY-ALL",
)

REGIONS = ("Northeast", "Southeast", "Midwest", "West")
REGION_DISRUPTION_COLUMNS = {
    "Northeast": "east_region_disruption",
    "West": "west_region_disruption",
    "Southeast": "south_region_disruption",
    "Midwest": "central_region_disruption",
}
CARRIERS = ("ShipFast", "ParcelPro", "Northline")


INCIDENT_TYPE_DEFINITIONS = {
    "inventory_shortage": {
        "root_cause_category": "inventory planning",
        "business_impact_summary": "Stockouts increased, revenue softened, and customers contacted support about unavailable products.",
        "resolution_action": "Transferred inventory from another warehouse and raised the next purchase order.",
        "affected_metrics": ("stockout_units", "lost_sales_units", "net_revenue", "inventory_complaints"),
        "recovery_days": 3,
    },
    "supplier_delay": {
        "root_cause_category": "supplier operations",
        "business_impact_summary": "Inbound replenishment arrived late, increasing stockouts and lost sales.",
        "resolution_action": "Expedited inbound freight and split the delayed order across two receiving docks.",
        "affected_metrics": ("stockout_units", "lost_sales_units", "net_revenue", "support_ticket_count"),
        "recovery_days": 5,
    },
    "warehouse_staffing_shortage": {
        "root_cause_category": "warehouse labor",
        "business_impact_summary": "Warehouse backlog increased, shipments slowed, and delivery complaints rose.",
        "resolution_action": "Added temporary warehouse shifts and prioritized aged outbound orders.",
        "affected_metrics": ("warehouse_backlog", "shipping_delay_rate", "delivery_complaints", "support_ticket_count"),
        "recovery_days": 4,
    },
    "carrier_outage": {
        "root_cause_category": "carrier reliability",
        "business_impact_summary": "Carrier capacity dropped, shipping delays increased, and customers reported late deliveries.",
        "resolution_action": "Rerouted affected shipments to backup carriers and upgraded service for priority orders.",
        "affected_metrics": ("shipping_delay_rate", "carrier_capacity_utilization", "delivery_complaints"),
        "recovery_days": 3,
    },
    "refund_spike": {
        "root_cause_category": "returns and billing",
        "business_impact_summary": "Refund requests rose and net revenue was reduced by higher returns.",
        "resolution_action": "Audited refund reasons, fixed the billing rule, and contacted affected customers.",
        "affected_metrics": ("refund_rate", "refund_requests", "net_revenue", "billing_issue_tickets"),
        "recovery_days": 2,
    },
    "api_degradation": {
        "root_cause_category": "platform reliability",
        "business_impact_summary": "API latency rose, checkout failures increased, and conversion rate declined.",
        "resolution_action": "Rolled back the slow dependency and added latency alerts for the checkout path.",
        "affected_metrics": ("avg_api_latency_ms", "checkout_failure_rate", "conversion_rate", "net_revenue"),
        "recovery_days": 2,
    },
    "marketing_campaign_surge": {
        "root_cause_category": "demand generation",
        "business_impact_summary": "Visitors increased quickly, conversions improved slightly, and support volume rose.",
        "resolution_action": "Kept the campaign active while adding support coverage and checkout monitoring.",
        "affected_metrics": ("website_visitors", "conversion_rate", "support_ticket_count", "net_revenue"),
        "recovery_days": 1,
    },
    "holiday_demand_surge": {
        "root_cause_category": "seasonal demand",
        "business_impact_summary": "Demand exceeded normal seasonal levels, increasing orders, backlog, and support load.",
        "resolution_action": "Opened holiday fulfillment lanes and moved high-demand SKUs closer to customers.",
        "affected_metrics": ("website_visitors", "orders", "warehouse_backlog", "support_ticket_count"),
        "recovery_days": 4,
    },
    "regional_weather_disruption": {
        "root_cause_category": "weather",
        "business_impact_summary": "A regional weather event slowed deliveries and increased logistics complaints.",
        "resolution_action": "Paused promises in the affected region and rerouted shipments through nearby hubs.",
        "affected_metrics": ("shipping_delay_rate", "delivery_complaints", "warehouse_backlog"),
        "recovery_days": 3,
    },
    "fraud_spike": {
        "root_cause_category": "fraud controls",
        "business_impact_summary": "Fraud reviews and refund requests increased, reducing completed revenue.",
        "resolution_action": "Tightened fraud rules, manually reviewed held orders, and refunded confirmed fraud cases.",
        "affected_metrics": ("refund_rate", "checkout_failure_rate", "support_ticket_count", "net_revenue"),
        "recovery_days": 3,
    },
}


def generate_business_incidents(start_date: str, end_date: str) -> tuple[BusinessIncident, ...]:
    """Create deterministic business incidents spaced far enough apart for investigation grouping."""
    starts = pd.date_range(pd.Timestamp(start_date) + pd.Timedelta(days=12), pd.Timestamp(end_date) - pd.Timedelta(days=2), freq="5D")
    incident_types = tuple(INCIDENT_TYPE_DEFINITIONS)
    records: list[BusinessIncident] = []
    for index, start in enumerate(starts):
        incident_type = incident_types[index % len(incident_types)]
        definition = INCIDENT_TYPE_DEFINITIONS[incident_type]
        duration_days = 1 + (index % 2)
        severity = 0.75 + 0.15 * (index % 5)
        region = REGIONS[index % len(REGIONS)]
        records.append(
            BusinessIncident(
                start=start.normalize(),
                end=(start + pd.Timedelta(days=duration_days)).normalize(),
                incident_type=incident_type,
                severity=round(severity, 2),
                affected_region=region,
                root_cause_category=str(definition["root_cause_category"]),
                business_impact_summary=str(definition["business_impact_summary"]),
                resolution_action=str(definition["resolution_action"]),
                resolution_success=(index % 11 != 0),
                recovery_days=int(definition["recovery_days"]) + (index % 2),
                affected_metrics=tuple(definition["affected_metrics"]),
            )
        )
    return tuple(records)


PHASE_6_INCIDENTS = IncidentCatalog(
    deployments=(
        DeploymentIncident(
            start=pd.Timestamp("2025-03-18 09:00"),
            end=pd.Timestamp("2025-03-20 23:00"),
            severity=1.00,
            service="checkout-api",
            version="2025.03.18.1",
            change_type="dependency_upgrade",
        ),
        DeploymentIncident(
            start=pd.Timestamp("2025-07-22 14:00"),
            end=pd.Timestamp("2025-07-23 08:00"),
            severity=0.55,
            service="checkout-api",
            version="2025.07.22.1",
            change_type="payment_retry_refactor",
        ),
        DeploymentIncident(
            start=pd.Timestamp("2025-10-08 11:00"),
            end=pd.Timestamp("2025-10-11 02:00"),
            severity=1.25,
            service="checkout-api",
            version="2025.10.08.2",
            change_type="pricing_dependency_upgrade",
        ),
        DeploymentIncident(
            start=pd.Timestamp("2026-01-27 10:00"),
            end=pd.Timestamp("2026-01-28 18:00"),
            severity=0.70,
            service="checkout-api",
            version="2026.01.27.1",
            change_type="feature_release",
        ),
        DeploymentIncident(
            start=pd.Timestamp("2026-04-14 08:00"),
            end=pd.Timestamp("2026-04-18 22:00"),
            severity=1.45,
            service="checkout-api",
            version="2026.04.14.1",
            change_type="database_driver_upgrade",
        ),
        DeploymentIncident(
            start=pd.Timestamp("2026-08-03 13:00"),
            end=pd.Timestamp("2026-08-04 23:00"),
            severity=0.85,
            service="checkout-api",
            version="2026.08.03.1",
            change_type="fraud_screening_release",
        ),
        DeploymentIncident(
            start=pd.Timestamp("2026-11-16 09:00"),
            end=pd.Timestamp("2026-11-19 15:00"),
            severity=1.15,
            service="checkout-api",
            version="2026.11.16.1",
            change_type="tax_service_migration",
        ),
    ),
    inventory_shortages=(
        InventoryIncident(
            start=pd.Timestamp("2025-04-10"),
            end=pd.Timestamp("2025-04-20"),
            severity=1.00,
            sku="NSC-TRAVEL-MUG",
        ),
        InventoryIncident(
            start=pd.Timestamp("2025-08-12"),
            end=pd.Timestamp("2025-08-18"),
            severity=0.65,
            sku="NSC-CORE-TEE",
        ),
        InventoryIncident(
            start=pd.Timestamp("2025-12-03"),
            end=pd.Timestamp("2025-12-16"),
            severity=1.35,
            sku="NSC-WIRELESS-CHARGER",
        ),
        InventoryIncident(
            start=pd.Timestamp("2026-05-20"),
            end=pd.Timestamp("2026-05-30"),
            severity=0.90,
            sku="NSC-DESK-LAMP",
        ),
        InventoryIncident(
            start=pd.Timestamp("2026-09-09"),
            end=pd.Timestamp("2026-09-23"),
            severity=1.20,
            sku="NSC-CARRY-ALL",
        ),
    ),
    shipping_disruptions=(
        ShippingIncident(
            start=pd.Timestamp("2025-05-05"),
            end=pd.Timestamp("2025-05-14"),
            severity=1.00,
            affected_regions=("Northeast", "Midwest"),
            affected_carriers=("ShipFast", "ParcelPro"),
        ),
        ShippingIncident(
            start=pd.Timestamp("2025-09-15"),
            end=pd.Timestamp("2025-09-19"),
            severity=0.60,
            affected_regions=("West",),
            affected_carriers=("ParcelPro",),
        ),
        ShippingIncident(
            start=pd.Timestamp("2026-02-09"),
            end=pd.Timestamp("2026-02-19"),
            severity=1.30,
            affected_regions=("Southeast", "Midwest"),
            affected_carriers=("ShipFast",),
        ),
        ShippingIncident(
            start=pd.Timestamp("2026-06-22"),
            end=pd.Timestamp("2026-06-28"),
            severity=0.80,
            affected_regions=("Northeast", "West"),
            affected_carriers=("ParcelPro", "Northline"),
        ),
        ShippingIncident(
            start=pd.Timestamp("2026-10-05"),
            end=pd.Timestamp("2026-10-17"),
            severity=1.15,
            affected_regions=("Northeast", "Southeast", "West"),
            affected_carriers=("ShipFast", "ParcelPro"),
        ),
    ),
)


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


def deployment_severity(values: pd.DatetimeIndex, incidents: IncidentCatalog, normalize: bool = False) -> np.ndarray:
    effect = np.zeros(len(values), dtype=float)
    for incident in incidents.deployments:
        start = incident.start.normalize() if normalize else incident.start
        end = incident.end.normalize() if normalize else incident.end
        effect += np.where(in_window(values, start, end), incident.severity, 0.0)
    return effect


def inventory_severity(values: pd.DatetimeIndex, incidents: IncidentCatalog) -> np.ndarray:
    effect = np.zeros(len(values), dtype=float)
    for incident in incidents.inventory_shortages:
        effect += np.where(in_window(values, incident.start, incident.end), incident.severity, 0.0)
    return effect


def shipping_severity(values: pd.DatetimeIndex, incidents: IncidentCatalog) -> np.ndarray:
    effect = np.zeros(len(values), dtype=float)
    for incident in incidents.shipping_disruptions:
        effect += np.where(in_window(values, incident.start, incident.end), incident.severity, 0.0)
    return effect


def business_effect_by_type(values: pd.DatetimeIndex, incidents: IncidentCatalog, incident_type: str) -> np.ndarray:
    effect = np.zeros(len(values), dtype=float)
    normalized_values = values.normalize() if hasattr(values, "normalize") else values
    for incident in incidents.business_incidents:
        if incident.incident_type != incident_type:
            continue
        effect += np.where(in_window(normalized_values, incident.start, incident.end), incident.severity, 0.0)
    return effect


def business_effect(values: pd.DatetimeIndex, incidents: IncidentCatalog, incident_types: Iterable[str]) -> np.ndarray:
    effect = np.zeros(len(values), dtype=float)
    for incident_type in incident_types:
        effect += business_effect_by_type(values, incidents, incident_type)
    return effect


def business_incident_type_for_days(dates: pd.DatetimeIndex, incidents: IncidentCatalog) -> np.ndarray:
    incident_type = np.full(len(dates), "normal", dtype=object)
    for incident in incidents.business_incidents:
        mask = in_window(dates, incident.start, incident.end)
        incident_type[mask] = incident.incident_type
    return incident_type


def first_active_business_incident(date: pd.Timestamp, incidents: IncidentCatalog) -> BusinessIncident | None:
    for incident in incidents.business_incidents:
        if incident.start <= date.normalize() <= incident.end:
            return incident
    return None


def incident_type_for_days(
    dates: pd.DatetimeIndex,
    incidents: IncidentCatalog,
    deployment_effect: np.ndarray | None = None,
    inventory_effect: np.ndarray | None = None,
    shipping_effect: np.ndarray | None = None,
) -> np.ndarray:
    incident_type = np.full(len(dates), "normal", dtype=object)
    business_types = business_incident_type_for_days(dates, incidents)
    incident_type[business_types != "normal"] = business_types[business_types != "normal"]
    if shipping_effect is not None:
        incident_type[(shipping_effect > 0) & (incident_type == "normal")] = "shipping_disruption"
    if inventory_effect is not None:
        incident_type[(inventory_effect > 0) & (incident_type == "normal")] = "inventory_shortage"
    if deployment_effect is not None:
        incident_type[deployment_effect > 0] = "failed_deployment"
    return incident_type


def date_features(dates: pd.DatetimeIndex) -> pd.DataFrame:
    day_of_week = dates.dayofweek.to_numpy()
    day_index = np.arange(len(dates))
    weekend = day_of_week >= 5
    weekly_seasonality = 1.0 + 0.12 * np.sin(2 * np.pi * day_index / 7)
    monthly_seasonality = 1.0 + 0.08 * np.sin(2 * np.pi * (dates.month.to_numpy() - 1) / 12)
    trend = 1.0 + 0.0015 * day_index

    return pd.DataFrame(
        {
            "date": dates.date,
            "day_of_week": day_of_week,
            "month": dates.month.to_numpy(),
            "quarter": dates.quarter.to_numpy(),
            "is_weekend": weekend,
            "weekly_seasonality": weekly_seasonality,
            "monthly_seasonality": monthly_seasonality,
            "trend": trend,
        }
    )


def generate_sales_metrics(
    dates: pd.DatetimeIndex,
    rng: np.random.Generator,
    incidents: IncidentCatalog,
) -> pd.DataFrame:
    features = date_features(dates)
    deployment_effect = deployment_severity(dates, incidents, normalize=True)
    inventory_effect = inventory_severity(dates, incidents) + business_effect(
        dates, incidents, ("inventory_shortage", "supplier_delay")
    )
    shipping_effect = shipping_severity(dates, incidents) + business_effect(
        dates, incidents, ("warehouse_staffing_shortage", "carrier_outage", "regional_weather_disruption")
    )
    api_effect = business_effect(dates, incidents, ("api_degradation",))
    refund_effect = business_effect(dates, incidents, ("refund_spike", "fraud_spike"))
    demand_surge_effect = business_effect(dates, incidents, ("marketing_campaign_surge", "holiday_demand_surge"))
    fraud_effect = business_effect(dates, incidents, ("fraud_spike",))
    operational_incident_effect = deployment_effect + inventory_effect + 0.35 * shipping_effect

    expected_visitors = 11_200 * features["trend"] * features["weekly_seasonality"] * features["monthly_seasonality"]
    expected_visitors *= np.where(features["is_weekend"], 1.18, 1.0)
    expected_visitors *= np.where(features["month"].isin([11, 12]), 1.16, 1.0)
    expected_visitors *= 1.0 + 0.23 * demand_surge_effect
    expected_visitors *= np.clip(1.0 - 0.025 * operational_incident_effect, 0.88, None)
    website_visitors = rng.poisson(expected_visitors).astype(int)

    conversion_rate = rng.normal(0.043, 0.003, len(dates))
    conversion_rate += 0.004 * business_effect(dates, incidents, ("marketing_campaign_surge",))
    conversion_rate -= 0.012 * (deployment_effect + api_effect)
    conversion_rate -= 0.006 * inventory_effect
    conversion_rate -= 0.004 * shipping_effect
    conversion_rate -= 0.003 * fraud_effect
    conversion_rate = np.clip(conversion_rate, 0.015, 0.07)

    checkout_failure_rate = rng.normal(0.018, 0.003, len(dates))
    checkout_failure_rate += 0.085 * deployment_effect
    checkout_failure_rate += 0.050 * api_effect
    checkout_failure_rate += 0.026 * fraud_effect
    checkout_failure_rate = np.clip(checkout_failure_rate, 0.003, 0.24)

    active_customers = rng.poisson(website_visitors * rng.normal(0.62, 0.025, len(dates))).astype(int)
    orders = rng.poisson(website_visitors * conversion_rate * (1.0 - checkout_failure_rate)).astype(int)
    average_order_value = rng.normal(86.0, 5.5, len(dates))
    average_order_value -= 7.0 * deployment_effect
    average_order_value += np.where(features["month"].isin([11, 12]), 6.0, 0.0)
    average_order_value += np.where(features["quarter"] == 1, 2.0, 0.0)
    average_order_value = np.clip(average_order_value, 45.0, None)

    units_per_order = rng.normal(1.75, 0.12, len(dates))
    units_sold = np.maximum(np.round(orders * units_per_order), 0).astype(int)
    lost_sales_units = np.where(
        inventory_effect > 0,
        np.round(rng.integers(70, 150, len(dates)) * inventory_effect),
        0,
    ).astype(int)
    refund_rate = rng.normal(0.035, 0.004, len(dates))
    refund_rate += 0.014 * deployment_effect
    refund_rate += 0.010 * shipping_effect
    refund_rate += 0.006 * inventory_effect
    refund_rate += 0.030 * refund_effect
    refund_rate = np.clip(refund_rate, 0.01, 0.12)

    gross_revenue = orders * average_order_value
    lost_sales_penalty = lost_sales_units * average_order_value * rng.normal(0.42, 0.035, len(dates))
    stockout_penalty = inventory_effect * average_order_value * rng.normal(38.0, 4.0, len(dates))
    incident_penalty = gross_revenue * np.clip(0.018 * operational_incident_effect, 0, 0.12)
    incident_penalty += gross_revenue * np.clip(0.018 * refund_effect + 0.012 * fraud_effect, 0, 0.10)
    net_revenue = gross_revenue * (1.0 - refund_rate) - lost_sales_penalty - stockout_penalty - incident_penalty
    net_revenue += rng.normal(0, 950, len(dates))
    net_revenue = np.clip(net_revenue, 0, None)

    incident_type = incident_type_for_days(
        dates,
        incidents,
        deployment_effect=deployment_effect,
        inventory_effect=inventory_effect,
        shipping_effect=shipping_effect,
    )

    return pd.DataFrame(
        {
            "date": dates.date,
            "sessions": website_visitors,
            "website_visitors": website_visitors,
            "active_customers": active_customers,
            "orders": orders,
            "units_sold": units_sold,
            "gross_revenue": np.round(gross_revenue, 2),
            "net_revenue": np.round(net_revenue, 2),
            "conversion_rate": np.round(conversion_rate, 4),
            "average_order_value": np.round(average_order_value, 2),
            "lost_sales_units": lost_sales_units,
            "expected_refund_rate": np.round(refund_rate, 4),
            "expected_checkout_failure_rate": np.round(checkout_failure_rate, 4),
            "day_of_week": features["day_of_week"].astype(int),
            "month": features["month"].astype(int),
            "quarter": features["quarter"].astype(int),
            "is_weekend": features["is_weekend"].astype(bool),
            "incident_flag": incident_type != "normal",
            "incident_type": incident_type,
        }
    )


def generate_api_latency(
    hours: pd.DatetimeIndex,
    rng: np.random.Generator,
    incidents: IncidentCatalog,
) -> pd.DataFrame:
    hour = hours.hour.to_numpy()
    business_hours = (hour >= 9) & (hour <= 22)
    deployment_effect = deployment_severity(hours, incidents)
    api_effect = business_effect(hours, incidents, ("api_degradation",))
    platform_effect = deployment_effect + api_effect
    deployment_hours = platform_effect > 0

    base_latency = rng.normal(185, 18, len(hours)) + np.where(business_hours, 32, 0)
    base_latency += 18 * np.sin(2 * np.pi * hour / 24)
    p95_latency = base_latency + rng.normal(95, 16, len(hours))
    p99_latency = p95_latency + rng.normal(130, 30, len(hours))

    p95_latency += rng.normal(520, 90, len(hours)) * platform_effect
    p99_latency += rng.normal(1_150, 180, len(hours)) * platform_effect
    error_rate = rng.beta(1.4, 180, len(hours))
    error_rate += rng.uniform(0.025, 0.065, len(hours)) * platform_effect

    return pd.DataFrame(
        {
            "timestamp": hours,
            "service": "checkout-api",
            "request_count": rng.poisson(np.where(business_hours, 8_000, 2_500)).astype(int),
            "avg_latency_ms": np.round(np.clip(base_latency + 360 * platform_effect, 80, None), 1),
            "p95_latency_ms": np.round(np.clip(p95_latency, 120, None), 1),
            "p99_latency_ms": np.round(np.clip(p99_latency, 160, None), 1),
            "error_rate": np.round(np.clip(error_rate, 0, 0.25), 4),
            "incident_flag": deployment_hours,
            "incident_type": np.where(
                deployment_effect > 0,
                "failed_deployment",
                np.where(api_effect > 0, "api_degradation", "normal"),
            ),
        }
    )


def generate_checkout_failures(
    hours: pd.DatetimeIndex,
    rng: np.random.Generator,
    incidents: IncidentCatalog,
) -> pd.DataFrame:
    hour = hours.hour.to_numpy()
    business_hours = (hour >= 8) & (hour <= 23)
    deployment_effect = deployment_severity(hours, incidents)
    api_effect = business_effect(hours, incidents, ("api_degradation",))
    fraud_effect = business_effect(hours, incidents, ("fraud_spike",))
    platform_effect = deployment_effect + api_effect + 0.55 * fraud_effect
    deployment_hours = platform_effect > 0

    checkout_attempts = rng.poisson(np.where(business_hours, 1_850, 620)).astype(int)
    failure_rate = rng.normal(0.018, 0.004, len(hours))
    failure_rate += rng.uniform(0.075, 0.13, len(hours)) * platform_effect
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
            "incident_type": np.where(
                deployment_effect > 0,
                "failed_deployment",
                np.where(api_effect > 0, "api_degradation", np.where(fraud_effect > 0, "fraud_spike", "normal")),
            ),
        }
    )


def generate_support_tickets(
    dates: pd.DatetimeIndex,
    rng: np.random.Generator,
    incidents: IncidentCatalog,
    sales_metrics: pd.DataFrame | None = None,
    checkout_failures: pd.DataFrame | None = None,
    shipping_delays: pd.DataFrame | None = None,
) -> pd.DataFrame:
    deployment_effect = deployment_severity(dates, incidents, normalize=True)
    inventory_effect = inventory_severity(dates, incidents) + business_effect(
        dates, incidents, ("inventory_shortage", "supplier_delay")
    )
    shipping_effect = shipping_severity(dates, incidents) + business_effect(
        dates, incidents, ("warehouse_staffing_shortage", "carrier_outage", "regional_weather_disruption")
    )
    api_effect = business_effect(dates, incidents, ("api_degradation",))
    demand_surge_effect = business_effect(dates, incidents, ("marketing_campaign_surge", "holiday_demand_surge"))
    refund_effect = business_effect(dates, incidents, ("refund_spike", "fraud_spike"))
    incident_days = (
        (deployment_effect > 0)
        | (shipping_effect > 0)
        | (inventory_effect > 0)
        | (api_effect > 0)
        | (demand_surge_effect > 0)
        | (refund_effect > 0)
    )

    active_customers = np.full(len(dates), 7_200.0)
    if sales_metrics is not None and {"date", "active_customers"} <= set(sales_metrics.columns):
        sales = sales_metrics.copy()
        sales["date"] = pd.to_datetime(sales["date"], errors="raise").dt.normalize()
        active_customers = (
            pd.DataFrame({"date": dates})
            .merge(sales[["date", "active_customers"]], on="date", how="left")["active_customers"]
            .fillna(active_customers[0])
            .to_numpy(dtype=float)
        )

    checkout_failure_rate = np.full(len(dates), 0.018)
    if checkout_failures is not None and {"timestamp", "checkout_attempts", "failed_checkouts"} <= set(checkout_failures.columns):
        checkout = checkout_failures.copy()
        checkout["date"] = pd.to_datetime(checkout["timestamp"], errors="raise").dt.normalize()
        daily_checkout = checkout.groupby("date", as_index=False).agg(
            checkout_attempts=("checkout_attempts", "sum"),
            failed_checkouts=("failed_checkouts", "sum"),
        )
        daily_checkout["checkout_failure_rate"] = daily_checkout["failed_checkouts"] / daily_checkout["checkout_attempts"].where(
            daily_checkout["checkout_attempts"] != 0
        )
        checkout_failure_rate = (
            pd.DataFrame({"date": dates})
            .merge(daily_checkout[["date", "checkout_failure_rate"]], on="date", how="left")["checkout_failure_rate"]
            .fillna(0.018)
            .to_numpy(dtype=float)
        )

    shipping_delay_rate = np.full(len(dates), 0.055)
    if shipping_delays is not None and {"date", "shipments", "delayed_shipments"} <= set(shipping_delays.columns):
        shipping = shipping_delays.copy()
        shipping["date"] = pd.to_datetime(shipping["date"], errors="raise").dt.normalize()
        daily_shipping = shipping.groupby("date", as_index=False).agg(
            shipments=("shipments", "sum"),
            delayed_shipments=("delayed_shipments", "sum"),
        )
        daily_shipping["shipping_delay_rate"] = daily_shipping["delayed_shipments"] / daily_shipping["shipments"].where(
            daily_shipping["shipments"] != 0
        )
        shipping_delay_rate = (
            pd.DataFrame({"date": dates})
            .merge(daily_shipping[["date", "shipping_delay_rate"]], on="date", how="left")["shipping_delay_rate"]
            .fillna(0.055)
            .to_numpy(dtype=float)
        )

    customer_pressure = np.clip((active_customers - 6_800.0) / 1_000.0, -1.2, 3.0)
    checkout_pressure = np.clip((checkout_failure_rate - 0.018) / 0.01, 0.0, 18.0)
    shipping_pressure = np.clip((shipping_delay_rate - 0.055) / 0.01, 0.0, 22.0)

    shipping_complaint_tickets = rng.poisson(
        18 + 2.9 * customer_pressure + 5.3 * shipping_pressure + 42 * shipping_effect
    ).astype(int)
    checkout_issue_tickets = rng.poisson(
        12 + 2.1 * customer_pressure + 4.8 * checkout_pressure + 34 * (deployment_effect + api_effect)
    ).astype(int)
    billing_issue_tickets = rng.poisson(
        15 + 1.5 * customer_pressure + 11 * deployment_effect + 7 * shipping_effect + 5 * inventory_effect + 32 * refund_effect
    ).astype(int)
    account_access_tickets = rng.poisson(20 + 2.2 * customer_pressure + 36 * deployment_effect + 9 * demand_surge_effect).astype(int)
    general_support_tickets = rng.poisson(
        54
        + 5.4 * customer_pressure
        + 28 * (deployment_effect + api_effect)
        + 10 * shipping_effect
        + 8 * inventory_effect
        + 18 * demand_surge_effect
        + 16 * refund_effect
    ).astype(int)
    total = (
        shipping_complaint_tickets
        + checkout_issue_tickets
        + billing_issue_tickets
        + account_access_tickets
        + general_support_tickets
    )
    refund_requests = np.maximum(
        0,
        np.round(
            0.52 * billing_issue_tickets
            + rng.normal(8 + 6 * shipping_effect + 4 * deployment_effect + 22 * refund_effect, 2.5, len(dates))
        ),
    ).astype(int)

    incident_type = incident_type_for_days(
        dates,
        incidents,
        deployment_effect=deployment_effect,
        inventory_effect=inventory_effect,
        shipping_effect=shipping_effect,
    )

    return pd.DataFrame(
        {
            "date": dates.date,
            "total_tickets": total,
            "shipping_complaint_tickets": shipping_complaint_tickets,
            "checkout_issue_tickets": checkout_issue_tickets,
            "billing_issue_tickets": billing_issue_tickets,
            "account_access_tickets": account_access_tickets,
            "general_support_tickets": general_support_tickets,
            "checkout_complaints": checkout_issue_tickets,
            "delivery_complaints": shipping_complaint_tickets,
            "inventory_complaints": np.maximum(0, np.round(general_support_tickets * 0.18 + 18 * inventory_effect)).astype(int),
            "refund_requests": refund_requests,
            "avg_first_response_minutes": np.round(rng.normal(42, 8, len(dates)) + np.where(incident_days, 16, 0), 1),
            "incident_flag": incident_type != "normal",
            "incident_type": incident_type,
        }
    )


def generate_inventory_levels(
    dates: pd.DatetimeIndex,
    rng: np.random.Generator,
    incidents: IncidentCatalog,
) -> pd.DataFrame:
    records = []

    for sku_index, sku in enumerate(SKUS):
        starting_inventory = 1_150 + 175 * sku_index + rng.integers(-80, 90)
        daily_demand = 43 + 9 * sku_index
        on_hand = starting_inventory

        for date_index, date in enumerate(dates):
            active_shortages = [
                incident
                for incident in incidents.inventory_shortages
                if incident.sku == sku and incident.start <= date <= incident.end
            ]
            business_shortage = business_effect(pd.DatetimeIndex([date]), incidents, ("inventory_shortage", "supplier_delay"))[0]
            shortage_severity = sum(incident.severity for incident in active_shortages) + business_shortage
            is_shortage_day = shortage_severity > 0
            demand = max(0, int(rng.normal(daily_demand, 8)))
            received_units = 0

            if date_index % 21 == 0 and not is_shortage_day:
                received_units = int(rng.normal(760, 55))
            if is_shortage_day:
                received_units = 0
                demand += int(rng.normal(38 * shortage_severity, 8))

            on_hand = max(0, on_hand + received_units - demand)
            if is_shortage_day:
                on_hand = min(on_hand, rng.integers(0, max(2, int(36 / shortage_severity))))

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
                    "incident_type": (
                        first_active_business_incident(date, incidents).incident_type
                        if first_active_business_incident(date, incidents)
                        and first_active_business_incident(date, incidents).incident_type
                        in {"inventory_shortage", "supplier_delay"}
                        else "inventory_shortage"
                        if is_shortage_day
                        else "normal"
                    ),
                }
            )

    return pd.DataFrame.from_records(records)


def generate_shipping_delays(
    dates: pd.DatetimeIndex,
    rng: np.random.Generator,
    incidents: IncidentCatalog,
) -> pd.DataFrame:
    records = []

    for date_index, date in enumerate(dates):
        for region in REGIONS:
            for carrier in CARRIERS:
                active_disruptions = [
                    incident
                    for incident in incidents.shipping_disruptions
                    if incident.start <= date <= incident.end
                    and region in incident.affected_regions
                    and carrier in incident.affected_carriers
                ]
                regional_business_disruptions = [
                    incident
                    for incident in incidents.business_incidents
                    if incident.incident_type
                    in {"warehouse_staffing_shortage", "carrier_outage", "regional_weather_disruption", "holiday_demand_surge"}
                    and incident.start <= date <= incident.end
                    and incident.affected_region == region
                ]
                disruption_severity = sum(incident.severity for incident in active_disruptions) + sum(
                    incident.severity for incident in regional_business_disruptions
                )
                affected = disruption_severity > 0
                shipments = int(rng.poisson(420 if region != "West" else 360))
                weekday_pressure = 0.025 if date.dayofweek in (0, 1) else 0.0
                seasonal_pressure = 0.045 if date.month in (11, 12) else 0.0
                carrier_pressure = {"ShipFast": 0.025, "ParcelPro": 0.045, "Northline": 0.015}[carrier]
                utilization = rng.normal(0.64, 0.045) + weekday_pressure + seasonal_pressure + carrier_pressure
                utilization += 0.12 * disruption_severity
                utilization = float(np.clip(utilization, 0.35, 0.98))
                warehouse_backlog = max(
                    0,
                    int(
                        rng.normal(32, 11)
                        + shipments * max(utilization - 0.68, 0) * 0.42
                        + 92 * disruption_severity
                    ),
                )
                delay_rate = rng.normal(0.04, 0.01)
                delay_rate += 0.16 * disruption_severity
                delay_rate += 0.24 * max(utilization - 0.76, 0)
                delay_rate += 0.00065 * warehouse_backlog
                delay_rate = float(np.clip(delay_rate, 0.01, 0.45))
                delayed_shipments = int(rng.binomial(shipments, delay_rate))
                warehouse_backlog += int(delayed_shipments * rng.uniform(0.18, 0.32))
                avg_delay_hours = rng.normal(7.5, 1.6) + 22 * disruption_severity
                region_flags = {column: 0 for column in REGION_DISRUPTION_COLUMNS.values()}
                if affected:
                    region_flags[REGION_DISRUPTION_COLUMNS[region]] = 1

                records.append(
                    {
                        "date": date.date(),
                        "region": region,
                        "carrier": carrier,
                        "shipments": shipments,
                        "delayed_shipments": delayed_shipments,
                        "delay_rate": round(delay_rate, 4),
                        "carrier_capacity_utilization": round(utilization, 4),
                        "warehouse_backlog": warehouse_backlog,
                        "avg_delay_hours": round(max(avg_delay_hours, 0.5), 1),
                        **region_flags,
                        "incident_flag": affected,
                        "incident_type": (
                            regional_business_disruptions[0].incident_type
                            if regional_business_disruptions
                            else "shipping_disruption"
                            if affected
                            else "normal"
                        ),
                    }
                )

    return pd.DataFrame.from_records(records)


def generate_deployment_events(incidents: IncidentCatalog) -> pd.DataFrame:
    records: list[dict[str, object]] = [
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
            "timestamp": pd.Timestamp("2025-04-29 11:00"),
            "service": "recommendations-api",
            "version": "2025.04.29.1",
            "environment": "production",
            "status": "success",
            "change_type": "model_refresh",
            "incident_flag": False,
            "incident_type": "normal",
        },
        {
            "timestamp": pd.Timestamp("2026-03-10 10:30"),
            "service": "catalog-api",
            "version": "2026.03.10.1",
            "environment": "production",
            "status": "success",
            "change_type": "search_tuning",
            "incident_flag": False,
            "incident_type": "normal",
        },
        {
            "timestamp": pd.Timestamp("2026-07-07 09:45"),
            "service": "recommendations-api",
            "version": "2026.07.07.1",
            "environment": "production",
            "status": "success",
            "change_type": "model_refresh",
            "incident_flag": False,
            "incident_type": "normal",
        },
    ]

    for incident in incidents.deployments:
        records.extend(
            [
                {
                    "timestamp": incident.start,
                    "service": incident.service,
                    "version": incident.version,
                    "environment": "production",
                    "status": "failed",
                    "change_type": incident.change_type,
                    "incident_flag": True,
                    "incident_type": "failed_deployment",
                },
                {
                    "timestamp": incident.end + pd.Timedelta(minutes=30),
                    "service": incident.service,
                    "version": f"{incident.version}.rollback",
                    "environment": "production",
                    "status": "rollback_success",
                    "change_type": "rollback",
                    "incident_flag": True,
                    "incident_type": "failed_deployment",
                },
            ]
        )

    for incident in incidents.business_incidents:
        if incident.incident_type != "api_degradation":
            continue
        records.extend(
            [
                {
                    "timestamp": incident.start + pd.Timedelta(hours=9),
                    "service": "checkout-api",
                    "version": f"{incident.start:%Y.%m.%d}.api",
                    "environment": "production",
                    "status": "degraded",
                    "change_type": "dependency_slowdown",
                    "incident_flag": True,
                    "incident_type": "api_degradation",
                },
                {
                    "timestamp": incident.end + pd.Timedelta(hours=18),
                    "service": "checkout-api",
                    "version": f"{incident.start:%Y.%m.%d}.api.fix",
                    "environment": "production",
                    "status": "mitigated",
                    "change_type": "dependency_rollback",
                    "incident_flag": True,
                    "incident_type": "api_degradation",
                },
            ]
        )

    return pd.DataFrame(records).sort_values("timestamp").reset_index(drop=True)


def generate_all_datasets(
    start_date: str = "2024-01-01",
    end_date: str = "2026-12-31",
    seed: int = 42,
) -> Dict[str, pd.DataFrame]:
    rng = np.random.default_rng(seed)
    incidents = IncidentCatalog(
        deployments=PHASE_6_INCIDENTS.deployments,
        inventory_shortages=PHASE_6_INCIDENTS.inventory_shortages,
        shipping_disruptions=PHASE_6_INCIDENTS.shipping_disruptions,
        business_incidents=generate_business_incidents(start_date, end_date),
    )
    days = daily_dates(start_date, end_date)
    hours = hourly_dates(start_date, end_date)

    LOGGER.info("Generating Northstar Commerce synthetic data from %s to %s with seed=%s", start_date, end_date, seed)
    sales_metrics = generate_sales_metrics(days, rng, incidents)
    api_latency = generate_api_latency(hours, rng, incidents)
    checkout_failures = generate_checkout_failures(hours, rng, incidents)
    inventory_levels = generate_inventory_levels(days, rng, incidents)
    shipping_delays = generate_shipping_delays(days, rng, incidents)
    support_tickets = generate_support_tickets(days, rng, incidents, sales_metrics, checkout_failures, shipping_delays)
    return {
        "sales_metrics_daily": sales_metrics,
        "api_latency_hourly": api_latency,
        "checkout_failures_hourly": checkout_failures,
        "support_tickets_daily": support_tickets,
        "inventory_levels_daily": inventory_levels,
        "shipping_delays_daily": shipping_delays,
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
    parser.add_argument("--start-date", default="2024-01-01", help="Inclusive start date in YYYY-MM-DD format.")
    parser.add_argument("--end-date", default="2026-12-31", help="Inclusive end date in YYYY-MM-DD format.")
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
