"""Shared runner for evidence-grounded LLM specialist agents."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pandas as pd

from src.agents.llm_evidence import build_evidence_bundle
from src.llm.client import OpenAIResponseClient
from src.llm.config import LLMConfig
from src.llm.prompts import specialist_prompt
from src.llm.schemas import SCHEMA_VERSION, SpecialistFinding
from src.llm.validation import validate_or_raise


def confidence_label(score: float) -> str:
    if score >= 0.75:
        return "high"
    if score >= 0.45:
        return "medium"
    return "low"


def specialist_to_legacy_dict(finding: SpecialistFinding, domain: str, provenance: dict[str, Any]) -> dict[str, Any]:
    return {
        "agent": finding.agent_name,
        "finding_type": domain,
        "summary": finding.summary,
        "llm_structured_finding": finding.model_dump(),
        "metrics": [{"metric": metric} for metric in finding.affected_metrics],
        "historical_incident_context": [item.model_dump() for item in finding.historical_incident_references],
        "supporting_evidence": [item.observation for item in finding.supporting_evidence],
        "recommended_next_steps": finding.recommended_actions,
        "confidence": confidence_label(finding.confidence),
        "risk_level": finding.risk_level,
        "limitations": finding.limitations,
        "provenance": provenance,
    }


def run_llm_specialist(
    domain: str,
    agent_name: str,
    incident: dict[str, Any],
    kpis: pd.DataFrame,
    forecasts: pd.DataFrame,
    shap_importance: pd.DataFrame,
    config: LLMConfig,
    client: OpenAIResponseClient | None = None,
    retrieved_incidents: list[dict[str, Any]] | None = None,
    deployments: pd.DataFrame | None = None,
) -> dict[str, Any]:
    evidence = build_evidence_bundle(
        domain=domain,
        incident=incident,
        kpis=kpis,
        forecasts=forecasts,
        shap_importance=shap_importance,
        retrieved_incidents=retrieved_incidents,
        deployments=deployments,
        max_input_characters=config.max_input_characters,
    )
    prompt = specialist_prompt(domain, evidence)
    provider = client or OpenAIResponseClient(config)
    raw = provider.generate_structured(prompt.messages, SpecialistFinding, f"{domain}_specialist_finding")
    finding = validate_or_raise(raw, SpecialistFinding, evidence)
    if finding.agent_name != agent_name:
        finding.agent_name = agent_name
    provenance = {
        "execution_mode": "llm",
        "model_name": config.model,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "fallback_used": False,
        "fallback_reason": None,
        "evidence_sources": evidence["evidence_sources"],
        "retrieved_incident_ids": evidence["historical_incident_ids"],
        "prompt_version": prompt.version,
        "schema_version": SCHEMA_VERSION,
        "context_truncated": evidence["context_truncated"],
    }
    return specialist_to_legacy_dict(finding, domain, provenance)

