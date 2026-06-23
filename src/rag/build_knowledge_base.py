"""Build a local searchable knowledge base from historical incident reports."""

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


LOGGER = logging.getLogger(__name__)
DEFAULT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_INPUT_PATHS = [
    Path("outputs/reports/investigation_reports.json"),
    Path("outputs/reports/multi_agent_investigation_reports.json"),
]
DEFAULT_OUTPUT_PATH = Path("outputs/rag/incident_knowledge_base.pkl")


class KnowledgeBaseBuildError(RuntimeError):
    """Raised when the local incident knowledge base cannot be built."""


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s - %(message)s")


def _load_sentence_transformer(model_name: str, local_files_only: bool = False):
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise KnowledgeBaseBuildError(
            "sentence-transformers is required for local incident retrieval. "
            "Install dependencies with `python3 -m pip install -r requirements.txt`."
        ) from exc
    try:
        return SentenceTransformer(model_name, local_files_only=local_files_only)
    except TypeError:
        return SentenceTransformer(model_name)


def _as_list(value: object) -> list[object]:
    return value if isinstance(value, list) else []


def _string_list(value: object) -> list[str]:
    return [str(item) for item in _as_list(value) if item is not None]


def _date_range(incident: dict[str, object]) -> dict[str, object]:
    date_range = incident.get("date_range")
    if isinstance(date_range, dict):
        return {"start": date_range.get("start"), "end": date_range.get("end")}
    return {
        "start": incident.get("incident_start_date"),
        "end": incident.get("incident_end_date"),
    }


def _root_cause(incident: dict[str, object]) -> str:
    return str(incident.get("likely_cause") or incident.get("root_cause") or "Unknown")


def _recommendations(incident: dict[str, object]) -> list[str]:
    recommendations = _string_list(incident.get("recommended_next_steps"))
    if recommendations:
        return recommendations

    collected: list[str] = []
    for finding in _as_list(incident.get("agent_findings")):
        if not isinstance(finding, dict):
            continue
        for recommendation in _string_list(finding.get("recommended_next_steps")):
            if recommendation not in collected:
                collected.append(recommendation)
    return collected


def _confidence(incident: dict[str, object]) -> str:
    return str(incident.get("confidence_level") or incident.get("confidence") or "not specified")


def normalize_incident(incident: dict[str, object], source_path: Path) -> dict[str, object]:
    """Normalize first-pass and multi-agent incident reports into one record shape."""
    date_range = _date_range(incident)
    anomaly_types = [str(incident.get("main_anomaly_type"))] if incident.get("main_anomaly_type") else []
    for anomaly_type in _string_list(incident.get("related_anomaly_types")):
        if anomaly_type not in anomaly_types:
            anomaly_types.append(anomaly_type)

    record = {
        "incident_id": str(incident.get("incident_id")),
        "incident_type": str(incident.get("incident_title") or incident.get("title") or incident.get("main_anomaly_type")),
        "date_range": date_range,
        "anomaly_types": anomaly_types,
        "root_cause": _root_cause(incident),
        "recommendations": _recommendations(incident),
        "confidence_level": _confidence(incident),
        "source_path": str(source_path),
    }
    record["summary"] = build_incident_text(record)
    return record


def build_incident_text(record: dict[str, object]) -> str:
    """Create a compact searchable text chunk for one incident."""
    date_range = record.get("date_range") if isinstance(record.get("date_range"), dict) else {}
    recommendations = _string_list(record.get("recommendations"))
    anomaly_types = _string_list(record.get("anomaly_types"))
    return "\n".join(
        [
            f"Incident {record.get('incident_id')}: {record.get('incident_type')}",
            f"Date range: {date_range.get('start')} to {date_range.get('end')}",
            f"Anomaly types: {', '.join(anomaly_types) if anomaly_types else 'not specified'}",
            f"Root cause: {record.get('root_cause')}",
            f"Confidence level: {record.get('confidence_level')}",
            "Recommendations: " + ("; ".join(recommendations) if recommendations else "none recorded"),
        ]
    )


def load_incident_records(input_paths: Iterable[Path]) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    seen: set[tuple[str, str]] = set()
    for path in input_paths:
        if not path.exists():
            LOGGER.warning("Skipping missing incident report file: %s", path)
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        incidents = payload.get("incidents") if isinstance(payload, dict) else None
        if not isinstance(incidents, list):
            raise KnowledgeBaseBuildError(f"Incident report file missing incidents list: {path}")
        for incident in incidents:
            if not isinstance(incident, dict):
                continue
            record = normalize_incident(incident, path)
            key = (str(record["source_path"]), str(record["incident_id"]))
            if key not in seen:
                seen.add(key)
                records.append(record)
    if not records:
        raise KnowledgeBaseBuildError("No incidents were found for the knowledge base.")
    return records


def build_knowledge_base(
    input_paths: Iterable[Path] = DEFAULT_INPUT_PATHS,
    output_path: Path = DEFAULT_OUTPUT_PATH,
    model_name: str = DEFAULT_MODEL_NAME,
    model: object | None = None,
) -> dict[str, object]:
    records = load_incident_records(input_paths)
    text_chunks = [str(record["summary"]) for record in records]
    embedding_model = model or _load_sentence_transformer(model_name)
    embeddings = embedding_model.encode(text_chunks, convert_to_numpy=True, normalize_embeddings=True)
    embeddings = np.asarray(embeddings, dtype=np.float32)
    knowledge_base = {
        "model_name": model_name,
        "text_chunks": text_chunks,
        "embeddings": embeddings,
        "metadata": records,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as handle:
        pickle.dump(knowledge_base, handle)
    LOGGER.info("Wrote %s incident records to %s", len(records), output_path)
    return knowledge_base


def parse_args(args: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a local historical incident knowledge base.")
    parser.add_argument("--input-path", type=Path, action="append", dest="input_paths", default=None)
    parser.add_argument("--output-path", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--model-name", default=DEFAULT_MODEL_NAME)
    return parser.parse_args(args)


def main(args: Iterable[str] | None = None) -> None:
    configure_logging()
    parsed = parse_args(args)
    build_knowledge_base(
        input_paths=parsed.input_paths or DEFAULT_INPUT_PATHS,
        output_path=parsed.output_path,
        model_name=parsed.model_name,
    )


if __name__ == "__main__":
    main()
