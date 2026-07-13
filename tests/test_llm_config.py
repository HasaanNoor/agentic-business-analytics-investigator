import pytest

from src.llm.config import load_agent_mode, load_fallback_enabled, load_llm_config, model_supports_temperature
from src.llm.errors import LLMConfigurationError


def test_llm_disabled_by_default():
    config = load_llm_config({})

    assert config.enabled is False
    assert config.configured is False
    assert config.model is None


def test_enabled_requires_api_key():
    with pytest.raises(LLMConfigurationError):
        load_llm_config({"LLM_ENABLED": "true", "OPENAI_MODEL": "gpt-4o-mini"})


def test_enabled_uses_project_default_model_when_available():
    config = load_llm_config({"LLM_ENABLED": "true", "OPENAI_API_KEY": "sk-test-value"})

    assert config.configured is True
    assert config.model == "gpt-4o-mini"


def test_temperature_is_ignored_for_unsupported_model():
    config = load_llm_config(
        {
            "LLM_ENABLED": "true",
            "OPENAI_API_KEY": "sk-test-value",
            "OPENAI_MODEL": "gpt-5-small",
            "LLM_TEMPERATURE": "0.7",
        }
    )

    assert model_supports_temperature("gpt-5-small") is False
    assert config.temperature is None


def test_agent_mode_and_fallback_defaults():
    assert load_agent_mode({}) == "deterministic"
    assert load_fallback_enabled({}) is True


def test_invalid_agent_mode_is_rejected():
    with pytest.raises(LLMConfigurationError):
        load_agent_mode({"AGENT_MODE": "surprise"})

