"""Low-false-positive detection metrics (CLAUDE.md §2: never accuracy).

Conventions: `y` is 1 for attack, 0 for benign; `s` is the anomaly score
(higher = more anomalous); an alert is `s >= tau`.
"""

from __future__ import annotations

import numpy as np
from sklearn.metrics import roc_auc_score, roc_curve

SECONDS_PER_DAY = 86_400


def tpr_at_fpr(y: np.ndarray, s: np.ndarray, max_fpr: float) -> float:
    """Highest TPR on the ROC curve whose FPR does not exceed `max_fpr`.

    With n benign samples the FPR resolution is 1/n; below that this is the TPR
    at zero false positives.
    """
    y, s = np.asarray(y), np.asarray(s)
    if y.min() == y.max():
        return float("nan")
    fpr, tpr, _ = roc_curve(y, s)
    ok = fpr <= max_fpr
    return float(tpr[ok].max()) if ok.any() else 0.0


def partial_auc(y: np.ndarray, s: np.ndarray, max_fpr: float) -> float:
    """Standardised partial AUC over FPR in [0, max_fpr] (McClish correction; 0.5 = random)."""
    y = np.asarray(y)
    if y.min() == y.max():
        return float("nan")
    return float(roc_auc_score(y, s, max_fpr=max_fpr))


def threshold_for_fpr(benign_scores: np.ndarray, fpr: float) -> float:
    """Alert threshold set on benign validation scores only (no attack data, CLAUDE.md §8).

    The lowest threshold at which at most floor(fpr * n) validation samples alert
    (alert = score >= tau). Ties matter (D28): if several validation scores equal
    the candidate cut, all of them would alert, so the cut moves up to the next
    distinct score, or just above the maximum.
    """
    s = np.sort(np.asarray(benign_scores, dtype=float))
    if len(s) == 0:
        raise ValueError("need benign validation scores to set a threshold")
    n = len(s)
    k = int(np.floor(fpr * n))
    if k == 0:
        return float(np.nextafter(s[-1], np.inf))
    tau = s[n - k]
    if n - np.searchsorted(s, tau, side="left") > k:  # ties at the cut would exceed the budget
        above = s[s > tau]
        return float(above[0]) if len(above) else float(np.nextafter(s[-1], np.inf))
    return float(tau)


def threshold_for_alarm_rate(benign_scores: np.ndarray, alarms_per_day: float, window_s: float) -> float:
    """Threshold for a target number of false alarms per day of windows (see threshold_for_fpr)."""
    return threshold_for_fpr(benign_scores, alarms_per_day * window_s / SECONDS_PER_DAY)


def false_alarms_per_day(benign_scores: np.ndarray, tau: float, window_s: float) -> float:
    s = np.asarray(benign_scores, dtype=float)
    if len(s) == 0:
        return float("nan")
    return float((s >= tau).sum() / (len(s) * window_s / SECONDS_PER_DAY))


def detection_rate(attack_scores: np.ndarray, tau: float) -> float:
    s = np.asarray(attack_scores, dtype=float)
    return float((s >= tau).mean()) if len(s) else float("nan")


def persist_min(scores: np.ndarray, starts: np.ndarray, window_s: float, k: int) -> np.ndarray:
    """Causal k-window persistence (D40): each window's score becomes the minimum over itself and the
    previous k - 1 windows, if they follow it without a time gap (fewer after a gap or at the start).

    An isolated benign spike is cut to its neighbours' level; an attack that lasts k windows or more keeps
    its level from its k-th window on. On a router it is a ring buffer of k - 1 scores per device.
    """
    s = np.asarray(scores, dtype=float)
    starts = np.asarray(starts, dtype=float)
    out = s.copy()
    run = 1  # length of the contiguous run ending at i
    for i in range(1, len(s)):
        run = run + 1 if starts[i] - starts[i - 1] <= window_s * 1.5 else 1
        m = min(run, k)
        out[i] = s[i - m + 1: i + 1].min()
    return out


