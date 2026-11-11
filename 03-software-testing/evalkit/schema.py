"""Question schema, loading, and linting."""
from __future__ import annotations
import json, re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, List

@dataclass
class Question:
    id: str
    topic: str
    question: str
    answer: Any
    rationale: str = ""
    shortcut_trap: str = ""
    naive_answer: Any = None
    verification: str = ""
    verifier: str = ""
    sources: List[dict] = field(default_factory=list)
    tolerance: Any = None

    @staticmethod
    def from_dict(d: dict) -> "Question":
        return Question(
            id=str(d.get("id","")),
            topic=str(d.get("topic","")),
            question=str(d.get("question","")),
            answer=d.get("answer"),
            rationale=str(d.get("rationale","")),
            shortcut_trap=str(d.get("shortcut_trap","")),
            naive_answer=d.get("naive_answer"),
            verification=str(d.get("verification","")),
            verifier=str(d.get("verifier","")),
            sources=list(d.get("sources") or []),
            tolerance=d.get("tolerance"),
        )

def load_questions(path) -> List[Question]:
    p = Path(path)
    items = []
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            items.append(Question.from_dict(json.loads(line)))
    return items

_HEDGE = re.compile(r"\b(many|roughly|approximately|about|best|usually|often|sometimes)\b", re.I)

def lint(q: Question) -> List[str]:
    errs = []
    if not q.id: errs.append("missing id")
    if not q.question.strip(): errs.append("empty question")
    if q.answer is None or q.answer == "": errs.append("missing answer")
    if not q.rationale.strip(): errs.append("missing rationale")
    if not q.shortcut_trap.strip(): errs.append("missing shortcut_trap")
    if q.naive_answer is None or q.naive_answer == "": errs.append("missing naive_answer")
    if _HEDGE.search(q.question):
        errs.append("hedge word in question")
    if q.verification in ("code","both") and not q.verifier:
        errs.append("code/both verification requires verifier")
    return errs
