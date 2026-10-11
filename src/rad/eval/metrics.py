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


def time_to_detect(starts: np.ndarray, y: np.ndarray, s: np.ndarray, tau: float) -> float:
    """Seconds from the first attack window's start to the first alerting attack window (nan if never)."""
    starts, y, s = np.asarray(starts), np.asarray(y), np.asarray(s)
    attack = np.flatnonzero(y == 1)
    if len(attack) == 0:
        return float("nan")
    hits = attack[s[attack] >= tau]
    return float(starts[hits[0]] - starts[attack[0]]) if len(hits) else float("nan")
