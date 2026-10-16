from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
import yaml

from rad.attacks.boiling_frog import FrogConfig, build_stream
from rad.eval.poison_sweep import fnr_crossings, main
from test_boiling_frog import _benign


def test_start_frac_schedule_is_geometric_and_independent_of_launch_day():
    cfg = FrogConfig(kind="volumetric", final_rate=2.0, alpha=0.5, n_days=3, burst_s=60.0, start_frac=0.25)
    _, sched = build_stream(_benign(), cfg, day_offset_h=10)
    rates = sched.groupby("day").rate.first().to_numpy()
    assert np.allclose(rates, [0.5, 0.75, 1.125, 2.0])  # 0.25 R (1.5)^(k-1) on chaff days, then R
    assert (sched["packets"] == sched["rate"].map(lambda r: max(1, round(r * 60)))).all()
    # A later launch day only appends chaff days: the shared chaff history is identical.
    rec2, sched2 = build_stream(_benign(), FrogConfig(**{**cfg.__dict__, "n_days": 2}), day_offset_h=10)
    rec3, _ = build_stream(_benign(), cfg, day_offset_h=10)
    chaff_end = sched2.loc[sched2.phase == "chaff", "end"].max()
    inj = lambda r: r[(r["src_port"] == 40_000) & (r["ts"] < chaff_end)]["ts"].to_numpy()  # noqa: E731
    assert np.array_equal(inj(rec2), inj(rec3))


def test_launch_day_zero_is_attack_only():
    _, sched = build_stream(_benign(), FrogConfig(n_days=0, burst_s=60.0, start_frac=0.1), day_offset_h=10)
    assert list(sched.phase.unique()) == ["attack"] and np.allclose(sched.rate, 10.0)


def _curve(fnr):
    return pd.DataFrame({"launch_day": [0, 2, 4, 8][:len(fnr)], "chaff_packets": [0, 100, 300, 900][:len(fnr)],
                         "chaff_frac": [0, 0.1, 0.3, 0.9][:len(fnr)], "window_fnr": fnr, "event_fnr": fnr})


def test_fnr_crossings_known_answers():
    c = fnr_crossings(_curve([0.05, 0.2, 0.6, 0.7]), [0.1, 0.5, 0.9], ["window_fnr"]).set_index("level")
    assert c.loc[0.1, "status"] == "reached" and c.loc[0.1, "day"] == 2 and c.loc[0.1, "prev_day"] == 0
    assert c.loc[0.5, "status"] == "reached" and c.loc[0.5, "day"] == 4 and c.loc[0.5, "chaff_frac"] == 0.3
    assert c.loc[0.9, "status"] == "not_reached" and np.isnan(c.loc[0.9, "day"])
    b = fnr_crossings(_curve([0.6, 0.4, 0.9, 1.0]), [0.5], ["window_fnr"])
    assert b["status"].iat[0] == "baseline"  # missed without poisoning: not attributed to the chaff
    with pytest.raises(ValueError):
        fnr_crossings(_curve([0.1, 0.2, 0.3, 0.4]).iloc[1:], [0.5])


def test_sweep_end_to_end(tmp_path):
    """Loud chaff: the naive rule learns it, the gated rule never does; the outputs are complete."""
    dev_dir = tmp_path / "unsw" / "plug"
    dev_dir.mkdir(parents=True)
    benign = _benign()
    day = np.floor((benign["ts"] + 36_000) / 86_400).astype(int)
    names = []
    for i, (_, g) in enumerate(benign.groupby(day)):
        names.append(f"benign/day{i}")
        g.to_parquet(dev_dir / f"day{i}.parquet", index=False)
    data = {"window_s": 300,  # 10x fewer windows than 30 s keeps the test fast
             "tz_offset_h": 10, "guard_after_s": 120, "work_dir": str(tmp_path / "unsw"),
            "devices": {"plug": "aa:aa:aa:aa:aa:01"}}
    cfg = {"experiment": "sweep_t", "seed": 0, "out_dir": str(tmp_path / "res"), "work_dir": str(tmp_path / "work"),
           "data_config": str(tmp_path / "data.yaml"), "devices": ["plug"], "day_offset_h": 10, "benign_days": names,
           "variants": {"loud": {"kind": "volumetric", "final_rate": 1.0, "alpha": 0.0, "start_frac": 1.0,
                                 "burst_s": 60.0, "launch_days": [0, 1]}},
           "update_rules": ["frozen", "naive", "gated"], "features": {"exclude": ["is_weekend"]},
           "detector": {"type": "robust_z"}, "calibration": {"alarms_per_day": 1, "admit_quantile": 0.9},
           "pipeline": {"quarantine": {"t_delay_s": 3600, "purge_k": 10, "taint_on_alert": False}}}
    (tmp_path / "data.yaml").write_text(yaml.safe_dump(data))
    (tmp_path / "cfg.yaml").write_text(yaml.safe_dump(cfg))
    assert main(["--config", str(tmp_path / "cfg.yaml"), "--log-level", "WARNING"]) == 0

    out = tmp_path / "res" / "sweep_t_summary"
    curves = pd.read_csv(out / "curves_all.csv").set_index(["rule", "launch_day"])
    assert len(curves) == 6
    assert (curves.xs(0, level="launch_day")["chaff_packets"] == 0).all()
    assert (curves.xs(1, level="launch_day")["chaff_packets"] == 24 * 60).all()
    assert curves.loc[("naive", 1), "chaff_committed"] > 0
    assert curves.loc[("gated", 1), "chaff_committed"] == 0
    assert curves[["window_fnr", "event_fnr"]].apply(lambda s: s.between(0, 1)).all().all()
    cross = pd.read_csv(out / "crossings_all.csv")
    assert len(cross) == 3 * 2 * 3  # rules x metrics x default levels
    for f in ("summary_all.md", "window_fnr_all.png", "event_fnr_all.png", "meta_all.json", "config_all.yaml"):
        assert (out / f).exists()
    assert not (tmp_path / "res" / "sweep_t_plug_loud_d1_naive" / "windows.jsonl").exists()  # keep_windows: false
