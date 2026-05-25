"""Validate and profile Northstar Commerce synthetic datasets."""

from __future__ import annotations

import argparse
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd
from pandas.api.types import is_bool_dtype, is_numeric_dtype


LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class FileSpec:
    required_columns: tuple[str, ...]
    datetime_column: str
    duplicate_key_columns: tuple[str, ...]
    nonnegative_columns: tuple[str, ...]
    rate_columns: tuple[str, ...] = ()


@dataclass(frozen=True)
class IncidentSpec:
    incident_type: str
    start: pd.Timestamp
    end: pd.Timestamp
    affected_files: tuple[str, ...]


FILE_SPECS: dict[str, FileSpec] = {
    "sales_metrics_daily.csv": FileSpec(
        required_columns=(
            "date",
            "sessions",
            "orders",
            "units_sold",
            "gross_revenue",
            "net_revenue",
            "conversion_rate",
            "average_order_value",
            "lost_sales_units",
            "incident_flag",
            "incident_type",
        ),
        datetime_column="date",
        duplicate_key_columns=("date",),
        nonnegative_columns=(
            "sessions",
            "orders",
            "units_sold",
            "gross_revenue",
            "net_revenue",
            "average_order_value",
            "lost_sales_units",
        ),
        rate_columns=("conversion_rate",),
    ),
    "api_latency_hourly.csv": FileSpec(
        required_columns=(
            "timestamp",
            "service",
            "request_count",
            "avg_latency_ms",
            "p95_latency_ms",
            "p99_latency_ms",
            "error_rate",
            "incident_flag",
            "incident_type",
        ),
        datetime_column="timestamp",
        duplicate_key_columns=("timestamp",),
        nonnegative_columns=("request_count", "avg_latency_ms", "p95_latency_ms", "p99_latency_ms"),
        rate_columns=("error_rate",),
    ),
    "checkout_failures_hourly.csv": FileSpec(
        required_columns=(
            "timestamp",
            "checkout_attempts",
            "failed_checkouts",
            "failure_rate",
            "payment_gateway_errors",
            "api_timeout_errors",
            "incident_flag",
            "incident_type",
        ),
        datetime_column="timestamp",
        duplicate_key_columns=("timestamp",),
        nonnegative_columns=(
            "checkout_attempts",
            "failed_checkouts",
            "payment_gateway_errors",
            "api_timeout_errors",
        ),
        rate_columns=("failure_rate",),
    ),
    "support_tickets_daily.csv": FileSpec(
        required_columns=(
            "date",
            "total_tickets",
            "checkout_complaints",
            "delivery_complaints",
            "inventory_complaints",
            "refund_requests",
            "avg_first_response_minutes",
            "incident_flag",
            "incident_type",
        ),
        datetime_column="date",
        duplicate_key_columns=("date",),
        nonnegative_columns=(
            "total_tickets",
            "checkout_complaints",
            "delivery_complaints",
            "inventory_complaints",
            "refund_requests",
            "avg_first_response_minutes",
        ),
    ),
    "inventory_levels_daily.csv": FileSpec(
        required_columns=(
            "date",
            "sku",
            "warehouse",
            "on_hand_units",
            "units_demanded",
            "units_received",
            "stockout_units",
            "reorder_point",
            "incident_flag",
            "incident_type",
        ),
        datetime_column="date",
        duplicate_key_columns=("date", "sku", "warehouse"),
        nonnegative_columns=("on_hand_units", "units_demanded", "units_received", "stockout_units", "reorder_point"),
    ),
    "shipping_delays_daily.csv": FileSpec(
        required_columns=(
            "date",
            "region",
            "carrier",
            "shipments",
            "delayed_shipments",
            "delay_rate",
            "avg_delay_hours",
            "incident_flag",
            "incident_type",
        ),
        datetime_column="date",
        duplicate_key_columns=("date", "region", "carrier"),
        nonnegative_columns=("shipments", "delayed_shipments", "avg_delay_hours"),
        rate_columns=("delay_rate",),
    ),
    "deployment_events.csv": FileSpec(
        required_columns=(
            "timestamp",
            "service",
            "version",
            "environment",
            "status",
            "change_type",
            "incident_flag",
            "incident_type",
        ),
        datetime_column="timestamp",
        duplicate_key_columns=("timestamp", "service", "version"),
        nonnegative_columns=(),
    ),
}


