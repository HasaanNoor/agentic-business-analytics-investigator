from src.agents.llm_revenue_agent import analyze_revenue_llm
from src.llm.config import LLMConfig
from test_multi_agent_investigation import make_forecasts, make_incident, make_kpis, make_shap


class FakeLLMClient:
    def generate_structured(self, messages, schema_model, schema_name):
        assert "Evidence bundle" in messages[-1]["content"]
        return {
            "agent_name": "Revenue Agent",
            "incident_id": "INC-001",
            "summary": "net_revenue declined while checkout_failure_rate increased.",
            "likely_causes": ["checkout_failure_rate increased during the incident window"],
            "supporting_evidence": [
                {"metric_name": "net_revenue", "incident_id": None, "observation": "net_revenue was below baseline."}
            ],
            "affected_metrics": ["net_revenue", "checkout_failure_rate"],
            "risk_level": "high",
            "recommended_actions": ["Review checkout_failure_rate recovery."],
            "historical_incident_references": [],
            "confidence": 0.8,
            "limitations": ["Uses supplied evidence only."],
        }


def llm_config():
    return LLMConfig(
        enabled=True,
        api_key="sk-test-value",
        model="gpt-4o-mini",
        timeout_seconds=1,
        max_retries=0,
        temperature=None,
        max_input_characters=12000,
    )


def test_llm_revenue_agent_returns_legacy_finding_with_provenance():
    finding = analyze_revenue_llm(make_incident(), make_kpis(), make_forecasts(), make_shap(), llm_config(), FakeLLMClient())

    assert finding["agent"] == "Revenue Agent"
    assert finding["confidence"] == "high"
    assert finding["llm_structured_finding"]["confidence"] == 0.8
    assert finding["provenance"]["execution_mode"] == "llm"
    assert finding["provenance"]["prompt_version"] == "revenue-agent-v1"

