# RAG Knowledge Base

## Goal

Build a local searchable knowledge base of past incidents and retrieve similar historical incidents for new incident reviews.

## Inputs

- `outputs/reports/investigation_reports.json`
- `outputs/reports/multi_agent_investigation_reports.json`

## Outputs

- `outputs/rag/incident_knowledge_base.pkl`
- `outputs/reports/rag_retrieval_examples.md`

## Main files to create

- `src/rag/build_knowledge_base.py`
- `src/rag/retrieve_incidents.py`
- `tests/test_rag_retrieval.py`

## Required behavior

- Load incident reports from one or more JSON files.
- Normalize first-pass and multi-agent incidents into one common record shape.
- Store for each incident:
  - Incident id.
  - Incident type.
  - Date range.
  - Anomaly types.
  - Severity.
  - Region.
  - Root cause.
  - Root cause category.
  - Business impact summary.
  - Affected metrics.
  - Resolution.
  - Recovery days.
  - Outcome.
  - Recommendations.
  - Confidence level.
  - Source path.
- Convert each normalized incident into a compact text summary.
- Embed summaries using `sentence-transformers/all-MiniLM-L6-v2`.
- Save the knowledge base as a pickle with:
  - `model_name`
  - `text_chunks`
  - `embeddings`
  - `metadata`
- Retrieval should:
  - Load the local pickle.
  - Embed the query incident with the same model.
  - Use vector similarity to return the top results.
  - Skip the same incident id when comparing an incident to history.
  - Return similarity score, summary, root cause, resolution, outcome, recommendations, and metadata.
- Tests may use a fake embedding model so they do not depend on downloads.

## Acceptance criteria

- Knowledge base build writes `outputs/rag/incident_knowledge_base.pkl`.
- Retrieval returns ranked similar incidents with numeric similarity scores.
- Retrieval examples Markdown is created.
- Tests verify build, retrieval, metadata fields, and example output.

## Test commands where relevant

```bash
python3 src/rag/build_knowledge_base.py
python3 src/rag/retrieve_incidents.py
python3 -m pytest tests/test_rag_retrieval.py
python3 -m py_compile src/rag/build_knowledge_base.py
python3 -m py_compile src/rag/retrieve_incidents.py
```
