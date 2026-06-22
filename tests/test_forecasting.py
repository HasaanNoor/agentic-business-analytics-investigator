from pathlib import Path

import pandas as pd

from src.analytics.kpi_monitor import run_kpi_monitor
from src.forecasting.generate_forecasts import run_forecasting
from src.forecasting.train_forecasting_models import TARGET_KPIS, create_forecasting_dataset, get_feature_columns, run_training
from src.ingestion.generate_synthetic_data import generate_all_datasets, write_datasets


def write_default_synthetic_data(output_dir: Path) -> None:
    datasets = generate_all_datasets(seed=42)
    write_datasets(datasets, output_dir)


def build_test_kpi_summary(tmp_path: Path) -> Path:
    data_dir = tmp_path / "synthetic"
    kpi_path = tmp_path / "reports" / "kpi_summary_daily.csv"
    figures_dir = tmp_path / "figures"
    write_default_synthetic_data(data_dir)
    run_kpi_monitor(data_dir, kpi_path, figures_dir, create_plots=False)
    return kpi_path


def test_forecasting_dataset_uses_required_lag_features(tmp_path):
    kpi_path = build_test_kpi_summary(tmp_path)
    summary = pd.read_csv(kpi_path)
    dataset = create_forecasting_dataset(summary, "net_revenue")

    assert {
        "previous_day_value",
        "rolling_avg_3d",
        "rolling_avg_7d",
        "rolling_avg_14d",
        "lag_7d",
        "lag_14d",
        "website_visitors",
        "active_customers",
        "average_order_value",
        "day_of_week",
        "month",
        "quarter",
        "is_weekend",
        "avg_api_latency_ms",
        "checkout_failure_rate",
        "support_ticket_count",
        "shipping_delay_rate",
        "stockout_units",
        "lost_sales_units",
        "conversion_rate",
        "refund_rate",
    }.issubset(dataset.columns)
    assert set(get_feature_columns("net_revenue")).issubset(dataset.columns)
    assert {
        "website_visitors",
        "active_customers",
        "average_order_value",
    }.issubset(set(get_feature_columns("net_revenue")))
    assert dataset["previous_day_value"].notna().all()
    assert dataset["date"].is_monotonic_increasing


def test_phase_7_forecasting_feature_sets_use_operational_drivers(tmp_path):
    kpi_path = build_test_kpi_summary(tmp_path)
    summary = pd.read_csv(kpi_path)
    support_dataset = create_forecasting_dataset(summary, "support_ticket_count")
    shipping_dataset = create_forecasting_dataset(summary, "shipping_delay_rate")

    support_features = set(get_feature_columns("support_ticket_count"))
    shipping_features = set(get_feature_columns("shipping_delay_rate"))
    ticket_category_columns = {
        "shipping_complaint_tickets",
        "checkout_issue_tickets",
        "billing_issue_tickets",
        "account_access_tickets",
        "general_support_tickets",
    }

    assert {
        "active_customers",
        "website_visitors",
        "avg_api_latency_ms",
        "checkout_failure_rate",
        "shipping_delay_rate",
        "deployment_event_flag",
    }.issubset(support_features)
    assert support_features.isdisjoint(ticket_category_columns)
    assert "support_ticket_count" not in support_features
    for ticket_category in ticket_category_columns:
        assert {
            f"{ticket_category}_previous_day",
            f"{ticket_category}_rolling_avg_3d",
            f"{ticket_category}_rolling_avg_7d",
        }.issubset(support_features)
    assert {
        "carrier_capacity_utilization",
        "warehouse_backlog",
        "shipping_complaint_tickets",
        "east_region_disruption",
        "west_region_disruption",
        "south_region_disruption",
        "central_region_disruption",
    }.issubset(shipping_features)
    assert support_features.issubset(support_dataset.columns)
    assert shipping_features.issubset(shipping_dataset.columns)


def test_support_ticket_forecast_features_do_not_leak_same_day_ticket_categories(tmp_path):
    kpi_path = build_test_kpi_summary(tmp_path)
    summary = pd.read_csv(kpi_path).sort_values("date").reset_index(drop=True)
    support_dataset = create_forecasting_dataset(summary, "support_ticket_count")
    support_features = set(get_feature_columns("support_ticket_count"))
    leaking_columns = {
        "support_ticket_count",
        "shipping_complaint_tickets",
        "checkout_issue_tickets",
        "billing_issue_tickets",
        "account_access_tickets",
        "general_support_tickets",
    }

    assert support_features.isdisjoint(leaking_columns)
    first_model_row = support_dataset.iloc[0]
    source_row = summary[summary["date"] == first_model_row["date"]].index[0]
    assert source_row >= 14
    for column in leaking_columns.difference({"support_ticket_count"}):
        assert first_model_row[f"{column}_previous_day"] == summary.loc[source_row - 1, column]
        assert first_model_row[f"{column}_rolling_avg_3d"] == summary.loc[source_row - 3 : source_row - 1, column].mean()
        assert first_model_row[f"{column}_rolling_avg_7d"] == summary.loc[source_row - 7 : source_row - 1, column].mean()


def test_training_generates_metrics_and_model_artifacts(tmp_path):
    kpi_path = build_test_kpi_summary(tmp_path)
    metrics_path = tmp_path / "reports" / "model_metrics.csv"
    models_dir = tmp_path / "models"
    figures_dir = tmp_path / "figures"

    metrics = run_training(kpi_path, metrics_path, models_dir, figures_dir, create_plots=False)

    assert metrics_path.exists()
    assert len(metrics) == len(TARGET_KPIS) * 3
    assert set(metrics["kpi"]) == set(TARGET_KPIS)
    assert metrics.groupby("kpi")["selected_model"].sum().eq(1).all()
    assert metrics[["mae", "rmse", "r2"]].notna().all().all()
    for target_kpi in TARGET_KPIS:
        assert (models_dir / f"forecasting_{target_kpi}.joblib").exists()


def test_forecasting_outputs_exist_and_predictions_are_complete(tmp_path):
    kpi_path = build_test_kpi_summary(tmp_path)
    metrics_path = tmp_path / "reports" / "model_metrics.csv"
    forecast_path = tmp_path / "reports" / "forecast_summary.csv"
    models_dir = tmp_path / "models"
    figures_dir = tmp_path / "figures"
    run_training(kpi_path, metrics_path, models_dir, figures_dir, create_plots=False)

    forecasts = run_forecasting(models_dir, forecast_path, figures_dir, horizon_days=7, create_plots=True)

    assert forecast_path.exists()
    assert len(forecasts) == len(TARGET_KPIS) * 7
    assert set(forecasts["kpi"]) == set(TARGET_KPIS)
    assert forecasts["prediction"].notna().all()
    assert forecasts["prediction"].ge(0).all()
    for target_kpi in TARGET_KPIS:
        assert (figures_dir / f"forecast_extension_{target_kpi}.png").exists()
