"""Retrieve similar historical incidents from the local incident knowledge base."""

from __future__ import annotations

import argparse
import json
import logging
import pickle
import sys
from pathlib import Path
from typing import Iterable

import numpy as np

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.rag.build_knowledge_base import (
    DEFAULT_MODEL_NAME,
    DEFAULT_OUTPUT_PATH,
    KnowledgeBaseBuildError,
    build_incident_text,
    build_knowledge_base,
    normalize_incident,
)


LOGGER = logging.getLogger(__name__)
DEFAULT_REPORT_PATH = Path("outputs/reports/investigation_reports.json")
DEFAULT_EXAMPLES_PATH = Path("outputs/reports/rag_retrieval_examples.md")


class IncidentRetrievalError(RuntimeError):
    """Raised when similar historical incidents cannot be retrieved."""


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s - %(message)s")


def _load_sentence_transformer(model_name: str, local_files_only: bool = False):
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise IncidentRetrievalError(
            "sentence-transformers is required for local incident retrieval. "
            "Install dependencies with `python3 -m pip install -r requirements.txt`."
        ) from exc
    try:
        return SentenceTransformer(model_name, local_files_only=local_files_only)
    except TypeError:
        return SentenceTransformer(model_name)


def load_embedding_model(model_name: str, local_files_only: bool = False):
    return _load_sentence_transformer(model_name, local_files_only=local_files_only)


def load_knowledge_base(path: Path = DEFAULT_OUTPUT_PATH) -> dict[str, object]:
    if not path.exists():
        raise IncidentRetrievalError(f"Missing incident knowledge base: {path}")
    with path.open("rb") as handle:
        payload = pickle.load(handle)
    required_keys = {"text_chunks", "embeddings", "metadata", "model_name"}
    missing = required_keys - set(payload)
    if missing:
        raise IncidentRetrievalError(f"Knowledge base missing keys: {', '.join(sorted(missing))}")
    return payload


def incident_to_query_text(incident: dict[str, object]) -> str:
    normalized = normalize_incident(incident, Path("current_incident"))
    return build_incident_text(normalized)


def retrieve_similar_incidents(
    current_incident: dict[str, object],
    knowledge_base_path: Path = DEFAULT_OUTPUT_PATH,
    top_k: int = 3,
    model: object | None = None,
) -> list[dict[str, object]]:
    knowledge_base = load_knowledge_base(knowledge_base_path)
    embeddings = np.asarray(knowledge_base["embeddings"], dtype=np.float32)
    if embeddings.size == 0:
        return []

    model_name = str(knowledge_base.get("model_name") or DEFAULT_MODEL_NAME)
    embedding_model = model or _load_sentence_transformer(model_name)
    query_embedding = embedding_model.encode(
        [incident_to_query_text(current_incident)], convert_to_numpy=True, normalize_embeddings=True
    )
    query_vector = np.asarray(query_embedding, dtype=np.float32)[0]
    scores = embeddings @ query_vector

    current_id = str(current_incident.get("incident_id"))
    ranked_indexes = np.argsort(scores)[::-1]
    results: list[dict[str, object]] = []
    for index in ranked_indexes:
        metadata = dict(knowledge_base["metadata"][int(index)])
        if str(metadata.get("incident_id")) == current_id:
            continue
        results.append(
            {
                "similarity_score": round(float(scores[int(index)]), 4),
                "incident_summary": str(knowledge_base["text_chunks"][int(index)]),
                "recommendations_used_previously": metadata.get("recommendations", []),
                "metadata": metadata,
            }
        )
        if len(results) >= top_k:
            break
    return results


def _read_incidents(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        raise IncidentRetrievalError(f"Missing incident report file: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    incidents = payload.get("incidents") if isinstance(payload, dict) else None
    if not isinstance(incidents, list):
        raise IncidentRetrievalError(f"Incident report file missing incidents list: {path}")
    return [incident for incident in incidents if isinstance(incident, dict)]


def write_retrieval_examples(
    incidents: list[dict[str, object]],
    output_path: Path = DEFAULT_EXAMPLES_PATH,
    knowledge_base_path: Path = DEFAULT_OUTPUT_PATH,
    top_k: int = 3,
    model: object | None = None,
    max_examples: int = 5,
) -> None:
    if model is None:
        knowledge_base = load_knowledge_base(knowledge_base_path)
        model = _load_sentence_transformer(str(knowledge_base.get("model_name") or DEFAULT_MODEL_NAME), local_files_only=True)
    lines = [
        "# RAG Retrieval Examples",
        "",
        "These examples show which past incidents were retrieved before agents made recommendations.",
        "",
    ]
    for incident in incidents[:max_examples]:
        retrieved = retrieve_similar_incidents(incident, knowledge_base_path, top_k=top_k, model=model)
        lines.extend(
            [
                f"## Current incident: {incident.get('incident_id')} - {incident.get('title') or incident.get('incident_title')}",
                "",
                f"- **Date range:** {incident.get('incident_start_date') or incident.get('date_range', {}).get('start')} to "
                f"{incident.get('incident_end_date') or incident.get('date_range', {}).get('end')}",
                f"- **Anomaly type:** {incident.get('main_anomaly_type')}",
                "",
                "### Retrieved incidents",
                "",
            ]
        )
        if not retrieved:
            lines.append("- No similar incidents were retrieved.")
            lines.append("")
            continue
        for item in retrieved:
            metadata = item["metadata"]
            lines.extend(
                [
                    f"- **{metadata.get('incident_id')} - {metadata.get('incident_type')}**",
                    f"  Similarity score: `{item['similarity_score']}`",
                    f"  Root cause: {metadata.get('root_cause')}",
                    "  Retrieved recommendations:",
                ]
            )
            recommendations = item.get("recommendations_used_previously") or []
            lines.extend(f"  - {recommendation}" for recommendation in recommendations[:5])
        lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    LOGGER.info("Wrote retrieval examples to %s", output_path)


def parse_args(args: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Retrieve similar historical incidents.")
    parser.add_argument("--incident-report-path", type=Path, default=DEFAULT_REPORT_PATH)
    parser.add_argument("--knowledge-base-path", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--examples-output-path", type=Path, default=DEFAULT_EXAMPLES_PATH)
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--max-examples", type=int, default=5)
    return parser.parse_args(args)


def main(args: Iterable[str] | None = None) -> None:
    configure_logging()
    parsed = parse_args(args)
    if not parsed.knowledge_base_path.exists():
        try:
            build_knowledge_base(output_path=parsed.knowledge_base_path)
        except KnowledgeBaseBuildError as exc:
            raise IncidentRetrievalError(str(exc)) from exc
    incidents = _read_incidents(parsed.incident_report_path)
    knowledge_base = load_knowledge_base(parsed.knowledge_base_path)
    model = _load_sentence_transformer(str(knowledge_base.get("model_name") or DEFAULT_MODEL_NAME), local_files_only=True)
    write_retrieval_examples(
        incidents=incidents,
        output_path=parsed.examples_output_path,
        knowledge_base_path=parsed.knowledge_base_path,
        top_k=parsed.top_k,
        max_examples=parsed.max_examples,
        model=model,
    )


if __name__ == "__main__":
    main()
