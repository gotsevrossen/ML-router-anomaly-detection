"""Fixed-bin per-feature histograms for streaming medians and quantiles (Phase 2b).

Bin edges are fixed at bootstrap, so the C port needs only a static
`float counts[F][n_bins + 2]` array. Two extra bins catch values below and
above the range. Counts can be decayed to make a sketch track recent data.
"""

from __future__ import annotations

from typing import Sequence

import numpy as np


class FeatureHistograms:
    """One histogram per feature over [lo - margin*span, hi + margin*span], plus under/overflow bins."""

    def __init__(self, features: Sequence[str], lo: np.ndarray, hi: np.ndarray, n_bins: int = 64,
                 margin: float = 0.5) -> None:
        self.features = tuple(features)
        lo, hi = np.asarray(lo, dtype=float), np.asarray(hi, dtype=float)
        span = np.where(hi > lo, hi - lo, np.maximum(np.abs(lo), 1.0))  # constant feature: a unit-ish range
        self.lo_edge = lo - margin * span
        self.hi_edge = hi + margin * span
        self.n_bins = n_bins
        self.width = (self.hi_edge - self.lo_edge) / n_bins
        self.counts = np.zeros((len(self.features), n_bins + 2))  # [underflow, bins..., overflow]

    @classmethod
    def from_rows(cls, features: Sequence[str], rows: Sequence[dict[str, float]], n_bins: int = 64,
                  margin: float = 0.5) -> "FeatureHistograms":
        m = np.array([[r[f] for f in features] for r in rows], dtype=float)
        h = cls(features, m.min(axis=0), m.max(axis=0), n_bins, margin)
        for v in m:
            h.add_vec(v)
        return h

    def copy(self) -> "FeatureHistograms":
        new = object.__new__(FeatureHistograms)
        new.__dict__.update(self.__dict__)
        new.counts = self.counts.copy()
        return new

    def _bins(self, v: np.ndarray) -> np.ndarray:
        idx = np.floor((v - self.lo_edge) / self.width).astype(int) + 1
        return np.clip(idx, 0, self.n_bins + 1)

    def add_vec(self, v: np.ndarray, weight: float = 1.0) -> None:
        self.counts[np.arange(len(self.features)), self._bins(v)] += weight

    def add(self, x: dict[str, float], weight: float = 1.0) -> None:
        self.add_vec(np.array([x[f] for f in self.features], dtype=float), weight)

    def decay(self, factor: float) -> None:
        self.counts *= factor

    def quantile(self, q: float) -> np.ndarray:
        """Per-feature q-quantile, linear within a bin; under/overflow mass sits at the range edges."""
        total = self.counts.sum(axis=1)
        out = np.full(len(self.features), np.nan)
        cum = np.cumsum(self.counts, axis=1)
        for j in range(len(self.features)):
            if total[j] <= 0:
                continue
            target = q * total[j]
            b = int(np.searchsorted(cum[j], target, side="left"))
            if b == 0:
                out[j] = self.lo_edge[j]
            elif b >= self.n_bins + 1:
                out[j] = self.hi_edge[j]
            else:
                before = cum[j, b - 1]
                frac = (target - before) / self.counts[j, b] if self.counts[j, b] > 0 else 0.0
                out[j] = self.lo_edge[j] + (b - 1 + frac) * self.width[j]
        return out

    def median(self) -> np.ndarray:
        return self.quantile(0.5)
