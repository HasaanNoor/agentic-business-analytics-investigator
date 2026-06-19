"""Explain selected KPI forecasting models with SHAP or deterministic fallbacks."""

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
import numpy as np
import pandas as pd
import shap
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

try:
    from xgboost import XGBRegressor
except ImportError:  # pragma: no cover - xgboost is a project dependency.
    XGBRegressor = ()  # type: ignore[assignment]

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.forecasting.generate_forecasts import build_next_feature_row, constrain_prediction
from src.forecasting.train_forecasting_models import FEATURE_COLUMNS, TARGET_KPIS, ForecastingError, create_forecasting_dataset


LOGGER = logging.getLogger(__name__)
TREE_MODEL_TYPES = (RandomForestRegressor, XGBRegressor)


class ExplainabilityError(RuntimeError):
    """Raised when required explainability inputs are missing or invalid."""


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s - %(message)s")


def load_required_csv(path: Path, label: str) -> pd.DataFrame:
    if not path.exists():
        raise ExplainabilityError(f"Missing {label}: {path}")
    frame = pd.read_csv(path)
    if frame.empty:
        raise ExplainabilityError(f"{label} is empty: {path}")
    return frame


def load_model_artifact(models_dir: Path, target_kpi: str) -> dict[str, object]:
    artifact_path = models_dir / f"forecasting_{target_kpi}.joblib"
    if not artifact_path.exists():
        raise ExplainabilityError(f"Missing selected model artifact: {artifact_path}")

    artifact = joblib.load(artifact_path)
    required_keys = {"kpi", "model_name", "model", "feature_columns", "training_history"}
    missing_keys = required_keys.difference(artifact)
    if missing_keys:
        raise ExplainabilityError(f"Forecasting artifact missing required keys: {', '.join(sorted(missing_keys))}")
    return artifact


def validate_selected_model(metrics: pd.DataFrame, target_kpi: str, model_name: str) -> None:
    required_columns = {"kpi", "model_name", "selected_model"}
    missing_columns = required_columns.difference(metrics.columns)
    if missing_columns:
        raise ExplainabilityError(f"model metrics missing required columns: {', '.join(sorted(missing_columns))}")

    selected = metrics[(metrics["kpi"] == target_kpi) & (metrics["selected_model"].astype(str).str.lower() == "true")]
    if selected.empty:
        LOGGER.warning("No selected model row found in metrics for %s; using artifact model %s", target_kpi, model_name)
        return

    selected_name = str(selected.iloc[0]["model_name"])
    if selected_name != model_name:
        LOGGER.warning("Metrics selected %s for %s, but artifact contains %s", selected_name, target_kpi, model_name)


def prepare_training_features(artifact: dict[str, object]) -> pd.DataFrame:
    target_kpi = str(artifact["kpi"])
    feature_columns = list(artifact.get("feature_columns", FEATURE_COLUMNS))
    history = artifact["training_history"].copy()
    history["date"] = pd.to_datetime(history["date"], errors="raise").dt.normalize()
    dataset = create_forecasting_dataset(history, target_kpi)
    return dataset[feature_columns].astype(float).reset_index(drop=True)


