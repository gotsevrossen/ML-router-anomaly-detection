"""Streaming alarm logic for the per-device pipeline (D53).

The strict dual alarm, window by window, as a router runs it: two channels, both calibrated on
benign data only (bootstrap and validation), with constant state (a ring buffer of k scores).

  persistent  the minimum of the last k scores, once k consecutive windows (no time gap) have been
              observed, is at least t_per = max(validation threshold for `alarms_per_day`, just above
              the largest bootstrap value of that minimum)
  raw         one score more anomalous than every bootstrap and validation window, plus `margin`

It reproduces rad.eval.metrics.strict_dual_alarm_score exactly (tested), so offline benchmarks and
the router agree.
"""

from __future__ import annotations

from collections import deque
from typing import Sequence

import numpy as np

from rad.eval import metrics as M


def calibrate_strict_dual(boot_starts: Sequence[float], boot_scores: Sequence[float], val_starts: Sequence[float],
                          val_scores: Sequence[float], k: int, window_s: float, alarms_per_day: float,
                          margin: float) -> tuple[float, float]:
    """(t_per, t_raw) from bootstrap (in-sample) and validation scores, as metrics.strict_dual_alarm_score."""
    starts = np.r_[np.asarray(boot_starts, float), np.asarray(val_starts, float)]
    s = np.r_[np.asarray(boot_scores, float), np.asarray(val_scores, float)]
    known = np.r_[np.ones(len(boot_scores), bool), np.zeros(len(val_scores), bool)]
    p = M.persist_strict(s, starts, window_s, k)
    pv, pb = p[~known & np.isfinite(p)], p[known & np.isfinite(p)]
    t_per = M.threshold_for_alarm_rate(pv, alarms_per_day, window_s) if len(pv) else np.inf
    if len(pb):
        t_per = max(t_per, float(np.nextafter(pb.max(), np.inf)))
    t_raw = float(np.nextafter(s.max(), np.inf)) + margin
    return float(t_per), t_raw


class StrictDualAlarm:
    """Window-by-window strict dual alarm. `update` returns (alert, raw_channel, persistent_channel)."""

    def __init__(self, k: int, t_per: float, t_raw: float, window_s: float = 30.0) -> None:
        if k < 1:
            raise ValueError("k must be >= 1")
        self.k, self.t_per, self.t_raw, self.window_s = int(k), float(t_per), float(t_raw), float(window_s)
        self.buf: deque[float] = deque(maxlen=self.k)
        self.last_t: float | None = None

    def update(self, t: float, score: float) -> tuple[bool, bool, bool]:
        if self.last_t is None or t - self.last_t > self.window_s * 1.5:
            self.buf.clear()  # a time gap: persistence starts over
        self.last_t = float(t)
        self.buf.append(float(score))
        raw = score >= self.t_raw
        persistent = len(self.buf) == self.k and min(self.buf) >= self.t_per
        return bool(raw or persistent), bool(raw), bool(persistent)

    def prime(self, starts: Sequence[float], scores: Sequence[float]) -> None:
        """Feed history (e.g. the end of validation) without raising alarms, so live windows have context."""
        for t, s in zip(starts, scores):
            self.update(t, s)
