"""Robust statistics of the committed profile (Phase 2b/2c).

One object answers "what does this device normally look like right now?" for
both the drift budget (medians) and the disambiguation / explanations (robust
z-scores). Medians come from a decayed fixed-bin histogram of bootstrap +
committed windows. The drift budget's scale is the raw bootstrap IQR.

Explanation z-scores (D52) use RobustZ's recipe instead, because raw values over
raw IQRs gave |z| of 26-2,900 on ordinary windows (sparse counts have an IQR near
zero): values are log-transformed (slog), and each side of each feature gets a
bootstrap-fixed scale calibrated so that the edge of the bootstrap range is
z = tail_z = 3. A window inside the bootstrap range therefore never explains
itself with |z| > 3, and tau_div = 3 means "beyond anything seen in bootstrap".
"""

from __future__ import annotations

import math
from typing import Sequence

import numpy as np

from rad.continual.sketch import FeatureHistograms
from rad.models.robust_z import _slog

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
                 half_life_days: float = 1.0, day_s: float = 86_400.0, n_bins: int = 64,
                 tail_z: float = 3.0, min_scale: float = 0.05) -> None:
        self.features = tuple(features)
        m = np.array([[r[f] for f in self.features] for r in bootstrap_rows], dtype=float)
        self.bootstrap_median = np.median(m, axis=0)
        self.scale = robust_scale(m)  # drift budget units (D19); not used for explanations
        # D52: explanation scales in slog space, two-sided and range-calibrated as in RobustZ's sketch build
        # (sigma from the IQR, then mean absolute deviation, then 1), floored at min_scale like D32.
        L = _slog(m)
        med = np.median(L, axis=0)
        q25, q75 = np.quantile(L, [0.25, 0.75], axis=0)
        mean_ad = MEANAD_TO_SIGMA * np.abs(L - med).mean(axis=0)
        base = np.where(q75 > q25, (q75 - q25) / IQR_TO_SIGMA, np.where(mean_ad > 0, mean_ad, 1.0))
        self.tail_z = float(tail_z)
        self.z_up = np.maximum(np.maximum(base, (L.max(axis=0) - med) / tail_z), min_scale)
        self.z_dn = np.maximum(np.maximum(base, (med - L.min(axis=0)) / tail_z), min_scale)
        self.normal_lo, self.normal_hi = med - tail_z * self.z_dn, med + tail_z * self.z_up  # slog space
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
        """Signed z per feature against the committed median, in slog space with bootstrap-fixed scales (D52).

        As in RobustZ (D49), the bootstrap's normal interval stays normal when the committed median moves:
        each side's scale is widened so that the far edge of that interval is still at most tail_z away.
        """
        med = _slog(self.median())
        up = np.maximum(self.z_up, (self.normal_hi - med) / self.tail_z)
        dn = np.maximum(self.z_dn, (med - self.normal_lo) / self.tail_z)
        d = _slog(self.vec(x)) - med
        z = np.where(d >= 0, d / up, d / dn)
        return dict(zip(self.features, z.tolist()))
