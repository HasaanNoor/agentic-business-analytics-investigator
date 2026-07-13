"""Prompt templates for grounded LLM incident investigation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


PROMPT_VERSIONS = {
    "revenue": "revenue-agent-v1",
    "support": "support-agent-v1",
    "logistics": "logistics-agent-v1",
    "platform": "platform-agent-v1",
    "coordinator": "coordinator-v1",
}


SYSTEM_PROMPT = (
    "You are an evidence-grounded incident investigator. Use only the supplied evidence. "
    "Separate observations from inference. Cite metric names and historical incident IDs. "
    "State uncertainty. Do not invent dates, metrics, systems, measurements, incidents, or recommendations."
)

SPECIALIST_TASKS = {
    "revenue": (
        "Act as the Revenue Agent. Analyze sales, conversion, refunds, checkout failure, inventory loss, "
        "revenue forecasts, SHAP drivers, and historical incidents. Return only validated JSON."
    ),
    "support": (
        "Act as the Support Agent. Analyze ticket volume, ticket categories, customer complaint evidence, "
        "support forecasts, SHAP drivers, and historical incidents. Return only validated JSON."
    ),
    "logistics": (
        "Act as the Logistics Agent. Analyze shipping delays, capacity, backlog, delivery complaints, "
        "regional disruption flags, stockouts, forecasts, SHAP drivers, and historical incidents. Return only validated JSON."
    ),
    "platform": (
        "Act as the Platform Agent. Analyze API latency, checkout failures, deployment and rollback events, "
        "platform-related support evidence, forecasts, SHAP drivers, and historical incidents. Return only validated JSON."
    ),
}

COORDINATOR_TASK = (
    "Act as the Coordinator Agent. Combine the specialist findings into one unified investigation report. "
    "Resolve disagreements conservatively, keep unsupported claims out, and return only validated JSON."
)


@dataclass(frozen=True)
class Prompt:
    version: str
    messages: list[dict[str, str]]


def specialist_prompt(domain: str, evidence: dict[str, Any]) -> Prompt:
    task = SPECIALIST_TASKS[domain]
    evidence_json = json.dumps(evidence, indent=2, sort_keys=True)
    return Prompt(
        version=PROMPT_VERSIONS[domain],
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"{task}\n\nEvidence bundle:\n{evidence_json}"},
        ],
    )


def coordinator_prompt(evidence: dict[str, Any], findings: list[dict[str, Any]]) -> Prompt:
    bundle = {"evidence": evidence, "specialist_findings": findings}
    bundle_json = json.dumps(bundle, indent=2, sort_keys=True)
    return Prompt(
        version=PROMPT_VERSIONS["coordinator"],
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"{COORDINATOR_TASK}\n\nEvidence bundle:\n{bundle_json}"},
        ],
    )

