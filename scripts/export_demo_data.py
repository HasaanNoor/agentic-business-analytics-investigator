"""Export deterministic static demo fixtures for the frontend portfolio build."""

from __future__ import annotations

import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"
DEMO_DIR = PROJECT_ROOT / "frontend" / "public" / "demo-data"

KPI_SUMMARY_PATH = REPORTS_DIR / "kpi_summary_daily.csv"
INCIDENT_REPORTS_PATH = REPORTS_DIR / "multi_agent_investigation_reports.json"
FORECAST_SUMMARY_PATH = REPORTS_DIR / "forecast_summary.csv"
SHAP_FEATURE_IMPORTANCE_PATH = REPORTS_DIR / "shap_feature_importance.csv"
ACTIONABLE_REPORT_PATH = REPORTS_DIR / "executive_operations_report.md"

SCHEMA_VERSION = "1.0.0"
DATASET_NAME = "Northstar Commerce deterministic demo dataset"
DEMONSTRATION_LABEL = "Portfolio Demo · Pre-generated sample dataset"


def require_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Required output is missing: {path}. Run the local deterministic pipeline first.")


def read_csv(path: Path) -> list[dict[str, Any]]:
    require_file(path)
    with path.open(newline="", encoding="utf-8") as handle:
        return [normalize_record(row) for row in csv.DictReader(handle)]


def normalize_record(record: dict[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for key, value in record.items():
        if value == "":
            normalized[key] = None
            continue
        if isinstance(value, str):
            try:
                number = float(value)
            except ValueError:
                normalized[key] = value
                continue
            normalized[key] = int(number) if number.is_integer() else number
        else:
            normalized[key] = value
    return normalized


def read_json(path: Path) -> dict[str, Any]:
    require_file(path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object in {path}")
    return payload


def write_json(name: str, payload: Any) -> None:
    DEMO_DIR.mkdir(parents=True, exist_ok=True)
    (DEMO_DIR / name).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def incident_start(incident: dict[str, Any]) -> str:
    date_range = incident.get("date_range")
    if isinstance(date_range, dict):
        return str(date_range.get("start") or "")
    return str(incident.get("incident_start_date") or "")


def representative_incidents(incidents: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    seen_types: set[str] = set()
    for incident in sorted(incidents, key=lambda item: (item.get("incident_severity") != "critical", incident_start(item))):
        incident_type = str(incident.get("main_anomaly_type") or "unknown")
        if incident_type not in seen_types:
            selected.append(incident)
            seen_types.add(incident_type)
        if len(selected) >= 12:
            break
    return sorted(selected, key=incident_start)


def build_rag_fixture(incidents: list[dict[str, Any]]) -> dict[str, Any]:
    source = next(
        (
            incident
            for incident in incidents
            if incident.get("retrieved_incidents")
            or any(isinstance(finding, dict) and finding.get("historical_incident_context") for finding in incident.get("agent_findings", []))
        ),
        incidents[0],
    )
    retrieved = list(source.get("retrieved_incidents") or [])
    if not retrieved:
        for finding in source.get("agent_findings", []):
            if isinstance(finding, dict):
                retrieved.extend(finding.get("historical_incident_context") or [])
            if len(retrieved) >= 3:
                break
    results = []
    for item in retrieved[:3]:
        metadata = item.get("metadata") if isinstance(item.get("metadata"), dict) else {}
        results.append(
            {
                "similarity_score": item.get("similarity_score"),
                "metadata": {
                    "incident_id": item.get("incident_id") or metadata.get("incident_id"),
                    "incident_type": item.get("incident_type") or metadata.get("incident_type"),
                    "summary": item.get("summary") or metadata.get("summary"),
                    "root_cause": item.get("root_cause") or metadata.get("root_cause"),
                    "resolution": metadata.get("resolution") or "Historical resolution details are available in the source incident record.",
                    "outcome": metadata.get("outcome") or "Pre-generated deterministic comparison.",
                    "recommendations": item.get("recommendations") or metadata.get("recommendations") or [],
                    "severity": metadata.get("severity") or source.get("incident_severity"),
                    "region": metadata.get("region") or source.get("affected_region"),
                },
            }
        )
    return {"query": "checkout failures after deployment", "count": len(results), "results": results}


def main() -> None:
    kpi_rows = read_csv(KPI_SUMMARY_PATH)
    forecast_rows = read_csv(FORECAST_SUMMARY_PATH)
    explanation_rows = read_csv(SHAP_FEATURE_IMPORTANCE_PATH)
    incident_payload = read_json(INCIDENT_REPORTS_PATH)
    report_markdown = ACTIONABLE_REPORT_PATH.read_text(encoding="utf-8") if ACTIONABLE_REPORT_PATH.exists() else ""

    incidents = incident_payload.get("incidents")
    if not isinstance(incidents, list) or not incidents:
        raise ValueError(f"No incidents found in {INCIDENT_REPORTS_PATH}")

    demo_incidents = representative_incidents([incident for incident in incidents if isinstance(incident, dict)])
    demo_kpis = kpi_rows[-180:]
    date_range = {"start": str(demo_kpis[0]["date"]), "end": str(demo_kpis[-1]["date"])}
    generated_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": generated_at,
        "dataset_name": DATASET_NAME,
        "demonstration_label": DEMONSTRATION_LABEL,
        "date_range": date_range,
        "execution_mode": str(incident_payload.get("execution_mode") or "deterministic"),
        "source_descriptions": [
            "KPI rows exported from outputs/reports/kpi_summary_daily.csv.",
            "Incidents exported from outputs/reports/multi_agent_investigation_reports.json.",
            "Forecasts exported from outputs/reports/forecast_summary.csv.",
            "Explainability rows exported from outputs/reports/shap_feature_importance.csv.",
            "Actionable report exported from outputs/reports/executive_operations_report.md.",
        ],
    }

    llm_status = {
        "enabled": False,
        "configured": False,
        "selected_model": None,
        "agent_mode": "deterministic",
        "fallback_enabled": True,
        "configuration_error": None,
    }
    health = {
        "status": "ready",
        "project": "Agentic Business Analytics Investigator",
        "read_only": True,
        "api": {"status": "static-demo"},
        "database": {"configured": False, "available": False, "error": "Static demo mode does not connect to PostgreSQL."},
        "llm": llm_status,
        "file_fallback": {"available": True, "missing_outputs": []},
        "ready": True,
        "files": {
            "kpis": {"path": "demo-data/kpis.json", "exists": True},
            "incidents": {"path": "demo-data/incidents.json", "exists": True},
            "forecasts": {"path": "demo-data/forecasts.json", "exists": True},
            "explanations": {"path": "demo-data/explanations.json", "exists": True},
            "actionable_report": {"path": "demo-data/actionable_report.json", "exists": True},
            "rag_search": {"path": "demo-data/rag_search.json", "exists": True},
        },
        "missing_outputs": [],
    }

    write_json("manifest.json", manifest)
    write_json("health.json", health)
    write_json("llm_status.json", llm_status)
    write_json("kpis.json", {"count": len(demo_kpis), "rows": demo_kpis})
    write_json("incidents.json", {"count": len(demo_incidents), "incidents": demo_incidents})
    write_json("forecasts.json", {"count": len(forecast_rows), "rows": forecast_rows})
    write_json("explanations.json", {"count": len(explanation_rows), "rows": explanation_rows})
    write_json("actionable_report.json", {"format": "markdown", "content": report_markdown})
    write_json("rag_search.json", build_rag_fixture(demo_incidents))
    print(f"Wrote static demo fixtures to {DEMO_DIR.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
