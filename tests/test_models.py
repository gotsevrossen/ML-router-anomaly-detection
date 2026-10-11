"""Detector contract tests on small seeded synthetic data with an obvious outlier."""

from __future__ import annotations

import numpy as np
import pytest

from rad.features.packet_schema import ARP_REQUEST, PacketRecord
from rad.models import build_detector
from rad.models.base import FixedMinMaxScaler, score_many, squash
from rad.models.kitsune_wrapper import kitsune_packet_fields, kitsune_window_scores
from rad.models.mad import MADDetector

FEATURES = ["a", "b", "c", "d"]
PARAMS = {
    "hst": {"n_trees": 10, "height": 6, "window_size": 50, "seed": 1},
    "iforest": {"n_estimators": 50, "seed": 1},
    "autoencoder": {"hidden": 2, "bootstrap_steps": 300, "seed": 1},
    "mad": {},
    "kitnet": {"max_autoencoder_size": 2},
}


def normal_rows(n: int, seed: int = 0) -> list[dict[str, float]]:
    rng = np.random.default_rng(seed)
    return [dict(zip(FEATURES, rng.normal([10, 5, 0.5, 100], [1, 0.5, 0.05, 5]).tolist())) for _ in range(n)]


OUTLIER = {"a": 40.0, "b": 30.0, "c": 0.0, "d": 400.0}


@pytest.mark.parametrize("name", list(PARAMS))
def test_outlier_scores_above_every_normal_window(name):
    det = build_detector(name, FEATURES, PARAMS[name])
    det.bootstrap(normal_rows(200))
    normal = [det.score_one(x) for x in normal_rows(50, seed=1)]
    outlier = det.score_one(OUTLIER)
    assert all(0.0 <= s <= 1.0 for s in [*normal, outlier])
    assert outlier > max(normal)


@pytest.mark.parametrize("name", list(PARAMS))
def test_scoring_does_not_learn(name):
    det = build_detector(name, FEATURES, PARAMS[name])
    det.bootstrap(normal_rows(100))
    probe = normal_rows(3, seed=5)
    first = [det.score_one(x) for x in probe]
    for _ in range(3):
        det.score_one(OUTLIER)
    assert [det.score_one(x) for x in probe] == first


@pytest.mark.parametrize("name", list(PARAMS))
def test_same_seed_same_scores(name):
    scores = []
    for _ in range(2):
        det = build_detector(name, FEATURES, PARAMS[name])
        det.bootstrap(normal_rows(100))
        scores.append([det.score_one(x) for x in normal_rows(5, seed=9)])
    assert scores[0] == scores[1]


@pytest.mark.parametrize("name", list(PARAMS))
def test_score_many_equals_score_one(name):
    det = build_detector(name, FEATURES, PARAMS[name])
    det.bootstrap(normal_rows(100))
    probe = normal_rows(10, seed=3) + [OUTLIER]
    assert score_many(det, probe) == pytest.approx([det.score_one(x) for x in probe], rel=1e-6, abs=1e-9)


def test_hst_rejects_bootstrap_shorter_than_window():
    det = build_detector("hst", FEATURES, {"window_size": 50})
    with pytest.raises(ValueError, match="window_size"):
        det.bootstrap(normal_rows(10))


def test_fixed_minmax_scaler_freezes_and_clips():
    sc = FixedMinMaxScaler(["x", "k"]).fit([{"x": 0, "k": 3}, {"x": 10, "k": 3}])
    assert sc.transform({"x": 5, "k": 3}) == {"x": 0.5, "k": 0.0}
    assert sc.transform({"x": 50, "k": 4}) == {"x": 1.0, "k": 1.0}  # clipped; constant feature rose
    assert sc.transform({"x": -5, "k": 2}) == {"x": 0.0, "k": 0.0}


def test_scaler_margin_keeps_headroom_beyond_bootstrap():
    sc = FixedMinMaxScaler(["x", "k"], margin=0.25).fit([{"x": 0, "k": 3}, {"x": 10, "k": 3}])
    assert sc.transform({"x": 0, "k": 3}) == {"x": 0.25, "k": 0.25}
    assert sc.transform({"x": 10, "k": 4}) == {"x": 0.75, "k": 1.0}
    assert sc.transform({"x": 15, "k": 3})["x"] == pytest.approx(1.0)  # half a range beyond the max
    assert sc.transform({"x": 100, "k": 3})["x"] == 1.0
    with pytest.raises(ValueError):
        FixedMinMaxScaler(["x"], margin=0.5)


