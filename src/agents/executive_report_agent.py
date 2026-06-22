"""Generate an executive operations report from deterministic analytics outputs."""

from __future__ import annotations

import argparse
import json
import logging
import os
from pathlib import Path
from typing import Iterable

import pandas as pd


LOGGER = logging.getLogger(__name__)

REQUIRED_SECTIONS = [
    "Executive Summary",
    "Key Incidents",
    "Forecast Outlook",
    "Main Business Drivers",
    "Recommended Actions",
    "Limitations",
]


class ExecutiveReportError(RuntimeError):
    """Raised when executive reporting cannot complete."""


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s - %(message)s")


def _read_csv(path: Path, label: str) -> pd.DataFrame:
    if not path.exists():
        raise ExecutiveReportError(f"Missing {label}: {path}")
    frame = pd.read_csv(path)
    if frame.empty:
        raise ExecutiveReportError(f"{label} is empty: {path}")
    return frame


def _read_text(path: Path, label: str) -> str:
    if not path.exists():
        raise ExecutiveReportError(f"Missing {label}: {path}")
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        raise ExecutiveReportError(f"{label} is empty: {path}")
    return text


def _read_investigation_payload(path: Path) -> dict[str, object]:
    if not path.exists():
        raise ExecutiveReportError(f"Missing investigation reports: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or "incidents" not in payload:
        raise ExecutiveReportError(f"Investigation reports missing incidents: {path}")
    return payload


def _as_float(value: object) -> float:
    return round(float(value), 6)


def _incident_rank(incident: dict[str, object]) -> tuple[int, int, int]:
    known_pattern = int(str(incident.get("likely_cause", "")) != "No known deterministic root-cause pattern matched")
    event_count = len(incident.get("anomaly_events", []) or [])
    kpi_count = len(incident.get("affected_kpis", []) or [])
    return known_pattern, event_count, kpi_count


def summarize_incidents(payload: dict[str, object], max_incidents: int = 5) -> list[dict[str, object]]:
    incidents = list(payload.get("incidents", []) or [])
    ranked = sorted(incidents, key=_incident_rank, reverse=True)[:max_incidents]
    summaries: list[dict[str, object]] = []
    for incident in ranked:
        summaries.append(
            {
                "incident_id": incident.get("incident_id"),
                "title": incident.get("title"),
                "date_range": f"{incident.get('incident_start_date')} to {incident.get('incident_end_date')}",
                "main_anomaly_type": incident.get("main_anomaly_type"),
                "related_anomaly_types": incident.get("related_anomaly_types", []),
                "likely_cause": incident.get("likely_cause"),
                "affected_kpis": [
                    {
                        "metric": kpi.get("metric"),
                        "minimum": kpi.get("minimum"),
                        "maximum": kpi.get("maximum"),
                        "average": kpi.get("average"),
                        "event_count": kpi.get("event_count"),
                    }
                    for kpi in incident.get("affected_kpis", []) or []
                ],
                "supporting_evidence": incident.get("supporting_evidence", []),
                "recommended_next_steps": incident.get("recommended_next_steps", []),
            }
        )
    return summaries


def summarize_forecasts(forecasts: pd.DataFrame) -> list[dict[str, object]]:
    required_columns = {"date", "kpi", "forecast_day", "prediction", "model_name"}
    missing = required_columns.difference(forecasts.columns)
    if missing:
        raise ExecutiveReportError(f"forecast summary missing required columns: {', '.join(sorted(missing))}")

    summaries: list[dict[str, object]] = []
    for kpi, group in forecasts.groupby("kpi"):
        ordered = group.sort_values("forecast_day")
        first = ordered.iloc[0]
        last = ordered.iloc[-1]
        delta = float(last["prediction"]) - float(first["prediction"])
        direction = "up" if delta > 0 else "down" if delta < 0 else "flat"
        summaries.append(
            {
                "kpi": str(kpi),
                "model_name": str(last["model_name"]),
                "start_date": str(first["date"]),
                "end_date": str(last["date"]),
                "start_prediction": _as_float(first["prediction"]),
                "end_prediction": _as_float(last["prediction"]),
                "change": _as_float(delta),
                "direction": direction,
            }
        )
    return sorted(summaries, key=lambda row: row["kpi"])


def summarize_shap_drivers(importance: pd.DataFrame, max_features_per_kpi: int = 3) -> list[dict[str, object]]:
    required_columns = {"kpi", "model_name", "feature", "mean_abs_attribution", "rank", "explanation_method"}
    missing = required_columns.difference(importance.columns)
    if missing:
        raise ExecutiveReportError(f"SHAP feature importance missing required columns: {', '.join(sorted(missing))}")

    drivers: list[dict[str, object]] = []
    for kpi, group in importance.sort_values(["kpi", "rank"]).groupby("kpi"):
        top = group.head(max_features_per_kpi)
        drivers.append(
            {
                "kpi": str(kpi),
                "model_name": str(top.iloc[0]["model_name"]),
                "explanation_method": str(top.iloc[0]["explanation_method"]),
                "top_features": [
                    {
                        "feature": str(row["feature"]),
                        "rank": int(row["rank"]),
                        "mean_abs_attribution": _as_float(row["mean_abs_attribution"]),
                    }
                    for row in top.to_dict("records")
                ],
            }
        )
    return drivers


def summarize_model_limitations(metrics: pd.DataFrame) -> list[dict[str, object]]:
    required_columns = {"kpi", "model_name", "mae", "rmse", "r2", "selected_model"}
    missing = required_columns.difference(metrics.columns)
    if missing:
        raise ExecutiveReportError(f"model metrics missing required columns: {', '.join(sorted(missing))}")

    selected = metrics[metrics["selected_model"].astype(str).str.lower() == "true"]
    if selected.empty:
        selected = metrics.sort_values(["kpi", "rmse"]).groupby("kpi", as_index=False).head(1)

    limitations: list[dict[str, object]] = []
    for row in selected.sort_values("kpi").to_dict("records"):
        limitations.append(
            {
                "kpi": str(row["kpi"]),
                "selected_model": str(row["model_name"]),
                "mae": _as_float(row["mae"]),
                "rmse": _as_float(row["rmse"]),
                "r2": _as_float(row["r2"]),
                "limitation": "Forecast metrics measure historical test performance; they do not prove causal relationships or guarantee future accuracy.",
            }
        )
    return limitations


def build_evidence_bundle(
    investigation_payload: dict[str, object],
    investigation_summary: str,
    forecasts: pd.DataFrame,
    forecast_explanations: str,
    shap_importance: pd.DataFrame,
    model_metrics: pd.DataFrame,
) -> dict[str, object]:
    """Build a compact evidence bundle for reporting without exposing raw datasets."""
    return {
        "source_files": [
            "outputs/reports/investigation_reports.json",
            "outputs/reports/investigation_summary.md",
            "outputs/reports/forecast_summary.csv",
            "outputs/reports/forecast_explanations.md",
            "outputs/reports/shap_feature_importance.csv",
            "outputs/reports/model_metrics.csv",
        ],
        "incident_method": investigation_payload.get("method"),
        "incident_count": investigation_payload.get("incident_count"),
        "top_incidents": summarize_incidents(investigation_payload),
        "forecast_outlook": summarize_forecasts(forecasts),
        "shap_drivers": summarize_shap_drivers(shap_importance),
        "model_limitations": summarize_model_limitations(model_metrics),
        "input_report_lengths": {
            "investigation_summary_chars": len(investigation_summary),
            "forecast_explanations_chars": len(forecast_explanations),
        },
    }


def build_prompt(evidence: dict[str, object]) -> list[dict[str, str]]:
    evidence_json = json.dumps(evidence, indent=2)
    system_message = (
        "You write concise executive operations reports. Use only the evidence provided. "
        "Do not infer facts, causal claims, dates, KPIs, incidents, drivers, or recommendations that are not present. "
        "If evidence is incomplete, say so in Limitations."
    )
    user_message = "\n".join(
        [
            "Create a markdown report with exactly these sections:",
            *[f"- {section}" for section in REQUIRED_SECTIONS],
            "",
            "The report must cover top incidents, affected KPIs, likely causes, forecast outlook, SHAP drivers, and model limitations.",
            "Keep recommendations grounded in the deterministic recommended_next_steps and model evidence.",
            "",
            "Evidence bundle:",
            evidence_json,
        ]
    )
    return [{"role": "system", "content": system_message}, {"role": "user", "content": user_message}]


def _extract_responses_text(response: object) -> str:
    output_text = getattr(response, "output_text", None)
    if output_text:
        return str(output_text)
    parts: list[str] = []
    for item in getattr(response, "output", []) or []:
        for content in getattr(item, "content", []) or []:
            text = getattr(content, "text", None)
            if text:
                parts.append(str(text))
    return "\n".join(parts)


def generate_llm_report(prompt: list[dict[str, str]], model: str) -> str:
    try:
        from openai import OpenAI
    except ImportError as error:  # pragma: no cover - dependency is declared for normal installs.
        raise ExecutiveReportError("OpenAI package is not installed") from error

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    if hasattr(client, "responses"):
        response = client.responses.create(model=model, input=prompt)
        return _extract_responses_text(response)

    response = client.chat.completions.create(model=model, messages=prompt)
    return str(response.choices[0].message.content or "")


def _format_kpi_list(kpis: list[dict[str, object]]) -> str:
    if not kpis:
        return "No affected KPI detail was provided."
    return "; ".join(
        f"`{kpi['metric']}` avg {kpi['average']}, range {kpi['minimum']} to {kpi['maximum']}"
        for kpi in kpis
    )


def _format_recommendations(incidents: list[dict[str, object]]) -> list[str]:
    seen: set[str] = set()
    recommendations: list[str] = []
    for incident in incidents:
        for item in incident.get("recommended_next_steps", []) or []:
            text = str(item)
            if text not in seen:
                recommendations.append(text)
                seen.add(text)
    if not recommendations:
        recommendations.append("Review deterministic incident evidence before selecting operational actions.")
    return recommendations[:8]


def generate_fallback_report(evidence: dict[str, object]) -> str:
    incidents = list(evidence.get("top_incidents", []) or [])
    forecasts = list(evidence.get("forecast_outlook", []) or [])
    drivers = list(evidence.get("shap_drivers", []) or [])
    limitations = list(evidence.get("model_limitations", []) or [])
    recommendations = _format_recommendations(incidents)

    lines = [
        "# Executive Operations Report",
        "",
        "## Executive Summary",
        "",
        f"The deterministic pipeline found {evidence.get('incident_count', 0)} grouped incident(s). "
        f"This report summarizes the top {len(incidents)} incident(s), the forecast outlook, model drivers, "
        "and recommended actions from structured pipeline outputs only.",
        "",
        "## Key Incidents",
        "",
    ]

    for incident in incidents:
        lines.extend(
            [
                f"### {incident['incident_id']}: {incident['title']}",
                "",
                f"- Date range: {incident['date_range']}",
                f"- Likely cause: {incident['likely_cause']}",
                f"- Main anomaly: `{incident['main_anomaly_type']}`",
                f"- Affected KPIs: {_format_kpi_list(incident.get('affected_kpis', []))}",
                "- Evidence: " + " ".join(str(item) for item in incident.get("supporting_evidence", []) or []),
                "",
            ]
        )

    lines.extend(["## Forecast Outlook", ""])
    for forecast in forecasts:
        lines.append(
            f"- `{forecast['kpi']}` is forecast {forecast['direction']} from {forecast['start_prediction']} "
            f"on {forecast['start_date']} to {forecast['end_prediction']} on {forecast['end_date']} "
            f"using `{forecast['model_name']}`."
        )

    lines.extend(["", "## Main Business Drivers", ""])
    for driver in drivers:
        features = ", ".join(f"`{item['feature']}`" for item in driver["top_features"])
        lines.append(
            f"- `{driver['kpi']}`: top SHAP drivers are {features} "
            f"({driver['explanation_method']}, `{driver['model_name']}`)."
        )

    lines.extend(["", "## Recommended Actions", ""])
    lines.extend(f"- {item}" for item in recommendations)

    lines.extend(["", "## Limitations", ""])
    lines.extend(
        [
            "- This report does not read raw full datasets and does not add RAG, dashboard, or API behavior.",
            "- The narrative is grounded in deterministic incident, forecast, SHAP, and model-metric outputs.",
            "- SHAP attributions explain model behavior and should not be treated as proof of real-world causality.",
        ]
    )
    for limitation in limitations:
        lines.append(
            f"- `{limitation['kpi']}` uses `{limitation['selected_model']}` with RMSE {limitation['rmse']} "
            f"and R2 {limitation['r2']}; {limitation['limitation']}"
        )

    return "\n".join(lines).strip() + "\n"


def _has_required_sections(report: str) -> bool:
    return all(section in report for section in REQUIRED_SECTIONS)


def run_executive_report(
    investigation_reports_path: Path,
    investigation_summary_path: Path,
    forecast_summary_path: Path,
    forecast_explanations_path: Path,
    shap_feature_importance_path: Path,
    model_metrics_path: Path,
    output_path: Path,
    model: str = "gpt-4o-mini",
) -> str:
    investigation_payload = _read_investigation_payload(investigation_reports_path)
    investigation_summary = _read_text(investigation_summary_path, "investigation summary")
    forecasts = _read_csv(forecast_summary_path, "forecast summary")
    forecast_explanations = _read_text(forecast_explanations_path, "forecast explanations")
    shap_importance = _read_csv(shap_feature_importance_path, "SHAP feature importance")
    model_metrics = _read_csv(model_metrics_path, "model metrics")

    evidence = build_evidence_bundle(
        investigation_payload,
        investigation_summary,
        forecasts,
        forecast_explanations,
        shap_importance,
        model_metrics,
    )

    if os.environ.get("OPENAI_API_KEY"):
        prompt = build_prompt(evidence)
        try:
            report = generate_llm_report(prompt, model=model).strip() + "\n"
            if not _has_required_sections(report):
                LOGGER.warning("LLM report missed required sections; using deterministic fallback.")
                report = generate_fallback_report(evidence)
        except Exception as error:  # noqa: BLE001 - fallback keeps reporting pipeline deterministic.
            LOGGER.warning("OpenAI report generation failed; using deterministic fallback: %s", error)
            report = generate_fallback_report(evidence)
    else:
        LOGGER.info("OPENAI_API_KEY is not set; using deterministic fallback report.")
        report = generate_fallback_report(evidence)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    LOGGER.info("Wrote executive operations report to %s", output_path)
    return report


def parse_args(args: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an executive operations report from deterministic outputs.")
    parser.add_argument("--investigation-reports-path", type=Path, default=Path("outputs/reports/investigation_reports.json"))
    parser.add_argument("--investigation-summary-path", type=Path, default=Path("outputs/reports/investigation_summary.md"))
    parser.add_argument("--forecast-summary-path", type=Path, default=Path("outputs/reports/forecast_summary.csv"))
    parser.add_argument("--forecast-explanations-path", type=Path, default=Path("outputs/reports/forecast_explanations.md"))
    parser.add_argument("--shap-feature-importance-path", type=Path, default=Path("outputs/reports/shap_feature_importance.csv"))
    parser.add_argument("--model-metrics-path", type=Path, default=Path("outputs/reports/model_metrics.csv"))
    parser.add_argument("--output-path", type=Path, default=Path("outputs/reports/executive_operations_report.md"))
    parser.add_argument("--model", default=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"))
    return parser.parse_args(args)


def main(args: Iterable[str] | None = None) -> None:
    configure_logging()
    parsed = parse_args(args)
    run_executive_report(
        investigation_reports_path=parsed.investigation_reports_path,
        investigation_summary_path=parsed.investigation_summary_path,
        forecast_summary_path=parsed.forecast_summary_path,
        forecast_explanations_path=parsed.forecast_explanations_path,
        shap_feature_importance_path=parsed.shap_feature_importance_path,
        model_metrics_path=parsed.model_metrics_path,
        output_path=parsed.output_path,
        model=parsed.model,
    )


if __name__ == "__main__":
    main()
