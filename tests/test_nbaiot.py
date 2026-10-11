from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from rad.eval.metrics import threshold_for_fpr
from rad.eval.nbaiot import run_nbaiot, sample_rows

COLS = ["MI_dir_L5_weight", "MI_dir_L5_mean", "H_L5_weight", "HH_L5_magnitude"]


@pytest.fixture
def device_dir(tmp_path):
    rng = np.random.default_rng(0)
    d = tmp_path / "Toy_Device"
    (d / "mirai_attacks").mkdir(parents=True)
    (d / "gafgyt_attacks").mkdir()
    pd.DataFrame(rng.normal([10, 60, 5, 1], [1, 3, 0.5, 0.1], size=(1000, 4)), columns=COLS).to_csv(
        d / "benign_traffic.csv", index=False)
    pd.DataFrame(rng.normal([300, 60, 90, 1], [20, 3, 5, 0.1], size=(500, 4)), columns=COLS).to_csv(
        d / "mirai_attacks" / "syn.csv", index=False)
    pd.DataFrame(rng.normal([10, 400, 5, 9], [1, 30, 0.5, 1], size=(300, 4)), columns=COLS).to_csv(
        d / "gafgyt_attacks" / "udp.csv", index=False)
    return d


def test_sample_rows_is_seeded_and_sized(device_dir):
    path = device_dir / "mirai_attacks" / "syn.csv"
    a = sample_rows(path, 50, np.random.default_rng(1))
    b = sample_rows(path, 50, np.random.default_rng(1))
    assert len(a) == 50 and list(a.columns) == COLS
    pd.testing.assert_frame_equal(a, b)
    assert len(sample_rows(path, 10_000, np.random.default_rng(1))) == 500  # asks for more than exist


def test_end_to_end(device_dir, tmp_path):
    cfg = {
        "experiment": "toy_nbaiot",
        "out_dir": str(tmp_path / "results"),
        "device_dir": str(device_dir),
        "attack_rows_per_file": 100,
        "threshold": {"target_fpr": 0.01},
        "detectors": {"hst": {"window_size": 100, "n_trees": 10, "height": 6}, "mad": {"window": 5000},
                      "kitnet": {"max_autoencoder_size": 2}},
    }
    res = run_nbaiot(cfg)
    assert res["counts"] == {"benign": 1000, "bootstrap": 500, "validation": 200, "test_benign": 300,
                             "test_attack": 200, "features": 4}
    table = res["table"].set_index("detector")
    assert (table["pauc@0.1"] > 0.9).all()
    assert list(res["per_attack"].index) == ["gafgyt/udp", "mirai/syn"]
    out = tmp_path / "results" / "toy_nbaiot"
    for name in ("summary_nbaiot.csv", "summary_nbaiot.md", "per_attack.csv", "config.yaml", "meta.json"):
        assert (out / name).exists()


def test_threshold_for_fpr():
    s = np.arange(1000, dtype=float)
    assert threshold_for_fpr(s, 0.01) == 990  # top 10 may alert
    assert threshold_for_fpr(s, 0.0001) > 999