def build_forecast_feature_rows(artifact: dict[str, object], forecast_rows: pd.DataFrame) -> pd.DataFrame:
    target_kpi = str(artifact["kpi"])
    model = artifact["model"]
    model_name = str(artifact["model_name"])
    feature_columns = list(artifact.get("feature_columns", FEATURE_COLUMNS))
    history = artifact["training_history"].copy()
    history["date"] = pd.to_datetime(history["date"], errors="raise").dt.normalize()
    history[target_kpi] = history[target_kpi].astype(float)
    history = history.sort_values("date").reset_index(drop=True)

    kpi_forecasts = forecast_rows[forecast_rows["kpi"] == target_kpi].copy()
    if kpi_forecasts.empty:
        raise ExplainabilityError(f"forecast summary has no rows for {target_kpi}")
    kpi_forecasts["date"] = pd.to_datetime(kpi_forecasts["date"], errors="raise").dt.normalize()
    kpi_forecasts = kpi_forecasts.sort_values(["date", "forecast_day"]).reset_index(drop=True)

    explanation_rows: list[dict[str, object]] = []
    for _, forecast in kpi_forecasts.iterrows():
        feature_row = build_next_feature_row(history, target_kpi, feature_columns)
        prediction = constrain_prediction(target_kpi, float(model.predict(feature_row[feature_columns])[0]))
        explanation_row = {
            "date": forecast["date"],
            "kpi": target_kpi,
            "forecast_day": int(forecast["forecast_day"]),
            "prediction": float(forecast["prediction"]),
            "replayed_prediction": prediction,
            "model_name": model_name,
        }
        explanation_row.update(feature_row.iloc[0].to_dict())
        explanation_rows.append(explanation_row)
        next_history_row = history.iloc[-1].copy()
        next_history_row["date"] = forecast["date"]
        next_history_row[target_kpi] = float(forecast["prediction"])
        history = pd.concat(
            [history, pd.DataFrame([next_history_row])],
            ignore_index=True,
        )

    return pd.DataFrame(explanation_rows)


def explain_with_shap(model: object, model_name: str, background: pd.DataFrame, explain_rows: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, str]:
    if isinstance(model, TREE_MODEL_TYPES):
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(background)
        prediction_values = explainer.shap_values(explain_rows)
        return np.asarray(shap_values), np.asarray(prediction_values), "SHAP TreeExplainer"

    if isinstance(model, LinearRegression):
        masker = shap.maskers.Independent(background)
        explainer = shap.LinearExplainer(model, masker)
        shap_values = explainer.shap_values(background)
        prediction_values = explainer.shap_values(explain_rows)
        return np.asarray(shap_values), np.asarray(prediction_values), "SHAP LinearExplainer"

    raise ExplainabilityError(f"SHAP explainer is not configured for model type {type(model).__name__} ({model_name})")


def coefficient_fallback(model: object, background: pd.DataFrame, explain_rows: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, str]:
    if not hasattr(model, "coef_"):
        raise ExplainabilityError(f"Model type {type(model).__name__} has no coefficients for fallback explanation")

    coefficients = np.asarray(model.coef_, dtype=float).reshape(-1)
    if len(coefficients) != len(background.columns):
        raise ExplainabilityError("Coefficient count does not match feature count")

    feature_means = background.mean(axis=0).to_numpy(dtype=float)
    background_values = background.to_numpy(dtype=float)
    explain_values = explain_rows.to_numpy(dtype=float)
    shap_like_values = (background_values - feature_means) * coefficients
    prediction_values = (explain_values - feature_means) * coefficients
    return shap_like_values, prediction_values, "coefficient fallback"


def model_importance_fallback(model: object, background: pd.DataFrame, explain_rows: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, str]:
    if isinstance(model, LinearRegression) or hasattr(model, "coef_"):
        return coefficient_fallback(model, background, explain_rows)

    if hasattr(model, "feature_importances_"):
        importances = np.asarray(model.feature_importances_, dtype=float).reshape(-1)
        centered_background = background.to_numpy(dtype=float) - background.mean(axis=0).to_numpy(dtype=float)
        centered_explain = explain_rows.to_numpy(dtype=float) - background.mean(axis=0).to_numpy(dtype=float)
        return centered_background * importances, centered_explain * importances, "model-native importance fallback"

    baseline_prediction = float(np.mean(model.predict(background)))
    prediction_values = np.repeat((model.predict(explain_rows).reshape(-1, 1) - baseline_prediction) / len(background.columns), len(background.columns), axis=1)
    background_values = np.zeros((len(background), len(background.columns)))
    return background_values, prediction_values, "prediction-difference fallback"


def create_summary_plot(kpi: str, shap_values: np.ndarray, features: pd.DataFrame, figures_dir: Path) -> Path:
    figures_dir.mkdir(parents=True, exist_ok=True)
    output_path = figures_dir / f"shap_summary_{kpi}.png"
    plt.figure()
    shap.summary_plot(shap_values, features, show=False, max_display=len(features.columns))
    plt.tight_layout()
    plt.savefig(output_path, dpi=140, bbox_inches="tight")
    plt.close()
    return output_path


