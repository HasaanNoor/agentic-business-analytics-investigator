"""Environment-driven LLM configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping

from src.llm.errors import LLMConfigurationError


PROJECT_DEFAULT_MODEL = "gpt-4o-mini"
TEMPERATURE_UNSUPPORTED_PREFIXES = ("gpt-5", "o1", "o3")


def _bool(value: str | None, default: bool = False) -> bool:
    if value is None or value == "":
        return default
    text = value.strip().lower()
    if text in {"1", "true", "yes", "y", "on"}:
        return True
    if text in {"0", "false", "no", "n", "off"}:
        return False
    raise LLMConfigurationError(f"Invalid boolean value: {value!r}")


def _int(env: Mapping[str, str], key: str, default: int, minimum: int, maximum: int) -> int:
    raw = env.get(key)
    if raw in {None, ""}:
        return default
    try:
        value = int(str(raw))
    except ValueError as exc:
        raise LLMConfigurationError(f"{key} must be an integer") from exc
    if value < minimum or value > maximum:
        raise LLMConfigurationError(f"{key} must be between {minimum} and {maximum}")
    return value


def _float(env: Mapping[str, str], key: str, default: float, minimum: float, maximum: float) -> float:
    raw = env.get(key)
    if raw in {None, ""}:
        return default
    try:
        value = float(str(raw))
    except ValueError as exc:
        raise LLMConfigurationError(f"{key} must be a number") from exc
    if value < minimum or value > maximum:
        raise LLMConfigurationError(f"{key} must be between {minimum} and {maximum}")
    return value


def model_supports_temperature(model: str) -> bool:
    lowered = model.lower()
    return not lowered.startswith(TEMPERATURE_UNSUPPORTED_PREFIXES)


@dataclass(frozen=True)
class LLMConfig:
    enabled: bool
    api_key: str | None
    model: str | None
    timeout_seconds: int
    max_retries: int
    temperature: float | None
    max_input_characters: int

    @property
    def configured(self) -> bool:
        return bool(self.enabled and self.api_key and self.model)


def load_llm_config(env: Mapping[str, str] | None = None) -> LLMConfig:
    source = env or os.environ
    enabled = _bool(source.get("LLM_ENABLED"), default=False)
    api_key = source.get("OPENAI_API_KEY") or None
    model = source.get("OPENAI_MODEL") or (PROJECT_DEFAULT_MODEL if enabled else None)
    timeout = _int(source, "LLM_TIMEOUT_SECONDS", default=30, minimum=1, maximum=300)
    retries = _int(source, "LLM_MAX_RETRIES", default=2, minimum=0, maximum=5)
    max_input = _int(source, "LLM_MAX_INPUT_CHARACTERS", default=24000, minimum=1000, maximum=200000)
    temperature_raw = source.get("LLM_TEMPERATURE")
    temperature = None
    if temperature_raw not in {None, ""}:
        if not model:
            raise LLMConfigurationError("OPENAI_MODEL is required when LLM_TEMPERATURE is set")
        if model_supports_temperature(model):
            temperature = _float(source, "LLM_TEMPERATURE", default=0.2, minimum=0.0, maximum=2.0)

    if enabled:
        if not api_key:
            raise LLMConfigurationError("LLM_ENABLED=true requires OPENAI_API_KEY")
        if not model:
            raise LLMConfigurationError("LLM_ENABLED=true requires OPENAI_MODEL")
        if len(api_key.strip()) < 8:
            raise LLMConfigurationError("OPENAI_API_KEY appears to be invalid")

    return LLMConfig(
        enabled=enabled,
        api_key=api_key,
        model=model,
        timeout_seconds=timeout,
        max_retries=retries,
        temperature=temperature,
        max_input_characters=max_input,
    )


def load_agent_mode(env: Mapping[str, str] | None = None) -> str:
    source = env or os.environ
    mode = (source.get("AGENT_MODE") or "deterministic").strip().lower()
    if mode not in {"deterministic", "llm", "auto"}:
        raise LLMConfigurationError("AGENT_MODE must be deterministic, llm, or auto")
    return mode


def load_fallback_enabled(env: Mapping[str, str] | None = None) -> bool:
    source = env or os.environ
    return _bool(source.get("LLM_FALLBACK_ENABLED"), default=True)

