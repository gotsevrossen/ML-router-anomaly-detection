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


def test_robust_profile_z_and_decay():
    rng = np.random.default_rng(0)
    rows = [{"a": float(v), "k": 0.0} for v in rng.normal(10, 2, 1000)]
    p = RobustProfile(["a", "k"], rows, half_life_days=1.0)
    z = p.robust_z({"a": 10.0 + p.scale[0] * 3, "k": 5.0})
    assert z["a"] == pytest.approx(3.0, abs=0.2)
    assert z["k"] == pytest.approx(5.0, abs=0.1)  # constant feature: unit scale
    p.advance(0.0)
    for _ in range(3000):
        p.add({"a": 20.0, "k": 0.0})
    assert p.median()[0] > 15  # committed data moved the median
    p.advance(86_400.0 * 10)  # ten days of decay without commits leaves quantiles unchanged
    assert p.median()[0] > 15
