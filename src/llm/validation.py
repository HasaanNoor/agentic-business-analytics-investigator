"""Validation for structured, evidence-grounded LLM outputs."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any, Type

from pydantic import BaseModel, ValidationError

from src.llm.errors import LLMResponseValidationError
from src.llm.schemas import CoordinatorFinding, SpecialistFinding


IDENTIFIER_PATTERN = re.compile(r"\b[a-z][a-z0-9]+(?:_[a-z0-9]+)+\b")
INCIDENT_PATTERN = re.compile(r"\bINC-\d+\b")
DATE_PATTERN = re.compile(r"\b20\d{2}-\d{2}-\d{2}\b")


@dataclass
class ValidationResult:
    accepted: bool
    value: BaseModel | None = None
    errors: list[str] = field(default_factory=list)


def validate_or_raise(payload: str | dict[str, Any], schema: Type[BaseModel], evidence: dict[str, Any]) -> BaseModel:
    result = validate_model_response(payload, schema, evidence)
    if not result.accepted:
        raise LLMResponseValidationError("; ".join(result.errors))
    assert result.value is not None
    return result.value


def validate_model_response(payload: str | dict[str, Any], schema: Type[BaseModel], evidence: dict[str, Any]) -> ValidationResult:
    errors: list[str] = []
    try:
        raw = json.loads(payload) if isinstance(payload, str) else payload
        value = schema.model_validate(raw)
    except (json.JSONDecodeError, ValidationError, TypeError) as exc:
        return ValidationResult(False, errors=[f"Schema validation failed: {exc}"])

    allowed_metrics = {str(item) for item in evidence.get("allowed_metric_names", [])}
    allowed_incidents = {str(item) for item in evidence.get("historical_incident_ids", [])}
    allowed_incidents.add(str(evidence.get("incident_id")))
    allowed_dates = {str(item) for item in evidence.get("allowed_dates", [])}

    findings = [value] if isinstance(value, SpecialistFinding) else []
    if isinstance(value, CoordinatorFinding):
        findings = [*value.agent_findings]
        _check_metrics(value.affected_metrics, allowed_metrics, errors)
        _check_evidence_citations(value.combined_evidence, allowed_metrics, allowed_incidents, errors)
        _check_historical_refs(value.historical_incident_references, allowed_incidents, errors)
        _check_text_fields(
            [value.overall_summary, value.likely_root_cause, value.business_impact, *value.recommended_actions, *value.limitations],
            allowed_metrics,
            allowed_incidents,
            allowed_dates,
            errors,
        )

    for finding in findings:
        _check_metrics(finding.affected_metrics, allowed_metrics, errors)
        _check_evidence_citations(finding.supporting_evidence, allowed_metrics, allowed_incidents, errors)
        _check_historical_refs(finding.historical_incident_references, allowed_incidents, errors)
        _check_text_fields(
            [finding.summary, *finding.likely_causes, *finding.recommended_actions, *finding.limitations],
            allowed_metrics,
            allowed_incidents,
            allowed_dates,
            errors,
        )
        finding.recommended_actions[:] = _dedupe(finding.recommended_actions)

    if isinstance(value, CoordinatorFinding):
        value.recommended_actions[:] = _dedupe(value.recommended_actions)

    serialized_size = len(value.model_dump_json())
    max_output = int(evidence.get("max_output_characters", 16000))
    if serialized_size > max_output:
        errors.append(f"Output exceeds maximum size: {serialized_size} > {max_output}")

    return ValidationResult(not errors, value=value if not errors else None, errors=errors)


def _check_metrics(metrics: list[str], allowed_metrics: set[str], errors: list[str]) -> None:
    for metric in metrics:
        if metric not in allowed_metrics:
            errors.append(f"Unsupported metric cited: {metric}")


def _check_evidence_citations(citations: list[Any], allowed_metrics: set[str], allowed_incidents: set[str], errors: list[str]) -> None:
    for citation in citations:
        metric = getattr(citation, "metric_name", None)
        incident_id = getattr(citation, "incident_id", None)
        if metric and metric not in allowed_metrics:
            errors.append(f"Unsupported metric cited in evidence: {metric}")
        if incident_id and incident_id not in allowed_incidents:
            errors.append(f"Unsupported incident cited in evidence: {incident_id}")


def _check_historical_refs(refs: list[Any], allowed_incidents: set[str], errors: list[str]) -> None:
    for ref in refs:
        incident_id = str(getattr(ref, "incident_id", ""))
        if incident_id not in allowed_incidents:
            errors.append(f"Unsupported historical incident cited: {incident_id}")


def _check_text_fields(
    texts: list[str],
    allowed_metrics: set[str],
    allowed_incidents: set[str],
    allowed_dates: set[str],
    errors: list[str],
) -> None:
    allowed_words = {
        "api",
        "avg",
        "root_cause",
        "support_ticket",
        "historical_incident",
        "incident_id",
        "date_range",
    }
    for text in texts:
        for incident_id in INCIDENT_PATTERN.findall(text):
            if incident_id not in allowed_incidents:
                errors.append(f"Unsupported incident mentioned: {incident_id}")
        for date_text in DATE_PATTERN.findall(text):
            if allowed_dates and date_text not in allowed_dates:
                errors.append(f"Unsupported date mentioned: {date_text}")
        for identifier in IDENTIFIER_PATTERN.findall(text):
            if identifier not in allowed_metrics and identifier not in allowed_words and not identifier.endswith("_agent"):
                errors.append(f"Unsupported metric or system mentioned: {identifier}")


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for item in items:
        normalized = " ".join(str(item).split()).lower()
        if normalized not in seen:
            output.append(str(item))
            seen.add(normalized)
    return output

