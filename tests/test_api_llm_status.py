from fastapi.testclient import TestClient

import src.api.main as api


def test_llm_status_never_exposes_api_key(monkeypatch):
    monkeypatch.setenv("LLM_ENABLED", "true")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-secret-value")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-4o-mini")
    monkeypatch.setenv("AGENT_MODE", "auto")
    client = TestClient(api.app)

    response = client.get("/llm/status")

    assert response.status_code == 200
    payload = response.json()
    assert payload["enabled"] is True
    assert payload["configured"] is True
    assert payload["selected_model"] == "gpt-4o-mini"
    assert "sk-secret-value" not in response.text
    assert "api_key" not in response.text.lower()

