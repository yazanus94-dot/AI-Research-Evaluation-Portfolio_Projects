"""Minimal evaluation harness with mock models (oracle/trap)."""
from __future__ import annotations
import json, argparse
from datetime import datetime, timezone
from pathlib import Path
from .schema import load_questions
from .grader import extract, is_correct, fmt_answer

def _model_answer(q, model: str) -> str:
    m = (model or "").lower()
    if m in ("mock-oracle","oracle"):
        return f"FINAL ANSWER: {fmt_answer(q.answer)}"
    if m in ("mock-trap","trap"):
        return f"FINAL ANSWER: {fmt_answer(q.naive_answer)}"
    return ""

def run(questions_path, model="mock-oracle", attempts=1, out_dir="reports", too_easy_threshold=0.67):
    qpath = Path(questions_path)
    qs = load_questions(qpath)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    items = []
    flagged = []
    total_correct = 0
    total = 0
    for q in qs:
        att = []
        correct_n = 0
        for i in range(attempts):
            raw = _model_answer(q, model)
            ex = extract(raw)
            ok = is_correct(ex, q.answer, q.tolerance)
            if ok: correct_n += 1
            att.append({"extracted": ex, "correct": ok})
        pr = correct_n / attempts if attempts else 0.0
        too_easy = pr >= too_easy_threshold
        if too_easy: flagged.append(q.id)
        total_correct += correct_n; total += attempts
        items.append({"id": q.id, "topic": q.topic, "pass_rate": round(pr, 4), "too_easy": too_easy, "attempts": att})
    overall = (total_correct / total) if total else 0.0
    result = {
        "model": model, "attempts": attempts, "too_easy_threshold": too_easy_threshold,
        "run_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "overall_pass_rate": round(overall, 4), "flagged_too_easy": flagged, "items": items
    }
    stem = f"results_{model.replace(':','_')}"
    (out_dir / f"{stem}.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [f"# Results: {model}", "", f"Overall pass rate: **{overall*100:.0f}%** ({attempts} attempts/item). Items at or above {int(too_easy_threshold*100)}% are flagged for hardening.", "", "| ID | Topic | Pass rate | Flag |", "|---|---|---|---|"]
    for it in items:
        lines.append(f"| {it['id']} | {it['topic']} | {it['pass_rate']*100:.0f}% | {'too easy' if it['too_easy'] else ''} |")
    (out_dir / f"{stem}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return result

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--questions", default="questions/questions.jsonl")
    ap.add_argument("--model", default="mock-oracle")
    ap.add_argument("--attempts", type=int, default=1)
    ap.add_argument("--out-dir", default="reports")
    ap.add_argument("--too-easy-threshold", type=float, default=0.67)
    args = ap.parse_args(argv)
    r = run(args.questions, args.model, args.attempts, args.out_dir, args.too_easy_threshold)
    print(json.dumps({"model": r["model"], "overall_pass_rate": r["overall_pass_rate"], "flagged": r["flagged_too_easy"]}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
