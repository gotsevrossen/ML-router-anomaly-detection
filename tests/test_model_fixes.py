"""Regression tests for the IForest headroom / extended variants (D22) and MAD's tail floor (D23)."""

from __future__ import annotations

import numpy as np
import pytest

from rad.models import build_detector
from rad.models.base import score_many
from rad.models.mad import MADDetector, tail_calibrated_scale


def rows(n: int, n_feat: int, seed: int = 0) -> list[dict[str, float]]:
    rng = np.random.default_rng(seed)
    return [{f"f{j}": float(v) for j, v in enumerate(r)} for r in rng.normal(10, 1, size=(n, n_feat))]


def feats(n_feat: int) -> list[str]:
    return [f"f{j}" for j in range(n_feat)]


def test_headroom_forest_separates_far_out_points_from_the_training_edge():
    """Textbook IF puts a point far beyond the range in the same leaf as the extreme training point."""
    train = [{"a": float(v)} for v in np.random.default_rng(0).normal(10, 1, 500)]
    edge, far = {"a": max(r["a"] for r in train)}, {"a": 1000.0}
    gap = {}
    for name, params in {"sklearn": {}, "headroom": {"margin": 0.25}}.items():
        det = build_detector("iforest", ["a"], {"n_estimators": 100, "seed": 0, **params})
        det.bootstrap(train)
        gap[name] = det.score_one(far) - det.score_one(edge)
    assert gap["sklearn"] == pytest.approx(0.0, abs=1e-9)
    assert gap["headroom"] > 0.02


def test_extended_forest_finds_an_outlier_in_a_few_of_many_features():
    n_feat = 100
    train = rows(600, n_feat)
    normal_probe = rows(200, n_feat, seed=1)
    outlier = dict(normal_probe[0])
    for j in range(5):  # 5 of 100 features far out of range
        outlier[f"f{j}"] = 60.0
    scores = {}
    for name, params in {"axis": {"margin": 0.25}, "extended": {"margin": 0.25, "hyperplane": True}}.items():
        det = build_detector("iforest", feats(n_feat), {"n_estimators": 100, "seed": 0, **params})
        det.bootstrap(train)
        s_norm = score_many(det, normal_probe)
        scores[name] = (det.score_one(outlier) - np.quantile(s_norm, 0.99))
    assert scores["extended"] > 0.05
    assert scores["extended"] > scores["axis"]


@pytest.mark.parametrize("params", [{"margin": 0.25}, {"margin": 0.25, "hyperplane": True}])
def test_custom_forest_is_deterministic_bounded_and_batch_consistent(params):
    train, probe = rows(300, 6), rows(20, 6, seed=2)
    a = build_detector("iforest", feats(6), {"n_estimators": 30, "seed": 3, **params})
    b = build_detector("iforest", feats(6), {"n_estimators": 30, "seed": 3, **params})
    a.bootstrap(train)
    b.bootstrap(train)
    sa = score_many(a, probe)
    assert (sa == score_many(b, probe)).all()
    assert ((sa > 0) & (sa <= 1)).all()
    assert sa == pytest.approx([a.score_one(x) for x in probe])


def test_tail_floor_stops_near_constant_features_dominating():
    rng = np.random.default_rng(0)
    # 'noise' is constant except rare tiny wiggles (MAD = 0); 'signal' carries the real behaviour.
    def make(n, wiggle):
        noise = np.where(rng.random(n) < 0.05, 1e-9 * rng.normal(size=n), 0.0) if wiggle else np.zeros(n)
        return [{"noise": float(a), "signal": float(b)} for a, b in zip(noise, rng.normal(50, 5, n))]

    train, benign = make(5000, True), make(2000, True)
    attack = [{"noise": 0.0, "signal": 150.0}] * 50
    for tail, expect_ok in ((None, False), (0.999, True)):
        det = MADDetector(["noise", "signal"], window=10_000, tail_quantile=tail)
        det.bootstrap(train)
        separated = bool(score_many(det, attack).min() > np.quantile(score_many(det, benign), 0.999))
        assert separated is expect_ok, tail


def test_tail_calibrated_scale_maps_the_training_extreme_to_tail_z():
    data = np.random.default_rng(0).normal(0, 1, size=(10_000, 1))
    med, scale = tail_calibrated_scale(data, 1.0, 3.0)
    assert np.abs(data - med).max() / scale[0] == pytest.approx(3.0)
    _, plain = tail_calibrated_scale(data, None)
    assert plain[0] == pytest.approx(1.0, abs=0.05)  # plain MAD scale estimates sigma
    with pytest.raises(ValueError):
        MADDetector(["a"], tail_quantile=0.2)


def test_type_alias_builds_variants():
    det = build_detector("mad_tail", ["a"], {"type": "mad", "tail_quantile": 0.99})
    assert isinstance(det, MADDetector) and det.tail_quantile == 0.99