def test_hst_separates_values_far_beyond_bootstrap_range():
    """Regression for D14: with clipping and no headroom, far-out values look like the bootstrap max."""
    rng = np.random.default_rng(0)
    rows = [{"a": float(v)} for v in rng.normal(10, 1, 300)]
    top = {"a": max(r["a"] for r in rows)}
    gap = {}
    for margin in (0.0, 0.25):
        det = build_detector("hst", ["a"], {"n_trees": 25, "height": 8, "window_size": 250, "seed": 0, "margin": margin})
        det.bootstrap(rows)
        gap[margin] = det.score_one({"a": 1000.0}) - det.score_one(top)
    assert gap[0.0] == 0.0  # clipped onto the bootstrap max: indistinguishable
    assert gap[0.25] > 0.0


def test_mad_score_matches_formula():
    det = MADDetector(["x", "k"])
    det.bootstrap([{"x": v, "k": 7.0} for v in [1.0, 2.0, 3.0, 4.0, 100.0]])
    # x: median 3, |dev| = 2,1,0,1,97 -> MAD 1 -> scale 1.4826; k constant -> scale 1.0
    z = det.robust_z({"x": 6.0, "k": 7.0})
    assert z == pytest.approx([3 / 1.4826, 0.0])
    assert det.score_one({"x": 4.0, "k": 9.0}) == pytest.approx(squash(2.0))  # k dominates: 2 units


def test_squash_is_monotone_and_bounded():
    vals = [squash(r) for r in (0, 0.5, 1, 10, 1e9)]
    assert vals == sorted(vals) and vals[0] == 0 and vals[-1] < 1
    assert squash(-3) == 0


def _rec(i: int, ts: float, **kw) -> PacketRecord:
    base = dict(pkt_index=i, ts=ts, cap_len=60, ip_len=46, src_mac="02:00:00:00:00:01", dst_mac="02:00:00:00:00:fe",
                ip_version=4, src_ip="192.168.1.50", dst_ip="8.8.8.8", ip_proto=6, src_port=40000, dst_port=443,
                direction="out", peer_ip="8.8.8.8")
    base.update(kw)
    return PacketRecord(**base)


def test_kitsune_packet_fields_mirror_its_parser():
    assert kitsune_packet_fields(_rec(0, 1.0))[:7] == (0, "02:00:00:00:00:01", "02:00:00:00:00:fe",
                                                       "192.168.1.50", "40000", "8.8.8.8", "443")
    arp = _rec(1, 2.0, ip_version=0, ip_proto=-1, src_port=-1, dst_port=-1, dst_ip="192.168.1.9", arp_op=ARP_REQUEST)
    assert kitsune_packet_fields(arp)[0] == 0 and kitsune_packet_fields(arp)[4:7] == ("arp", "192.168.1.9", "arp")
    icmp = _rec(2, 3.0, ip_proto=1, src_port=-1, dst_port=-1)
    assert kitsune_packet_fields(icmp)[4] == "icmp"
    v6 = _rec(3, 4.0, ip_version=6, ip_proto=17, src_ip="fe80::1", dst_ip="ff02::fb", src_port=5353, dst_port=5353)
    assert kitsune_packet_fields(v6)[0] == 1 and kitsune_packet_fields(v6)[7:] == (60, 4.0)


def test_kitsune_window_scores_align_to_windows():
    records = [_rec(i, i * 1.0, src_port=40000 + i % 5) for i in range(300)]
    # 10 windows of 30 records each, plus one empty window in the middle.
    spans = [(w * 30, w * 30 + 29) for w in range(5)] + [(-1, -1)] + [(w * 30, w * 30 + 29) for w in range(5, 10)]
    scores = kitsune_window_scores(records, spans, n_bootstrap_windows=4, max_autoencoder_size=5)
    assert len(scores) == 11
    assert (scores[:4] == 0).all() and scores[5] == 0  # bootstrap windows and the empty window
    assert (scores[[4, 6, 7, 8, 9, 10]] > 0).all() and (scores <= 1).all()
