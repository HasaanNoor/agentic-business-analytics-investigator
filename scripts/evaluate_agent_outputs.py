"""Evaluate deterministic and mocked LLM multi-agent outputs."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.agents.multi_agent_investigation import run_multi_agent_investigation
from src.llm.config import LLMConfig


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"
DATA_DIR = PROJECT_ROOT / "data" / "synthetic"
RAG_DIR = PROJECT_ROOT / "outputs" / "rag"


class MockEvaluationLLMClient:
    """Evidence-grounded fake client for repeatable evaluation."""

    def generate_structured(self, messages: list[dict[str, str]], schema_model: object, schema_name: str) -> dict[str, Any]:
        evidence = _extract_evidence(messages[-1]["content"])
        if "coordinator" in schema_name:
            return _coordinator_payload(evidence)
        domain = schema_name.split("_")[0]
        return _specialist_payload(domain, evidence)


def _extract_evidence(text: str) -> dict[str, Any]:
    marker = "Evidence bundle:\n"
    raw = text.split(marker, 1)[1]
    payload = json.loads(raw)
    return payload.get("evidence", payload)


def _first_metric(evidence: dict[str, Any], default: str = "net_revenue") -> str:
    metrics = evidence.get("allowed_metric_names", []) or [default]
    return str(metrics[0])


def _specialist_payload(domain: str, evidence: dict[str, Any]) -> dict[str, Any]:
    names = {
        "revenue": "Revenue Agent",
        "support": "Customer Support Agent",
        "logistics": "Logistics Agent",
        "platform": "Platform Reliability Agent",
    }
    metric = _first_metric(evidence)
    incident_id = str(evidence.get("incident_id"))
    historical_ids = evidence.get("historical_incident_ids", []) or []
    return {
        "agent_name": names.get(domain, "Specialist Agent"),
        "incident_id": incident_id,
        "summary": f"{metric} was reviewed using supplied evidence for {incident_id}.",
        "likely_causes": [f"{metric} changed during the incident window"],
        "supporting_evidence": [{"metric_name": metric, "incident_id": None, "observation": f"{metric} was cited in the evidence bundle."}],
        "affected_metrics": [metric],
        "risk_level": "medium",
        "recommended_actions": [f"Review {metric} recovery before closing {incident_id}."],
        "historical_incident_references": [
            {"incident_id": str(historical_ids[0]), "relevance": "Closest supplied historical incident."}
        ]
        if historical_ids
        else [],
        "confidence": 0.62,
        "limitations": ["Mocked LLM output for deterministic evaluation; not a provider quality claim."],
    }


def _coordinator_payload(evidence: dict[str, Any]) -> dict[str, Any]:
    incident_id = str(evidence.get("incident_id"))
    metrics = [str(metric) for metric in (evidence.get("allowed_metric_names", []) or ["net_revenue"])[:4]]
    metric = metrics[0]
    historical_ids = evidence.get("historical_incident_ids", []) or []
    return {
        "incident_id": incident_id,
        "overall_summary": f"{incident_id} was reviewed with specialist findings and supplied evidence.",
        "likely_root_cause": f"{metric} changed during the supplied incident window.",
        "root_cause_category": "mixed",
        "business_impact": f"Affected metrics include {', '.join(metrics)}.",
        "affected_metrics": metrics,
        "combined_evidence": [{"metric_name": metric, "incident_id": None, "observation": f"{metric} appeared in validated evidence."}],
        "recommended_actions": [f"Review {metric} recovery before closing {incident_id}."],
        "historical_incident_references": [
            {"incident_id": str(historical_ids[0]), "relevance": "Closest supplied historical incident."}
        ]
        if historical_ids
        else [],
        "confidence": 0.64,
        "disagreements": [],
        "limitations": ["Mocked LLM output validates schema and grounding behavior only."],
        "agent_findings": [],
    }


def _config() -> LLMConfig:
    return LLMConfig(
        enabled=True,
        api_key="sk-evaluation-fake",
        model="mock-evaluation-model",
        timeout_seconds=1,
        max_retries=0,
        temperature=None,
        max_input_characters=24000,
    )


def _unsupported_claim_count(report: dict[str, Any]) -> int:
    allowed = set(report.get("affected_metrics", []) or [])
    count = 0
    for item in report.get("supporting_evidence", []) or []:
        text = str(item)
        for token in text.split():
            if "_" in token and token.strip(".,;:") not in allowed:
                count += 1
    return count


def _row(label: str, report: dict[str, Any]) -> dict[str, Any]:
    historical_ids = []
    for item in report.get("retrieved_historical_incidents", []) or []:
        metadata = item.get("metadata", {}) if isinstance(item, dict) else {}
        if isinstance(metadata, dict) and metadata.get("incident_id"):
            historical_ids.append(str(metadata["incident_id"]))
    recommendations = report.get("recommended_next_steps", []) or []
    return {
        "mode": label,
        "incident_id": report.get("incident_id"),
        "schema_valid": bool(report.get("schema_version")),
        "evidence_citation_count": len(report.get("supporting_evidence", []) or []),
        "historical_reference_count": len(historical_ids),
        "unsupported_claim_count": _unsupported_claim_count(report),
        "recommendation_count": len(recommendations),
        "specific_recommendation_count": sum(1 for item in recommendations if any(metric in str(item) for metric in report.get("affected_metrics", []) or [])),
        "fallback_used": bool(report.get("fallback_used")),
        "output_completeness": sum(
            bool(report.get(field))
            for field in ["likely_cause", "business_impact_summary", "affected_metrics", "supporting_evidence", "recommended_next_steps"]
        ),
    }


def evaluate() -> list[dict[str, Any]]:
    with TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        deterministic = run_multi_agent_investigation(
            investigation_path=REPORTS_DIR / "investigation_reports.json",
            kpi_path=REPORTS_DIR / "kpi_summary_daily.csv",
            deployment_path=DATA_DIR / "deployment_events.csv",
            forecast_path=REPORTS_DIR / "forecast_summary.csv",
            shap_path=REPORTS_DIR / "shap_feature_importance.csv",
            json_output_path=temp / "deterministic.json",
            markdown_output_path=temp / "deterministic.md",
            knowledge_base_path=RAG_DIR / "incident_knowledge_base.pkl",
            agent_mode="deterministic",
        )
        mocked_llm = run_multi_agent_investigation(
            investigation_path=REPORTS_DIR / "investigation_reports.json",
            kpi_path=REPORTS_DIR / "kpi_summary_daily.csv",
            deployment_path=DATA_DIR / "deployment_events.csv",
            forecast_path=REPORTS_DIR / "forecast_summary.csv",
            shap_path=REPORTS_DIR / "shap_feature_importance.csv",
            json_output_path=temp / "mocked_llm.json",
            markdown_output_path=temp / "mocked_llm.md",
            knowledge_base_path=RAG_DIR / "incident_knowledge_base.pkl",
            agent_mode="auto",
            llm_config=_config(),
            llm_client=MockEvaluationLLMClient(),
        )
    rows: list[dict[str, Any]] = []
    for report in deterministic[:5]:
        rows.append(_row("deterministic", report))
    for report in mocked_llm[:5]:
        rows.append(_row("mocked_llm", report))
    return rows


def write_outputs(rows: list[dict[str, Any]]) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = REPORTS_DIR / "agent_evaluation.csv"
    md_path = REPORTS_DIR / "agent_evaluation.md"
    fieldnames = list(rows[0]) if rows else []
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    lines = [
        "# Agent Output Evaluation",
        "",
        "This deterministic evaluation compares existing rule-based findings with mocked LLM findings. It checks structure, citations, references, unsupported claims, recommendation specificity, fallback rate, and completeness. It does not claim the mocked LLM is better because of length.",
        "",
        "| Mode | Incident | Schema valid | Evidence citations | Historical refs | Unsupported claims | Recommendations | Specific recommendations | Fallback | Completeness |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['mode']} | {row['incident_id']} | {row['schema_valid']} | {row['evidence_citation_count']} | "
            f"{row['historical_reference_count']} | {row['unsupported_claim_count']} | {row['recommendation_count']} | "
            f"{row['specific_recommendation_count']} | {row['fallback_used']} | {row['output_completeness']} |"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {csv_path}")
    print(f"Wrote {md_path}")


def main() -> None:
    rows = evaluate()
    write_outputs(rows)


if __name__ == "__main__":
    main()

