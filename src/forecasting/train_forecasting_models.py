"""Train deterministic forecasting models for daily business KPIs."""

from __future__ import annotations

import argparse
import logging
import os
from pathlib import Path
from typing import Iterable

os.environ.setdefault("MPLCONFIGDIR", str(Path("outputs/.matplotlib")))
os.environ.setdefault("XDG_CACHE_HOME", str(Path("outputs/.cache")))

import joblib
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor


LOGGER = logging.getLogger(__name__)


TARGET_KPIS = ("net_revenue", "support_ticket_count", "shipping_delay_rate")
FEATURE_COLUMNS = (
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
    "delivery_complaints",
    "deployment_event_flag",
    "inventory_shortage_flag",
    "shipping_disruption_flag",
)
BASE_FEATURE_COLUMNS = FEATURE_COLUMNS[:6]
CROSS_KPI_FEATURES = {
    "net_revenue": (
        "website_visitors",
        "active_customers",
        "average_order_value",
        "day_of_week",
        "month",
        "quarter",
        "is_weekend",
        "conversion_rate",
        "refund_rate",
        "checkout_failure_rate",
        "avg_api_latency_ms",
        "support_ticket_count",
        "stockout_units",
        "lost_sales_units",
        "shipping_delay_rate",
    ),
    "support_ticket_count": (
        "avg_api_latency_ms",
        "checkout_failure_rate",
        "shipping_delay_rate",
        "deployment_event_flag",
    ),
    "shipping_delay_rate": (
        "delivery_complaints",
        "support_ticket_count",
        "stockout_units",
        "shipping_disruption_flag",
    ),
}
RANDOM_STATE = 42


class ForecastingError(RuntimeError):
    """Raised when deterministic forecasting cannot complete."""


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s - %(message)s")


