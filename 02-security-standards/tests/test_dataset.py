"""Dataset quality tests. Run: python -m pytest -q   (or python tests/run_tests.py without pytest)"""
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from evalkit.schema import load_questions, lint
from evalkit.grader import extract, grade
from evalkit.validate import audit
from evalkit.llm import get_model
from evalkit.run_eval import run

Q = ROOT / "questions" / "questions.jsonl"

def test_ten_questions():
    assert len(load_questions(Q)) == 10

def test_ids_unique():
    ids = [q.id for q in load_questions(Q)]
    assert len(ids) == len(set(ids))

def test_lint_clean():
    for q in load_questions(Q):
        assert lint(q) == [], (q.id, lint(q))

def test_audit_clean():
    assert audit(Q) == []

def test_every_question_has_trap():
    for q in load_questions(Q):
        assert q.shortcut_trap and q.naive_answer is not None

def test_extract_last_final_answer():
    assert extract("FINAL ANSWER: 1\nthinking\nFINAL ANSWER: 2") == "2"

def test_oracle_passes_all_and_trap_fails_all(tmp_path):
    a = run(Q, "mock-oracle", attempts=1, out_dir=tmp_path)
    b = run(Q, "mock-trap", attempts=1, out_dir=tmp_path)
    assert a["overall_pass_rate"] == 1.0
    assert b["overall_pass_rate"] == 0.0
