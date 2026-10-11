"""Feature preprocessing that wraps any detector (D24).

Steps, applied in this order and frozen after bootstrap (C-port rule):
  slog     x -> sign(x) * log(1 + |x|). Window counts (packets, ARP requests,
           connections) jump 100-1000x under attack, so on a linear scale the
           benign variation is squashed into a sliver of the range. The log
           spreads it out while keeping order. In C: a small lookup table.
  project  robustly standardise (D23 tail-calibrated scale), then take
           `n_projections` random unit directions (seeded). Every projected
           feature mixes all inputs, so an attack that moves a few of many
           features shows up in every projection (the same reason Extended IF
           works, D22). In C: one fixed k x F matrix-vector product per window.
"""

from __future__ import annotations

from typing import Callable, Sequence

import numpy as np

from rad.models.base import Detector, score_many

STEPS = ("slog", "project")
FLOAT_BYTES = 4  # the C port stores weights as float32 or Q16.16 fixed point


def slog(m: np.ndarray) -> np.ndarray:
    return np.sign(m) * np.log1p(np.abs(m))


class PreprocessedDetector:
    """Applies the configured steps, then delegates to an inner detector built on the new features."""

    def __init__(self, features: Sequence[str], inner_factory: Callable[[Sequence[str]], Detector],
                 steps: Sequence[str], n_projections: int = 32, tail_quantile: float = 0.999, tail_z: float = 3.0,
                 seed: int = 0) -> None:
        unknown = [s for s in steps if s not in STEPS]
        if unknown or not steps:
            raise ValueError(f"preprocess steps must be a non-empty subset of {STEPS}, got {list(steps)}")
        self.features = tuple(features)
        self.steps = tuple(steps)
        self.inner_factory = inner_factory
        self.n_projections = n_projections
        self.tail_quantile, self.tail_z = tail_quantile, tail_z
        self.seed = seed
        self.center: np.ndarray | None = None
        self.scale: np.ndarray | None = None
        self.W: np.ndarray | None = None
        self.out_features: tuple[str, ...] = self.features
        self.inner: Detector | None = None

    def _matrix(self, xs: Sequence[dict[str, float]]) -> np.ndarray:
        return np.array([[x[f] for f in self.features] for x in xs], dtype=float).reshape(-1, len(self.features))

    def _apply(self, m: np.ndarray) -> np.ndarray:
        if "slog" in self.steps:
            m = slog(m)
        if self.W is not None:
            m = ((m - self.center) / self.scale) @ self.W.T
        return m

    def _rows(self, m: np.ndarray) -> list[dict[str, float]]:
        return [dict(zip(self.out_features, r.tolist())) for r in m]

    def bootstrap(self, xs: Sequence[dict[str, float]]) -> None:
        m = self._matrix(xs)
        if "slog" in self.steps:
            m = slog(m)
        if "project" in self.steps:
            from rad.models.mad import tail_calibrated_scale

            self.center, self.scale = tail_calibrated_scale(m, self.tail_quantile, self.tail_z)
            W = np.random.default_rng(self.seed).normal(size=(self.n_projections, len(self.features)))
            self.W = W / np.linalg.norm(W, axis=1, keepdims=True)
            self.out_features = tuple(f"p{i}" for i in range(self.n_projections))
            m = ((m - self.center) / self.scale) @ self.W.T
        self.inner = self.inner_factory(self.out_features)
        self.inner.bootstrap(self._rows(m))

    def transform(self, xs: Sequence[dict[str, float]]) -> list[dict[str, float]]:
        return self._rows(self._apply(self._matrix(xs)))

    def score_many(self, xs: Sequence[dict[str, float]]) -> np.ndarray:
        return score_many(self.inner, self.transform(xs))

    def score_one(self, x: dict[str, float]) -> float:
        return float(self.score_many([x])[0])

    def learn_one(self, x: dict[str, float]) -> None:
        self.inner.learn_one(self.transform([x])[0])

    def model_bytes(self) -> int:
        own = 0 if self.W is None else FLOAT_BYTES * (self.W.size + 2 * len(self.features))
        inner = getattr(self.inner, "model_bytes", lambda: 0)()
        return own + inner
