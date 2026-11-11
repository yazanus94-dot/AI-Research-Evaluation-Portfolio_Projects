"""Independent recomputation of every computed answer in questions/questions.jsonl (standard library only)."""
import itertools
import math

SEMVER_INPUT = ["1.0.0-rc.1", "1.0.0-beta.11", "1.0.0", "1.0.0-alpha.beta", "1.0.0-beta", "1.0.0-alpha", "1.0.0-beta.2", "1.0.0-alpha.1"]


def three_value_bva_count(lo=18, hi=65):
    return len({lo - 1, lo, lo + 1, hi - 1, hi, hi + 1})


def suite_failure_probability_pct(n=300, p_pass=0.995):
    return 100 * (1 - p_pass ** n)


def _semver_key_cmp(a: str, b: str) -> int:
    """SemVer 2.0.0 section 11 precedence (build metadata ignored)."""
    def split(v):
        core, _, pre = v.split("+")[0].partition("-")
        return tuple(int(x) for x in core.split(".")), (pre.split(".") if pre else None)
    (ca, pa), (cb, pb) = split(a), split(b)
    if ca != cb:
        return -1 if ca < cb else 1
    if pa is None and pb is None:
        return 0
    if pa is None:
        return 1            # a release outranks any of its pre-releases
    if pb is None:
        return -1
    for x, y in zip(pa, pb):
        if x == y:
            continue
        xn, yn = x.isdigit(), y.isdigit()
        if xn and yn:
            return -1 if int(x) < int(y) else 1
        if xn != yn:
            return -1 if xn else 1   # numeric identifiers rank lower than alphanumeric
        return -1 if x < y else 1
    return (len(pa) > len(pb)) - (len(pa) < len(pb))


def semver_sorted(versions=SEMVER_INPUT):
    import functools
    return sorted(versions, key=functools.cmp_to_key(_semver_key_cmp))


def lexical_sorted(versions=SEMVER_INPUT):
    return sorted(versions)


def two_value_bva_coverage_pct(lo=6, hi=15, tests=(5, 6, 10, 15)):
    items = {lo - 1, lo, hi, hi + 1}
    return 100 * len(items & set(tests)) / len(items)


def three_value_bva_coverage_pct(lo=6, hi=15, tests=(4, 6, 8, 14, 15)):
    items = {lo - 1, lo, lo + 1, hi - 1, hi, hi + 1}
    return 100 * len(items & set(tests)) / len(items)


def pairwise_minimum(domains=(3, 3, 3)):
    """Lower bound = product of the two largest domains; verify it is achievable for 3x3x3 with an orthogonal array."""
    lower = math.prod(sorted(domains)[-2:])
    if tuple(domains) == (3, 3, 3):
        rows = [(a, b, (a + b) % 3) for a in range(3) for b in range(3)]        # OA(9,3,3,2)
        for i, j in itertools.combinations(range(3), 2):
            assert len({(r[i], r[j]) for r in rows}) == 9, "not all pairs covered"
        assert len(rows) == lower
    return lower


def mutation_score_pct(total=56, equivalent=6, killed=42):
    return 100 * killed / (total - equivalent)


def passes_needed(fail_p=0.05, alpha=0.05):
    return math.ceil(math.log(alpha) / math.log(1 - fail_p))


def slo_downtime_minutes(slo=0.999, days=30):
    return (1 - slo) * days * 24 * 60


EXPECTED = {
    "three_value_bva_count": three_value_bva_count, "suite_failure_probability_pct": suite_failure_probability_pct,
    "semver_sorted": semver_sorted, "two_value_bva_coverage_pct": two_value_bva_coverage_pct,
    "three_value_bva_coverage_pct": three_value_bva_coverage_pct, "pairwise_minimum": pairwise_minimum,
    "mutation_score_pct": mutation_score_pct, "passes_needed": passes_needed, "slo_downtime_minutes": slo_downtime_minutes,
}

if __name__ == "__main__":
    for name, fn in EXPECTED.items():
        print(f"{name:32s} {fn()}")
    print("lexical:", lexical_sorted(), "| naive mutation", 100 * 42 / 56, "| rule of three", 3 / 0.05)
