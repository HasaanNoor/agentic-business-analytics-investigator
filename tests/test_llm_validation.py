from src.llm.schemas import CoordinatorFinding, SpecialistFinding
from src.llm.validation import validate_model_response


EVIDENCE = {
    "incident_id": "INC-001",
    "allowed_metric_names": ["net_revenue", "checkout_failure_rate"],
    "historical_incident_ids": ["INC-014"],
    "allowed_dates": ["2026-01-16", "2026-01-17"],
    "max_output_characters": 16000,
}


def valid_specialist_payload():
    return {
        "agent_name": "Revenue Agent",
        "incident_id": "INC-001",
        "summary": "net_revenue declined while checkout_failure_rate increased.",
        "likely_causes": ["checkout_failure_rate increased during the incident window"],
        "supporting_evidence": [{"metric_name": "net_revenue", "incident_id": None, "observation": "net_revenue was below baseline."}],
        "affected_metrics": ["net_revenue", "checkout_failure_rate"],
        "risk_level": "high",
        "recommended_actions": ["Review checkout_failure_rate recovery.", "Review checkout_failure_rate recovery."],
        "historical_incident_references": [{"incident_id": "INC-014", "relevance": "Similar checkout pattern."}],
        "confidence": 0.8,
        "limitations": ["Uses supplied evidence only."],
    }


def test_valid_structured_response_is_accepted_and_deduped():
    result = validate_model_response(valid_specialist_payload(), SpecialistFinding, EVIDENCE)

    assert result.accepted is True
    assert result.value is not None
    assert result.value.recommended_actions == ["Review checkout_failure_rate recovery."]


def test_malformed_json_is_rejected():
    result = validate_model_response("{not json", SpecialistFinding, EVIDENCE)

    assert result.accepted is False
    assert "Schema validation failed" in result.errors[0]


def test_missing_required_field_is_rejected():
    payload = valid_specialist_payload()
    payload.pop("summary")

    result = validate_model_response(payload, SpecialistFinding, EVIDENCE)

    assert result.accepted is False


def test_unsupported_incident_id_is_rejected():
    payload = valid_specialist_payload()
    payload["historical_incident_references"] = [{"incident_id": "INC-999", "relevance": "Not supplied."}]

    result = validate_model_response(payload, SpecialistFinding, EVIDENCE)

    assert result.accepted is False
    assert any("Unsupported historical incident" in error for error in result.errors)


def test_invented_metric_name_is_rejected():
    payload = valid_specialist_payload()
    payload["affected_metrics"] = ["mystery_metric"]

    result = validate_model_response(payload, SpecialistFinding, EVIDENCE)

    assert result.accepted is False
    assert any("Unsupported metric" in error for error in result.errors)


def test_coordinator_validation_checks_nested_findings():
    specialist = valid_specialist_payload()
    specialist["affected_metrics"] = ["invented_metric"]
    payload = {
        "incident_id": "INC-001",
        "overall_summary": "net_revenue was affected.",
        "likely_root_cause": "checkout_failure_rate increased.",
        "root_cause_category": "platform reliability",
        "business_impact": "Revenue was affected.",
        "affected_metrics": ["net_revenue"],
        "combined_evidence": [{"metric_name": "net_revenue", "incident_id": None, "observation": "net_revenue was below baseline."}],
        "recommended_actions": ["Review checkout_failure_rate recovery."],
        "historical_incident_references": [],
        "confidence": 0.7,
        "disagreements": [],
        "limitations": [],
        "agent_findings": [specialist],
    }

    result = validate_model_response(payload, CoordinatorFinding, EVIDENCE)

    assert result.accepted is False
    assert any("invented_metric" in error for error in result.errors)

