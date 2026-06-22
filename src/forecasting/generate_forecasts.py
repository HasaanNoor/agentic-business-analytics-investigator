"""Generate deterministic 7-day KPI forecasts from selected model artifacts."""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Iterable

os.environ.setdefault("MPLCONFIGDIR", str(Path("outputs/.matplotlib")))
os.environ.setdefault("XDG_CACHE_HOME", str(Path("outputs/.cache")))

import joblib
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.forecasting.train_forecasting_models import (
    BASE_FEATURE_COLUMNS,
    FEATURE_COLUMNS,
    SUPPORT_TICKET_CATEGORY_COLUMNS,
    TARGET_KPIS,
    ForecastingError,
)


LOGGER = logging.getLogger(__name__)
DATE_FEATURE_COLUMNS = {"day_of_week", "month", "quarter", "is_weekend"}
SUPPORT_CATEGORY_FEATURE_SUFFIXES = ("_previous_day", "_rolling_avg_3d", "_rolling_avg_7d")


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s - %(message)s")


def load_model_artifact(models_dir: Path, target_kpi: str) -> dict[str, object]:
    artifact_path = models_dir / f"forecasting_{target_kpi}.joblib"
    if not artifact_path.exists():
        raise ForecastingError(f"Missing selected model artifact: {artifact_path}")

    artifact = joblib.load(artifact_path)
    required_keys = {"kpi", "model_name", "model", "feature_columns", "training_history"}
    missing_keys = required_keys.difference(artifact)
    if missing_keys:
        raise ForecastingError(f"Forecasting artifact missing required keys: {', '.join(sorted(missing_keys))}")
    return artifact


def build_support_category_forecast_features(history: pd.DataFrame) -> dict[str, float]:
    if len(history) < 7:
        raise ForecastingError("At least 7 history rows are required to build support ticket category features")

    features: dict[str, float] = {}
    for column in SUPPORT_TICKET_CATEGORY_COLUMNS:
        if column not in history.columns:
            raise ForecastingError(f"Training history missing support ticket category column for forecasting: {column}")
        values = history[column].astype(float)
        features[f"{column}_previous_day"] = float(values.iloc[-1])
        features[f"{column}_rolling_avg_3d"] = float(values.iloc[-3:].mean())
        features[f"{column}_rolling_avg_7d"] = float(values.iloc[-7:].mean())
    return features


def build_next_feature_row(history: pd.DataFrame, target_kpi: str, feature_columns: Iterable[str] | None = None) -> pd.DataFrame:
    selected_columns = list(feature_columns or FEATURE_COLUMNS)
    values = history[target_kpi].astype(float)
    if len(values) < 14:
        raise ForecastingError(f"At least 14 history rows are required to forecast {target_kpi}")
    forecast_date = pd.to_datetime(history["date"], errors="raise").max().normalize() + pd.Timedelta(days=1)

    features = {
        "previous_day_value": values.iloc[-1],
        "rolling_avg_3d": values.iloc[-3:].mean(),
        "rolling_avg_7d": values.iloc[-7:].mean(),
        "rolling_avg_14d": values.iloc[-14:].mean(),
        "lag_7d": values.iloc[-7],
        "lag_14d": values.iloc[-14],
        "day_of_week": forecast_date.dayofweek,
        "month": forecast_date.month,
        "quarter": forecast_date.quarter,
        "is_weekend": int(forecast_date.dayofweek >= 5),
    }
    if target_kpi == "support_ticket_count":
        features.update(build_support_category_forecast_features(history))
    latest_row = history.iloc[-1]
    for column in selected_columns:
        if column in BASE_FEATURE_COLUMNS or column in DATE_FEATURE_COLUMNS:
            continue
        if target_kpi == "support_ticket_count" and column.endswith(SUPPORT_CATEGORY_FEATURE_SUFFIXES):
            continue
        if column not in history.columns:
            raise ForecastingError(f"Training history missing feature column for forecasting: {column}")
        features[column] = float(latest_row[column])
    return pd.DataFrame([{column: features[column] for column in selected_columns}], columns=selected_columns)


def constrain_prediction(target_kpi: str, value: float) -> float:
    constrained = max(0.0, float(value))
    if target_kpi.endswith("_rate"):
        constrained = min(1.0, constrained)
    return round(constrained, 6)


