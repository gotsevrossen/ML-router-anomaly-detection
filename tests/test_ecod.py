from __future__ import annotations

import numpy as np

from rad.models import build_detector
from rad.models.base import score_many


def _rows(n=2000, seed=0):
    rng = np.random.default_rng(seed)
    rows = [{"pkts": float(rng.integers(50, 150)), "new_lan": 0.0} for _ in range(n)]
    if n > 100:
        rows[100]["new_lan"] = 8.0  # one benign burst in training
    return rows


def test_rare_novelty_scores_high_even_after_a_training_burst():
    """D39: one new LAN peer is rare (1 window in 2000 had any), so it must stand out."""
    det = build_detector("ecod", ["pkts", "new_lan"], {"top_k": 1})
    det.bootstrap(_rows())
    normal = det.score_one({"pkts": 100.0, "new_lan": 0.0})
    attacker = det.score_one({"pkts": 100.0, "new_lan": 1.0})
    rz = build_detector("robust_z", ["pkts", "new_lan"], {"top_k": 1})
    rz.bootstrap(_rows())
    # RobustZ scales new_lan by the burst (z of one new peer < 1); ECOD ranks it by rarity instead.
    assert attacker > normal + 0.3  # a typical value scores about -log(0.5) on its own feature
    assert attacker > rz.score_one({"pkts": 100.0, "new_lan": 1.0}) + 0.2


def test_scores_keep_growing_beyond_the_training_range():
    det = build_detector("ecod", ["pkts", "new_lan"], {"top_k": 1})
    det.bootstrap(_rows())
    s = [det.score_one({"pkts": v, "new_lan": 0.0}) for v in (200.0, 2_000.0, 200_000.0)]
    assert s[0] < s[1] < s[2] < 1.0


def test_score_many_matches_score_one():
    det = build_detector("ecod", ["pkts", "new_lan"], {"top_k": 2})
    det.bootstrap(_rows())
    xs = _rows(20, seed=1)
    assert np.allclose(score_many(det, xs), [det.score_one(x) for x in xs])