def load_kpi_summary(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise ForecastingError(f"Missing KPI summary file: {path}")

    summary = pd.read_csv(path)
    required_columns = {"date", *TARGET_KPIS}
    missing_columns = sorted(required_columns.difference(summary.columns))
    if missing_columns:
        raise ForecastingError(f"KPI summary missing required columns: {', '.join(missing_columns)}")

    summary["date"] = pd.to_datetime(summary["date"], errors="raise").dt.normalize()
    return summary.sort_values("date").reset_index(drop=True)


def get_feature_columns(target_kpi: str) -> tuple[str, ...]:
    if target_kpi not in TARGET_KPIS:
        raise ForecastingError(f"Unsupported target KPI: {target_kpi}")
    return (*BASE_FEATURE_COLUMNS, *CROSS_KPI_FEATURES[target_kpi])


def create_forecasting_dataset(summary: pd.DataFrame, target_kpi: str) -> pd.DataFrame:
    if target_kpi not in summary.columns:
        raise ForecastingError(f"KPI summary missing target column: {target_kpi}")

    feature_columns = get_feature_columns(target_kpi)
    required_columns = {"date", target_kpi, *CROSS_KPI_FEATURES[target_kpi]}
    missing_columns = sorted(required_columns.difference(summary.columns))
    if missing_columns:
        raise ForecastingError(f"KPI summary missing required feature columns: {', '.join(missing_columns)}")

    dataset = summary[["date", target_kpi, *CROSS_KPI_FEATURES[target_kpi]]].copy()
    dataset[target_kpi] = dataset[target_kpi].astype(float)
    for column in CROSS_KPI_FEATURES[target_kpi]:
        dataset[column] = dataset[column].astype(float)
    prior_values = dataset[target_kpi].shift(1)
    dataset["previous_day_value"] = prior_values
    dataset["rolling_avg_3d"] = prior_values.rolling(window=3, min_periods=3).mean()
    dataset["rolling_avg_7d"] = prior_values.rolling(window=7, min_periods=7).mean()
    dataset["rolling_avg_14d"] = prior_values.rolling(window=14, min_periods=14).mean()
    dataset["lag_7d"] = dataset[target_kpi].shift(7)
    dataset["lag_14d"] = dataset[target_kpi].shift(14)

    return dataset.dropna(subset=[*feature_columns, target_kpi]).reset_index(drop=True)


def split_time_ordered(dataset: pd.DataFrame, test_fraction: float = 0.2, minimum_test_rows: int = 14) -> tuple[pd.DataFrame, pd.DataFrame]:
    if len(dataset) < minimum_test_rows + 10:
        raise ForecastingError(f"Not enough rows for time-ordered train/test split: {len(dataset)}")

    test_rows = max(minimum_test_rows, int(round(len(dataset) * test_fraction)))
    test_rows = min(test_rows, len(dataset) - 10)
    split_index = len(dataset) - test_rows
    return dataset.iloc[:split_index].copy(), dataset.iloc[split_index:].copy()


def build_model_candidates() -> dict[str, object]:
    return {
        "linear_regression": LinearRegression(),
        "random_forest": RandomForestRegressor(
            n_estimators=250,
            max_depth=8,
            min_samples_leaf=2,
            random_state=RANDOM_STATE,
            n_jobs=1,
        ),
        "xgboost": XGBRegressor(
            objective="reg:squarederror",
            n_estimators=250,
            max_depth=3,
            learning_rate=0.05,
            subsample=1.0,
            colsample_bytree=1.0,
            random_state=RANDOM_STATE,
            n_jobs=1,
        ),
    }


def evaluate_predictions(actual: pd.Series, predicted: np.ndarray) -> dict[str, float]:
    mae = mean_absolute_error(actual, predicted)
    rmse = float(np.sqrt(mean_squared_error(actual, predicted)))
    r2 = r2_score(actual, predicted)
    return {"mae": round(float(mae), 6), "rmse": round(rmse, 6), "r2": round(float(r2), 6)}


def plot_actual_vs_predicted(kpi: str, predictions: pd.DataFrame, figures_dir: Path) -> Path:
    figures_dir.mkdir(parents=True, exist_ok=True)
    output_path = figures_dir / f"forecast_actual_vs_predicted_{kpi}.png"

    figure, axis = plt.subplots(figsize=(10, 4))
    axis.plot(predictions["date"], predictions["actual"], label="Actual", linewidth=1.8)
    axis.plot(predictions["date"], predictions["predicted"], label="Predicted", linewidth=1.8)
    axis.set_title(f"Actual vs Predicted: {kpi}")
    axis.set_xlabel("Date")
    axis.set_ylabel(kpi)
    axis.grid(True, alpha=0.3)
    axis.legend()
    figure.autofmt_xdate()
    figure.tight_layout()
    figure.savefig(output_path, dpi=140)
    plt.close(figure)
    return output_path


def train_models_for_kpi(
    summary: pd.DataFrame,
    target_kpi: str,
    models_dir: Path,
    figures_dir: Path,
    create_plots: bool = True,
) -> tuple[list[dict[str, object]], object]:
    dataset = create_forecasting_dataset(summary, target_kpi)
    train, test = split_time_ordered(dataset)
    feature_columns = get_feature_columns(target_kpi)
    x_train = train[list(feature_columns)]
    y_train = train[target_kpi]
    x_test = test[list(feature_columns)]
    y_test = test[target_kpi]

    metrics: list[dict[str, object]] = []
    fitted_models: dict[str, object] = {}
    test_predictions: dict[str, np.ndarray] = {}
    for model_name, model in build_model_candidates().items():
        model.fit(x_train, y_train)
        predicted = model.predict(x_test)
        model_metrics = evaluate_predictions(y_test, predicted)
        metrics.append(
            {
                "kpi": target_kpi,
                "model_name": model_name,
                **model_metrics,
                "train_rows": len(train),
                "test_rows": len(test),
                "selected_model": False,
            }
        )
        fitted_models[model_name] = model
        test_predictions[model_name] = predicted

    best_metrics = min(metrics, key=lambda row: (float(row["rmse"]), float(row["mae"]), str(row["model_name"])))
    best_metrics["selected_model"] = True
    best_model_name = str(best_metrics["model_name"])
    best_model = fitted_models[best_model_name]

    if create_plots:
        predictions = pd.DataFrame(
            {
                "date": test["date"],
                "actual": y_test,
                "predicted": test_predictions[best_model_name],
            }
        )
        plot_actual_vs_predicted(target_kpi, predictions, figures_dir)

    models_dir.mkdir(parents=True, exist_ok=True)
    artifact = {
        "kpi": target_kpi,
        "model_name": best_model_name,
        "model": best_model,
        "feature_columns": list(feature_columns),
        "training_history": summary.copy(),
        "last_training_date": summary["date"].max(),
    }
    joblib.dump(artifact, models_dir / f"forecasting_{target_kpi}.joblib")
    LOGGER.info("Selected %s for %s", best_model_name, target_kpi)
    return metrics, best_model


def write_model_metrics(metrics: list[dict[str, object]], output_path: Path) -> pd.DataFrame:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_frame = pd.DataFrame(metrics).sort_values(["kpi", "selected_model", "rmse"], ascending=[True, False, True])
    metrics_frame.to_csv(output_path, index=False)
    LOGGER.info("Wrote %s model metric rows to %s", len(metrics_frame), output_path)
    return metrics_frame


def write_model_comparison(baseline_metrics: pd.DataFrame, enhanced_metrics: pd.DataFrame, output_path: Path) -> pd.DataFrame:
    required_columns = {"kpi", "model_name", "mae", "rmse", "r2", "selected_model"}
    missing_columns = sorted(required_columns.difference(baseline_metrics.columns).union(required_columns.difference(enhanced_metrics.columns)))
    if missing_columns:
        raise ForecastingError(f"Cannot compare metrics; missing columns: {', '.join(missing_columns)}")

    baseline = baseline_metrics[list(required_columns)].rename(
        columns={
            "mae": "before_mae",
            "rmse": "before_rmse",
            "r2": "before_r2",
            "selected_model": "before_selected_model",
        }
    )
    enhanced = enhanced_metrics[list(required_columns)].rename(
        columns={
            "mae": "after_mae",
            "rmse": "after_rmse",
            "r2": "after_r2",
            "selected_model": "after_selected_model",
        }
    )
    comparison = baseline.merge(enhanced, on=["kpi", "model_name"], how="outer")
    comparison["mae_delta"] = comparison["after_mae"] - comparison["before_mae"]
    comparison["rmse_delta"] = comparison["after_rmse"] - comparison["before_rmse"]
    comparison["r2_delta"] = comparison["after_r2"] - comparison["before_r2"]
    comparison = comparison.sort_values(["kpi", "after_selected_model", "rmse_delta"], ascending=[True, False, True])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    comparison.to_csv(output_path, index=False)
    LOGGER.info("Wrote model comparison to %s", output_path)
    return comparison


def run_training(
    input_path: Path,
    metrics_path: Path,
    models_dir: Path,
    figures_dir: Path,
    create_plots: bool = True,
    comparison_path: Path | None = Path("outputs/reports/model_comparison.csv"),
) -> pd.DataFrame:
    baseline_metrics = pd.read_csv(metrics_path) if metrics_path.exists() else None
    summary = load_kpi_summary(input_path)
    all_metrics: list[dict[str, object]] = []
    for target_kpi in TARGET_KPIS:
        metrics, _ = train_models_for_kpi(
            summary=summary,
            target_kpi=target_kpi,
            models_dir=models_dir,
            figures_dir=figures_dir,
            create_plots=create_plots,
        )
        all_metrics.extend(metrics)
    enhanced_metrics = write_model_metrics(all_metrics, metrics_path)
    if baseline_metrics is not None and comparison_path is not None:
        write_model_comparison(baseline_metrics, enhanced_metrics, comparison_path)
    return enhanced_metrics


def parse_args(args: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train deterministic KPI forecasting models.")
    parser.add_argument(
        "--input-path",
        type=Path,
        default=Path("outputs/reports/kpi_summary_daily.csv"),
        help="Input daily KPI summary CSV path.",
    )
    parser.add_argument(
        "--metrics-path",
        type=Path,
        default=Path("outputs/reports/model_metrics.csv"),
        help="Output model metrics CSV path.",
    )
    parser.add_argument(
        "--models-dir",
        type=Path,
        default=Path("outputs/models"),
        help="Directory for selected forecasting model artifacts.",
    )
    parser.add_argument(
        "--figures-dir",
        type=Path,
        default=Path("outputs/figures"),
        help="Directory for forecasting plot PNG files.",
    )
    parser.add_argument(
        "--comparison-path",
        type=Path,
        default=Path("outputs/reports/model_comparison.csv"),
        help="Output before/after model comparison CSV path.",
    )
    parser.add_argument("--no-plots", action="store_true", help="Skip writing forecasting plot files.")
    return parser.parse_args(args)


def main(args: Iterable[str] | None = None) -> None:
    configure_logging()
    parsed = parse_args(args)
    run_training(
        input_path=parsed.input_path,
        metrics_path=parsed.metrics_path,
        models_dir=parsed.models_dir,
        figures_dir=parsed.figures_dir,
        create_plots=not parsed.no_plots,
        comparison_path=parsed.comparison_path,
    )


if __name__ == "__main__":
    main()
