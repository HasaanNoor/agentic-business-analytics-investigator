"""Validated schemas for LLM incident investigation outputs."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


SCHEMA_VERSION = "llm-investigation-schema-v1"
RiskLevel = Literal["low", "medium", "high", "critical"]
RootCauseCategory = Literal[
    "platform reliability",
    "logistics",
    "inventory",
    "customer support",
    "revenue",
    "demand",
    "unknown",
    "mixed",
]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class EvidenceCitation(StrictModel):
    metric_name: str | None = None
    incident_id: str | None = None
    observation: str = Field(min_length=1, max_length=600)


class HistoricalIncidentReference(StrictModel):
    incident_id: str
    relevance: str = Field(min_length=1, max_length=500)


class SpecialistFinding(StrictModel):
    agent_name: str
    incident_id: str
    summary: str = Field(min_length=1, max_length=1200)
    likely_causes: list[str] = Field(default_factory=list, max_length=6)
    supporting_evidence: list[EvidenceCitation] = Field(default_factory=list, max_length=12)
    affected_metrics: list[str] = Field(default_factory=list, max_length=12)
    risk_level: RiskLevel
    recommended_actions: list[str] = Field(default_factory=list, max_length=10)
    historical_incident_references: list[HistoricalIncidentReference] = Field(default_factory=list, max_length=6)
    confidence: float = Field(ge=0.0, le=1.0)
    limitations: list[str] = Field(default_factory=list, max_length=8)


class CoordinatorFinding(StrictModel):
    incident_id: str
    overall_summary: str = Field(min_length=1, max_length=1600)
    likely_root_cause: str = Field(min_length=1, max_length=1200)
    root_cause_category: RootCauseCategory
    business_impact: str = Field(min_length=1, max_length=1200)
    affected_metrics: list[str] = Field(default_factory=list, max_length=20)
    combined_evidence: list[EvidenceCitation] = Field(default_factory=list, max_length=18)
    recommended_actions: list[str] = Field(default_factory=list, max_length=12)
    historical_incident_references: list[HistoricalIncidentReference] = Field(default_factory=list, max_length=8)
    confidence: float = Field(ge=0.0, le=1.0)
    disagreements: list[str] = Field(default_factory=list, max_length=8)
    limitations: list[str] = Field(default_factory=list, max_length=8)
    agent_findings: list[SpecialistFinding] = Field(default_factory=list, max_length=4)

