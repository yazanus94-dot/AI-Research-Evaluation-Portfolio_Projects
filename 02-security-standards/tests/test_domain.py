import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

def test_rfc4226_vectors():
    import verifiers
    rfc = ["755224","287082","359152","969429","338314","254676","287922","162583","399871","520489"]
    assert [verifiers.hotp(b"12345678901234567890", i) for i in range(10)] == rfc

def test_rfc6238_sha1_vector():
    import verifiers
    assert verifiers.EXPECTED["totp_1111111109"]() == "07081804"
