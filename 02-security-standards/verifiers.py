"""Independent recomputation of every computed answer in questions/questions.jsonl (standard library only)."""
import hashlib
import hmac
import math
import struct

SECRET = b"12345678901234567890"          # ASCII test secret used by RFC 4226 App. D and RFC 6238 App. B (SHA-1)


def hotp(secret: bytes, counter: int, digits: int = 6, algo=hashlib.sha1) -> str:
    mac = hmac.new(secret, struct.pack(">Q", counter), algo).digest()
    off = mac[-1] & 0x0F
    snum = struct.unpack(">I", mac[off:off + 4])[0] & 0x7FFFFFFF          # keep the last 31 bits
    return str(snum % 10 ** digits).zfill(digits)


def totp(secret: bytes, unix_time: int, step: int = 30, t0: int = 0, digits: int = 8, algo=hashlib.sha1) -> str:
    return hotp(secret, (unix_time - t0) // step, digits, algo)


def hotp_counter_5():
    return hotp(SECRET, 5)


def totp_1111111109():
    return totp(SECRET, 1111111109, digits=8)


def time_step(unix_time=1234567910, step=30):
    return unix_time // step


def entropy_gap_bits():
    return 12 * math.log2(94) - 6 * math.log2(7776)


def birthday_50pct_billions(bits=64):
    n_space = 2.0 ** bits
    lo, hi = 1.0, 2.0 ** (bits / 2 + 2)
    for _ in range(200):                          # bisection on P(collision) = 1 - exp(-n(n-1)/2N) = 0.5
        mid = (lo + hi) / 2
        p = 1 - math.exp(-mid * (mid - 1) / (2 * n_space))
        lo, hi = (mid, hi) if p < 0.5 else (lo, mid)
    return lo / 1e9


# ---- CVSS v3.1 base score (equations from the FIRST CVSS v3.1 specification) ----
_W = {"AV": {"N": .85, "A": .62, "L": .55, "P": .2}, "AC": {"L": .77, "H": .44}, "UI": {"N": .85, "R": .62},
      "CIA": {"H": .56, "L": .22, "N": 0.0}}
_PR = {"U": {"N": .85, "L": .62, "H": .27}, "C": {"N": .85, "L": .68, "H": .5}}


def _roundup(x: float) -> float:
    i = round(x * 100000)
    return i / 100000.0 if i % 10000 == 0 else (math.floor(i / 10000) + 1) / 10.0


def cvss31_base(vector: str) -> float:
    m = dict(p.split(":") for p in vector.split("/")[1:])
    iss = 1 - (1 - _W["CIA"][m["C"]]) * (1 - _W["CIA"][m["I"]]) * (1 - _W["CIA"][m["A"]])
    changed = m["S"] == "C"
    impact = 7.52 * (iss - 0.029) - 3.25 * (iss - 0.02) ** 15 if changed else 6.42 * iss
    expl = 8.22 * _W["AV"][m["AV"]] * _W["AC"][m["AC"]] * _PR["C" if changed else "U"][m["PR"]] * _W["UI"][m["UI"]]
    if impact <= 0:
        return 0.0
    return _roundup(min((1.08 if changed else 1.0) * (impact + expl), 10))


def cvss_scope_changed_priv_low():
    return cvss31_base("CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H")


def cvss_reflected_xss():
    return cvss31_base("CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N")


def hotp_zero_code_count(digits=6):
    mod = 10 ** digits
    return (2 ** 31 - 1) // mod + 1               # integers n in [0, 2^31) with n % mod == 0


def argon2_first_option_mib():
    return 2 ** 21 / 1024                         # m is in KiB (2^21 KiB)


EXPECTED = {
    "hotp_counter_5": hotp_counter_5, "totp_1111111109": totp_1111111109, "time_step": time_step,
    "entropy_gap_bits": entropy_gap_bits, "birthday_50pct_billions": birthday_50pct_billions,
    "cvss_scope_changed_priv_low": cvss_scope_changed_priv_low, "cvss_reflected_xss": cvss_reflected_xss,
    "hotp_zero_code_count": hotp_zero_code_count, "argon2_first_option_mib": argon2_first_option_mib,
}

if __name__ == "__main__":
    for name, fn in EXPECTED.items():
        print(f"{name:30s} {fn()}")
    print("RFC4226 App.D counts 0-9:", [hotp(SECRET, c) for c in range(10)])
    print("RFC6238 App.B SHA1:", [(t, totp(SECRET, t)) for t in (59, 1111111109, 1111111111, 1234567890, 2000000000)])
    print("cvss 9.8 check:", cvss31_base("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"),
          "| scope-unchanged variant:", cvss31_base("CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H"),
          "| xss S:U variant:", cvss31_base("CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:L/A:N"), "| 2^32 billions:", 2**32/1e9)
