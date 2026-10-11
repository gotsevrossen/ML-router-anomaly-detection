"""RobustZ: the router-ready MAD-family detector (D27).

One fused, vectorised pass per window:

    L   = slog(x)                                  sign(x) * log(1 + |x|)
    d   = L - median                               per feature
    z_j = d_j / s_up_j  if d_j >= 0  else  -d_j / s_dn_j
    r   = mean of the k largest z_j                (k = 3)
    score = log1p(r) / (1 + log1p(r))

Scales are two-sided and range-calibrated (D27): for each side of each feature,
s = max(robust MAD-type scale, extreme training deviation on that side / tail_z),
so the training range ends at z <= tail_z = 3 on every side of every feature (the
robust floor can only pull the edge inward). A long tail on one side no longer
inflates the other side's scale, which is what hid the Gafgyt TCP/UDP floods on
N-BaIoT: they step just below a lopsided feature's minimum. The robust floor was
kept because removing it was slightly worse on the development sets.

Router state for scoring: median plus two reciprocal scales per feature
(3F float32, or 3F int16 mantissas plus one shared exponent each, see
`precision`). Learning can keep `stats: sketch` state instead of a window of rows:
one fixed-bin histogram per feature (D19 sketch) plus running per-side extremes.
"""

from __future__ import annotations

from collections import deque
from typing import Sequence

import numpy as np

from rad.continual.sketch import FeatureHistograms

MAD_TO_SIGMA = 1.4826
MEANAD_TO_SIGMA = 1.2533
IQR_TO_SIGMA = 1.349


def _slog(m: np.ndarray) -> np.ndarray:
    return np.sign(m) * np.log1p(np.abs(m))


def _quantize(v: np.ndarray) -> np.ndarray:
    """Round to int16 mantissas with one power-of-two exponent per feature (block floating point)."""
    e = np.ceil(np.log2(np.maximum(np.abs(v), 1e-300))) - 14  # leaves headroom inside int16
    return np.round(v / 2.0 ** e) * 2.0 ** e


