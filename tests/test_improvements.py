"""Preprocessing wrappers (D24), fusion (D25), sparse Extended IF and model sizes (D26)."""

from __future__ import annotations

import numpy as np
import pytest

from rad.models import build_detector
from rad.models.base import score_many
from rad.models.fusion import FusionDetector, TailCalibrator
from rad.models.preprocess import PreprocessedDetector, slog


def rows(n: int, n_feat: int, seed: int = 0, heavy: bool = False) -> list[dict[str, float]]:
    rng = np.random.default_rng(seed)
    m = rng.lognormal(3, 1, size=(n, n_feat)) if heavy else rng.normal(10, 1, size=(n, n_feat))
    return [{f"f{j}": float(v) for j, v in enumerate(r)} for r in m]


def feats(n: int) -> list[str]:
    return [f"f{j}" for j in range(n)]


ALL = {
    "hst": {"n_trees": 10, "height": 6, "window_size": 50, "seed": 0},
    "iforest": {"n_estimators": 30, "margin": 0.25, "hyperplane": True, "hyperplane_features": "sqrt", "seed": 0},
    "autoencoder": {"bootstrap_steps": 200, "seed": 0},
    "mad": {"tail_quantile": 0.999},
    "kitnet": {"max_autoencoder_size": 3},
}


def test_slog_is_odd_monotone_and_compressive():
    v = np.array([-1e6, -1.0, 0.0, 1.0, 1e6])
    out = slog(v)
    assert (np.diff(out) > 0).all() and out[2] == 0 and out[0] == -out[-1]
    assert out[-1] == pytest.approx(np.log1p(1e6))


@pytest.mark.parametrize("name", list(ALL))
@pytest.mark.parametrize("steps", [["slog"], ["slog", "project"]])
def test_preprocessing_wraps_every_detector(name, steps):
    params = {**ALL[name], "preprocess": {"steps": steps, "n_projections": 8}}
    det = build_detector(name, feats(6), params)
    assert isinstance(det, PreprocessedDetector)
    det.bootstrap(rows(200, 6, heavy=True))
    probe = rows(10, 6, seed=1, heavy=True)
    outlier = {f: 1e5 for f in feats(6)}
    s = score_many(det, probe + [outlier])
    assert ((s >= 0) & (s <= 1)).all()
    assert s[-1] > s[:-1].max()
    assert s == pytest.approx([det.score_one(x) for x in probe + [outlier]], rel=1e-5, abs=1e-8)  # float32 kernels
    det.learn_one(probe[0])  # learning goes through the same transform
    if "project" in steps:
        assert det.inner.features == tuple(f"p{i}" for i in range(8))


def test_projection_is_frozen_and_seeded():
    a = build_detector("mad", feats(5), {"preprocess": {"steps": ["project"], "n_projections": 4, "seed": 7}})
    b = build_detector("mad", feats(5), {"preprocess": {"steps": ["project"], "n_projections": 4, "seed": 7}})
    a.bootstrap(rows(100, 5))
    b.bootstrap(rows(100, 5))
    np.testing.assert_array_equal(a.W, b.W)
    np.testing.assert_allclose(np.linalg.norm(a.W, axis=1), 1.0)
    w0 = a.W.copy()
    for x in rows(20, 5, seed=3):
        a.learn_one(x)
    np.testing.assert_array_equal(a.W, w0)  # learning never moves the transform


def test_preprocess_rejects_unknown_steps():
    with pytest.raises(ValueError):
        PreprocessedDetector(feats(2), lambda f: None, ["fft"])


def test_tail_calibrator_orders_scores_beyond_calibration():
    cal = TailCalibrator(0.9).fit(np.linspace(0, 1, 101))
    nlp = cal.neg_log_p(np.array([0.0, 0.5, 0.95, 1.0, 2.0, 10.0]))
    assert (np.diff(nlp) > 0).all()  # strictly increasing, no ties beyond the max
    assert nlp[0] == pytest.approx(0.0, abs=0.01)


def test_fusion_catches_what_either_member_catches():
    train = rows(400, 4)
    det = FusionDetector(feats(4), {"mad": {"tail_quantile": 0.999},
                                    "iforest": {"n_estimators": 50, "margin": 0.25, "hyperplane": True, "seed": 0}})
    det.bootstrap(train)
    benign = score_many(det, rows(300, 4, seed=5))
    one_feature = dict(rows(1, 4, seed=6)[0], f0=40.0)
    assert det.score_one(one_feature) > np.quantile(benign, 0.99)
    assert ((benign >= 0) & (benign < 1)).all()
    assert det.model_bytes() > 0


def test_sparse_hyperplanes_use_sqrt_features():
    det = build_detector("iforest", feats(100), ALL["iforest"])
    det.bootstrap(rows(300, 100))
    normals = det.model.trees[0][5]
    internal = det.model.trees[0][0] >= 0
    assert ((normals[internal] != 0).sum(axis=1) == 10).all()  # ceil(sqrt(100))


@pytest.mark.parametrize("name", list(ALL))
def test_every_detector_reports_a_router_model_size(name):
    det = build_detector(name, feats(28), ALL[name])
    det.bootstrap(rows(200, 28))
    kb = det.model_bytes() / 1024
    assert 0 < kb < 10 * 1024  # under the 10 MB router budget
