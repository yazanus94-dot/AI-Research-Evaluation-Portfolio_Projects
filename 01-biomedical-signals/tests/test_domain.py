import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

def test_rmssd_denominator_is_n_minus_1():
    import verifiers
    d = [b - a for a, b in zip(verifiers.RR, verifiers.RR[1:])]
    assert len(d) == len(verifiers.RR) - 1
    assert abs(verifiers.EXPECTED["rmssd"]() - (sum(x*x for x in d)/len(d))**0.5) < 1e-9

def test_alias_formula():
    import verifiers
    assert verifiers.EXPECTED["alias_frequency"]() == abs(60 - 90)
