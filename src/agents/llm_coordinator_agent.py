"""Optional LLM-backed Coordinator Agent."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pandas as pd

from src.agents.coordinator_agent import _top_forecast_rows, _top_shap_features
from src.agents.llm_evidence import build_evidence_bundle
from src.agents.llm_specialist_runner import confidence_label
from src.llm.client import OpenAIResponseClient
from src.llm.config import LLMConfig
from src.llm.prompts import coordinator_prompt
from src.llm.schemas import SCHEMA_VERSION, CoordinatorFinding
from src.llm.validation import validate_or_raise


def _sources_from_findings(findings: list[dict[str, Any]]) -> list[str]:
    sources: list[str] = []
    for finding in findings:
        provenance = finding.get("provenance", {}) if isinstance(finding, dict) else {}
        for source in provenance.get("evidence_sources", []) or []:
            if source not in sources:
                sources.append(str(source))
    return sources


def coordinate_incident_report_llm(
    incident: dict[str, Any],
    findings: list[dict[str, Any]],
    forecasts: pd.DataFrame,
    shap_importance: pd.DataFrame,
    kpis: pd.DataFrame,
    config: LLMConfig,
    client: OpenAIResponseClient | None = None,
    retrieved_incidents: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    evidence = build_evidence_bundle(
        domain="revenue",
        incident=incident,
        kpis=kpis,
        forecasts=forecasts,
        shap_importance=shap_importance,
        retrieved_incidents=retrieved_incidents,
        max_input_characters=config.max_input_characters,
    )
    allowed_metrics = set(evidence["allowed_metric_names"])
    allowed_metrics.update(str(column) for column in kpis.columns if column != "date")
    for finding in findings:
        structured = finding.get("llm_structured_finding", {}) if isinstance(finding, dict) else {}
        allowed_metrics.update(str(metric) for metric in structured.get("affected_metrics", []) or [])
    evidence["allowed_metric_names"] = sorted(allowed_metrics)
    prompt = coordinator_prompt(evidence, [finding.get("llm_structured_finding", finding) for finding in findings])
    provider = client or OpenAIResponseClient(config)
    raw = provider.generate_structured(prompt.messages, CoordinatorFinding, "coordinator_finding")
    coordinator = validate_or_raise(raw, CoordinatorFinding, evidence)
    retrieved_ids = evidence["historical_incident_ids"]
    provenance = {
        "execution_mode": "llm",
        "model_name": config.model,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "fallback_used": False,
        "fallback_reason": None,
        "evidence_sources": _sources_from_findings(findings) or evidence["evidence_sources"],
        "retrieved_incident_ids": retrieved_ids,
        "prompt_version": prompt.version,
        "schema_version": SCHEMA_VERSION,
        "context_truncated": evidence["context_truncated"],
    }
    return {
        "incident_id": incident.get("incident_id"),
        "incident_title": incident.get("title"),
        "date_range": {
            "start": incident.get("incident_start_date"),
            "end": incident.get("incident_end_date"),
        },
        "main_anomaly_type": incident.get("main_anomaly_type"),
        "related_anomaly_types": incident.get("related_anomaly_types", []),
        "incident_severity": incident.get("incident_severity", "not specified"),
        "affected_region": incident.get("affected_region", "not specified"),
        "root_cause_category": coordinator.root_cause_category,
        "business_impact_summary": coordinator.business_impact,
        "resolution_action": incident.get("resolution_action", "not specified"),
        "resolution_success": incident.get("resolution_success"),
        "recovery_days": incident.get("recovery_days"),
        "affected_metrics": coordinator.affected_metrics,
        "likely_cause": coordinator.likely_root_cause,
        "agent_findings": findings,
        "supporting_evidence": [item.observation for item in coordinator.combined_evidence],
        "retrieved_historical_incidents": retrieved_incidents or [],
        "forecast_context": _top_forecast_rows(forecasts),
        "model_driver_context": _top_shap_features(shap_importance),
        "recommended_next_steps": coordinator.recommended_actions,
        "confidence_level": confidence_label(coordinator.confidence),
        "llm_coordinator_finding": coordinator.model_dump(),
        "limitations": coordinator.limitations,
        "disagreements": coordinator.disagreements,
        "provenance": provenance,
        **provenance,
    }
