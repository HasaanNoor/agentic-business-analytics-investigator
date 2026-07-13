"""Optional LLM-backed Revenue Agent."""

from __future__ import annotations

from typing import Any

import pandas as pd

from src.agents.llm_specialist_runner import run_llm_specialist
from src.llm.client import OpenAIResponseClient
from src.llm.config import LLMConfig


def analyze_revenue_llm(
    incident: dict[str, Any],
    kpis: pd.DataFrame,
    forecasts: pd.DataFrame,
    shap_importance: pd.DataFrame,
    config: LLMConfig,
    client: OpenAIResponseClient | None = None,
    retrieved_incidents: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return run_llm_specialist("revenue", "Revenue Agent", incident, kpis, forecasts, shap_importance, config, client, retrieved_incidents)

