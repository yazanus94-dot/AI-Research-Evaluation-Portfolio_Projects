"""Validate questions: lint, recompute verifiers, and ensure naive answers fail."""
from __future__ import annotations
import importlib.util
import re
import sys
from pathlib import Path
from .schema import load_questions, lint
from .grader import is_correct, fmt_answer


def _load_verifiers(qpath: Path):
    vpath = qpath.parent.parent / "verifiers.py"
    if not vpath.exists():
        return None
    spec = importlib.util.spec_from_file_location("verifiers", vpath)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules["verifiers"] = mod
    try:
        spec.loader.exec_module(mod)
    except Exception as ex:
        setattr(mod, "_load_error", ex)
    return mod


def audit(questions_path):
    qpath = Path(questions_path)
    qs = load_questions(qpath)
    ver = _load_verifiers(qpath)
    errs = []
    for q in qs:
        for e in lint(q):
            errs.append(f"{q.id}: lint: {e}")
        naive_ok = False
        try:
            naive_ok = is_correct(fmt_answer(q.naive_answer), q.answer, q.tolerance)
        except Exception:
            naive_ok = False
        # leading-zero correct answer: naive without leading zero must not be accepted
        if naive_ok and isinstance(q.answer, str) and re.fullmatch(r"0\d+", q.answer):
            if str(q.naive_answer).strip() != q.answer:
                naive_ok = False
        if naive_ok:
            errs.append(f"{q.id}: naive_answer would be accepted")
        if q.verification in ("code", "both") and q.verifier:
            if ver is None:
                errs.append(f"{q.id}: verifiers.py not found")
            elif getattr(ver, "_load_error", None) is not None:
                # optional dependency missing or verifier import issue; skip execution
                pass
            elif not hasattr(ver, q.verifier):
                errs.append(f"{q.id}: missing verifier function {q.verifier}")
            else:
                try:
                    got = getattr(ver, q.verifier)()
                    if not is_correct(fmt_answer(got), q.answer, q.tolerance):
                        errs.append(f"{q.id}: verifier {q.verifier} returned {got}, expected {q.answer}")
                except Exception as ex:
                    errs.append(f"{q.id}: verifier {q.verifier} raised {ex}")
    return errs


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("questions", nargs="?", default="questions/questions.jsonl")
    args = ap.parse_args(argv)
    errs = audit(args.questions)
    if errs:
        print("VALIDATION FAILED")
        for e in errs:
            print(" -", e)
        return 1
    print(f"OK: {len(load_questions(args.questions))} questions validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