def build_importance_rows(kpi: str, model_name: str, explanation_method: str, shap_values: np.ndarray, feature_columns: list[str]) -> list[dict[str, object]]:
    mean_abs = np.abs(shap_values).mean(axis=0)
    rows = []
    for rank, feature_index in enumerate(np.argsort(mean_abs)[::-1], start=1):
        rows.append(
            {
                "kpi": kpi,
                "model_name": model_name,
                "feature": feature_columns[feature_index],
                "mean_abs_attribution": round(float(mean_abs[feature_index]), 6),
                "rank": rank,
                "explanation_method": explanation_method,
            }
        )
    return rows


def describe_prediction_influence(prediction_values: np.ndarray, latest_features: pd.Series) -> list[str]:
    contributions = prediction_values.reshape(-1)
    ordered_indices = np.argsort(np.abs(contributions))[::-1]
    descriptions: list[str] = []
    for feature_index in ordered_indices[:3]:
        feature_name = str(latest_features.index[feature_index])
        contribution = float(contributions[feature_index])
        direction = "increased" if contribution >= 0 else "decreased"
        descriptions.append(
            f"- `{feature_name}` {direction} the forecast by about {abs(contribution):.4f} model units "
            f"(feature value: {float(latest_features.iloc[feature_index]):.4f})."
        )
    return descriptions


def explain_kpi(
    artifact: dict[str, object],
    metrics: pd.DataFrame,
    forecasts: pd.DataFrame,
    figures_dir: Path,
) -> tuple[list[dict[str, object]], str]:
    target_kpi = str(artifact["kpi"])
    model_name = str(artifact["model_name"])
    model = artifact["model"]
    feature_columns = list(artifact.get("feature_columns", FEATURE_COLUMNS))
    validate_selected_model(metrics, target_kpi, model_name)

    background = prepare_training_features(artifact)
    forecast_features = build_forecast_feature_rows(artifact, forecasts)
    latest_forecast = forecast_features.sort_values(["date", "forecast_day"]).iloc[-1]
    latest_features = latest_forecast[feature_columns].astype(float)
    latest_feature_frame = pd.DataFrame([latest_features.to_dict()], columns=feature_columns)

    limitation = ""
    try:
        shap_values, prediction_values, explanation_method = explain_with_shap(model, model_name, background, latest_feature_frame)
    except Exception as error:  # noqa: BLE001 - report graceful model-specific fallback.
        LOGGER.warning("SHAP failed for %s (%s); using fallback: %s", target_kpi, model_name, error)
        shap_values, prediction_values, explanation_method = model_importance_fallback(model, background, latest_feature_frame)
        limitation = f"SHAP could not explain this model cleanly, so the report uses {explanation_method}: {error}"

    plot_path: Path | None = None
    if explanation_method.startswith("SHAP"):
        try:
            plot_path = create_summary_plot(target_kpi, shap_values, background, figures_dir)
        except Exception as error:  # noqa: BLE001 - plots are useful but should not block reports.
            limitation = f"SHAP values were computed, but the summary plot could not be created: {error}"
    else:
        plot_path = create_summary_plot(target_kpi, shap_values, background, figures_dir)

    importance_rows = build_importance_rows(target_kpi, model_name, explanation_method, shap_values, feature_columns)
    top_features = importance_rows[:3]
    top_feature_text = ", ".join(f"`{row['feature']}`" for row in top_features)
    influence_lines = describe_prediction_influence(prediction_values, latest_features)
    forecast_date = pd.to_datetime(latest_forecast["date"]).strftime("%Y-%m-%d")
    forecast_value = float(latest_forecast["prediction"])
    plot_text = f"- SHAP summary plot: `{plot_path}`" if plot_path else "- SHAP summary plot: not available."
    limitation_text = limitation or "SHAP attributions explain model behavior, not guaranteed real-world causality."

    report = "\n".join(
        [
            f"### {target_kpi}",
            "",
            f"- Predicted KPI: `{target_kpi}`",
            f"- Selected model: `{model_name}`",
            f"- Explanation method: {explanation_method}",
            f"- Most recent forecast explained: {forecast_date}, forecast value `{forecast_value:.6f}`",
            f"- Features that mattered most: {top_feature_text}",
            plot_text,
            "",
            "Prediction-level influence:",
            *influence_lines,
            "",
            f"Limitations: {limitation_text}",
            "",
        ]
    )
    return importance_rows, report


