from pathlib import Path

import pandas as pd

from src.analytics.kpi_monitor import run_kpi_monitor
from src.forecasting.generate_forecasts import run_forecasting
from src.forecasting.train_forecasting_models import TARGET_KPIS, create_forecasting_dataset, run_training
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
    }.issubset(dataset.columns)
    assert dataset["previous_day_value"].notna().all()
    assert dataset["date"].is_monotonic_increasing


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
