# Gemini Test Prompt

## Goal

Use this prompt after uploading all markdown files in `gemini_spec/`.

## Inputs

- The uploaded markdown specification files.
- No private data.
- No API keys.

## Outputs

- A complete regenerated project.
- Source code.
- Tests.
- README updates.
- Run commands.
- A short list of assumptions.

## Main files to create

All files described across the attached markdown specifications, including:

- `requirements.txt`
- `README.md`
- Source files under `src/`
- Test files under `tests/`

## Required behavior

Paste this prompt:

```text
Use the attached markdown files as the source of truth.

Generate the complete Agentic Business Analytics Investigator project.

Follow the specs exactly. Use Python and the repository structure described in the markdown files. Include all source code, tests, README updates, requirements, and run commands.

Keep the behavior deterministic. Use pandas, numpy, scikit-learn, xgboost, shap, fastapi, uvicorn, sentence-transformers, and pytest as specified. Avoid unnecessary complexity. Do not add a database, dashboard, or cloud deployment unless the specs ask for it.

Create code that generates synthetic data, validates it, builds KPI summaries, detects anomalies, investigates incidents, trains forecasts, explains forecasts, writes reports, builds and queries a local RAG knowledge base, and serves generated outputs through a read-only FastAPI backend.

Create tests for every major phase. Tests must not require API keys or network access. Use fake models or deterministic fallbacks where needed.

After generating the project, explain any assumptions you made. Then list the commands to run the pipeline, run tests, compile key modules, and start the API.
```

## Acceptance criteria

- The generated project follows all attached specs.
- The generated project includes code, tests, README content, and run commands.
- Assumptions are stated clearly.
- The response does not include private information or API keys.

## Test commands where relevant

```bash
python3 -m pytest
python3 -m py_compile src/api/main.py
python3 -m uvicorn src.api.main:app --reload
```