def persist_strict(scores: np.ndarray, starts: np.ndarray, window_s: float, k: int) -> np.ndarray:
    """Strict k-window persistence (D53): the minimum over the last k windows once k consecutive windows
    have been observed, NaN before that (stream start, or after a time gap).

    D40's version falls back to fewer windows after a gap, so the first window after a recording gap was
    judged on itself alone, exactly where capture artefacts sit (inter-arrival times spanning the gap).
    A router that just restarted has no history either; it waits for k windows of evidence.
    """
    s = np.asarray(scores, dtype=float)
    starts = np.asarray(starts, dtype=float)
    out = np.full(len(s), np.nan)
    run = 0
    for i in range(len(s)):
        run = run + 1 if i > 0 and starts[i] - starts[i - 1] <= window_s * 1.5 else 1
        if run >= k:
            out[i] = s[i - k + 1: i + 1].min()
    return out


def strict_dual_alarm_score(scores: np.ndarray, starts: np.ndarray, window_s: float, k: int, known: np.ndarray,
                            val: np.ndarray, alarms_per_day: float, margin: float) -> np.ndarray:
    """Two label-free alarm channels folded into one score that alarms at >= 0 (D53):

    persistent  strict k-window minimum above max(validation threshold for `alarms_per_day`, just above
                its largest bootstrap value), as D47 does for the raw score
    raw         a single window more anomalous than every bootstrap and validation window, plus `margin`
                (strong but intermittent attacks that dip below the persistent level)

    `known` marks bootstrap rows, `val` validation rows. Windows without k windows of history have no
    persistent channel; the raw channel still applies, so the folded score is always finite.
    """
    s = np.asarray(scores, dtype=float)
    p = persist_strict(s, starts, window_s, k)
    pv = p[val & np.isfinite(p)]
    pb = p[known & np.isfinite(p)]
    t_per = threshold_for_alarm_rate(pv, alarms_per_day, window_s) if len(pv) else np.inf
    if len(pb):
        t_per = max(t_per, float(np.nextafter(pb.max(), np.inf)))
    t_raw = float(np.nextafter(s[known | val].max(), np.inf)) + margin
    return np.maximum(np.where(np.isfinite(p), p - t_per, -np.inf), s - t_raw)


def attack_events(starts: np.ndarray, y: np.ndarray, window_s: float) -> list[np.ndarray]:
    """Index arrays of attack episodes: runs of attack windows that follow each other in time."""
    starts, y = np.asarray(starts, dtype=float), np.asarray(y)
    idx = np.flatnonzero(y == 1)
    if len(idx) == 0:
        return []
    breaks = np.flatnonzero(np.diff(starts[idx]) > window_s * 1.5) + 1
    return np.split(idx, breaks)


def event_detection_rate(starts: np.ndarray, y: np.ndarray, s: np.ndarray, tau: float,
                         window_s: float) -> tuple[float, int]:
    """Share of attack episodes with at least one alerting window while the attack runs, and the count.

    This is what an operator sees: the attack was flagged (per-window detection is stricter,
    because every 30 s of a 10-minute attack must alert to reach 100%).
    """
    events = attack_events(starts, y, window_s)
    if not events:
        return float("nan"), 0
    s = np.asarray(s, dtype=float)
    return float(np.mean([(s[e] >= tau).any() for e in events])), len(events)


def time_to_detect(starts: np.ndarray, y: np.ndarray, s: np.ndarray, tau: float) -> float:
    """Seconds from the first attack window's start to the first alerting attack window (nan if never)."""
    starts, y, s = np.asarray(starts), np.asarray(y), np.asarray(s)
    attack = np.flatnonzero(y == 1)
    if len(attack) == 0:
        return float("nan")
    hits = attack[s[attack] >= tau]
    return float(starts[hits[0]] - starts[attack[0]]) if len(hits) else float("nan")
