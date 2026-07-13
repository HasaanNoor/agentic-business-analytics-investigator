import pytest
from pydantic import ValidationError

from src.llm.schemas import CoordinatorFinding, EvidenceCitation, SpecialistFinding


def make_specialist() -> SpecialistFinding:
    return SpecialistFinding(
        agent_name="Revenue Agent",
        incident_id="INC-001",
        summary="net_revenue declined while checkout_failure_rate increased.",
        likely_causes=["checkout_failure_rate increased during the incident window"],
        supporting_evidence=[EvidenceCitation(metric_name="net_revenue", observation="net_revenue was below baseline.")],
        affected_metrics=["net_revenue"],
        risk_level="high",
        recommended_actions=["Review checkout_failure_rate recovery."],
        historical_incident_references=[],
        confidence=0.8,
        limitations=["Causation is inferred from supplied evidence only."],
    )


def test_specialist_schema_accepts_bounded_confidence():
    finding = make_specialist()

    assert finding.confidence == 0.8


def test_specialist_schema_rejects_missing_required_fields():
    with pytest.raises(ValidationError):
        SpecialistFinding(agent_name="Revenue Agent", incident_id="INC-001")


def test_coordinator_schema_nests_agent_findings():
    specialist = make_specialist()
    coordinator = CoordinatorFinding(
        incident_id="INC-001",
        overall_summary="Checkout issues affected revenue.",
        likely_root_cause="checkout_failure_rate increased during the incident.",
        root_cause_category="platform reliability",
        business_impact="Revenue and conversion were affected.",
        affected_metrics=["net_revenue", "checkout_failure_rate"],
        combined_evidence=[EvidenceCitation(metric_name="checkout_failure_rate", observation="checkout_failure_rate increased.")],
        recommended_actions=["Review checkout_failure_rate recovery."],
        historical_incident_references=[],
        confidence=0.7,
        disagreements=[],
        limitations=[],
        agent_findings=[specialist],
    )

    assert coordinator.agent_findings[0].agent_name == "Revenue Agent"

