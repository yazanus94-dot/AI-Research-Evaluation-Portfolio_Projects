# AI Research Evaluation Portfolio

## Project title
**AI Research Evaluation Portfolio** — Verifiable, Shortcut-Resistant Evaluation Datasets for Biomedical Signals, Security Standards, and Software Testing

## Overview
This repository is a curated portfolio of three domain-focused AI/research evaluation projects authored and structured by [Yazan Aljabari](https://www.linkedin.com/in/yazan-aljabari-878202139/). Each project provides high-difficulty, self-contained assessment items with explicit conventions, reference answers, reasoning, and designed shortcut traps (plausible but incorrect answers). The portfolio demonstrates a verification-first workflow: authoring discriminative questions, recomputing/verifying answers with code and cited sources, validating datasets with automated checks, and reporting results transparently. Included results are **mock harness evaluation artifacts** (oracle/trap) used to demonstrate item quality and tooling—not real LLM benchmark measurements.

## Problem statement
Naive or loosely specified evaluation questions often reward memorization, convention errors, or shortcut heuristics instead of genuine reasoning. In technical domains, small mistakes—wrong denominators or conventions, outdated standards recall, incorrect scoring formulas, off-by-one/counting errors, or misread specifications—can appear plausible while being incorrect. This project addresses that problem by building **shortcut-resistant, verification-first** evaluation items where each question has an unambiguous answer, an explicitly modeled trap, and an independent path to verification.

## Objectives
- Design clear, unambiguous, and self-contained evaluation items across biomedical signal processing, security standards, and software testing/quality engineering.
- Pair every item with a reference answer, rationale, and a plausible naive (shortcut) answer.
- Enable independent verification through code (`verifiers.py`) and/or cited normative sources.
- Provide reproducible tooling (`evalkit`), tests, and CI workflows to validate question quality and harness behavior.
- Present methodology, results, and limitations transparently in a professional, recruiter-ready portfolio.

## Features
- **Three browsable domain projects (10 items each):**
  - **[01-biomedical-signals](01-biomedical-signals/)** (A01–A10): HRV time-domain metrics (RMSSD/SDNN/pNN50), heart-rate averaging pitfall, aliasing, zero-phase filtering attenuation, Welch LF-bin counting, R-peak timing/quantization, Poincaré SD1, and QRS window scaling.
  - **[02-security-standards](02-security-standards/)** (SEC01–SEC10): RFC 4226 HOTP, RFC 6238 TOTP, time-step calculation, password entropy, birthday bound, CVSS v3.1 base scoring, NIST SP 800-63B-4 policy, RFC 9106 Argon2 parameters, and HOTP truncation bias.
  - **[03-software-testing](03-software-testing/)** (B01–B10): two/three-value BVA and coverage, flaky-suite probability, SemVer 2.0.0 precedence, RFC 8259 duplicate JSON key behavior, pairwise minimum tests, mutation score, rerun confidence, and SLO downtime budget.
- **Verification-first artifacts:** `questions/questions.jsonl`, `verifiers.py`, reasoning, shortcut traps, and verification/source metadata per item.
- **Evaluation toolkit (`evalkit/`):** schema/loading/linting, answer extraction/grading, validation, mock evaluation harness, and question-catalog generation.
- **Mock evaluation artifacts:** per-project `results_mock-oracle` and `results_mock-trap` reports (JSON/MD) showing discriminative trap behavior.
- **Visual evidence:** SVG charts per project (`reports/results_chart.svg`) and portfolio summary (`assets/portfolio_results.svg`).
- **Documentation:** per-project methodology, reviewer checklists, revision logs, question catalogs; root technical overview and results dashboard.
- **Quality automation:** dataset/domain tests and GitHub Actions CI workflow(s).
- **Portfolio presentation:** structured READMEs, `index.html` landing page, and MIT license.

## Technologies
- **Programming language:** Python (3.10+ recommended)
- **Standard library:** `json`, `re`, `math`, `statistics`, `hmac`, `hashlib`, `struct`, `argparse`, `pathlib`, `datetime`, `importlib`, etc.
- **Scientific libraries (biomedical verifiers):** `numpy`, `scipy`
- **Testing:** `pytest` (plus included `tests/run_tests.py` runners)
- **CI/CD:** GitHub Actions (`.github/workflows/ci.yml`, per-project validate workflows)
- **Formats & docs:** Markdown, JSON/JSONL, SVG, HTML, YAML

## Project structure
```text
.
├── README.md                         # Portfolio overview and documentation (this file)
├── LICENSE                           # MIT license
├── requirements.txt                  # Python dependencies
├── pyproject.toml                    # Project metadata and pytest configuration
├── .gitignore
├── index.html                        # Portfolio landing page
├── .github/
│   └── workflows/
│       └── ci.yml                    # Root CI: validate, test, mock-eval smoke per project
├── docs/
│   ├── PORTFOLIO_OVERVIEW.md         # Technical overview, methodology, reconstruction notes
│   └── RESULTS_DASHBOARD.md          # Consolidated mock results summary
├── assets/
│   └── portfolio_results.svg         # Portfolio-level mock results chart
├── 01-biomedical-signals/
│   ├── README.md                     # Project-specific documentation
│   ├── questions/questions.jsonl     # 10 biomedical evaluation items
│   ├── verifiers.py                  # Independent answer recomputation (numpy/scipy)
│   ├── evalkit/                      # Schema/lint, grading, validation, mock eval, catalog
│   ├── docs/                         # Methodology, review checklist, revision log, catalog
│   ├── reports/                      # Mock oracle/trap reports (JSON/MD) and chart
│   ├── tests/                        # Dataset/domain sanity tests
│   └── .github/workflows/validate.yml
├── 02-security-standards/
│   ├── README.md
│   ├── questions/questions.jsonl     # 10 security/standards evaluation items
│   ├── verifiers.py                  # Independent answer recomputation (stdlib)
│   ├── evalkit/
│   ├── docs/
│   ├── reports/
│   ├── tests/
│   └── .github/workflows/validate.yml
└── 03-software-testing/
    ├── README.md
    ├── questions/questions.jsonl     # 10 software testing/quality evaluation items
    ├── verifiers.py                  # Independent answer recomputation (stdlib)
    ├── evalkit/
    ├── docs/
    ├── reports/
    ├── tests/
    └── .github/workflows/validate.yml
```

## Installation
### Requirements
- Python **3.10+** (3.11 recommended)
- `pip` and virtual environment support
- For biomedical numeric verifiers: `numpy` and `scipy`

### Setup
```bash
# 1) Clone the repository
git clone https://github.com/yazanus94-dot/AI-Research-Evaluation-Portfolio_Projects.git
cd AI-Research-Evaluation-Portfolio_Projects

# 2) Create and activate a virtual environment
python -m venv .venv
# Windows (PowerShell): .venv\Scripts\Activate.ps1
# Windows (cmd):       .venv\Scripts\activate.bat
# macOS/Linux:         source .venv/bin/activate

# 3) Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

## Usage
Run commands from inside a project directory (e.g. `02-security-standards`) unless noted.

```bash
# Validate a question set (lint, naive-answer rejection, verifier checks where available)
python -m evalkit.validate questions/questions.jsonl

# Run tests
python -m pytest -q
# or, where provided:
python tests/run_tests.py

# Run included mock evaluation harness
python -m evalkit.run_eval --questions questions/questions.jsonl --model mock-oracle --attempts 1
python -m evalkit.run_eval --questions questions/questions.jsonl --model mock-trap --attempts 1

# (Re)generate question catalog from questions.jsonl
python -m evalkit.catalog
```

**Project examples:**
```bash
cd 01-biomedical-signals && python -m evalkit.validate questions/questions.jsonl
cd 02-security-standards && python -m evalkit.validate questions/questions.jsonl
cd 03-software-testing  && python -m evalkit.validate questions/questions.jsonl
```

> **Note:** Biomedical code verifiers import `numpy`/`scipy`. Full numeric recomputation runs when these dependencies are installed (as in CI); validation tooling is designed to remain usable for schema/lint/consistency checks in minimal environments.

## Methodology
Each project follows a verification-first evaluation workflow:

1. **Item authoring:** Write self-contained questions with explicit conventions, units, precision, and a single unambiguous answer.
2. **Trap design:** Define a plausible shortcut/naive answer and the reasoning error that produces it.
3. **Independent verification:** Recompute answers in `verifiers.py` (code-verified) and/or cite normative sources/sections (source-verified/both).
4. **Quality checks:** Lint for ambiguity/hedging and ensure naive answers are not accepted by the grader/validator.
5. **Harness evaluation:** Run mock oracle/trap evaluations to confirm gradability and discriminative behavior; summarize pass rates and flags.
6. **Review & revision:** Apply reviewer checklists and record hardening/feedback in revision logs.

**Algorithms/workflow components (as implemented):** deterministic answer recomputation (e.g. HRV statistics, OTP/CVSS/entropy/birthday/Argon2/SemVer/BVA/SLO calculations), JSONL schema loading and lint rules, answer extraction/grading with tolerance/format handling, audit/validation pipeline, and mock-model evaluation/report generation.

See: [docs/PORTFOLIO_OVERVIEW.md](docs/PORTFOLIO_OVERVIEW.md), per-project `docs/methodology.md`, `docs/review-checklist.md`, and `docs/question-catalog.md`.

## Results
### Included mock evaluation summary (repository artifacts)
| Project | Items | `mock-oracle` pass rate | `mock-trap` pass rate | Notes |
|---|---:|---:|---:|---|
| 01 — Biomedical Signals | 10 (A01–A10) | 100% | 0% | Reference/harness check vs designed shortcut traps |
| 02 — Security Standards | 10 (SEC01–SEC10) | 100% | 0% | Standards/calculation items with discriminative traps |
| 03 — Software Testing | 10 (B01–B10) | 100% | 0% | Test-design/quality items with discriminative traps |

- **Detailed reports:** per-project `reports/results_mock-oracle.{json,md}` and `reports/results_mock-trap.{json,md}` (1 attempt/item).
- **Dashboard:** [docs/RESULTS_DASHBOARD.md](docs/RESULTS_DASHBOARD.md)
- **Visuals:** [assets/portfolio_results.svg](assets/portfolio_results.svg) and `*/reports/results_chart.svg`

> **Important:** These are **mock harness runs included as repository artifacts**, not measurements from real AI/LLM models. No real-model benchmark performance is claimed.

## Testing
- **Validation:** `python -m evalkit.validate questions/questions.jsonl` performs lint/schema checks, naive-answer rejection checks, and verifier recomputation where executable.
- **Automated tests:** per-project `tests/` cover dataset integrity and domain checks (e.g. item count/IDs, lint cleanliness, trap presence, extraction/grading behavior, and domain-specific vectors/calculations where applicable).
- **Continuous Integration:** [.github/workflows/ci.yml](.github/workflows/ci.yml) runs validation, tests, and mock-eval smoke checks across projects on push/PR (matrix).

## Limitations
- **Mock-only reported results:** included pass rates come from `mock-oracle`/`mock-trap` harness runs, not real-model evaluations.
- **Demonstration scale:** 10 items per domain; not a statistically comprehensive benchmark.
- **Partial artifact reconstruction:** the original repository was ZIP-only and some referenced source artifacts were incomplete. To restore a coherent, browsable portfolio, `questions/questions.jsonl` and compatible `evalkit` components were reconstructed from included catalogs, verifiers, docs, and reports (documented in [docs/PORTFOLIO_OVERVIEW.md](docs/PORTFOLIO_OVERVIEW.md)). Reconstructions are best-effort and aligned to available artifacts, not a claim of original upstream provenance.
- **Environment dependencies:** biomedical verifiers require `numpy`/`scipy` for full numeric execution.
- **Standards drift:** source-cited items (NIST/CVSS/RFC/ISTQB/SemVer, etc.) should be re-checked against the latest normative documents before external reliance.

## Future improvements
- Add larger, versioned question banks with per-item provenance and difficulty calibration.
- Run and publish measured evaluations against real model targets (model IDs, dates, prompts/configs, attempt counts).
- Expand property-based/domain tests and strengthen schema/CI quality gates.
- Generate richer analytics/figures from real runs and publish a hosted dashboard (e.g. GitHub Pages).
- Incorporate peer review and track item-level revisions with before/after pass-rate evidence.

## References
**Standards, papers, and sources reflected in included artifacts:**
- Pan J, Tompkins WJ. *A Real-Time QRS Detection Algorithm.* IEEE Trans Biomed Eng, 1985. https://people.ece.cornell.edu/land/courses/ece5030/labs/s2014/Pan_Tompkins.pdf
- RFC 4226 — HOTP: https://datatracker.ietf.org/doc/html/rfc4226
- RFC 6238 — TOTP: https://datatracker.ietf.org/doc/html/rfc6238
- RFC 8259 — JSON: https://datatracker.ietf.org/doc/html/rfc8259#section-4
- RFC 9106 — Argon2: https://datatracker.ietf.org/doc/html/rfc9106
- FIRST CVSS v3.1 Specification: https://www.first.org/cvss/v3.1/specification-document
- NIST SP 800-63B-4 (Digital Identity Guidelines): https://pages.nist.gov/800-63-4/sp800-63b/authenticators
- ISTQB Boundary Value Analysis (white paper): https://istqb.org/wp-content/uploads/2025/10/Boundary-Value-Analysis-white-paper.pdf
- Semantic Versioning 2.0.0: https://semver.org/
- Jia Y, Harman M. *An Analysis and Survey of the Development of Mutation Testing.* IEEE TSE, 2011.

**Repository resources:** [docs/PORTFOLIO_OVERVIEW.md](docs/PORTFOLIO_OVERVIEW.md), [docs/RESULTS_DASHBOARD.md](docs/RESULTS_DASHBOARD.md), per-project `docs/question-catalog.md` and `docs/methodology.md`.

## License
This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

**Author:** [Yazan Aljabari](https://www.linkedin.com/in/yazan-aljabari-878202139/)  
**Repository:** https://github.com/yazanus94-dot/AI-Research-Evaluation-Portfolio_Projects
