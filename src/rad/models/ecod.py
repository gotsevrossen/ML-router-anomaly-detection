"""ECOD-style empirical tail detector with an exponential tail beyond the training range (D39).

Li et al., "ECOD: Unsupervised Outlier Detection Using Empirical Cumulative Distribution
Functions" (IEEE TKDE 2022): per feature, how rare is a value under the training data's
own distribution? This suits the novelty counts of D31/D37 (new senders, new LAN peers,
new local ports), which are 0 in almost every benign window. A z-score detector scales
them by the largest training value, so one benign burst in two days (e.g. 8 new LAN
peers) makes every later single new attacker look normal. A rank-based score instead
sees that "any new LAN peer" happened in about 0.02% of training windows.

Per feature j, on slog values (D24), with n training windows:
    tail count  c_j = min(#{train >= x_j}, #{train <= x_j})
    o_j = -log((c_j + 1) / (n + 1))                       (two-sided empirical tail)
    beyond the training range, o_j += (x_j - max_j) / s_up_j   (or the lower side)
where s_up / s_dn are RobustZ's side scales (D27) floored at `min_scale` (D32). The
extra term keeps scores ordered beyond the largest training value (ECOD alone saturates
at log(n + 1)), in the spirit of D25's exponential tail.
score = squash(mean of the `top_k` largest o_j) (D15). Unsupervised, benign data only.

Router note: exact mode keeps the sorted training values (n x F floats). The C port would
keep a quantile sketch plus an exact count of each feature's most common value, which is
what the sparse novelty counts need; that variant is future work.
"""

from __future__ import annotations

from collections import deque
from typing import Sequence

import numpy as np

from rad.models.robust_z import _slog


class ECODTailDetector:
    def __init__(self, features: Sequence[str], slog: bool = True, top_k: int = 3, tail_z: float = 3.0,
                 min_scale: float = 0.05, window: int = 50_000) -> None:
        if top_k < 1:
            raise ValueError("top_k must be >= 1")
        self.features = tuple(features)
        self.slog = slog
        self.top_k = min(top_k, len(self.features))
        self.tail_z, self.min_scale = tail_z, min_scale
        self.buffer: deque[np.ndarray] = deque(maxlen=window)
        self.sorted: np.ndarray | None = None
        self._stale = False

    def matrix(self, xs: Sequence[dict[str, float]]) -> np.ndarray:
        return np.array([[x[f] for f in self.features] for x in xs], dtype=float)

    def _transform(self, m: np.ndarray) -> np.ndarray:
        return _slog(m) if self.slog else m

    def _fit(self) -> None:
        L = np.vstack(self.buffer)
        self.sorted = np.sort(L, axis=0)
        self.n = L.shape[0]
        self.lo, self.hi = self.sorted[0], self.sorted[-1]
        med = np.median(L, axis=0)
        base = 1.4826 * np.median(np.abs(L - med), axis=0)
        base = np.where(base > 0, base, 1.0)
        self.s_up = np.maximum(np.maximum(base, (self.hi - med) / self.tail_z), self.min_scale)
        self.s_dn = np.maximum(np.maximum(base, (med - self.lo) / self.tail_z), self.min_scale)
        self._stale = False

    def bootstrap(self, rows: Sequence[dict[str, float]]) -> None:
        for v in self._transform(self.matrix(rows)):
            self.buffer.append(v)
        self._fit()

    def outlyingness(self, X: np.ndarray) -> np.ndarray:
        """Per-feature o_j for a matrix of raw feature rows (n_rows x F)."""
        if self._stale or self.sorted is None:
            self._fit()
        L = self._transform(np.asarray(X, dtype=float))
        o = np.empty_like(L)
        for j in range(L.shape[1]):
            col = self.sorted[:, j]
            ge = self.n - np.searchsorted(col, L[:, j], side="left")
            le = np.searchsorted(col, L[:, j], side="right")
            o[:, j] = -np.log((np.minimum(ge, le) + 1.0) / (self.n + 1.0))
        o += np.maximum(L - self.hi, 0.0) / self.s_up + np.maximum(self.lo - L, 0.0) / self.s_dn
        return o

    def score_matrix(self, X: np.ndarray) -> np.ndarray:
        o = self.outlyingness(X)
        k = self.top_k
        r = np.partition(o, o.shape[1] - k, axis=1)[:, -k:].mean(axis=1) if k > 1 else o.max(axis=1)
        lg = np.log1p(np.maximum(r, 0.0))
        return lg / (1.0 + lg)

    def score_many(self, xs: Sequence[dict[str, float]]) -> np.ndarray:
        return self.score_matrix(self.matrix(xs))

    def score_one(self, x: dict[str, float]) -> float:
        return float(self.score_many([x])[0])

    def learn_one(self, x: dict[str, float]) -> None:
        self.buffer.append(self._transform(self.matrix([x])[0]))
        self._stale = True

    def model_bytes(self) -> int:
        """Exact mode: sorted training values plus two side scales per feature (float32)."""
        n = len(self.buffer)
        return 4 * len(self.features) * (n + 2)
