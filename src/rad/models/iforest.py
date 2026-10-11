"""Isolation Forest baseline, retrained on a sliding window of accepted windows."""

from __future__ import annotations

from collections import deque
from typing import Sequence

import numpy as np
from sklearn.ensemble import IsolationForest


class IForestDetector:
    """sklearn IsolationForest refit every `retrain_every` learned windows on the last `window` of them.

    Score is the original paper's anomaly score s(x) = -score_samples(x), which lies in (0, 1].
    """

    def __init__(self, features: Sequence[str], n_estimators: int = 100, max_samples: int = 256,
                 window: int = 2880, retrain_every: int = 120, seed: int = 0) -> None:
        self.features = tuple(features)
        self.n_estimators = n_estimators
        self.max_samples = max_samples
        self.retrain_every = retrain_every
        self.seed = seed
        self.buffer: deque[np.ndarray] = deque(maxlen=window)
        self.model: IsolationForest | None = None
        self._since_fit = 0

    def _vec(self, x: dict[str, float]) -> np.ndarray:
        return np.array([x[f] for f in self.features], dtype=float)

    def _fit(self) -> None:
        data = np.vstack(self.buffer)
        self.model = IsolationForest(n_estimators=self.n_estimators, max_samples=min(self.max_samples, len(data)),
                                     random_state=self.seed).fit(data)
        self._since_fit = 0

    def bootstrap(self, xs: Sequence[dict[str, float]]) -> None:
        for x in xs:
            self.buffer.append(self._vec(x))
        self._fit()

    def score_many(self, xs: Sequence[dict[str, float]]) -> np.ndarray:
        if self.model is None:
            return np.zeros(len(xs))
        return -self.model.score_samples(np.vstack([self._vec(x) for x in xs]))

    def score_one(self, x: dict[str, float]) -> float:
        return float(self.score_many([x])[0])

    def learn_one(self, x: dict[str, float]) -> None:
        self.buffer.append(self._vec(x))
        self._since_fit += 1
        if self._since_fit >= self.retrain_every:
            self._fit()
