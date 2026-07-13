"""Small OpenAI client wrapper for structured LLM responses."""

from __future__ import annotations

import json
import logging
import time
from typing import Any, Type

from pydantic import BaseModel

from src.llm.config import LLMConfig
from src.llm.errors import LLMProviderError, LLMTimeoutError, LLMUnavailableError


LOGGER = logging.getLogger(__name__)


class OpenAIResponseClient:
    """Provider-isolated wrapper around the official OpenAI Python SDK."""

    def __init__(self, config: LLMConfig, client: object | None = None) -> None:
        self.config = config
        if client is not None:
            self._client = client
            return
        try:
            from openai import OpenAI
        except ImportError as exc:  # pragma: no cover - dependency is declared for normal installs.
            raise LLMUnavailableError("OpenAI Python SDK is not installed") from exc
        self._client = OpenAI(api_key=config.api_key, timeout=config.timeout_seconds, max_retries=0)

    def generate_structured(
        self,
        messages: list[dict[str, str]],
        schema_model: Type[BaseModel],
        schema_name: str,
    ) -> dict[str, Any]:
        """Return a parsed JSON object matching the requested schema."""
        last_error: Exception | None = None
        for attempt in range(self.config.max_retries + 1):
            started = time.monotonic()
            try:
                payload = self._call_provider(messages, schema_model, schema_name)
                LOGGER.info("LLM request succeeded in %.2fs after %s retry attempt(s)", time.monotonic() - started, attempt)
                return payload
            except LLMTimeoutError:
                LOGGER.warning("LLM request timed out after %.2fs on attempt %s", time.monotonic() - started, attempt + 1)
                last_error = None
                if attempt >= self.config.max_retries:
                    raise
            except LLMProviderError as exc:
                last_error = exc
                if "permanent" in str(exc).lower() or attempt >= self.config.max_retries:
                    raise
                LOGGER.warning("Transient LLM provider error on attempt %s; retrying", attempt + 1)
                time.sleep(min(2**attempt, 4))
        raise LLMProviderError("LLM provider failed after bounded retries") from last_error

    def _call_provider(
        self,
        messages: list[dict[str, str]],
        schema_model: Type[BaseModel],
        schema_name: str,
    ) -> dict[str, Any]:
        request: dict[str, Any] = {
            "model": self.config.model,
            "input": messages,
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": schema_name,
                    "schema": schema_model.model_json_schema(),
                    "strict": True,
                }
            },
        }
        if self.config.temperature is not None:
            request["temperature"] = self.config.temperature
        try:
            if hasattr(self._client, "responses"):
                response = self._client.responses.create(**request)
                return _extract_json_object(response)
            response = self._client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=self.config.temperature if self.config.temperature is not None else None,
                response_format={"type": "json_object"},
                timeout=self.config.timeout_seconds,
            )
            return json.loads(str(response.choices[0].message.content or "{}"))
        except TimeoutError as exc:
            raise LLMTimeoutError("LLM request timed out") from exc
        except Exception as exc:  # noqa: BLE001 - provider exceptions are mapped here.
            _raise_provider_error(exc)


def _extract_json_object(response: object) -> dict[str, Any]:
    output_text = getattr(response, "output_text", None)
    if output_text:
        return json.loads(str(output_text))
    parts: list[str] = []
    for item in getattr(response, "output", []) or []:
        for content in getattr(item, "content", []) or []:
            parsed = getattr(content, "parsed", None)
            if isinstance(parsed, dict):
                return parsed
            text = getattr(content, "text", None)
            if text:
                parts.append(str(text))
    if parts:
        return json.loads("\n".join(parts))
    raise LLMProviderError("LLM provider returned no structured content")


def _raise_provider_error(exc: Exception) -> None:
    name = type(exc).__name__.lower()
    status = getattr(exc, "status_code", None)
    if "timeout" in name:
        raise LLMTimeoutError("LLM request timed out") from exc
    if status in {400, 401, 403, 404} or "authentication" in name or "permission" in name:
        raise LLMProviderError("Permanent LLM provider request error") from exc
    raise LLMProviderError("Transient LLM provider error") from exc

