from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression

from src.analytics.kpi_monitor import run_kpi_monitor
from src.explainability.explain_forecasts import run_explainability
from src.forecasting.generate_forecasts import run_forecasting
from src.forecasting.train_forecasting_models import TARGET_KPIS, create_forecasting_dataset, get_feature_columns, run_training
from src.ingestion.generate_synthetic_data import generate_all_datasets, write_datasets


def build_forecasting_outputs(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    data_dir = tmp_path / "synthetic"
    reports_dir = tmp_path / "reports"
    figures_dir = tmp_path / "figures"
    models_dir = tmp_path / "models"
    write_datasets(generate_all_datasets(seed=42), data_dir)
    kpi_path = reports_dir / "kpi_summary_daily.csv"
    metrics_path = reports_dir / "model_metrics.csv"
    forecast_path = reports_dir / "forecast_summary.csv"
    run_kpi_monitor(data_dir, kpi_path, figures_dir, create_plots=False)
    run_training(kpi_path, metrics_path, models_dir, figures_dir, create_plots=False)
    run_forecasting(models_dir, forecast_path, figures_dir, horizon_days=7, create_plots=False)
    return models_dir, metrics_path, forecast_path, figures_dir


def test_explainability_outputs_are_created_and_complete(tmp_path):
    models_dir, metrics_path, forecast_path, figures_dir = build_forecasting_outputs(tmp_path)
    importance_path = tmp_path / "reports" / "shap_feature_importance.csv"
    report_path = tmp_path / "reports" / "forecast_explanations.md"

    importance = run_explainability(models_dir, metrics_path, forecast_path, importance_path, report_path, figures_dir)
    report_text = report_path.read_text(encoding="utf-8")

    assert report_path.exists()
    assert importance_path.exists()
    assert report_text.strip()
    assert not importance.empty
    assert set(importance["kpi"]) == set(TARGET_KPIS)
    assert importance.groupby("kpi").size().ge(1).all()
    for target_kpi in TARGET_KPIS:
        assert f"### {target_kpi}" in report_text
        assert (figures_dir / f"shap_summary_{target_kpi}.png").exists()


def test_explainability_handles_selected_linear_regression_for_net_revenue(tmp_path):
    models_dir, metrics_path, forecast_path, figures_dir = build_forecasting_outputs(tmp_path)
    kpi_path = tmp_path / "reports" / "kpi_summary_daily.csv"
    summary = pd.read_csv(kpi_path)
    dataset = create_forecasting_dataset(summary, "net_revenue")
    feature_columns = list(get_feature_columns("net_revenue"))
    model = LinearRegression()
    model.fit(dataset[feature_columns], dataset["net_revenue"])

    artifact_path = models_dir / "forecasting_net_revenue.joblib"
    artifact = joblib.load(artifact_path)
    artifact["model_name"] = "linear_regression"
    artifact["model"] = model
    joblib.dump(artifact, artifact_path)

    metrics = pd.read_csv(metrics_path)
    metrics.loc[metrics["kpi"] == "net_revenue", "selected_model"] = False
    metrics.loc[(metrics["kpi"] == "net_revenue") & (metrics["model_name"] == "linear_regression"), "selected_model"] = True
    metrics.to_csv(metrics_path, index=False)

    importance_path = tmp_path / "reports" / "linear_shap_feature_importance.csv"
    report_path = tmp_path / "reports" / "linear_forecast_explanations.md"
    importance = run_explainability(models_dir, metrics_path, forecast_path, importance_path, report_path, figures_dir)
    report_text = report_path.read_text(encoding="utf-8")
    net_revenue_rows = importance[importance["kpi"] == "net_revenue"]

    assert not net_revenue_rows.empty
    assert "### net_revenue" in report_text
    assert "linear_regression" in report_text
    assert net_revenue_rows["explanation_method"].str.contains("LinearExplainer|coefficient fallback", regex=True).all()
