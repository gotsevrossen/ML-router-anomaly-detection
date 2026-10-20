"""D53: strict persistence, the strict dual alarm channel, and direction-aware detectors."""
from __future__ import annotations

import numpy as np
import pytest

from rad.eval import metrics as M
from rad.models import build_detector


def test_persist_strict_needs_k_observed_windows_and_resets_after_gaps():
    starts = np.array([0, 30, 60, 90, 120, 1000, 1030, 1060], dtype=float)  # a gap before 1000
    s = np.array([5, 1, 2, 3, 4, 9, 9, 9], dtype=float)
    p = M.persist_strict(s, starts, 30.0, 3)
    assert np.isnan(p[:2]).all() and p[2] == 1 and p[3] == 1 and p[4] == 2
    assert np.isnan(p[5:7]).all()  # the first windows after the gap have no persistent channel
    assert p[7] == 9
    # D40's version judged the first window after the gap on itself alone:
    assert M.persist_min(s, starts, 30.0, 3)[5] == 9


def test_strict_dual_channels_and_thresholds():
    starts = np.arange(40, dtype=float) * 30
    known = np.zeros(40, bool); known[:10] = True
    val = np.zeros(40, bool); val[10:20] = True
    s = np.full(40, 0.5)
    s[:20] = np.linspace(0.40, 0.60, 20)  # benign: max 0.60
    s[25] = 0.65  # one strong window: raw channel only if beyond max + margin
    s[30:36] = 0.62  # sustained, moderately high: persistent channel
    f = M.strict_dual_alarm_score(s, starts, 30.0, 4, known, val, alarms_per_day=0.0, margin=0.02)
    assert f[25] >= 0  # 0.65 > 0.60 + 0.02
    assert f[33] >= 0 and f[35] >= 0  # 4 windows at 0.62 > every persistent bootstrap/validation level
    assert (f[:20] < 0).all()  # nothing seen in bootstrap/validation alarms
    g = M.strict_dual_alarm_score(s, starts, 30.0, 4, known, val, alarms_per_day=0.0, margin=0.1)
    assert g[25] < 0  # the margin keeps the raw channel above the benign maximum


@pytest.mark.parametrize("name,params", [("ecod", {"type": "ecod", "stats": "sketch"}),
                                         ("robust_z", {"type": "robust_z"})])
def test_directional_detectors_ignore_the_benign_side(name, params):
    rng = np.random.default_rng(0)
    feats = ["pkts_in", "iat_mean", "pkt_size_mean"]  # up, down, both
    rows = [{"pkts_in": float(v), "iat_mean": float(a), "pkt_size_mean": float(b)}
            for v, a, b in zip(rng.integers(50, 150, 2000), rng.uniform(1, 3, 2000), rng.uniform(100, 300, 2000))]
    two = build_detector(name, feats, {**params, "top_k": 1})
    one = build_detector(name, feats, {**params, "top_k": 1, "directional": True})
    two.bootstrap(rows); one.bootstrap(rows)
    quiet = {"pkts_in": 1.0, "iat_mean": 2.0, "pkt_size_mean": 200.0}  # far fewer packets: benign side
    slow = {"pkts_in": 100.0, "iat_mean": 60.0, "pkt_size_mean": 200.0}  # much larger gaps: benign side
    flood = {"pkts_in": 5000.0, "iat_mean": 0.001, "pkt_size_mean": 200.0}
    small = {"pkts_in": 100.0, "iat_mean": 2.0, "pkt_size_mean": 20.0}  # 'both' feature keeps both sides
    for x in (quiet, slow):
        assert two.score_one(x) > 0.5 and one.score_one(x) < two.score_one(x)
    assert one.score_one(flood) == pytest.approx(two.score_one(flood), rel=1e-6)
    assert one.score_one(small) == pytest.approx(two.score_one(small), rel=1e-6)


def test_ecod_refit_every_batches_learning():
    """D57: refit_every=1 is the old behaviour; with N, the model changes after every N learned windows."""
    rng = np.random.default_rng(2)
    feats = ["pkts_in", "bytes_in"]
    rows = [{"pkts_in": float(v), "bytes_in": float(v * 100)} for v in rng.integers(50, 150, 500)]
    new = [{"pkts_in": 400.0, "bytes_in": 40_000.0}] * 10
    probe = {"pkts_in": 400.0, "bytes_in": 40_000.0}
    every1 = build_detector("ecod", feats, {"type": "ecod", "stats": "sketch"})
    every5 = build_detector("ecod", feats, {"type": "ecod", "stats": "sketch", "refit_every": 5})
    every1.bootstrap(rows); every5.bootstrap(rows)
    before = every5.score_one(probe)
    for i, x in enumerate(new, 1):
        every1.learn_one(x); every5.learn_one(x)
        if i == 4:
            assert every5.score_one(probe) == before  # nothing refitted yet
        if i == 5:
            assert every5.score_one(probe) < before  # refitted after 5
    assert every1.score_one(probe) == pytest.approx(every5.score_one(probe))  # same data after 10
    with pytest.raises(ValueError):
        build_detector("ecod", feats, {"type": "ecod", "refit_every": 0})
