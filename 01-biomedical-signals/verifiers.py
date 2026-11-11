"""Independent recomputation of every computed answer in questions/questions.jsonl.

Each function derives the answer from first principles (no answer key is read), so a mistake in the key
or in the question wording shows up as a mismatch in `python -m evalkit.validate`.
"""
import math
import statistics

import numpy as np
from scipy import signal

RR = [800, 810, 790, 830, 760, 800, 845, 790]  # NN intervals in ms used by A01-A03, A09


def _diffs(rr):
    return [b - a for a, b in zip(rr, rr[1:])]


def rmssd(rr=RR):
    d = _diffs(rr)
    return math.sqrt(sum(x * x for x in d) / len(d))


def rmssd_wrong_denominator(rr=RR):
    d = _diffs(rr)
    return math.sqrt(sum(x * x for x in d) / len(rr))


def sdnn(rr=RR):
    return statistics.stdev(rr)  # sample SD, n-1


def sdnn_population(rr=RR):
    return statistics.pstdev(rr)


def pnn50_total_intervals(rr=RR):
    nn50 = sum(1 for x in _diffs(rr) if abs(x) > 50)
    return 100.0 * nn50 / len(rr)


def pnn50_over_differences(rr=RR):
    d = _diffs(rr)
    return 100.0 * sum(1 for x in d if abs(x) > 50) / len(d)


def jensen_gap_bpm(rr=(600, 1200)):
    mean_of_rates = statistics.fmean(60000 / x for x in rr)
    rate_of_mean = 60000 / statistics.fmean(rr)
    return mean_of_rates - rate_of_mean


def alias_frequency(f=60, fs=90):
    return abs(f - round(f / fs) * fs)


def filtfilt_attenuation_db():
    """Gain of sosfiltfilt at the lower -3 dB edge, derived from the frequency response (|H|^2)."""
    sos = signal.butter(4, [5, 15], btype="bandpass", fs=100, output="sos")
    _, h = signal.sosfreqz(sos, worN=[5.0], fs=100)
    return -20 * math.log10(abs(h[0]) ** 2)


def single_pass_attenuation_db():
    sos = signal.butter(4, [5, 15], btype="bandpass", fs=100, output="sos")
    _, h = signal.sosfreqz(sos, worN=[5.0], fs=100)
    return -20 * math.log10(abs(h[0]))


def welch_lf_bins():
    f = np.fft.rfftfreq(256, d=1 / 4)  # 4 Hz resampled tachogram, nperseg=256
    return int(np.sum((f >= 0.04) & (f <= 0.15)))


def rr_quantisation_max_ms(fs=250):
    """Max |error| of an RR interval when both peak times are rounded to the nearest sample (grid search)."""
    u = np.linspace(-0.5, 0.5, 1001)           # each peak's rounding error in samples
    worst = np.abs(u[:, None] - u[None, :]).max()
    return worst * 1000.0 / fs


def sd1(rr=RR):
    return math.sqrt(0.5 * statistics.variance(_diffs(rr)))


def sd1_via_rmssd(rr=RR):
    return rmssd(rr) / math.sqrt(2)


def window_samples(fs_new=360, width_ms=150.0):
    return round(width_ms / 1000.0 * fs_new)


EXPECTED = {
    "rmssd": rmssd, "sdnn": sdnn, "pnn50_total_intervals": pnn50_total_intervals, "jensen_gap_bpm": jensen_gap_bpm,
    "alias_frequency": alias_frequency, "filtfilt_attenuation_db": filtfilt_attenuation_db, "welch_lf_bins": welch_lf_bins,
    "rr_quantisation_max_ms": rr_quantisation_max_ms, "sd1": sd1, "window_samples": window_samples,
}

if __name__ == "__main__":
    for name, fn in EXPECTED.items():
        print(f"{name:28s} {fn()}")
    print("naive: rmssd/n", rmssd_wrong_denominator(), "| sdnn pop", sdnn_population(), "| pnn50 /diffs", pnn50_over_differences(),
          "| single pass dB", single_pass_attenuation_db(), "| sd1 via rmssd", sd1_via_rmssd())
