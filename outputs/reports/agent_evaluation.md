# Agent Output Evaluation

This deterministic evaluation compares existing rule-based findings with mocked LLM findings. It checks structure, citations, references, unsupported claims, recommendation specificity, fallback rate, and completeness. It does not claim the mocked LLM is better because of length.

| Mode | Incident | Schema valid | Evidence citations | Historical refs | Unsupported claims | Recommendations | Specific recommendations | Fallback | Completeness |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| deterministic | INC-001 | True | 14 | 3 | 1 | 35 | 0 | False | 5 |
| deterministic | INC-002 | True | 17 | 3 | 1 | 17 | 0 | False | 5 |
| deterministic | INC-003 | True | 19 | 3 | 0 | 18 | 0 | False | 5 |
| deterministic | INC-004 | True | 20 | 3 | 0 | 16 | 0 | False | 5 |
| deterministic | INC-005 | True | 18 | 3 | 0 | 17 | 0 | False | 5 |
| mocked_llm | INC-001 | True | 1 | 3 | 0 | 1 | 1 | False | 5 |
| mocked_llm | INC-002 | True | 1 | 3 | 0 | 1 | 1 | False | 5 |
| mocked_llm | INC-003 | True | 1 | 3 | 0 | 1 | 1 | False | 5 |
| mocked_llm | INC-004 | True | 1 | 3 | 0 | 1 | 1 | False | 5 |
| mocked_llm | INC-005 | True | 1 | 3 | 0 | 1 | 1 | False | 5 |
