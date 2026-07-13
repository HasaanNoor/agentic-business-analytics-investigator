"""Project-specific LLM exceptions."""

from __future__ import annotations


class LLMError(RuntimeError):
    """Base class for LLM integration errors."""


class LLMConfigurationError(LLMError):
    """Raised when LLM configuration is invalid or incomplete."""


class LLMUnavailableError(LLMError):
    """Raised when the provider or client library is unavailable."""


class LLMTimeoutError(LLMError):
    """Raised when an LLM request times out."""


class LLMResponseValidationError(LLMError):
    """Raised when an LLM response cannot be validated against project rules."""


class LLMProviderError(LLMError):
    """Raised for provider errors that should not leak raw details."""

