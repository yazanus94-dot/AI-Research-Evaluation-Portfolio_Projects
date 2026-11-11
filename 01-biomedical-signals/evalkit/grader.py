"""Answer extraction and grading utilities."""
from __future__ import annotations
import re


def fmt_answer(a):
    if isinstance(a, list):
        return ", ".join(str(x) for x in a)
    if isinstance(a, float):
        s = f"{a:.10f}".rstrip("0").rstrip(".")
        return s or "0"
    return str(a)


def extract(text: str) -> str:
    if text is None:
        return ""
    matches = list(re.finditer(r"FINAL ANSWER:\s*(.+)", text, flags=re.I))
    if matches:
        return matches[-1].group(1).strip().strip("`")
    lines = [ln.strip() for ln in text.strip().splitlines() if ln.strip()]
    return lines[-1] if lines else ""


def _norm_num(s):
    try:
        return float(str(s).replace(",", "").strip())
    except Exception:
        return None


def is_correct(extracted, answer, tolerance=None) -> bool:
    if isinstance(answer, list):
        if isinstance(extracted, list):
            return [str(x).strip() for x in extracted] == [str(x).strip() for x in answer]
        e2 = re.sub(r"\s+", " ", str(extracted)).strip().lower()
        a2 = re.sub(r"\s+", " ", ", ".join(str(x) for x in answer)).strip().lower()
        return e2 == a2
    e = str(extracted).strip()
    a = str(answer).strip()
    if e == a:
        return True
    # leading-zero string answer (e.g. OTP code) must match exactly
    if re.fullmatch(r"0\d+", a):
        return e == a
    en = _norm_num(e)
    an = _norm_num(a)
    if en is not None and an is not None:
        tol = 0.0
        if isinstance(tolerance, (int, float)):
            tol = float(tolerance)
        if tol == 0.0 and ("." in a or "." in e):
            dec = len(a.split(".")[-1]) if "." in a else 0
            tol = 0.5 * 10 ** (-dec) if dec else 1e-9
        return abs(en - an) <= tol + 1e-12
    e2 = re.sub(r"\s+", " ", e).strip().lower().strip(".")
    a2 = re.sub(r"\s+", " ", a).strip().lower().strip(".")
    return e2 == a2


def grade(extracted, answer, tolerance=None):
    return is_correct(extracted, answer, tolerance)
