"""Half-Space Trees, the primary detector (river implementation behind fixed min-max scaling)."""

from __future__ import annotations

from typing import Sequence

from river import anomaly

from rad.models.base import FixedMinMaxScaler


class HSTDetector:
    """river.anomaly.HalfSpaceTrees on features scaled with bounds frozen after bootstrap.

    river's HST scores 0 until its first reference window (`window_size` learned
    samples) is complete, so `window_size` must not exceed the bootstrap length.
    """

    def __init__(self, features: Sequence[str], n_trees: int = 25, height: int = 10,
                 window_size: int = 250, seed: int = 0) -> None:
        self.features = tuple(features)
        self.window_size = window_size
        self.scaler = FixedMinMaxScaler(self.features)
        self.model = anomaly.HalfSpaceTrees(n_trees=n_trees, height=height, window_size=window_size, seed=seed)

    def bootstrap(self, xs: Sequence[dict[str, float]]) -> None:
        if len(xs) < self.window_size:
            raise ValueError(f"HST needs at least window_size={self.window_size} bootstrap windows, got {len(xs)}")
        self.scaler.fit(xs)
        for x in xs:
            self.learn_one(x)

    def score_one(self, x: dict[str, float]) -> float:
        return float(self.model.score_one(self.scaler.transform(x)))

    def learn_one(self, x: dict[str, float]) -> None:
        self.model.learn_one(self.scaler.transform(x))
