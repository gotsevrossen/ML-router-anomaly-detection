"""Drift budget: bounded profile shift per day and in total (Phase 2b, CLAUDE.md §5 2b).

    D(m) = sum_j |m_j - median_anchor_j| / scale_anchor_j

`scale_anchor` is the bootstrap IQR, falling back to a normal-equivalent mean
absolute deviation and then to 1.0 for features that were constant (as in MAD).
The fast profile is a decayed histogram of bootstrap + committed windows
(half-life `fast_half_life_days`), so it follows what the fast model recently learned.

Before each commit the budget checks two shifts of the fast median:
  daily      vs the fast median at the start of the current day   <= b_daily
  cumulative vs the anchor median                                   <= b_total
A commit that would break either is refused, and commits stop: until the next
day for the daily budget, and until `rebase` (anchor update or operator review)
for the cumulative one. Either way a `possible_slow_poisoning_or_major_change`
notice is raised. Nothing adapts silently.
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from rad.continual.profile_stats import RobustProfile, robust_scale  # noqa: F401 (robust_scale re-exported)

log = logging.getLogger(__name__)

NOTICE = "possible_slow_poisoning_or_major_change"


def drift_measure(median: np.ndarray, reference: np.ndarray, scale: np.ndarray, measure: str = "sum",
                  cap: float = 3.0) -> float:
    """Profile shift in IQR units.

    sum          CLAUDE.md 2b: sum_j |m_j - ref_j| / IQR_j
    capped_mean  D43: mean_j min(|m_j - ref_j| / IQR_j, cap). On real devices the sum is dominated by
                 near-constant features (tiny IQR), so calibrated budgets ranged from 0.03 to 475 across
                 five devices; capping each feature and averaging gives one comparable unit.
    """
    r = np.abs(np.asarray(median) - np.asarray(reference)) / scale
    return float(np.sum(r)) if measure == "sum" else float(np.mean(np.minimum(r, cap)))


@dataclass(frozen=True)
class DriftNotice:
    t: float
    kind: str  # "daily" | "cumulative"
    drift: float  # the shift the refused commit would have caused
    budget: float
    message: str = NOTICE


class DriftBudget:
    """Gate for commits that bounds how fast and how far the learned profile may move."""

    def __init__(self, features: Sequence[str], bootstrap_rows: Sequence[dict[str, float]], b_daily: float,
                 b_total: float, day_s: float = 86_400.0, fast_half_life_days: float = 1.0,
                 n_bins: int = 64, profile: RobustProfile | None = None, measure: str = "sum",
                 cap: float = 3.0) -> None:
        """`profile` may be shared with the disambiguation; the budget then owns adding commits to it."""
        self.profile = profile or RobustProfile(features, bootstrap_rows, fast_half_life_days, day_s, n_bins)
        self.features = self.profile.features
        self.anchor_median = self.profile.bootstrap_median.copy()
        self.scale = self.profile.scale
        self.b_daily, self.b_total = float(b_daily), float(b_total)
        if measure not in ("sum", "capped_mean"):
            raise ValueError("measure must be sum|capped_mean")
        self.measure, self.cap = measure, float(cap)
        self.day_s = float(day_s)
        self._day: int | None = None
        self._day_start_median = self.fast.median()
        self.halted_today = False
        self.halted_total = False
        self.notices: list[DriftNotice] = []
        self.daily_log: list[dict[str, float]] = []  # one row per finished day, for plots and RQ3

    @property
    def fast(self):
        """The decayed histogram of the committed (fast) profile."""
        return self.profile.hist

    def shift(self, median: np.ndarray, reference: np.ndarray) -> float:
        return drift_measure(median, reference, self.scale, self.measure, self.cap)

    def drift_vs_anchor(self) -> float:
        return self.shift(self.fast.median(), self.anchor_median)

    def _roll_day(self, t: float) -> None:
        day = math.floor(t / self.day_s)
        if self._day is None:
            self._day = day
            self.profile.advance(t)
            return
        if day == self._day:
            return
        self.daily_log.append({"day": float(self._day), "daily_shift": self.shift(self.fast.median(), self._day_start_median),
                               "drift_vs_anchor": self.drift_vs_anchor(), "halted": float(self.halted_today)})
        self.profile.advance(t)
        self._day = day
        self._day_start_median = self.fast.median()
        self.halted_today = False

    def try_commit(self, t: float, x: dict[str, float]) -> bool:
        """Add x to the fast profile if both budgets allow it; otherwise refuse and halt."""
        self._roll_day(t)
        if self.halted_today or self.halted_total:
            return False
        v = self.profile.vec(x)
        self.fast.add_vec(v)
        median = self.fast.median()
        daily = self.shift(median, self._day_start_median)
        total = self.shift(median, self.anchor_median)
        if daily > self.b_daily:
            self.fast.add_vec(v, -1.0)  # exact undo: counts are additive
            self.halted_today = True
            self._notify(t, "daily", daily, self.b_daily)
            return False
        if total > self.b_total:
            self.fast.add_vec(v, -1.0)
            self.halted_total = True
            self._notify(t, "cumulative", total, self.b_total)
            return False
        return True

    def rebase(self, anchor_median: np.ndarray | None = None) -> None:
        """Accept the current profile as the new anchor (after an anchor update or operator review)."""
        self.anchor_median = self.fast.median() if anchor_median is None else np.asarray(anchor_median, dtype=float)
        self.halted_total = False

    def _notify(self, t: float, kind: str, drift: float, budget: float) -> None:
        n = DriftNotice(t=t, kind=kind, drift=drift, budget=budget)
        self.notices.append(n)
        log.warning("%s at t=%.0f: %s shift %.3f would exceed budget %.3f; commits halted", NOTICE, t, kind,
                    drift, budget)
