"""D53 streaming alarm: identical to the batch metric, and usable in the pipeline."""
from __future__ import annotations

import numpy as np
import pyarrow.parquet as pq
import pytest

from rad.eval import metrics as M
from rad.features.packet_schema import records_to_table
from rad.pipeline.alarm import StrictDualAlarm, calibrate_strict_dual
from rad.pipeline.run import run_pipeline
from rad.pipeline.stream import PipelineConfig
from test_baseline import ATTACK_FROM, N_WINDOWS, _device_stream

W = 30.0


def test_streaming_alarm_equals_batch_metric_with_gaps():
    rng = np.random.default_rng(1)
    n = 600
    starts = np.arange(n, dtype=float) * W
    starts[300:] += 10 * W  # a recording gap inside the test period
    starts[150:] += 5 * W  # and one inside validation
    s = rng.normal(0.5, 0.03, n)
    s[400:420] += 0.2  # a sustained attack
    s[500] += 0.3  # one strong window
    known = np.zeros(n, bool); known[:100] = True
    val = np.zeros(n, bool); val[100:200] = True
    batch = M.strict_dual_alarm_score(s, starts, W, 8, known, val, 1.0, 0.02) >= 0
    t_per, t_raw = calibrate_strict_dual(starts[known], s[known], starts[val], s[val], 8, W, 1.0, 0.02)
    alarm = StrictDualAlarm(8, t_per, t_raw, W)
    alarm.prime(starts[:200], s[:200])
    stream = np.array([alarm.update(t, v)[0] for t, v in zip(starts[200:], s[200:])])
    assert np.array_equal(stream, batch[200:])
    assert stream[400 - 200 + 7] and stream[500 - 200]  # both channels fire
    assert not stream[300 - 200: 300 - 200 + 7].any()  # no persistent alarm until 8 windows after the gap


def test_strict_dual_needs_an_alarm_object():
    from rad.pipeline.stream import DevicePipeline
    cfg = PipelineConfig(update_rule="frozen", alarm={"mode": "strict_dual", "k": 8})
    with pytest.raises(ValueError):
        DevicePipeline("d", ["a"], lambda: None, [{"a": 0.0}], cfg, 0.5, 0.6, bootstrapped_fast=object())
    with pytest.raises(ValueError):
        PipelineConfig(alarm={"mode": "bogus"})


@pytest.mark.parametrize("rule", ["frozen", "gated"])
def test_pipeline_end_to_end_with_strict_dual(tmp_path, rule):
    recs, _ = _device_stream()
    packets = tmp_path / "dev.parquet"
    pq.write_table(records_to_table(recs), packets)
    cfg = {"experiment": f"toy_strict_{rule}", "out_dir": str(tmp_path / "results"), "device": "toy",
           "packets": str(packets), "features": {"exclude": ["tod_sin", "tod_cos", "is_weekend"]},
           "detector": {"name": "ecod", "params": {"stats": "sketch", "directional": True}},
           "split": {"bootstrap_windows": 60, "validation_windows": 40},
           "pipeline": {"update_rule": rule, "quarantine": {"t_delay_s": 300, "purge_k": 3},
                        "alarm": {"mode": "strict_dual", "k": 4, "margin": 0.0}}}
    res = run_pipeline(cfg)
    df = res["records"]
    assert len(df) == N_WINDOWS - 100
    attack = df["t"] >= df["t"].iloc[0] + (ATTACK_FROM - 100) * W
    assert df.loc[attack, "alert"].iloc[3:].all()  # alerts from the 4th attack window at the latest
    # 40 toy validation windows put the persistent threshold at the edge of normal: allow one benign alarm.
    assert df.loc[~attack, "alert"].sum() <= 1
    assert {"t_per", "t_raw"} <= set(res["summary"])
