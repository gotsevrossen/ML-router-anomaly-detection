"""RobustZ (D27): two-sided range-calibrated robust z, top-k aggregation, sketch state, int16 params."""

from __future__ import annotations

import numpy as np
import pytest

from rad.models import build_detector
from rad.models.base import score_many
from rad.models.robust_z import RobustZDetector


def rows(m: np.ndarray, names) -> list[dict[str, float]]:
    return [dict(zip(names, r.tolist())) for r in m]


def test_training_range_edge_is_at_tail_z_on_both_sides_of_every_feature():
    rng = np.random.default_rng(0)
    # a: symmetric; b: heavily right-skewed (the N-BaIoT failure case)
    m = np.c_[rng.normal(0, 1, 5000), rng.lognormal(0, 1.5, 5000)]
    det = RobustZDetector(["a", "b"], slog=False, top_k=1)
    det.bootstrap(rows(m, "ab"))
    for j in range(2):
        hi = (m[:, j].max() - det.median[j]) * det.inv_up[j]
        lo = (det.median[j] - m[:, j].min()) * det.inv_dn[j]
        assert hi == pytest.approx(3.0, rel=1e-4) or hi < 3.0  # the robust floor can only make it smaller
        assert lo == pytest.approx(3.0, rel=1e-4) or lo < 3.0
    sym = RobustZDetector(["a", "b"], slog=False, two_sided=False, top_k=1)
    sym.bootstrap(rows(m, "ab"))
    assert sym.inv_up[1] == sym.inv_dn[1]


def test_a_long_tail_on_one_side_no_longer_inflates_the_other_side():
    """The Gafgyt TCP/UDP case: a step below a right-skewed feature's minimum must count more
    with two-sided scales than with one symmetric scale set by the long upper tail."""
    rng = np.random.default_rng(1)
    m = np.c_[rng.normal(10, 1, 3000), rng.lognormal(2, 1.0, 3000)]
    two = RobustZDetector(["a", "b"], slog=False, top_k=1)
    one = RobustZDetector(["a", "b"], slog=False, top_k=1, two_sided=False)
    for d in (two, one):
        d.bootstrap(rows(m, "ab"))
    assert two.inv_dn[1] > 3 * one.inv_dn[1]  # the lower side gets a much tighter scale
    below_b = {"a": 10.0, "b": float(m[:, 1].min() - 2.0)}
    inside = score_many(two, rows(m[:2000], "ab"))
    assert two.score_one(below_b) > one.score_one(below_b)
    assert two.score_one(below_b) > np.median(inside)  # the robust floor keeps this side moderate (D27)


def test_top_k_needs_several_unusual_features():
    m = np.random.default_rng(2).normal(0, 1, (2000, 6))
    names = [f"f{i}" for i in range(6)]
    det = RobustZDetector(names, slog=False, top_k=3)
    det.bootstrap(rows(m, names))
    one_feature = dict(zip(names, [20.0, 0, 0, 0, 0, 0]))
    three_features = dict(zip(names, [20.0, 20.0, 20.0, 0, 0, 0]))
    assert det.score_one(three_features) > det.score_one(one_feature)


@pytest.mark.parametrize("stats", ["exact", "sketch"])
@pytest.mark.parametrize("precision", ["float32", "int16"])
def test_variants_agree_closely_and_paths_match(stats, precision):
    m = np.random.default_rng(3).lognormal(1, 1, (3000, 8))
    names = [f"f{i}" for i in range(8)]
    ref = RobustZDetector(names)
    det = RobustZDetector(names, stats=stats, precision=precision)
    for d in (ref, det):
        d.bootstrap(rows(m[:2000], names))
    probe = rows(m[2000:], names)
    a, b = score_many(ref, probe), score_many(det, probe)
    assert np.corrcoef(a, b)[0, 1] > 0.98  # sketch / int16 only perturb the parameters
    assert b == pytest.approx(det.score_matrix(m[2000:]), rel=1e-6)
    assert b == pytest.approx([det.score_one(x) for x in probe[:20]] + list(b[20:]), rel=1e-6)


def test_learning_updates_lazily_and_sketch_state_is_small():
    m = np.random.default_rng(4).normal(5, 1, (1000, 28))
    names = [f"f{i}" for i in range(28)]
    det = RobustZDetector(names, stats="sketch", precision="int16")
    det.bootstrap(rows(m, names))
    far = dict(zip(names, [50.0] * 28))
    before = det.score_one(far)
    for _ in range(50):
        det.learn_one(far)  # a committed shift widens the learned range
    assert det.score_one(far) < before
    assert det.model_bytes() == 28 * 9  # 3 int16 mantissas + 3 int8 exponents per feature
    assert det.state_bytes() < 8 * 1024  # histograms + extremes, no row buffer
    exact = RobustZDetector(names, window=2880)
    exact.bootstrap(rows(m, names))
    assert exact.state_bytes() > 300 * 1024


def test_registered_and_validated():
    det = build_detector("robust_z", ["a"], {"stats": "sketch"})
    assert isinstance(det, RobustZDetector)
    with pytest.raises(ValueError):
        RobustZDetector(["a"], stats="median-of-medians")
    with pytest.raises(ValueError):
        RobustZDetector(["a"], top_k=0)
