"""Min-p fusion of several detectors (D25).

Different detectors miss different attacks (on N-BaIoT, MAD with the tail floor
catches Mirai scans that the autoencoder misses, and the autoencoder catches
Gafgyt combo that HST misses). Fusion alerts on whichever member is most surprised:

  1. Bootstrap: members train on the first (1 - calib_frac) of the bootstrap
     windows; the last calib_frac windows, which they never trained on, calibrate
     each member's score to a benign p-value.
  2. p-value: empirical below the calibration `tail_quantile`, exponential tail
     above it (peaks-over-threshold with an exponential excess, Siffer et al. 2017
     style), so scores beyond anything seen in calibration keep their order
     instead of all tying at p = 1/(n+1).
  3. Combined: p = min(1, m * min_i p_i) (Bonferroni over m members), and the
     score is squash(-log p). Computed in log space, so it never underflows.

Unsupervised and benign-only throughout. Router cost: the members, plus a
sorted calibration array and two floats per member.
"""

from __future__ import annotations

import math
from typing import Any, Sequence

import numpy as np

from rad.models.base import Detector, score_many, squash_array


class TailCalibrator:
    """Benign score -> -log(p-value), from calibration scores."""

    def __init__(self, tail_quantile: float = 0.9) -> None:
        self.tail_quantile = tail_quantile
        self.cal: np.ndarray | None = None
        self.u = 0.0
        self.log_pu = 0.0
        self.beta = 1.0

    def fit(self, scores: np.ndarray) -> "TailCalibrator":
        s = np.sort(np.asarray(scores, dtype=float))
        if len(s) == 0:
            raise ValueError("need calibration scores")
        self.cal = s
        n = len(s)
        self.u = float(np.quantile(s, self.tail_quantile))
        excess = s[s > self.u] - self.u
        spread = float(s[-1] - s[0])
        self.beta = float(excess.mean()) if len(excess) and excess.mean() > 0 else max(spread, 1e-6) / 10
        self.log_pu = math.log((1 + int((s > self.u).sum())) / (n + 1))
        return self

    def neg_log_p(self, scores: np.ndarray) -> np.ndarray:
        s = np.asarray(scores, dtype=float)
        n = len(self.cal)
        at_or_above = n - np.searchsorted(self.cal, s, side="left")
        empirical = -np.log((1 + at_or_above) / (n + 1))
        tail = -(self.log_pu - (s - self.u) / self.beta)
        return np.where(s > self.u, np.maximum(tail, -self.log_pu), empirical)


class FusionDetector:
    def __init__(self, features: Sequence[str], members: dict[str, dict[str, Any]], calib_frac: float = 0.2,
                 tail_quantile: float = 0.9) -> None:
        if not members:
            raise ValueError("fusion needs at least one member")
        if not 0 < calib_frac < 1:
            raise ValueError("calib_frac must be in (0, 1)")
        self.features = tuple(features)
        self.member_cfg = members
        self.calib_frac = calib_frac
        self.tail_quantile = tail_quantile
        self.members: dict[str, Detector] = {}
        self.calibrators: dict[str, TailCalibrator] = {}

    def bootstrap(self, xs: Sequence[dict[str, float]]) -> None:
        from rad.models import build_detector

        xs = list(xs)
        n_cal = max(2, int(round(self.calib_frac * len(xs))))
        train, cal = xs[:-n_cal], xs[-n_cal:]
        for name, params in self.member_cfg.items():
            det = build_detector(name, self.features, params)
            det.bootstrap(train)
            self.members[name] = det
            self.calibrators[name] = TailCalibrator(self.tail_quantile).fit(score_many(det, cal))

    def member_neg_log_p(self, xs: Sequence[dict[str, float]]) -> dict[str, np.ndarray]:
        return {name: self.calibrators[name].neg_log_p(score_many(det, xs)) for name, det in self.members.items()}

    def score_many(self, xs: Sequence[dict[str, float]]) -> np.ndarray:
        nlp = np.vstack(list(self.member_neg_log_p(xs).values()))
        combined = np.maximum(nlp.max(axis=0) - math.log(len(self.members)), 0.0)  # -log(min(1, m * min p))
        return squash_array(combined)

    def score_one(self, x: dict[str, float]) -> float:
        return float(self.score_many([x])[0])

    def learn_one(self, x: dict[str, float]) -> None:
        for det in self.members.values():
            det.learn_one(x)

    def model_bytes(self) -> int:
        total = sum(getattr(d, "model_bytes", lambda: 0)() for d in self.members.values())
        return total + sum(4 * (len(c.cal) + 3) for c in self.calibrators.values())
