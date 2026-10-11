"""Isolation Forest baseline, retrained on a sliding window of accepted windows.

Two implementations:
  margin = 0 (default)  sklearn's IsolationForest, the textbook algorithm.
  margin > 0            a numpy forest whose split values are drawn from each
                        node's training range widened by `margin` on both sides
                        (D22). Textbook IF only splits inside the node's range, so
                        a point far beyond the training data lands in the same leaf
                        as the most extreme training point and cannot be told apart
                        from it. With headroom, points beyond the range are isolated
                        sooner the further out they are. Same idea as D14 for HST.
  hyperplane = True     Extended Isolation Forest (Hariri et al. 2019): each split is a
                        random hyperplane over all features, on robustly standardised
                        features, with the same headroom on the projected range (D22).
                        With many features an axis-parallel split rarely looks at the
                        few features an attack pushes out of range; a hyperplane always does.
"""

from __future__ import annotations

import math
from collections import deque
from typing import Sequence

import numpy as np
from sklearn.ensemble import IsolationForest

EULER_GAMMA = 0.5772156649015329


def _c(n: np.ndarray | int) -> np.ndarray:
    """Average path length of an unsuccessful BST search over n points (Liu et al. 2008)."""
    n = np.asarray(n, dtype=float)
    out = np.zeros_like(n)
    big = n > 2
    out[big] = 2.0 * (np.log(n[big] - 1.0) + EULER_GAMMA) - 2.0 * (n[big] - 1.0) / n[big]
    out[n == 2] = 1.0
    return out


class _HeadroomForest:
    """Isolation forest with split values drawn from the node range widened by `margin`.

    Trees are stored as flat arrays (feature, threshold, left, right, size), which is
    also the layout a C port would use.
    """

    def __init__(self, n_estimators: int, max_samples: int, margin: float, extra_depth: int, seed: int,
                 hyperplane: bool = False, hyperplane_features: int | None = None) -> None:
        self.n_estimators, self.max_samples = n_estimators, max_samples
        self.margin, self.extra_depth = margin, extra_depth
        self.hyperplane = hyperplane
        self.hyperplane_features = hyperplane_features  # None = all features (fully extended)
        self.rng = np.random.default_rng(seed)
        self.trees: list[tuple[np.ndarray, ...]] = []
        self.psi = 0

    def fit(self, X: np.ndarray) -> "_HeadroomForest":
        n = len(X)
        self.psi = min(self.max_samples, n)
        depth_limit = math.ceil(math.log2(max(self.psi, 2))) + self.extra_depth
        global_span = X.max(axis=0) - X.min(axis=0)
        global_span = np.where(global_span > 0, global_span, np.maximum(np.abs(X.max(axis=0)), 1.0))
        self.trees = [self._build(X[self.rng.choice(n, self.psi, replace=False)], depth_limit, global_span)
                      for _ in range(self.n_estimators)]
        return self

    def _build(self, X: np.ndarray, depth_limit: int, global_span: np.ndarray) -> tuple[np.ndarray, ...]:
        feat, thr, left, right, size, normal = [], [], [], [], [], []
        n_feat = X.shape[1]

        def node(idx: np.ndarray, depth: int) -> int:
            me = len(feat)
            feat.append(-1); thr.append(0.0); left.append(-1); right.append(-1); size.append(len(idx))
            normal.append(None)
            if depth >= depth_limit or len(idx) <= 1:
                return me
            if self.hyperplane:
                w = np.zeros(n_feat)
                k = n_feat if self.hyperplane_features is None else min(self.hyperplane_features, n_feat)
                on = self.rng.choice(n_feat, size=k, replace=False) if k < n_feat else np.arange(n_feat)
                w[on] = self.rng.normal(size=k)
                w /= np.linalg.norm(w)
                v = X[idx] @ w
                fallback = float(np.abs(w) @ global_span)
                f = 0  # any value >= 0 marks an internal node
            else:
                w = None
                f = int(self.rng.integers(n_feat))
                v = X[idx, f]
                fallback = float(global_span[f])
            lo, hi = float(v.min()), float(v.max())
            span = hi - lo if hi > lo else fallback
            t = float(self.rng.uniform(lo - self.margin * span, hi + self.margin * span))
            go_left = v < t
            feat[me], thr[me], normal[me] = f, t, w
            l_child = node(idx[go_left], depth + 1)
            r_child = node(idx[~go_left], depth + 1)
            left[me], right[me] = l_child, r_child
            return me

        node(np.arange(len(X)), 0)
        normals = np.zeros((len(feat), n_feat if self.hyperplane else 0))
        for i, w in enumerate(normal):
            if w is not None:
                normals[i] = w
        return (np.array(feat), np.array(thr), np.array(left), np.array(right), np.array(size), normals)

    def score_samples(self, X: np.ndarray) -> np.ndarray:
        """Anomaly score s(x) = 2^(-E[h(x)] / c(psi)), in (0, 1]."""
        total = np.zeros(len(X))
        for feat, thr, left, right, size, normals in self.trees:
            pos = np.zeros(len(X), dtype=int)
            depth = np.zeros(len(X))
            active = feat[pos] >= 0
            while active.any():
                rows = np.flatnonzero(active)
                t = thr[pos[rows]]
                if self.hyperplane:
                    proj = np.einsum("ij,ij->i", X[rows], normals[pos[rows]])
                else:
                    proj = X[rows, feat[pos[rows]]]
                go_left = proj < t
                pos[rows] = np.where(go_left, left[pos[rows]], right[pos[rows]])
                depth[rows] += 1
                active = feat[pos] >= 0
            total += depth + _c(size[pos])
        return 2.0 ** (-(total / len(self.trees)) / _c(self.psi))


