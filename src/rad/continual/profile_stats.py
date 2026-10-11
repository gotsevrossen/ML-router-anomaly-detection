"""Robust statistics of the committed profile (Phase 2b/2c).

One object answers "what does this device normally look like right now?" for
both the drift budget (medians) and the disambiguation / explanations (robust
z-scores). Medians come from a decayed fixed-bin histogram of bootstrap +
committed windows. Scales are fixed at bootstrap, so a z-score of 5 always means
"5 bootstrap IQRs away".
"""

from __future__ import annotations

import math
from typing import Sequence

import numpy as np

from rad.continual.sketch import FeatureHistograms

IQR_TO_SIGMA = 1.349
MEANAD_TO_SIGMA = 1.2533


def robust_scale(m: np.ndarray) -> np.ndarray:
    """Per-feature IQR, with the same fallbacks as the MAD detector for degenerate features."""
    q25, q75 = np.quantile(m, [0.25, 0.75], axis=0)
    iqr = q75 - q25
    fallback = MEANAD_TO_SIGMA * np.abs(m - np.median(m, axis=0)).mean(axis=0) * IQR_TO_SIGMA
    return np.where(iqr > 0, iqr, np.where(fallback > 0, fallback, 1.0))


class RobustProfile:
    """Decayed committed-data medians with bootstrap-fixed robust scales."""

    def __init__(self, features: Sequence[str], bootstrap_rows: Sequence[dict[str, float]],
                 half_life_days: float = 1.0, day_s: float = 86_400.0, n_bins: int = 64) -> None:
        self.features = tuple(features)
        m = np.array([[r[f] for f in self.features] for r in bootstrap_rows], dtype=float)
        self.bootstrap_median = np.median(m, axis=0)
        self.scale = robust_scale(m)
        self.hist = FeatureHistograms.from_rows(self.features, bootstrap_rows, n_bins=n_bins)
        self.day_s = float(day_s)
        self.decay_per_day = 0.5 ** (1.0 / half_life_days)
        self._day: int | None = None

    def vec(self, x: dict[str, float]) -> np.ndarray:
        return np.array([x[f] for f in self.features], dtype=float)

    def advance(self, t: float) -> None:
        """Apply one decay step per elapsed day. Idempotent within a day, so several callers are safe."""
        day = math.floor(t / self.day_s)
        if self._day is not None and day > self._day:
            self.hist.decay(self.decay_per_day ** (day - self._day))
        if self._day is None or day > self._day:
            self._day = day

    def add_vec(self, v: np.ndarray, weight: float = 1.0) -> None:
        self.hist.add_vec(v, weight)

    def add(self, x: dict[str, float]) -> None:
        self.add_vec(self.vec(x))

    def median(self) -> np.ndarray:
        return self.hist.median()

    def robust_z(self, x: dict[str, float]) -> dict[str, float]:
        """Signed z per feature: (x - committed median) / bootstrap scale."""
        z = (self.vec(x) - self.median()) / self.scale
        return dict(zip(self.features, z.tolist()))
