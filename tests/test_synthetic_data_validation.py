from pathlib import Path

import pandas as pd
import pytest

from src.ingestion.generate_synthetic_data import generate_all_datasets, write_datasets
from src.ingestion.validate_synthetic_data import (
    SyntheticDataValidationError,
    generate_profile_report,
    main,
    validate_synthetic_data,
)


def write_default_synthetic_data(output_dir: Path) -> None:
    datasets = generate_all_datasets(seed=42)
    write_datasets(datasets, output_dir)


def test_validate_generated_synthetic_data_passes_and_profiles(tmp_path):
    data_dir = tmp_path / "synthetic"
    report_path = tmp_path / "reports" / "synthetic_data_profile.md"
    write_default_synthetic_data(data_dir)

    datasets, errors = validate_synthetic_data(data_dir)
    generate_profile_report(datasets, report_path)

    assert errors == []
    assert set(datasets) == {
        "sales_metrics_daily.csv",
        "api_latency_hourly.csv",
        "checkout_failures_hourly.csv",
        "support_tickets_daily.csv",
        "inventory_levels_daily.csv",
        "shipping_delays_daily.csv",
        "deployment_events.csv",
    }

    report = report_path.read_text(encoding="utf-8")
    assert "## Row Counts and Date Ranges" in report
    assert "## Missing Values" in report
    assert "## Numeric Descriptive Statistics" in report
    assert "## Detected Incident Windows" in report
    assert "failed_deployment" in report
    assert "inventory_shortage" in report
    assert "shipping_disruption" in report


def test_generated_sales_data_includes_revenue_driver_fields():
    sales = generate_all_datasets(seed=42)["sales_metrics_daily"]

    assert {
        "website_visitors",
        "active_customers",
        "average_order_value",
        "expected_refund_rate",
        "expected_checkout_failure_rate",
        "day_of_week",
        "month",
        "quarter",
        "is_weekend",
    }.issubset(sales.columns)
    assert sales["website_visitors"].gt(0).all()
    assert sales["active_customers"].gt(0).all()
    assert sales["average_order_value"].gt(0).all()


def test_generated_operational_data_includes_phase_7_drivers():
    datasets = generate_all_datasets(seed=42)
    support = datasets["support_tickets_daily"]
    shipping = datasets["shipping_delays_daily"]

    support_categories = [
        "shipping_complaint_tickets",
        "checkout_issue_tickets",
        "billing_issue_tickets",
        "account_access_tickets",
        "general_support_tickets",
    ]
    assert set(support_categories).issubset(support.columns)
    assert support["total_tickets"].equals(support[support_categories].sum(axis=1))
    assert support.loc[support["incident_type"] == "shipping_disruption", "shipping_complaint_tickets"].mean() > support.loc[
        support["incident_type"] == "normal", "shipping_complaint_tickets"
    ].mean()
    assert support.loc[support["incident_type"] == "failed_deployment", "checkout_issue_tickets"].mean() > support.loc[
        support["incident_type"] == "normal", "checkout_issue_tickets"
    ].mean()

    assert {
        "carrier_capacity_utilization",
        "warehouse_backlog",
        "east_region_disruption",
        "west_region_disruption",
        "south_region_disruption",
        "central_region_disruption",
    }.issubset(shipping.columns)
    assert shipping["carrier_capacity_utilization"].between(0, 1).all()
    assert shipping["warehouse_backlog"].ge(0).all()


def test_validation_reports_missing_required_file(tmp_path):
    data_dir = tmp_path / "synthetic"
    write_default_synthetic_data(data_dir)
    (data_dir / "sales_metrics_daily.csv").unlink()

    _, errors = validate_synthetic_data(data_dir)

    assert any("Missing required file" in error for error in errors)
    assert any("sales_metrics_daily.csv" in error for error in errors)


def test_validation_reports_schema_date_duplicate_and_range_errors(tmp_path):
    data_dir = tmp_path / "synthetic"
    write_default_synthetic_data(data_dir)

    sales_path = data_dir / "sales_metrics_daily.csv"
    sales = pd.read_csv(sales_path)
    sales = pd.concat([sales, sales.iloc[[1]]], ignore_index=True)
    sales.loc[0, "date"] = "not-a-date"
    sales.loc[1, "gross_revenue"] = -1
    sales = sales.drop(columns=["orders"])
    sales.to_csv(sales_path, index=False)

    _, errors = validate_synthetic_data(data_dir)

    assert any("missing required columns: orders" in error for error in errors)

    sales["orders"] = 1
    sales.to_csv(sales_path, index=False)
    _, errors = validate_synthetic_data(data_dir)

    assert any("contains unparseable date/time values" in error for error in errors)
    assert any("duplicate rows found" in error for error in errors)
    assert any("gross_revenue contains negative values" in error for error in errors)


def test_validation_reports_missing_expected_incident_window(tmp_path):
    data_dir = tmp_path / "synthetic"
    write_default_synthetic_data(data_dir)

    latency_path = data_dir / "api_latency_hourly.csv"
    latency = pd.read_csv(latency_path)
    latency.loc[latency["incident_type"] == "failed_deployment", "incident_flag"] = False
    latency.loc[latency["incident_type"] == "failed_deployment", "incident_type"] = "normal"
    latency.to_csv(latency_path, index=False)

    _, errors = validate_synthetic_data(data_dir)

    assert any("api_latency_hourly.csv: missing expected failed_deployment rows" in error for error in errors)


def test_main_raises_on_validation_failure(tmp_path):
    data_dir = tmp_path / "synthetic"
    write_default_synthetic_data(data_dir)
    (data_dir / "deployment_events.csv").unlink()

    with pytest.raises(SyntheticDataValidationError):
        main(["--data-dir", str(data_dir), "--report-path", str(tmp_path / "profile.md")])