class IForestDetector:
    """Isolation Forest refit every `retrain_every` learned windows on the last `window` of them.

    Score is the original paper's anomaly score s(x) = 2^(-E[h]/c(psi)), in (0, 1].
    """

    def __init__(self, features: Sequence[str], n_estimators: int = 100, max_samples: int = 256,
                 window: int = 2880, retrain_every: int = 120, margin: float = 0.0, extra_depth: int = 4,
                 hyperplane: bool = False, hyperplane_features: int | str | None = None,
                 tail_quantile: float = 0.999, tail_z: float = 3.0, min_scale: float = 0.0,
                 seed: int = 0) -> None:
        self.features = tuple(features)
        self.n_estimators = n_estimators
        self.max_samples = max_samples
        self.retrain_every = retrain_every
        self.margin = margin
        self.extra_depth = extra_depth
        self.hyperplane = hyperplane
        if hyperplane_features == "sqrt":
            hyperplane_features = math.ceil(math.sqrt(len(self.features)))  # sparse EIF (D26)
        self.hyperplane_features = hyperplane_features
        self.tail_quantile, self.tail_z = tail_quantile, tail_z
        self.min_scale = min_scale  # D32 resolution floor for the hyperplane standardisation
        self._center: np.ndarray | None = None
        self._scale: np.ndarray | None = None
        self.seed = seed
        self.buffer: deque[np.ndarray] = deque(maxlen=window)
        self.model: IsolationForest | _HeadroomForest | None = None
        self._since_fit = 0
        self._fits = 0

    def _vec(self, x: dict[str, float]) -> np.ndarray:
        return np.array([x[f] for f in self.features], dtype=float)

    def _fit(self) -> None:
        data = np.vstack(self.buffer)
        if self.hyperplane:
            # Hyperplanes mix features, so put them on one robust scale first (the D23 scale).
            from rad.models.mad import tail_calibrated_scale

            self._center, self._scale = tail_calibrated_scale(data, self.tail_quantile, self.tail_z, self.min_scale)
            data = (data - self._center) / self._scale
        if self.margin > 0 or self.hyperplane:
            self.model = _HeadroomForest(self.n_estimators, self.max_samples, self.margin, self.extra_depth,
                                         self.seed + self._fits, hyperplane=self.hyperplane,
                                         hyperplane_features=self.hyperplane_features).fit(data)
        else:
            self.model = IsolationForest(n_estimators=self.n_estimators,
                                         max_samples=min(self.max_samples, len(data)),
                                         random_state=self.seed).fit(data)
        self._fits += 1
        self._since_fit = 0

    def bootstrap(self, xs: Sequence[dict[str, float]]) -> None:
        for x in xs:
            self.buffer.append(self._vec(x))
        self._fit()

    def score_many(self, xs: Sequence[dict[str, float]]) -> np.ndarray:
        if self.model is None:
            return np.zeros(len(xs))
        X = np.vstack([self._vec(x) for x in xs])
        if self._scale is not None:
            X = (X - self._center) / self._scale
        if isinstance(self.model, _HeadroomForest):
            return self.model.score_samples(X)
        return -self.model.score_samples(X)

    def score_one(self, x: dict[str, float]) -> float:
        return float(self.score_many([x])[0])

    def learn_one(self, x: dict[str, float]) -> None:
        self.buffer.append(self._vec(x))
        self._since_fit += 1
        if self._since_fit >= self.retrain_every:
            self._fit()

    def model_bytes(self) -> int:
        """C layout (D26): per node float32 cut, two int32 children, int32 leaf size, uint16 feature;
        hyperplane nodes add (uint16 index + float32 weight) per non-zero weight; plus scaling vectors."""
        if self.model is None:
            return 0
        per_node = 4 + 8 + 4 + 2
        if isinstance(self.model, IsolationForest):
            return sum(est.tree_.node_count for est in self.model.estimators_) * per_node
        total = 0
        for feat, _thr, _l, _r, _size, normals in self.model.trees:
            total += len(feat) * per_node
            if self.hyperplane:
                total += int((normals != 0).sum()) * 6
        if self._scale is not None:
            total += 2 * 4 * len(self.features)
        return total
