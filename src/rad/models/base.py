"""Common detector interface and helpers (Phase 1c).

Every window-level detector implements `Detector`. The continual-learning
wrappers in Phase 2 only ever call these three methods, so the same update rule
can be ablated across models (CLAUDE.md §5 Phase 2).
"""

from __future__ import annotations

from typing import Iterable, Protocol, Sequence

import numpy as np


class Detector(Protocol):
    """Unsupervised streaming anomaly detector over one feature vector at a time."""

    def bootstrap(self, xs: Sequence[dict[str, float]]) -> None:
        """Initial training on data assumed clean. Fixes any scaling bounds (C-port rule)."""
        ...

    def score_one(self, x: dict[str, float]) -> float:
        """Higher = more anomalous, in [0, 1]. Never learns."""
        ...

    def learn_one(self, x: dict[str, float]) -> None:
        """Absorb one window the update rule has accepted."""
        ...


def score_many(det: Detector, xs: Sequence[dict[str, float]]) -> np.ndarray:
    """Score a batch without learning. Uses a detector's vectorised `score_many` when it has one;
    the result must equal calling `score_one` on each row (tested)."""
    fast = getattr(det, "score_many", None)
    if fast is not None:
        return np.asarray(fast(xs), dtype=float)
    return np.array([det.score_one(x) for x in xs], dtype=float)


def squash(r: float) -> float:
    """Map an unbounded non-negative score to [0, 1) monotonically: r / (1 + r).

    Rank-based metrics are unchanged; it only gives every detector the same range.
    """
    r = max(0.0, float(r))
    return r / (1.0 + r)


class FixedMinMaxScaler:
    """Min-max scaling to [0, 1] with bounds frozen after bootstrap; out-of-range values are clipped.

    Frozen bounds keep scores comparable over time and let the C port use fixed-point
    features (CLAUDE.md §5 1c). A feature that was constant during bootstrap maps to 0
    at its bootstrap value and to 1 above it (0 below).
    """

    def __init__(self, features: Sequence[str]) -> None:
        self.features = tuple(features)
        self.lo: np.ndarray | None = None
        self.hi: np.ndarray | None = None

    def fit(self, xs: Iterable[dict[str, float]]) -> "FixedMinMaxScaler":
        m = self.matrix(xs)
        if len(m) == 0:
            raise ValueError("cannot fit a scaler on zero rows")
        self.lo, self.hi = m.min(axis=0), m.max(axis=0)
        return self

    def matrix(self, xs: Iterable[dict[str, float]]) -> np.ndarray:
        return np.array([[x[f] for f in self.features] for x in xs], dtype=float).reshape(-1, len(self.features))

    def _scale(self, m: np.ndarray) -> np.ndarray:
        if self.lo is None or self.hi is None:
            raise RuntimeError("scaler used before bootstrap")
        span = self.hi - self.lo
        out = np.where(span > 0, (m - self.lo) / np.where(span > 0, span, 1.0), (m > self.lo).astype(float))
        return np.clip(out, 0.0, 1.0)

    def transform_vec(self, x: dict[str, float]) -> np.ndarray:
        return self._scale(np.array([x[f] for f in self.features], dtype=float))

    def matrix_scaled(self, xs: Iterable[dict[str, float]]) -> np.ndarray:
        return self._scale(self.matrix(xs))

    def transform(self, x: dict[str, float]) -> dict[str, float]:
        return dict(zip(self.features, self.transform_vec(x).tolist()))
