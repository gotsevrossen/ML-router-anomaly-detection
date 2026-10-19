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

State (`stats`):
  exact   sorted training values, n x F floats (12 MB for 25k N-BaIoT rows x 115 features).
  sketch  per feature, fixed size: if the feature has <= `max_distinct` distinct values (counts:
          novelty, ARP, DNS ...), every distinct value with its count, so tail counts are exact;
          otherwise `n_quantiles` quantiles for the body plus the `tail_keep` smallest and
          largest values kept exactly, so the rare tail (where alarms happen) stays exact.
          About 4 KB per feature regardless of n.
"""

from __future__ import annotations

from collections import deque
from typing import Sequence

import numpy as np

from rad.models.robust_z import _direction_masks, _slog


class ECODTailDetector:
    def __init__(self, features: Sequence[str], slog: bool = True, top_k: int = 3, tail_z: float = 3.0,
                 min_scale: float = 0.05, window: int = 50_000, stats: str = "exact", max_distinct: int = 256,
                 n_quantiles: int = 257, tail_keep: int = 64, directional: bool = False) -> None:
        if stats not in ("exact", "sketch"):
            raise ValueError("stats must be exact|sketch")
        self.stats, self.max_distinct, self.n_quantiles, self.tail_keep = stats, max_distinct, n_quantiles, tail_keep
        if top_k < 1:
            raise ValueError("top_k must be >= 1")
        self.features = tuple(features)
        # D53: only the attack-like side of each feature counts (FEATURE_DIRECTIONS; unknown features: both).
        self._up, self._dn = _direction_masks(self.features, directional)
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
        if self.stats == "sketch":
            self._sketch = [self._sketch_col(self.sorted[:, j]) for j in range(L.shape[1])]
            self.sorted = None  # only the fixed-size sketch is kept
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

    def _sketch_col(self, col: np.ndarray) -> tuple:
        vals, counts = np.unique(col, return_counts=True)
        if len(vals) <= self.max_distinct:
            cum = np.concatenate([[0], np.cumsum(counts)])
            return ("distinct", vals, cum)
        k = self.tail_keep
        q = np.quantile(col, np.linspace(0, 1, self.n_quantiles))
        return ("quantile", q, col[:k].copy(), col[-k:].copy())

    def _tail_counts(self, j: int, x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """(#train >= x, #train <= x) for feature j."""
        n = self.n
        if self.stats == "exact":
            col = self.sorted[:, j]
            return n - np.searchsorted(col, x, side="left"), np.searchsorted(col, x, side="right")
        sk = self._sketch[j]
        if sk[0] == "distinct":
            vals, cum = sk[1], sk[2]
            return n - cum[np.searchsorted(vals, x, side="left")], cum[np.searchsorted(vals, x, side="right")]
        _, q, bot, top = sk
        k = len(top)
        p = np.linspace(0, 1, len(q))
        ge = n * (1.0 - np.interp(x, q, p))  # body: interpolated quantiles
        le = n * np.interp(x, q, p)
        hi_tail = x > top[0]  # above the k-th largest value: exact rank among the kept extremes
        ge = np.where(hi_tail, k - np.searchsorted(top, x, side="left"), ge)
        lo_tail = x < bot[-1]
        le = np.where(lo_tail, np.searchsorted(bot, x, side="right"), le)
        return np.maximum(ge, 0.0), np.maximum(le, 0.0)

    def outlyingness(self, X: np.ndarray) -> np.ndarray:
        """Per-feature o_j for a matrix of raw feature rows (n_rows x F)."""
        if self._stale:
            self._fit()
        L = self._transform(np.asarray(X, dtype=float))
        o = np.empty_like(L)
        for j in range(L.shape[1]):
            ge, le = self._tail_counts(j, L[:, j])
            # max of the two one-sided tails = the two-sided min-count tail; a masked side contributes 0
            o_up = -np.log((ge + 1.0) / (self.n + 1.0)) if self._up[j] else 0.0
            o_dn = -np.log((le + 1.0) / (self.n + 1.0)) if self._dn[j] else 0.0
            o[:, j] = np.maximum(o_up, o_dn)
        o += (self._up * np.maximum(L - self.hi, 0.0) / self.s_up
              + self._dn * np.maximum(self.lo - L, 0.0) / self.s_dn)
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
        """Scoring state in float32: exact = sorted values; sketch = the fixed-size per-feature sketches.
        Both add range ends and side scales (4 floats per feature)."""
        if self.stats == "exact":
            return 4 * len(self.features) * (len(self.buffer) + 4)
        per = [2 * len(sk[1]) + 1 if sk[0] == "distinct" else len(sk[1]) + len(sk[2]) + len(sk[3])
               for sk in self._sketch]
        return 4 * (sum(per) + 4 * len(self.features))
