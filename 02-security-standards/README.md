# Information Security Standards: Expert Evaluation Dataset

10 original, high-difficulty questions on HOTP/TOTP (RFC 4226/6238), CVSS 3.1, NIST SP 800-63B-4, Argon2 (RFC 9106) and cryptographic probability. Reference values are checked against the RFC test vectors.

> **Status:** self-directed portfolio project. It was written to demonstrate the workflow of an AI research-evaluation specialist: authoring hard questions, sourcing and verifying answers, designing shortcut-resistant items, testing them against models and hardening. **No results from real AI models are included.** The reports in `reports/` come from built-in mock models and only demonstrate that the harness works.

## What is in here

| Path | Purpose |
|---|---|
| `questions/questions.jsonl` | 10 questions with answer, reasoning, citations, designed shortcut trap and the wrong answer it produces |
| `verifiers.py` | Independent code that recomputes every reference answer |
| `evalkit/` | Schema and lint, grader, model harness (OpenAI / Anthropic / Ollama adapters), validator, catalog generator |
| `tests/` | Dataset quality tests |
| `docs/methodology.md` | How questions are written, verified and hardened |
| `docs/review-checklist.md` | Checklist a reviewer applies to each item |
| `docs/revision-log.md` | Template for recording reviewer feedback and hardening rounds |
| `docs/question-catalog.md` | Generated, reviewer-friendly view of every item |

## Quick start (standard library only)

```bash
python -m evalkit.validate questions/questions.jsonl      # recompute answers, check naive answers fail, lint
python -m pytest -q                                       # or: python tests/run_tests.py
python -m evalkit.run_eval --questions questions/questions.jsonl --model mock-oracle --attempts 1
python -m evalkit.catalog                                 # regenerate docs/question-catalog.md
```

## Testing against a real model

```bash
export OPENAI_API_KEY=...        # or ANTHROPIC_API_KEY=...
python -m evalkit.run_eval --questions questions/questions.jsonl --model openai:<model-name> --attempts 3
python -m evalkit.run_eval --questions questions/questions.jsonl --model anthropic:<model-name> --attempts 3
python -m evalkit.run_eval --questions questions/questions.jsonl --model ollama:<local-model> --attempts 3
```

Items with a pass rate of 0.67 or higher are flagged **too easy**. Rewrite them (add a constraint, change the numbers, tighten the convention) and record the change in `docs/revision-log.md`. Write the measured pass rate into the `measured_pass_rate` field only after a real run.

## Honest limits

* Answers marked `verification: code` are arithmetic or algorithm outputs with the definition stated in the question. They are independently recomputed, not looked up.
* Answers marked `source` or `both` cite a specific document and section. Re-open each source before relying on it; standards get revised.
* Ten items per domain is a demonstration set, not a benchmark.