def write_feature_importance(rows: list[dict[str, object]], output_path: Path) -> pd.DataFrame:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    frame = pd.DataFrame(rows)
    if frame.empty:
        raise ExplainabilityError("No feature importance rows were generated")
    frame = frame.sort_values(["kpi", "rank"]).reset_index(drop=True)
    frame.to_csv(output_path, index=False)
    LOGGER.info("Wrote %s feature importance rows to %s", len(frame), output_path)
    return frame


def write_markdown_report(sections: list[str], output_path: Path) -> Path:
    if not sections:
        raise ExplainabilityError("No forecast explanation sections were generated")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    content = "\n".join(
        [
            "# Forecast Explainability Report",
            "",
            "This report explains the selected deterministic forecasting models using SHAP where supported. "
            "Fallback explanations are used only when SHAP cannot explain a model cleanly.",
            "",
            *sections,
        ]
    )
    if not content.strip():
        raise ExplainabilityError("Forecast explanation report is empty")
    output_path.write_text(content, encoding="utf-8")
    LOGGER.info("Wrote forecast explanations to %s", output_path)
    return output_path


def run_explainability(
    models_dir: Path,
    metrics_path: Path,
    forecast_path: Path,
    importance_path: Path,
    report_path: Path,
    figures_dir: Path,
) -> pd.DataFrame:
    metrics = load_required_csv(metrics_path, "model metrics")
    forecasts = load_required_csv(forecast_path, "forecast summary")
    if "kpi" not in forecasts.columns:
        raise ExplainabilityError("forecast summary missing required column: kpi")

    all_importance_rows: list[dict[str, object]] = []
    report_sections: list[str] = []
    for target_kpi in TARGET_KPIS:
        artifact = load_model_artifact(models_dir, target_kpi)
        importance_rows, report_section = explain_kpi(artifact, metrics, forecasts, figures_dir)
        all_importance_rows.extend(importance_rows)
        report_sections.append(report_section)

    write_markdown_report(report_sections, report_path)
    return write_feature_importance(all_importance_rows, importance_path)


def parse_args(args: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Explain selected KPI forecasting models with SHAP.")
    parser.add_argument("--models-dir", type=Path, default=Path("outputs/models"), help="Directory containing selected forecasting model artifacts.")
    parser.add_argument("--metrics-path", type=Path, default=Path("outputs/reports/model_metrics.csv"), help="Input model metrics CSV path.")
    parser.add_argument("--forecast-path", type=Path, default=Path("outputs/reports/forecast_summary.csv"), help="Input forecast summary CSV path.")
    parser.add_argument(
        "--importance-path",
        type=Path,
        default=Path("outputs/reports/shap_feature_importance.csv"),
        help="Output feature importance CSV path.",
    )
    parser.add_argument(
        "--report-path",
        type=Path,
        default=Path("outputs/reports/forecast_explanations.md"),
        help="Output markdown explanation report path.",
    )
    parser.add_argument("--figures-dir", type=Path, default=Path("outputs/figures"), help="Directory for SHAP summary plots.")
    return parser.parse_args(args)


def main(args: Iterable[str] | None = None) -> None:
    configure_logging()
    parsed = parse_args(args)
    run_explainability(
        models_dir=parsed.models_dir,
        metrics_path=parsed.metrics_path,
        forecast_path=parsed.forecast_path,
        importance_path=parsed.importance_path,
        report_path=parsed.report_path,
        figures_dir=parsed.figures_dir,
    )


if __name__ == "__main__":
    main()
