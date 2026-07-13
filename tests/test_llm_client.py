import pytest

from src.llm.client import OpenAIResponseClient
from src.llm.config import LLMConfig
from src.llm.errors import LLMProviderError, LLMTimeoutError
from src.llm.schemas import SpecialistFinding


class FakeResponses:
    def __init__(self, response=None, error=None):
        self.response = response
        self.error = error
        self.calls = 0

    def create(self, **kwargs):
        self.calls += 1
        if self.error:
            raise self.error
        return self.response


class FakeOpenAI:
    def __init__(self, responses):
        self.responses = responses


class FakeResponse:
    output_text = (
        '{"agent_name":"Revenue Agent","incident_id":"INC-001","summary":"net_revenue declined.",'
        '"likely_causes":[],"supporting_evidence":[],"affected_metrics":["net_revenue"],"risk_level":"medium",'
        '"recommended_actions":["Review net_revenue."],"historical_incident_references":[],"confidence":0.6,"limitations":[]}'
    )


def config(retries=0):
    return LLMConfig(
        enabled=True,
        api_key="sk-test-value",
        model="gpt-4o-mini",
        timeout_seconds=1,
        max_retries=retries,
        temperature=None,
        max_input_characters=10000,
    )


def test_client_returns_json_from_responses_api():
    responses = FakeResponses(response=FakeResponse())
    client = OpenAIResponseClient(config(), client=FakeOpenAI(responses))

    payload = client.generate_structured([], SpecialistFinding, "finding")

    assert payload["agent_name"] == "Revenue Agent"
    assert responses.calls == 1


def test_client_retries_transient_provider_errors():
    class FlakyResponses:
        def __init__(self):
            self.calls = 0

        def create(self, **kwargs):
            self.calls += 1
            if self.calls == 1:
                raise RuntimeError("temporary outage")
            return FakeResponse()

    responses = FlakyResponses()
    client = OpenAIResponseClient(config(retries=1), client=FakeOpenAI(responses))

    payload = client.generate_structured([], SpecialistFinding, "finding")

    assert payload["incident_id"] == "INC-001"
    assert responses.calls == 2


def test_client_maps_timeout():
    responses = FakeResponses(error=TimeoutError("slow"))
    client = OpenAIResponseClient(config(), client=FakeOpenAI(responses))

    with pytest.raises(LLMTimeoutError):
        client.generate_structured([], SpecialistFinding, "finding")


def test_client_does_not_retry_permanent_errors():
    class PermanentError(Exception):
        status_code = 401

    responses = FakeResponses(error=PermanentError("bad key"))
    client = OpenAIResponseClient(config(retries=2), client=FakeOpenAI(responses))

    with pytest.raises(LLMProviderError):
        client.generate_structured([], SpecialistFinding, "finding")
    assert responses.calls == 1