INCIDENT_SPECS: tuple[IncidentSpec, ...] = (
    IncidentSpec(
        incident_type="failed_deployment",
        start=pd.Timestamp("2025-03-18 09:00"),
        end=pd.Timestamp("2025-03-20 23:59:59"),
        affected_files=(
            "sales_metrics_daily.csv",
            "api_latency_hourly.csv",
            "checkout_failures_hourly.csv",
            "support_tickets_daily.csv",
            "deployment_events.csv",
        ),
    ),
    IncidentSpec(
        incident_type="inventory_shortage",
        start=pd.Timestamp("2025-04-10"),
        end=pd.Timestamp("2025-04-20 23:59:59"),
        affected_files=("sales_metrics_daily.csv", "inventory_levels_daily.csv"),
    ),
    IncidentSpec(
        incident_type="shipping_disruption",
        start=pd.Timestamp("2025-05-05"),
        end=pd.Timestamp("2025-05-14 23:59:59"),
        affected_files=("support_tickets_daily.csv", "shipping_delays_daily.csv"),
    ),
)


class SyntheticDataValidationError(RuntimeError):
    """Raised when synthetic data validation fails."""


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s - %(message)s")


def read_datasets(data_dir: Path) -> tuple[dict[str, pd.DataFrame], list[str]]:
    datasets: dict[str, pd.DataFrame] = {}
    errors: list[str] = []

    for file_name in FILE_SPECS:
        path = data_dir / file_name
        if not path.exists():
            errors.append(f"Missing required file: {path}")
            continue
        try:
            datasets[file_name] = pd.read_csv(path)
        except Exception as exc:  # pragma: no cover - defensive CLI path
            errors.append(f"Could not read {path}: {exc}")

    return datasets, errors


def validate_dataset(file_name: str, dataframe: pd.DataFrame, spec: FileSpec) -> tuple[pd.DataFrame, list[str]]:
    errors: list[str] = []
    missing_columns = [column for column in spec.required_columns if column not in dataframe.columns]
    if missing_columns:
        errors.append(f"{file_name}: missing required columns: {', '.join(missing_columns)}")
        return dataframe.copy(), errors

    profiled = dataframe.copy()
    datetime_format = "%Y-%m-%d %H:%M:%S" if spec.datetime_column == "timestamp" else "%Y-%m-%d"
    parsed_datetimes = pd.to_datetime(profiled[spec.datetime_column], format=datetime_format, errors="coerce")
    if parsed_datetimes.isna().any():
        errors.append(f"{file_name}: {spec.datetime_column} contains unparseable date/time values")
    profiled[spec.datetime_column] = parsed_datetimes

    duplicated = profiled.duplicated(subset=list(spec.duplicate_key_columns), keep=False)
    if duplicated.any():
        errors.append(
            f"{file_name}: duplicate rows found for key columns "
            f"{', '.join(spec.duplicate_key_columns)} ({int(duplicated.sum())} rows)"
        )

    numeric_columns = list(profiled.select_dtypes(include="number").columns)
    for column in numeric_columns:
        if profiled[column].isna().all():
            errors.append(f"{file_name}: numeric column {column} is entirely null")

    for column in spec.nonnegative_columns:
        numeric_values = pd.to_numeric(profiled[column], errors="coerce")
        if (numeric_values < 0).any():
            errors.append(f"{file_name}: {column} contains negative values")

    for column in spec.rate_columns:
        numeric_values = pd.to_numeric(profiled[column], errors="coerce")
        invalid_rates = (numeric_values < 0) | (numeric_values > 1)
        if invalid_rates.any():
            errors.append(f"{file_name}: {column} contains values outside [0, 1]")

    if "incident_flag" in profiled.columns and not profiled["incident_flag"].dropna().isin([True, False]).all():
        errors.append(f"{file_name}: incident_flag contains non-boolean values")

    return profiled, errors


def detect_incident_windows(datasets: dict[str, pd.DataFrame]) -> list[dict[str, str | int]]:
    detected: list[dict[str, str | int]] = []
    for file_name, dataframe in datasets.items():
        if {"incident_type", "incident_flag"} - set(dataframe.columns):
            continue

        spec = FILE_SPECS[file_name]
        incident_rows = dataframe[(dataframe["incident_flag"] == True) & (dataframe["incident_type"] != "normal")]  # noqa: E712
        for incident_type, group in incident_rows.groupby("incident_type"):
            detected.append(
                {
                    "file": file_name,
                    "incident_type": str(incident_type),
                    "start": str(group[spec.datetime_column].min()),
                    "end": str(group[spec.datetime_column].max()),
                    "rows": int(len(group)),
                }
            )
    return sorted(detected, key=lambda row: (str(row["incident_type"]), str(row["file"])))


def validate_expected_incidents(datasets: dict[str, pd.DataFrame]) -> list[str]:
    errors: list[str] = []
    for incident in INCIDENT_SPECS:
        for file_name in incident.affected_files:
            dataframe = datasets.get(file_name)
            if dataframe is None or {"incident_type", "incident_flag"} - set(dataframe.columns):
                continue

            spec = FILE_SPECS[file_name]
            in_window = dataframe[spec.datetime_column].between(incident.start, incident.end)
            matching_rows = dataframe[
                in_window
                & (dataframe["incident_flag"] == True)  # noqa: E712
                & (dataframe["incident_type"] == incident.incident_type)
            ]
            if matching_rows.empty:
                errors.append(
                    f"{file_name}: missing expected {incident.incident_type} rows between "
                    f"{incident.start} and {incident.end}"
                )

    return errors