def generate_forecast_for_kpi(artifact: dict[str, object], horizon_days: int = 7) -> pd.DataFrame:
    target_kpi = str(artifact["kpi"])
    model = artifact["model"]
    model_name = str(artifact["model_name"])
    history = artifact["training_history"].copy()
    history["date"] = pd.to_datetime(history["date"], errors="raise").dt.normalize()
    history[target_kpi] = history[target_kpi].astype(float)
    history = history.sort_values("date").reset_index(drop=True)

    forecast_rows: list[dict[str, object]] = []
    feature_columns = list(artifact.get("feature_columns", FEATURE_COLUMNS))
    for step in range(1, horizon_days + 1):
        feature_row = build_next_feature_row(history, target_kpi, feature_columns)
        prediction = constrain_prediction(target_kpi, float(model.predict(feature_row)[0]))
        forecast_date = history["date"].max() + pd.Timedelta(days=1)
        forecast_rows.append(
            {
                "date": forecast_date,
                "kpi": target_kpi,
                "forecast_day": step,
                "prediction": prediction,
                "model_name": model_name,
            }
        )
        next_history_row = history.iloc[-1].copy()
        next_history_row["date"] = forecast_date
        next_history_row[target_kpi] = prediction
        for column in DATE_FEATURE_COLUMNS.intersection(next_history_row.index).intersection(feature_row.columns):
            next_history_row[column] = feature_row.iloc[0][column]
        history = pd.concat(
            [history, pd.DataFrame([next_history_row])],
            ignore_index=True,
        )

    return pd.DataFrame(forecast_rows)


def write_forecasts(forecasts: pd.DataFrame, output_path: Path) -> pd.DataFrame:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    export = forecasts.copy()
    export["date"] = pd.to_datetime(export["date"]).dt.strftime("%Y-%m-%d")
    export.to_csv(output_path, index=False)
    LOGGER.info("Wrote %s forecast rows to %s", len(export), output_path)
    return export


def plot_forecast_extension(artifact: dict[str, object], forecasts: pd.DataFrame, figures_dir: Path) -> Path:
    figures_dir.mkdir(parents=True, exist_ok=True)
    target_kpi = str(artifact["kpi"])
    history = artifact["training_history"].copy()
    history["date"] = pd.to_datetime(history["date"], errors="raise").dt.normalize()
    recent_history = history.sort_values("date").tail(45)
    kpi_forecasts = forecasts[forecasts["kpi"] == target_kpi].copy()

    output_path = figures_dir / f"forecast_extension_{target_kpi}.png"
    figure, axis = plt.subplots(figsize=(10, 4))
    axis.plot(recent_history["date"], recent_history[target_kpi], label="Actual", linewidth=1.8)
    axis.plot(kpi_forecasts["date"], kpi_forecasts["prediction"], label="7-day forecast", linewidth=1.8, marker="o")
    axis.axvline(recent_history["date"].max(), color="black", linestyle="--", linewidth=1.0, alpha=0.6)
    axis.set_title(f"Forecast Extension: {target_kpi}")
    axis.set_xlabel("Date")
    axis.set_ylabel(target_kpi)
    axis.grid(True, alpha=0.3)
    axis.legend()
    figure.autofmt_xdate()
    figure.tight_layout()
    figure.savefig(output_path, dpi=140)
    plt.close(figure)
    return output_path


def run_forecasting(
    models_dir: Path,
    output_path: Path,
    figures_dir: Path,
    horizon_days: int = 7,
    create_plots: bool = True,
) -> pd.DataFrame:
    artifacts = [load_model_artifact(models_dir, target_kpi) for target_kpi in TARGET_KPIS]
    forecasts = pd.concat(
        [generate_forecast_for_kpi(artifact, horizon_days=horizon_days) for artifact in artifacts],
        ignore_index=True,
    )
    forecasts = forecasts.sort_values(["kpi", "forecast_day"]).reset_index(drop=True)
    written = write_forecasts(forecasts, output_path)

    if create_plots:
        plot_frame = forecasts.copy()
        for artifact in artifacts:
            plot_forecast_extension(artifact, plot_frame, figures_dir)

    return written


def parse_args(args: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate deterministic 7-day KPI forecasts.")
    parser.add_argument(
        "--models-dir",
        type=Path,
        default=Path("outputs/models"),
        help="Directory containing selected forecasting model artifacts.",
    )
    parser.add_argument(
        "--output-path",
        type=Path,
        default=Path("outputs/reports/forecast_summary.csv"),
        help="Output forecast summary CSV path.",
    )
    parser.add_argument(
        "--figures-dir",
        type=Path,
        default=Path("outputs/figures"),
        help="Directory for forecast extension plot PNG files.",
    )
    parser.add_argument("--horizon-days", type=int, default=7, help="Number of future days to forecast.")
    parser.add_argument("--no-plots", action="store_true", help="Skip writing forecast extension plot files.")
    return parser.parse_args(args)


def main(args: Iterable[str] | None = None) -> None:
    configure_logging()
    parsed = parse_args(args)
    run_forecasting(
        models_dir=parsed.models_dir,
        output_path=parsed.output_path,
        figures_dir=parsed.figures_dir,
        horizon_days=parsed.horizon_days,
        create_plots=not parsed.no_plots,
    )


if __name__ == "__main__":
    main()