class RobustZDetector:
    def __init__(self, features: Sequence[str], slog: bool = True, two_sided: bool = True,
                 tail_quantile: float = 1.0, tail_z: float = 3.0, top_k: int = 3, stats: str = "exact",
                 window: int = 2880, n_bins: int = 64, precision: str = "float32", min_scale: float = 0.0,
                 monotone_scales: bool = False) -> None:
        if stats not in ("exact", "sketch") or precision not in ("float32", "int16"):
            raise ValueError("stats must be exact|sketch and precision float32|int16")
        if not 0.5 <= tail_quantile <= 1.0 or top_k < 1:
            raise ValueError("need tail_quantile in [0.5, 1] and top_k >= 1")
        self.features = tuple(features)
        self.slog, self.two_sided = slog, two_sided
        self.tail_quantile, self.tail_z = tail_quantile, tail_z
        self.top_k = min(top_k, len(self.features))
        self.min_scale = min_scale  # D32: resolution floor on every side's scale
        # D44: after learning, a side's scale never falls below its bootstrap value. Adaptation may widen
        # "normal" (fewer false alarms through drift) but never makes the model more sensitive than at
        # bootstrap; how far it may widen is the drift budget's job.
        self.monotone_scales = monotone_scales
        self._boot_inv: tuple[np.ndarray, np.ndarray] | None = None
        self.stats, self.precision = stats, precision
        self.n_bins = n_bins
        self.buffer: deque[np.ndarray] = deque(maxlen=window)  # stats == "exact"
        self.hist: FeatureHistograms | None = None  # stats == "sketch"
        self.ext_hi: np.ndarray | None = None
        self.ext_lo: np.ndarray | None = None
        self.median = self.inv_up = self.inv_dn = None
        self._stale = False

    # -- parameters -------------------------------------------------------------------

    def _transform(self, m: np.ndarray) -> np.ndarray:
        return _slog(m) if self.slog else m

    def _set(self, med: np.ndarray, base: np.ndarray, up_dev: np.ndarray, dn_dev: np.ndarray) -> None:
        base = np.where(base > 0, base, 1.0)
        up = np.maximum(base, np.where(up_dev > 0, up_dev / self.tail_z, base))
        dn = np.maximum(base, np.where(dn_dev > 0, dn_dev / self.tail_z, base))
        up, dn = np.maximum(up, self.min_scale), np.maximum(dn, self.min_scale)
        if self.monotone_scales and self._boot_inv is not None:
            up, dn = np.maximum(up, 1.0 / self._boot_inv[0]), np.maximum(dn, 1.0 / self._boot_inv[1])
        if not self.two_sided:
            up = dn = np.maximum(up, dn)
        inv_up, inv_dn = 1.0 / up, 1.0 / dn
        if self.precision == "int16":
            med, inv_up, inv_dn = _quantize(med), _quantize(inv_up), _quantize(inv_dn)
        self.median = med.astype(np.float32)
        self.inv_up = inv_up.astype(np.float32)
        self.inv_dn = inv_dn.astype(np.float32)
        self._stale = False

    def _fit_exact(self, L: np.ndarray) -> None:
        med = np.median(L, axis=0)
        absdev = np.abs(L - med)
        base = MAD_TO_SIGMA * np.median(absdev, axis=0)
        fb = MEANAD_TO_SIGMA * absdev.mean(axis=0)
        base = np.where(base > 0, base, fb)
        q = self.tail_quantile
        up_dev = np.quantile(np.maximum(L - med, 0.0), q, axis=0)
        dn_dev = np.quantile(np.maximum(med - L, 0.0), q, axis=0)
        self._set(med, base, up_dev, dn_dev)

    def _fit_sketch(self) -> None:
        med = self.hist.median()
        q25, q75 = self.hist.quantile(0.25), self.hist.quantile(0.75)
        base = (q75 - q25) / IQR_TO_SIGMA  # sigma from the IQR (equals 1.4826 * MAD for normal data)
        if self.tail_quantile >= 1.0:
            up_dev, dn_dev = np.maximum(self.ext_hi - med, 0.0), np.maximum(med - self.ext_lo, 0.0)
        else:
            up_dev = np.maximum(self.hist.quantile(self.tail_quantile) - med, 0.0)
            dn_dev = np.maximum(med - self.hist.quantile(1.0 - self.tail_quantile), 0.0)
        self._set(med, base, up_dev, dn_dev)

    # -- Detector interface ---------------------------------------------------------------

    def matrix(self, xs: Sequence[dict[str, float]]) -> np.ndarray:
        return np.array([[x[f] for f in self.features] for x in xs], dtype=float).reshape(-1, len(self.features))

    def bootstrap(self, xs: Sequence[dict[str, float]]) -> None:
        L = self._transform(self.matrix(xs))
        if self.stats == "exact":
            self.buffer.extend(L)
            self._fit_exact(L)
        else:
            lo, hi = L.min(axis=0), L.max(axis=0)
            self.hist = FeatureHistograms(self.features, lo, hi, n_bins=self.n_bins)
            for v in L:
                self.hist.add_vec(v)
            self.ext_lo, self.ext_hi = lo.copy(), hi.copy()
            self._fit_sketch()
        self._boot_inv = (np.array(self.inv_up, dtype=float), np.array(self.inv_dn, dtype=float))

    def score_matrix(self, X: np.ndarray) -> np.ndarray:
        """Fast path on a float matrix in feature order (what the C port does per window)."""
        if self._stale:
            if self.stats == "exact":
                self._fit_exact(np.vstack(self.buffer))
            else:
                self._fit_sketch()
        d = self._transform(np.asarray(X, dtype=np.float32)) - self.median
        z = np.where(d >= 0, d * self.inv_up, -d * self.inv_dn)
        k = self.top_k
        r = np.partition(z, z.shape[1] - k, axis=1)[:, -k:].mean(axis=1) if k > 1 else z.max(axis=1)
        lg = np.log1p(np.maximum(r, 0.0).astype(np.float64))
        return lg / (1.0 + lg)

    def score_many(self, xs: Sequence[dict[str, float]]) -> np.ndarray:
        return self.score_matrix(self.matrix(xs))

    def score_one(self, x: dict[str, float]) -> float:
        return float(self.score_many([x])[0])

    def learn_one(self, x: dict[str, float]) -> None:
        v = self._transform(self.matrix([x])[0])
        if self.stats == "exact":
            self.buffer.append(v)
        else:
            self.hist.add_vec(v)
            self.ext_lo, self.ext_hi = np.minimum(self.ext_lo, v), np.maximum(self.ext_hi, v)
        self._stale = True  # parameters are refreshed lazily at the next score

    def model_bytes(self) -> int:
        """Scoring state: median + two reciprocal scales per feature (D27)."""
        per = 2 if self.precision == "int16" else 4
        return 3 * len(self.features) * per + (3 * 1 if self.precision == "int16" else 0) * len(self.features)

    def state_bytes(self) -> int:
        """Scoring state plus what learning keeps (row window for exact, histograms + extremes for sketch)."""
        if self.stats == "exact":
            return self.model_bytes() + 4 * len(self.features) * (self.buffer.maxlen or len(self.buffer))
        return self.model_bytes() + 4 * len(self.features) * (self.n_bins + 2 + 2)
