# Methodology

## 1. Write the question
* Self-contained: all data, conventions and units are in the question. If two conventions exist (for example pNN50 denominators), the question picks one.
* One unambiguous answer with a stated precision and tolerance. Hedge words ("many", "roughly", "best") are rejected by the linter.
* Requires multi-step reasoning or exact knowledge of a standard. Pure recall that a search engine answers in one query is avoided.

## 2. Design the shortcut
For each item, write down the tempting wrong answer (`naive_answer`) and why a model or person would produce it (`shortcut_trap`). Typical traps: wrong denominator, library default, off-by-one, rounding instead of flooring, remembered value from an older revision of a standard.

## 3. Verify
* **code**: `verifiers.py` recomputes the answer without reading the question file; `evalkit.validate` fails if it disagrees, or if the naive answer would also be accepted.
* **source**: the answer is quoted or derived from a cited section (title, locator, URL where available).
* **both**: code reproduces the number the source defines.

## 4. Test and harden
Run `evalkit.run_eval` with several attempts per item against the target model(s). Flag items that are too easy, rewrite, re-verify, and log the change.

## 5. Review
Apply `docs/review-checklist.md`. Integrate reviewer feedback in `docs/revision-log.md` with before/after wording.
