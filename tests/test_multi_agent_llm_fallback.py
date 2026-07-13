import json

import pytest

from src.agents.multi_agent_investigation import MultiAgentInvestigationError, run_multi_agent_investigation
from src.llm.config import LLMConfig
from src.llm.errors import LLMTimeoutError
from test_multi_agent_investigation import write_inputs


class SequencedLLMClient:
    def __init__(self, invalid=False, error=None):
        self.calls = 0
        self.invalid = invalid
        self.error = error

    def generate_structured(self, messages, schema_model, schema_name):
        self.calls += 1
        if self.error:
            raise self.error
        if self.invalid:
            return {"bad": "shape"}
        if "coordinator" in schema_name:
            return {
                "incident_id": "INC-001",
                "overall_summary": "checkout_failure_rate affected net_revenue and support_ticket_count.",
                "likely_root_cause": "checkout_failure_rate increased during the incident window.",
                "root_cause_category": "platform reliability",
                "business_impact": "net_revenue and support_ticket_count were affected.",
                "affected_metrics": ["net_revenue", "checkout_failure_rate", "support_ticket_count", "shipping_delay_rate", "avg_api_latency_ms"],
                "combined_evidence": [
                    {
                        "metric_name": "checkout_failure_rate",
                        "incident_id": None,
                        "observation": "checkout_failure_rate increased during the incident.",
                    }
                ],
                "recommended_actions": ["Review checkout_failure_rate recovery."],
                "historical_incident_references": [],
                "confidence": 0.78,
                "disagreements": [],
                "limitations": ["Uses supplied evidence only."],
                "agent_findings": [],
            }
        metric = {
            "revenue": "net_revenue",
            "support": "support_ticket_count",
            "logistics": "shipping_delay_rate",
            "platform": "checkout_failure_rate",
        }[schema_name.split("_")[0]]
        return {
            "agent_name": "Revenue Agent",
            "incident_id": "INC-001",
            "summary": f"{metric} changed during the incident.",
            "likely_causes": [f"{metric} changed during the incident window"],
            "supporting_evidence": [{"metric_name": metric, "incident_id": None, "observation": f"{metric} changed."}],
            "affected_metrics": [metric],
            "risk_level": "high",
            "recommended_actions": [f"Review {metric} recovery."],
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


def test_deterministic_mode_remains_default(tmp_path, monkeypatch):
    monkeypatch.delenv("AGENT_MODE", raising=False)
    monkeypatch.delenv("LLM_ENABLED", raising=False)
    paths = write_inputs(tmp_path)

    reports = run_multi_agent_investigation(**paths)

    assert reports[0]["execution_mode"] == "deterministic"
    assert reports[0]["fallback_used"] is False


def test_auto_mode_uses_llm_when_configured(tmp_path):
    paths = write_inputs(tmp_path)
    client = SequencedLLMClient()

    reports = run_multi_agent_investigation(**paths, agent_mode="auto", llm_config=llm_config(), llm_client=client)

    assert reports[0]["execution_mode"] == "llm"
    assert reports[0]["model_name"] == "gpt-4o-mini"
    assert reports[0]["prompt_version"] == "coordinator-v1"
    assert client.calls == 5


def test_auto_mode_without_api_key_falls_back(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_ENABLED", "true")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    paths = write_inputs(tmp_path)

    reports = run_multi_agent_investigation(**paths, agent_mode="auto", llm_fallback_enabled=True)

    assert reports[0]["execution_mode"] == "deterministic"
    assert reports[0]["fallback_used"] is True
    assert "OPENAI_API_KEY" in reports[0]["fallback_reason"]


def test_auto_mode_falls_back_on_timeout(tmp_path):
    paths = write_inputs(tmp_path)

    reports = run_multi_agent_investigation(
        **paths,
        agent_mode="auto",
        llm_fallback_enabled=True,
        llm_config=llm_config(),
        llm_client=SequencedLLMClient(error=LLMTimeoutError("timeout")),
    )

    assert reports[0]["execution_mode"] == "deterministic"
    assert reports[0]["fallback_used"] is True
    assert "timeout" in reports[0]["fallback_reason"]


def test_auto_mode_falls_back_on_validation_failure(tmp_path):
    paths = write_inputs(tmp_path)

    reports = run_multi_agent_investigation(
        **paths,
        agent_mode="auto",
        llm_fallback_enabled=True,
        llm_config=llm_config(),
        llm_client=SequencedLLMClient(invalid=True),
    )

    assert reports[0]["execution_mode"] == "deterministic"
    assert reports[0]["fallback_used"] is True


def test_llm_mode_without_fallback_returns_clear_failure(tmp_path):
    paths = write_inputs(tmp_path)

    with pytest.raises(MultiAgentInvestigationError):
        run_multi_agent_investigation(
            **paths,
            agent_mode="llm",
            llm_fallback_enabled=False,
            llm_config=llm_config(),
            llm_client=SequencedLLMClient(invalid=True),
        )


def test_report_files_include_provenance(tmp_path):
    paths = write_inputs(tmp_path)

    run_multi_agent_investigation(**paths, agent_mode="auto", llm_config=llm_config(), llm_client=SequencedLLMClient())

    payload = json.loads(paths["json_output_path"].read_text(encoding="utf-8"))
    markdown = paths["markdown_output_path"].read_text(encoding="utf-8")
    assert payload["execution_mode"] == "llm"
    assert payload["incidents"][0]["schema_version"]
    assert "Execution mode" in markdown
    assert "Fallback used" in markdown

