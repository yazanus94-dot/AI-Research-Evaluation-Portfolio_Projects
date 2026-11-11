import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

def test_semver_not_lexical():
    import verifiers
    assert verifiers.EXPECTED["semver_sorted"]()[-1] == "1.0.0"
    assert verifiers.EXPECTED["semver_sorted"]().index("1.0.0-beta.2") < verifiers.EXPECTED["semver_sorted"]().index("1.0.0-beta.11")

def test_pairwise_lower_bound():
    import verifiers
    assert verifiers.EXPECTED["pairwise_minimum"]() == 3 * 3
