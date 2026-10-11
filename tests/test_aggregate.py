from __future__ import annotations

import pandas as pd
import pytest

from rad.eval.aggregate import aggregate, main


def _summary(dir_, values):
    dir_.mkdir(parents=True)
    pd.DataFrame({"detector": ["a", "b"], "detection_rate@tau": values, "test_fpr@tau": [0.001, 0.002]}).to_csv(
        dir_ / "summary_nbaiot.csv", index=False)


def test_aggregate_separates_dev_from_held_out(tmp_path):
    _summary(tmp_path / "exp", [0.9, 0.1])  # development device
    _summary(tmp_path / "exp_DevA", [0.5, 0.2])
    _summary(tmp_path / "exp_DevB", [0.7, 0.4])
    t = aggregate(tmp_path, "exp", ["detection_rate@tau"])["detection_rate@tau"]
    assert t.loc["mean (held-out)", "a"] == pytest.approx(0.6)  # the dev device is excluded from the mean
    assert t.loc["dev(Danmini_Doorbell)", "a"] == 0.9
    assert main(["--prefix", "exp", "--results", str(tmp_path), "--metric", "detection_rate@tau"]) == 0
    assert (tmp_path / "exp_summary" / "summary_aggregate.md").exists()