def validate_synthetic_data(data_dir: Path) -> tuple[dict[str, pd.DataFrame], list[str]]:
    datasets, errors = read_datasets(data_dir)
    profiled_datasets: dict[str, pd.DataFrame] = {}

    for file_name, dataframe in datasets.items():
        profiled, dataset_errors = validate_dataset(file_name, dataframe, FILE_SPECS[file_name])
        profiled_datasets[file_name] = profiled
        errors.extend(dataset_errors)

    if not errors:
        errors.extend(validate_expected_incidents(profiled_datasets))

    return profiled_datasets, errors


def markdown_table(headers: Iterable[str], rows: Iterable[Iterable[object]]) -> str:
    header_list = list(headers)
    lines = [
        "| " + " | ".join(header_list) + " |",
        "| " + " | ".join("---" for _ in header_list) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)


def generate_profile_report(datasets: dict[str, pd.DataFrame], report_path: Path) -> None:
    lines: list[str] = [
        "# Synthetic Data Profile",
        "",
        "Generated by `src/ingestion/validate_synthetic_data.py`.",
        "",
        "## Row Counts and Date Ranges",
        "",
    ]

    range_rows = []
    for file_name, dataframe in datasets.items():
        spec = FILE_SPECS[file_name]
        range_rows.append(
            (
                file_name,
                len(dataframe),
                spec.datetime_column,
                dataframe[spec.datetime_column].min(),
                dataframe[spec.datetime_column].max(),
            )
        )
    lines.append(markdown_table(("File", "Rows", "Date column", "Start", "End"), range_rows))

    lines.extend(["", "## Missing Values", ""])
    for file_name, dataframe in datasets.items():
        missing = dataframe.isna().sum()
        rows = [(column, int(count)) for column, count in missing.items() if count > 0]
        lines.append(f"### {file_name}")
        lines.append("")
        if rows:
            lines.append(markdown_table(("Column", "Missing values"), rows))
        else:
            lines.append("No missing values detected.")
        lines.append("")

    lines.extend(["## Numeric Descriptive Statistics", ""])
    for file_name, dataframe in datasets.items():
        numeric_columns = [
            column
            for column in dataframe.columns
            if is_numeric_dtype(dataframe[column]) and not is_bool_dtype(dataframe[column])
        ]
        lines.append(f"### {file_name}")
        lines.append("")
        if not numeric_columns:
            lines.append("No numeric columns detected.")
            lines.append("")
            continue
        stats = dataframe[numeric_columns].describe().transpose()
        rows = []
        for column, values in stats.iterrows():
            rows.append(
                (
                    column,
                    int(values["count"]),
                    round(float(values["mean"]), 4),
                    round(float(values["std"]), 4) if pd.notna(values["std"]) else "",
                    round(float(values["min"]), 4),
                    round(float(values["50%"]), 4),
                    round(float(values["max"]), 4),
                )
            )
        lines.append(markdown_table(("Column", "Count", "Mean", "Std", "Min", "Median", "Max"), rows))
        lines.append("")

    lines.extend(["## Detected Incident Windows", ""])
    detected = detect_incident_windows(datasets)
    if detected:
        rows = [
            (item["incident_type"], item["file"], item["start"], item["end"], item["rows"])
            for item in detected
        ]
        lines.append(markdown_table(("Incident", "Affected metric file", "Start", "End", "Rows"), rows))
    else:
        lines.append("No incident windows detected.")

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args(args: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate and profile generated Northstar Commerce synthetic data.")
    parser.add_argument("--data-dir", type=Path, default=Path("data/synthetic"), help="Directory containing synthetic CSVs.")
    parser.add_argument(
        "--report-path",
        type=Path,
        default=Path("outputs/reports/synthetic_data_profile.md"),
        help="Markdown profile report output path.",
    )
    return parser.parse_args(args)


def main(args: Iterable[str] | None = None) -> None:
    configure_logging()
    parsed = parse_args(args)
    datasets, errors = validate_synthetic_data(parsed.data_dir)

    if errors:
        for error in errors:
            LOGGER.error(error)
        raise SyntheticDataValidationError(f"Synthetic data validation failed with {len(errors)} error(s).")

    generate_profile_report(datasets, parsed.report_path)
    LOGGER.info("Synthetic data validation passed.")
    LOGGER.info("Wrote profile report to %s", parsed.report_path)


if __name__ == "__main__":
    main()
