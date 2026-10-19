from __future__ import annotations

import numpy as np
import pytest

from rad.continual.disambiguation import (
    ATTACK,
    BENIGN_DRIFT,
    NORMAL,
    DisambiguationConfig,
    classify,
    group_z,
    top_features,
)
from rad.continual.profile_stats import RobustProfile

CFG = DisambiguationConfig(tau_div=3.0)


def z_of(**kw):
    base = {f: 0.0 for f in CFG.vol_features + CFG.div_features}
    base.update(kw)
    return base


def test_no_alert_is_always_normal():
    assert classify(False, 50.0, 50.0, CFG) == NORMAL


def test_firmware_update_like_volume_spike_is_benign_drift():
    zv, zd = group_z(z_of(bytes_in=12.0, pkts_in=8.0, n_new_ext_dst_ips=1.0), CFG)
    assert (zv, zd) == (12.0, 1.0)
    assert classify(True, zv, zd, CFG) == BENIGN_DRIFT


def test_scan_like_diversity_jump_is_attack():
    zv, zd = group_z(z_of(pkts_out=20.0, n_arp_targets=240.0), CFG)
    assert classify(True, zv, zd, CFG) == ATTACK  # diversity above tau_div wins even with high volume


def test_volume_drop_counts_as_volume_but_diversity_drop_does_not():
    zv, zd = group_z(z_of(bytes_out=-6.0, n_failed_tcp=-9.0), CFG)
    assert (zv, zd) == (6.0, 0.0)
    assert classify(True, zv, zd, CFG) == BENIGN_DRIFT


def test_unexplained_alert_fails_safe_to_attack():
    # Diversity below tau_div but larger than volume: not called benign.
    zv, zd = group_z(z_of(bytes_out=1.0, n_new_dst_ports=2.5), CFG)
    assert classify(True, zv, zd, CFG) == ATTACK


def test_missing_features_are_skipped():
    assert group_z({"bytes_out": 4.0}, CFG) == (4.0, 0.0)


def test_top_features_orders_by_magnitude_and_rounds():
    z = {"a": 0.5, "b": -7.25, "c": 3.0, "d": 7.25}
    assert top_features(z, 3) == [["b", -7.25], ["d", 7.25], ["c", 3.0]]  # ties broken by name
    assert top_features(z, 2, exclude=["b"]) == [["d", 7.25], ["c", 3.0]]


def test_from_dict():
    cfg = DisambiguationConfig.from_dict({"tau_div": 5, "div_features": ["n_failed_tcp"]})
    assert cfg.tau_div == 5 and cfg.div_features == ("n_failed_tcp",)


def _sparse_rows(n=2000, seed=0):
    """A busy feature, a sparse count (mostly 0, rarely 1-3, IQR 0) and a constant one."""
    rng = np.random.default_rng(seed)
    return [{"a": float(v), "s": float(rng.choice([0, 0, 0, 0, 0, 0, 0, 0, 1, 3])), "k": 0.0}
            for v in rng.lognormal(8, 1, n)]


def test_explanation_z_keeps_the_bootstrap_range_within_tail_z():
    """D52: no bootstrap window explains itself with |z| > 3, sparse counts included."""
    rows = _sparse_rows()
    p = RobustProfile(["a", "s", "k"], rows)
    zmax = max(abs(v) for r in rows for v in p.robust_z(r).values())
    assert zmax <= 3.0 + 1e-9
    m = np.array([[r["a"], r["s"]] for r in rows])
    edge = p.robust_z({"a": m[:, 0].max(), "s": 3.0, "k": 0.0})
    # The centre is the 64-bin histogram median (a bin centre), not the exact one, so the edge lands near 3.
    assert edge["a"] == pytest.approx(3.0, abs=0.15) and edge["s"] == pytest.approx(3.0, abs=0.15)


def test_explanation_z_still_flags_novelty_on_sparse_and_constant_features():
    p = RobustProfile(["a", "s", "k"], _sparse_rows())
    z = p.robust_z({"a": float(np.exp(8)), "s": 40.0, "k": 140.0})
    assert z["s"] > 3 and z["k"] > 3  # 40 new domains / 140 new IPs are beyond anything in bootstrap
    assert z["s"] < 20  # and on a readable scale (the raw-IQR version gave thousands here)
    assert abs(z["a"]) < 1


def test_drift_budget_scale_is_unchanged_by_explanation_scales():
    from rad.continual.profile_stats import robust_scale
    rows = _sparse_rows()
    p = RobustProfile(["a", "s", "k"], rows)
    m = np.array([[r[f] for f in ("a", "s", "k")] for r in rows])
    assert np.array_equal(p.scale, robust_scale(m))


def test_robust_profile_median_moves_and_decays():
    rng = np.random.default_rng(0)
    rows = [{"a": float(v), "k": 0.0} for v in rng.normal(10, 2, 1000)]
    p = RobustProfile(["a", "k"], rows, half_life_days=1.0)
    p.advance(0.0)
    for _ in range(3000):
        p.add({"a": 20.0, "k": 0.0})
    assert p.median()[0] > 15  # committed data moved the median
    assert abs(p.robust_z({"a": 20.0, "k": 0.0})["a"]) < 0.5  # explanations follow the committed profile
    assert abs(p.robust_z({"a": 10.0, "k": 0.0})["a"]) <= 3.0  # the old normal stays normal (as D49)
    p.advance(86_400.0 * 10)  # ten days of decay without commits leaves quantiles unchanged
    assert p.median()[0] > 15
