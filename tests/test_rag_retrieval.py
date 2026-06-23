import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.agents.revenue_agent import analyze_revenue
from src.rag.build_knowledge_base import build_knowledge_base
from src.rag.retrieve_incidents import retrieve_similar_incidents, write_retrieval_examples


class FakeEmbeddingModel:
    vocabulary = [
        "revenue",
        "checkout",
        "support",
        "shipping",
        "logistics",
        "inventory",
        "deployment",
        "latency",
        "refund",
    ]

    def encode(self, texts, convert_to_numpy=True, normalize_embeddings=True):
        rows = []
        for text in texts:
            lowered = str(text).lower()
            vector = np.array([lowered.count(term) for term in self.vocabulary], dtype=np.float32)
            if normalize_embeddings and np.linalg.norm(vector):
                vector = vector / np.linalg.norm(vector)
            rows.append(vector)
        return np.vstack(rows)


def write_report(path: Path, incidents: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"incident_count": len(incidents), "incidents": incidents}), encoding="utf-8")


def make_incidents() -> list[dict[str, object]]:
    return [
        {
            "incident_id": "INC-001",
            "title": "Checkout Failure Spike",
            "incident_start_date": "2026-01-10",
            "incident_end_date": "2026-01-11",
            "main_anomaly_type": "checkout_failure_spike",
            "related_anomaly_types": ["revenue_drop", "support_ticket_spike"],
            "likely_cause": "Likely deployment-related checkout incident",
            "recommended_next_steps": ["Roll back the checkout deployment.", "Watch revenue recovery."],
        },
        {
            "incident_id": "INC-002",
            "title": "Shipping Delay Spike",
            "incident_start_date": "2026-02-10",
            "incident_end_date": "2026-02-12",
            "main_anomaly_type": "shipping_delay_spike",
            "related_anomaly_types": ["support_ticket_spike"],
            "likely_cause": "Likely logistics disruption incident",
            "recommended_next_steps": ["Review carriers and warehouse backlog."],
        },
        {
            "incident_id": "INC-003",
            "title": "Inventory Shortage",
            "incident_start_date": "2026-03-10",
            "incident_end_date": "2026-03-14",
            "main_anomaly_type": "inventory_shortage_period",
            "related_anomaly_types": ["revenue_drop"],
            "likely_cause": "Likely inventory shortage incident",
            "recommended_next_steps": ["Replenish stocked-out products."],
        },
    ]


def make_kpis() -> pd.DataFrame:
    dates = pd.date_range("2026-01-01", periods=20, freq="D")
    return pd.DataFrame(
        {
            "date": dates,
            "net_revenue": [100000] * 9 + [80000, 79000] + [100000] * 9,
            "conversion_rate": [0.05] * 20,
            "refund_rate": [0.02] * 20,
            "website_visitors": [12000] * 20,
            "average_order_value": [85] * 20,
            "stockout_units": [0] * 20,
            "lost_sales_units": [0] * 20,
        }
    )


def test_knowledge_base_builds_successfully(tmp_path):
    report_path = tmp_path / "reports" / "investigation_reports.json"
    kb_path = tmp_path / "rag" / "incident_knowledge_base.pkl"
    write_report(report_path, make_incidents())

    knowledge_base = build_knowledge_base([report_path], kb_path, model=FakeEmbeddingModel())

    assert kb_path.exists()
    assert len(knowledge_base["text_chunks"]) == 3
    assert knowledge_base["embeddings"].shape[0] == 3
    assert knowledge_base["metadata"][0]["recommendations"]


def test_retrieval_returns_results_and_similarity_scores(tmp_path):
    report_path = tmp_path / "reports" / "investigation_reports.json"
    kb_path = tmp_path / "rag" / "incident_knowledge_base.pkl"
    incidents = make_incidents()
    write_report(report_path, incidents)
    build_knowledge_base([report_path], kb_path, model=FakeEmbeddingModel())

    results = retrieve_similar_incidents(
        {
            "incident_id": "CURRENT",
            "title": "Checkout and revenue issue",
            "incident_start_date": "2026-04-01",
            "incident_end_date": "2026-04-02",
            "main_anomaly_type": "checkout_failure_spike",
            "related_anomaly_types": ["revenue_drop", "support_ticket_spike"],
            "likely_cause": "Unknown",
            "recommended_next_steps": [],
        },
        kb_path,
        model=FakeEmbeddingModel(),
    )

    assert len(results) == 3
    assert all(isinstance(result["similarity_score"], float) for result in results)
    assert results[0]["metadata"]["incident_id"] == "INC-001"
    assert results[0]["recommendations_used_previously"]


def test_agents_can_consume_retrieved_context(tmp_path):
    report_path = tmp_path / "reports" / "investigation_reports.json"
    kb_path = tmp_path / "rag" / "incident_knowledge_base.pkl"
    incidents = make_incidents()
    write_report(report_path, incidents)
    build_knowledge_base([report_path], kb_path, model=FakeEmbeddingModel())
    retrieved = retrieve_similar_incidents(incidents[0] | {"incident_id": "CURRENT"}, kb_path, model=FakeEmbeddingModel())

    finding = analyze_revenue(incidents[0], make_kpis(), retrieved)

    assert finding["historical_incident_context"]
    assert any("Historical context" in evidence for evidence in finding["supporting_evidence"])
    assert any("retrieved historical incident" in step for step in finding["recommended_next_steps"])


def test_retrieval_examples_output_file_is_created(tmp_path):
    report_path = tmp_path / "reports" / "investigation_reports.json"
    kb_path = tmp_path / "rag" / "incident_knowledge_base.pkl"
    examples_path = tmp_path / "reports" / "rag_retrieval_examples.md"
    incidents = make_incidents()
    write_report(report_path, incidents)
    build_knowledge_base([report_path], kb_path, model=FakeEmbeddingModel())

    write_retrieval_examples(
        incidents,
        output_path=examples_path,
        knowledge_base_path=kb_path,
        model=FakeEmbeddingModel(),
    )

    markdown = examples_path.read_text(encoding="utf-8")
    assert examples_path.exists()
    assert "Current incident" in markdown
    assert "Similarity score" in markdown
    assert "Retrieved recommendations" in markdown
