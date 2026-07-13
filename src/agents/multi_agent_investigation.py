"""Run deterministic multi-agent investigation over incident reports."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import pandas as pd

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.agents.coordinator_agent import build_final_reports
from src.agents.llm_coordinator_agent import coordinate_incident_report_llm
from src.agents.llm_logistics_agent import analyze_logistics_llm
from src.agents.llm_platform_agent import analyze_platform_llm
from src.agents.llm_revenue_agent import analyze_revenue_llm
from src.agents.llm_support_agent import analyze_support_llm
from src.agents.logistics_agent import analyze_logistics
from src.agents.platform_agent import analyze_platform
from src.agents.revenue_agent import analyze_revenue
from src.agents.support_agent import analyze_support
from src.llm.config import LLMConfig, load_agent_mode, load_fallback_enabled, load_llm_config
from src.llm.errors import LLMConfigurationError, LLMError
from src.llm.schemas import SCHEMA_VERSION
from src.rag.retrieve_incidents import (
    IncidentRetrievalError,
    load_embedding_model,
    load_knowledge_base,
    retrieve_similar_incidents,
)


LOGGER = logging.getLogger(__name__)


class MultiAgentInvestigationError(RuntimeError):
    """Raised when the deterministic multi-agent investigation cannot run."""


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s - %(message)s")


def _read_csv(path: Path, label: str) -> pd.DataFrame:
    if not path.exists():
        raise MultiAgentInvestigationError(f"Missing {label}: {path}")
    frame = pd.read_csv(path)
    if frame.empty:
        raise MultiAgentInvestigationError(f"{label} is empty: {path}")
    return frame


def _read_investigation_reports(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        raise MultiAgentInvestigationError(f"Missing investigation reports: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    incidents = payload.get("incidents") if isinstance(payload, dict) else None
    if not isinstance(incidents, list):
        raise MultiAgentInvestigationError(f"Investigation reports missing incidents list: {path}")
    return incidents


def load_inputs(
    investigation_path: Path,
    kpi_path: Path,
    deployment_path: Path,
    forecast_path: Path,
    shap_path: Path,
) -> tuple[list[dict[str, object]], pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    incidents = _read_investigation_reports(investigation_path)
    kpis = _read_csv(kpi_path, "KPI summary")
    deployments = _read_csv(deployment_path, "deployment events")
    forecasts = _read_csv(forecast_path, "forecast summary")
    shap_importance = _read_csv(shap_path, "SHAP feature importance")

    required_kpi_columns = {"date"}
    missing_kpi_columns = required_kpi_columns - set(kpis.columns)
    if missing_kpi_columns:
        raise MultiAgentInvestigationError(f"KPI summary missing columns: {', '.join(sorted(missing_kpi_columns))}")
    if "timestamp" not in deployments.columns:
        raise MultiAgentInvestigationError("Deployment events missing timestamp column")

    kpis["date"] = pd.to_datetime(kpis["date"], errors="raise").dt.normalize()
    deployments["timestamp"] = pd.to_datetime(deployments["timestamp"], errors="raise")
    return incidents, kpis.sort_values("date"), deployments.sort_values("timestamp"), forecasts, shap_importance


def run_agent_reviews(
    incidents: list[dict[str, object]],
    kpis: pd.DataFrame,
    deployments: pd.DataFrame,
    retrieved_by_incident: dict[str, list[dict[str, object]]] | None = None,
) -> dict[str, list[dict[str, object]]]:
    findings_by_incident: dict[str, list[dict[str, object]]] = {}
    for incident in incidents:
        incident_id = str(incident.get("incident_id"))
        retrieved_incidents = (retrieved_by_incident or {}).get(incident_id, [])
        findings_by_incident[incident_id] = [
            analyze_revenue(incident, kpis, retrieved_incidents),
            analyze_support(incident, kpis, retrieved_incidents),
            analyze_logistics(incident, kpis, retrieved_incidents),
            analyze_platform(incident, kpis, deployments, retrieved_incidents),
        ]
    return findings_by_incident


def _provenance(
    execution_mode: str,
    model_name: str | None = None,
    fallback_used: bool = False,
    fallback_reason: str | None = None,
    evidence_sources: list[str] | None = None,
    retrieved_incident_ids: list[str] | None = None,
    prompt_version: str | None = None,
) -> dict[str, Any]:
    return {
        "execution_mode": execution_mode,
        "model_name": model_name,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "fallback_used": fallback_used,
        "fallback_reason": fallback_reason,
        "evidence_sources": evidence_sources or ["KPI summary", "forecast summary", "SHAP explanations", "retrieved historical incidents"],
        "retrieved_incident_ids": retrieved_incident_ids or [],
        "prompt_version": prompt_version,
        "schema_version": SCHEMA_VERSION,
    }


def _retrieved_ids(retrieved_incidents: list[dict[str, Any]] | None) -> list[str]:
    ids: list[str] = []
    for item in retrieved_incidents or []:
        metadata = item.get("metadata", {}) if isinstance(item, dict) else {}
        if isinstance(metadata, dict) and metadata.get("incident_id"):
            ids.append(str(metadata["incident_id"]))
    return ids


def _apply_report_provenance(
    reports: list[dict[str, Any]],
    execution_mode: str,
    fallback_used: bool = False,
    fallback_reason: str | None = None,
    model_name: str | None = None,
    retrieved_by_incident: dict[str, list[dict[str, Any]]] | None = None,
) -> list[dict[str, Any]]:
    for report in reports:
        incident_id = str(report.get("incident_id"))
        provenance = _provenance(
            execution_mode=execution_mode,
            model_name=model_name,
            fallback_used=fallback_used,
            fallback_reason=fallback_reason,
            retrieved_incident_ids=_retrieved_ids((retrieved_by_incident or {}).get(incident_id, [])),
        )
        report["provenance"] = provenance
        report.update(provenance)
        for finding in report.get("agent_findings", []) or []:
            if isinstance(finding, dict) and "provenance" not in finding:
                finding["provenance"] = provenance
    return reports


def run_llm_agent_reviews(
    incidents: list[dict[str, Any]],
    kpis: pd.DataFrame,
    deployments: pd.DataFrame,
    forecasts: pd.DataFrame,
    shap_importance: pd.DataFrame,
    config: LLMConfig,
    retrieved_by_incident: dict[str, list[dict[str, Any]]] | None = None,
    llm_client: object | None = None,
) -> dict[str, list[dict[str, Any]]]:
    findings_by_incident: dict[str, list[dict[str, Any]]] = {}
    for incident in incidents:
        incident_id = str(incident.get("incident_id"))
        retrieved_incidents = (retrieved_by_incident or {}).get(incident_id, [])
        findings_by_incident[incident_id] = [
            analyze_revenue_llm(incident, kpis, forecasts, shap_importance, config, llm_client, retrieved_incidents),
            analyze_support_llm(incident, kpis, forecasts, shap_importance, config, llm_client, retrieved_incidents),
            analyze_logistics_llm(incident, kpis, forecasts, shap_importance, config, llm_client, retrieved_incidents),
            analyze_platform_llm(incident, kpis, deployments, forecasts, shap_importance, config, llm_client, retrieved_incidents),
        ]
    return findings_by_incident


def build_llm_final_reports(
    incidents: list[dict[str, Any]],
    findings_by_incident: dict[str, list[dict[str, Any]]],
    kpis: pd.DataFrame,
    forecasts: pd.DataFrame,
    shap_importance: pd.DataFrame,
    config: LLMConfig,
    retrieved_by_incident: dict[str, list[dict[str, Any]]] | None = None,
    llm_client: object | None = None,
) -> list[dict[str, Any]]:
    reports: list[dict[str, Any]] = []
    for incident in incidents:
        incident_id = str(incident.get("incident_id"))
        reports.append(
            coordinate_incident_report_llm(
                incident=incident,
                findings=findings_by_incident.get(incident_id, []),
                forecasts=forecasts,
                shap_importance=shap_importance,
                kpis=kpis,
                config=config,
                client=llm_client,
                retrieved_incidents=(retrieved_by_incident or {}).get(incident_id, []),
            )
        )
    return reports


def _deterministic_reports(
    incidents: list[dict[str, Any]],
    kpis: pd.DataFrame,
    deployments: pd.DataFrame,
    forecasts: pd.DataFrame,
    shap_importance: pd.DataFrame,
    retrieved_by_incident: dict[str, list[dict[str, Any]]] | None,
    fallback_used: bool = False,
    fallback_reason: str | None = None,
) -> list[dict[str, Any]]:
    findings_by_incident = run_agent_reviews(incidents, kpis, deployments, retrieved_by_incident)
    reports = build_final_reports(
        incidents=incidents,
        findings_by_incident=findings_by_incident,
        forecasts=forecasts,
        shap_importance=shap_importance,
        retrieved_by_incident=retrieved_by_incident,
    )
    return _apply_report_provenance(
        reports,
        execution_mode="deterministic",
        fallback_used=fallback_used,
        fallback_reason=fallback_reason,
        retrieved_by_incident=retrieved_by_incident,
    )


def retrieve_context_for_incidents(
    incidents: list[dict[str, object]],
    knowledge_base_path: Path,
    top_k: int = 3,
) -> dict[str, list[dict[str, object]]]:
    if not knowledge_base_path.exists():
        LOGGER.warning("Skipping historical retrieval because knowledge base is missing: %s", knowledge_base_path)
        return {}
    knowledge_base = load_knowledge_base(knowledge_base_path)
    model = load_embedding_model(str(knowledge_base.get("model_name")), local_files_only=True)
    retrieved_by_incident: dict[str, list[dict[str, object]]] = {}
    for incident in incidents:
        incident_id = str(incident.get("incident_id"))
        try:
            retrieved_by_incident[incident_id] = retrieve_similar_incidents(
                current_incident=incident,
                knowledge_base_path=knowledge_base_path,
                top_k=top_k,
                model=model,
            )
        except IncidentRetrievalError as exc:
            LOGGER.warning("Skipping historical retrieval for %s: %s", incident_id, exc)
            retrieved_by_incident[incident_id] = []
    return retrieved_by_incident


def write_json_report(reports: list[dict[str, object]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    mode = reports[0].get("execution_mode", "deterministic") if reports else "deterministic"
    payload = {
        "method": "Optional LLM multi-agent investigation with deterministic fallback" if mode == "llm" else "Deterministic multi-agent investigation rules",
        "agent_count": 5,
        "incident_count": len(reports),
        "execution_mode": mode,
        "fallback_used": any(bool(report.get("fallback_used")) for report in reports),
        "incidents": reports,
    }
    output_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    LOGGER.info("Wrote %s multi-agent incident reports to %s", len(reports), output_path)


def write_markdown_summary(reports: list[dict[str, object]], output_path: Path) -> None:
    lines = [
        "# Multi-Agent Investigation Summary",
        "",
        "Generated by specialist agents with explicit provenance. The deterministic workflow remains available as fallback.",
        f"Total incidents: **{len(reports)}**",
        "",
    ]
    for report in reports:
        provenance = report.get("provenance", {}) if isinstance(report.get("provenance"), dict) else {}
        model_name = provenance.get("model_name") or "not used"
        fallback_text = "Yes" if provenance.get("fallback_used") else "No"
        historical_ids = ", ".join(provenance.get("retrieved_incident_ids", []) or []) or "none"
        evidence_sources = ", ".join(provenance.get("evidence_sources", []) or []) or "not recorded"
        lines.extend(
            [
                f"## {report['incident_id']}: {report['incident_title']}",
                "",
                f"- **Execution mode:** {provenance.get('execution_mode', report.get('execution_mode', 'deterministic'))}",
                f"- **Model:** {model_name}",
                f"- **Fallback used:** {fallback_text}",
                f"- **Fallback reason:** {provenance.get('fallback_reason') or 'none'}",
                f"- **Historical incidents used:** {historical_ids}",
                f"- **Evidence sources:** {evidence_sources}",
                f"- **Prompt version:** {provenance.get('prompt_version') or 'not applicable'}",
                f"- **Schema version:** {provenance.get('schema_version') or SCHEMA_VERSION}",
                f"- **Date range:** {report['date_range']['start']} to {report['date_range']['end']}",
                f"- **Severity:** {report.get('incident_severity')}",
                f"- **Affected region:** {report.get('affected_region')}",
                f"- **Likely cause:** {report['likely_cause']}",
                f"- **Root cause category:** {report.get('root_cause_category')}",
                f"- **Business impact:** {report.get('business_impact_summary')}",
                f"- **Resolution:** {report.get('resolution_action')}",
                f"- **Outcome:** success {report.get('resolution_success')}, recovery {report.get('recovery_days')} day(s)",
                f"- **Confidence level:** {report['confidence_level']}",
                "",
                "### Findings From Each Agent",
                "",
            ]
        )
        for finding in report["agent_findings"]:
            lines.append(f"- **{finding['agent']}:** {finding['summary']} Confidence: {finding['confidence']}.")
        if report.get("retrieved_historical_incidents"):
            lines.extend(["", "### Retrieved Historical Incidents", ""])
            for item in report["retrieved_historical_incidents"][:3]:
                metadata = item["metadata"]
                lines.append(
                    f"- **{metadata.get('incident_id')} - {metadata.get('incident_type')}:** "
                    f"similarity score {item['similarity_score']}; root cause: {metadata.get('root_cause')}; "
                    f"resolution: {metadata.get('resolution')}; outcome: {metadata.get('outcome')}."
                )
        lines.extend(["", "### Supporting Evidence", ""])
        lines.extend(f"- {item}" for item in report["supporting_evidence"][:12])
        lines.extend(["", "### Recommended Next Steps", ""])
        lines.extend(f"- {item}" for item in report["recommended_next_steps"][:10])
        lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    LOGGER.info("Wrote multi-agent investigation summary to %s", output_path)


def run_multi_agent_investigation(
    investigation_path: Path,
    kpi_path: Path,
    deployment_path: Path,
    forecast_path: Path,
    shap_path: Path,
    json_output_path: Path,
    markdown_output_path: Path,
    knowledge_base_path: Path | None = None,
    agent_mode: str | None = None,
    llm_fallback_enabled: bool | None = None,
    llm_config: LLMConfig | None = None,
    llm_client: object | None = None,
) -> list[dict[str, object]]:
    incidents, kpis, deployments, forecasts, shap_importance = load_inputs(
        investigation_path=investigation_path,
        kpi_path=kpi_path,
        deployment_path=deployment_path,
        forecast_path=forecast_path,
        shap_path=shap_path,
    )
    retrieved_by_incident = retrieve_context_for_incidents(incidents, knowledge_base_path) if knowledge_base_path else {}
    selected_mode = agent_mode or load_agent_mode()
    fallback_enabled = load_fallback_enabled() if llm_fallback_enabled is None else llm_fallback_enabled
    LOGGER.info("Selected multi-agent execution mode: %s", selected_mode)

    if selected_mode == "deterministic":
        reports = _deterministic_reports(incidents, kpis, deployments, forecasts, shap_importance, retrieved_by_incident)
    else:
        try:
            config = llm_config or load_llm_config()
            if not config.configured:
                raise LLMConfigurationError("LLM is not configured")
            LOGGER.info("Using LLM model for multi-agent investigation: %s", config.model)
            findings_by_incident = run_llm_agent_reviews(
                incidents, kpis, deployments, forecasts, shap_importance, config, retrieved_by_incident, llm_client
            )
            reports = build_llm_final_reports(
                incidents, findings_by_incident, kpis, forecasts, shap_importance, config, retrieved_by_incident, llm_client
            )
        except (LLMError, LLMConfigurationError) as exc:
            LOGGER.warning("LLM investigation path failed: %s", exc)
            if (selected_mode == "auto" and fallback_enabled) or (selected_mode == "llm" and fallback_enabled):
                reports = _deterministic_reports(
                    incidents,
                    kpis,
                    deployments,
                    forecasts,
                    shap_importance,
                    retrieved_by_incident,
                    fallback_used=True,
                    fallback_reason=str(exc),
                )
            else:
                raise MultiAgentInvestigationError(f"LLM investigation failed and fallback is disabled: {exc}") from exc
    write_json_report(reports, json_output_path)
    write_markdown_summary(reports, markdown_output_path)
    return reports


def parse_args(args: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run deterministic multi-agent incident investigation.")
    parser.add_argument("--investigation-path", type=Path, default=Path("outputs/reports/investigation_reports.json"))
    parser.add_argument("--kpi-path", type=Path, default=Path("outputs/reports/kpi_summary_daily.csv"))
    parser.add_argument("--deployment-path", type=Path, default=Path("data/synthetic/deployment_events.csv"))
    parser.add_argument("--forecast-path", type=Path, default=Path("outputs/reports/forecast_summary.csv"))
    parser.add_argument("--shap-path", type=Path, default=Path("outputs/reports/shap_feature_importance.csv"))
    parser.add_argument(
        "--json-output-path", type=Path, default=Path("outputs/reports/multi_agent_investigation_reports.json")
    )
    parser.add_argument(
        "--markdown-output-path", type=Path, default=Path("outputs/reports/multi_agent_investigation_summary.md")
    )
    parser.add_argument("--knowledge-base-path", type=Path, default=Path("outputs/rag/incident_knowledge_base.pkl"))
    parser.add_argument("--agent-mode", choices=["deterministic", "llm", "auto"], default=None)
    return parser.parse_args(args)


def main(args: Iterable[str] | None = None) -> None:
    configure_logging()
    parsed = parse_args(args)
    run_multi_agent_investigation(
        investigation_path=parsed.investigation_path,
        kpi_path=parsed.kpi_path,
        deployment_path=parsed.deployment_path,
        forecast_path=parsed.forecast_path,
        shap_path=parsed.shap_path,
        json_output_path=parsed.json_output_path,
        markdown_output_path=parsed.markdown_output_path,
        knowledge_base_path=parsed.knowledge_base_path,
        agent_mode=parsed.agent_mode,
    )


if __name__ == "__main__":
    main()
