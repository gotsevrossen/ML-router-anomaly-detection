"""Robust-statistics baseline: max per-feature robust z-score against median / MAD.

Kept deliberately simple because simple baselines can win at low FPR
(Arp et al., USENIX Security 2022; CLAUDE.md §8).
"""

from __future__ import annotations

from collections import deque
from typing import Sequence

import numpy as np

from rad.models.base import squash_array

MAD_TO_SIGMA = 1.4826  # MAD of a normal distribution * 1.4826 = sigma
MEANAD_TO_SIGMA = 1.2533  # mean absolute deviation of a normal * 1.2533 = sigma


def tail_calibrated_scale(data: np.ndarray, tail_quantile: float | None, tail_z: float = 3.0
                          ) -> tuple[np.ndarray, np.ndarray]:
    """(median, scale) per feature: 1.4826 * MAD with the fallbacks of MADDetector, floored at
    Q_tail(|x - median|) / tail_z when `tail_quantile` is set (D23)."""
    med = np.median(data, axis=0)
    absdev = np.abs(data - med)
    scale = MAD_TO_SIGMA * np.median(absdev, axis=0)
    fallback = MEANAD_TO_SIGMA * absdev.mean(axis=0)
    scale = np.where(scale > 0, scale, np.where(fallback > 0, fallback, 1.0))
    if tail_quantile is not None:
        tail = np.quantile(absdev, tail_quantile, axis=0) / tail_z
        scale = np.maximum(scale, np.where(tail > 0, tail, scale))
    return med, scale


class MADDetector:
    """score = squash(max_j |x_j - median_j| / scale_j) over a sliding window of accepted windows.

    scale_j = 1.4826 * MAD_j. When MAD_j is 0 (the feature was constant for most
    windows), fall back to 1.2533 * mean absolute deviation, and if that is 0 too,
    to 1.0, so any change from a constant feature counts as one unit of deviation.

    `tail_quantile` (off by default) adds a tail-calibrated floor (D23):
        scale_j >= Q_tail(|x_j - median_j|) / tail_z
    so a feature's own extreme training deviation maps to about `tail_z` units.
    Without it, near-constant features (MAD ~ 0) turn tiny benign fluctuations into
    astronomically large z and take over the maximum over features.
    """

    def __init__(self, features: Sequence[str], window: int = 2880, tail_quantile: float | None = None,
                 tail_z: float = 3.0) -> None:
        if tail_quantile is not None and not 0.5 <= tail_quantile <= 1.0:
            raise ValueError("tail_quantile must be in [0.5, 1]")
        self.features = tuple(features)
        self.tail_quantile = tail_quantile
        self.tail_z = tail_z
        self.buffer: deque[np.ndarray] = deque(maxlen=window)
        self._median: np.ndarray | None = None
        self._scale: np.ndarray | None = None

    def _vec(self, x: dict[str, float]) -> np.ndarray:
        return np.array([x[f] for f in self.features], dtype=float)

    def _refresh(self) -> None:
        self._median, self._scale = tail_calibrated_scale(np.vstack(self.buffer), self.tail_quantile, self.tail_z)

    def robust_z(self, x: dict[str, float]) -> np.ndarray:
        """Per-feature |robust z| (reused later for top_features explanations)."""
        if self._median is None:
            self._refresh()
        return np.abs(self._vec(x) - self._median) / self._scale

    def bootstrap(self, xs: Sequence[dict[str, float]]) -> None:
        for x in xs:
            self.buffer.append(self._vec(x))
        self._refresh()

    def score_many(self, xs: Sequence[dict[str, float]]) -> np.ndarray:
        if not self.buffer:
            return np.zeros(len(xs))
        if self._median is None:
            self._refresh()
        z = (np.abs(np.vstack([self._vec(x) for x in xs]) - self._median) / self._scale).max(axis=1)
        return squash_array(z)

    def score_one(self, x: dict[str, float]) -> float:
        return float(self.score_many([x])[0])

    def learn_one(self, x: dict[str, float]) -> None:
        self.buffer.append(self._vec(x))
        self._median = None  # recomputed lazily on the next score

    def model_bytes(self) -> int:
        """Scoring state: one float32 median and scale per feature (D26). Updating would add a
        streaming quantile sketch (D19 histograms) instead of this Python buffer."""
        return 2 * 4 * len(self.features)
