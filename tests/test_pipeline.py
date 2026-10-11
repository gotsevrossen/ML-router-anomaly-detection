"""Streaming pipeline (Phase 2d): update rules, output record, end-to-end run on synthetic packets."""

from __future__ import annotations

import gzip
import json

import pyarrow.parquet as pq
import pytest

from rad.continual.disambiguation import ATTACK, NORMAL
from rad.continual.quarantine import COMMITTED, QUARANTINED, REJECTED
from rad.features.packet_schema import records_to_table
from rad.pipeline.run import run_pipeline
from rad.pipeline.stream import DevicePipeline, PipelineConfig, calibrate_thresholds
from test_baseline import ATTACK_FROM, N_WINDOWS, _device_stream

W = 30.0
FEATS = ["bytes_out", "n_new_ext_dst_ips"]
RECORD_KEYS = {"t", "device", "score", "state", "alert", "threat_score", "top_features", "update_decision",
               "drift_notice", "raw_alert", "fast_score", "anchor_score", "divergence", "released"}


class Scripted:
    """score = x[role]; counts what it learned."""

    def __init__(self, role: str) -> None:
        self.role, self.learned = role, []

    def bootstrap(self, xs) -> None:
        pass

    def score_one(self, x) -> float:
        return x[self.role]

    def learn_one(self, x) -> None:
        self.learned.append(x)


def factory():
    roles = iter(["fast", "anchor"])
    made = []

    def make():
        d = Scripted(next(roles))
        made.append(d)
        return d

    return make, made


BOOT = [{"bytes_out": 100.0 + i % 5, "n_new_ext_dst_ips": 0.0, "fast": 0.1, "anchor": 0.1} for i in range(50)]


def make_pipe(rule: str, **cfg):
    make, made = factory()
    pcfg = PipelineConfig(update_rule=rule, quarantine={"t_delay_s": 2 * W, "purge_k": 1},
                          budget={"b_daily": 50.0, "b_total": 100.0}, alert_k=1, alert_n=1, **cfg)
    pipe = DevicePipeline("dev", FEATS + ["fast", "anchor"], make, BOOT, pcfg, tau_admit=0.5, tau_alert=0.9, window_s=W)
    return pipe, made


def window(i: int, fast=0.1, anchor=0.1, bytes_out=101.0, new_ips=0.0):
    return {"bytes_out": bytes_out, "n_new_ext_dst_ips": new_ips, "fast": fast, "anchor": anchor}


def test_record_has_the_specified_fields():
    pipe, _ = make_pipe("full")
    rec = pipe.process(0.0, window(0))
    assert set(rec) == RECORD_KEYS
    assert rec["state"] == NORMAL and rec["update_decision"] == QUARANTINED
    json.dumps(rec)  # serialisable


@pytest.mark.parametrize("rule,learned", [("frozen", 0), ("naive", 10), ("gated", 8), ("full", 8)])
def test_update_rules_learn_as_specified(rule, learned):
    pipe, made = make_pipe(rule)
    for i in range(10):
        pipe.process(i * W, window(i))
    assert len(made[0].learned) == learned  # gated/full: the last two windows are still quarantined


def test_attack_window_is_never_learned_under_any_gated_rule():
    for rule in ("gated", "full"):
        pipe, made = make_pipe(rule)
        recs = [pipe.process(i * W, window(i, fast=0.95 if i == 3 else 0.1)) for i in range(12)]
        assert recs[3]["alert"] and recs[3]["update_decision"] == REJECTED
        assert all(x["fast"] != 0.95 for x in made[0].learned)


def test_full_rule_gates_on_the_anchor_when_the_fast_model_is_fooled():
    pipe, made = make_pipe("full")
    rec = pipe.process(0.0, window(0, fast=0.2, anchor=0.97))
    assert rec["alert"] and rec["divergence"] and rec["score"] == pytest.approx(0.97)
    assert rec["update_decision"] == REJECTED


def test_alert_smoothing_k_of_n_and_threat_score():
    pipe, _ = make_pipe("frozen", )
    pipe.cfg.alert_k, pipe.cfg.alert_n = 2, 3
    pipe.recent = type(pipe.recent)(maxlen=3)
    scores = [0.95, 0.1, 0.95, 0.1, 0.1, 0.1]
    recs = [pipe.process(i * W, window(i, fast=s)) for i, s in enumerate(scores)]
    assert [r["raw_alert"] for r in recs] == [True, False, True, False, False, False]
    assert [r["alert"] for r in recs] == [False, False, True, False, False, False]  # 2 of the last 3
    assert recs[2]["threat_score"] == pytest.approx((2 / 3) * (0.95 - 0.5) / 0.5)
    assert recs[5]["threat_score"] == 0.0


def test_state_uses_diversity_vs_volume():
    pipe, _ = make_pipe("frozen")
    rec = pipe.process(0.0, window(0, fast=0.95, new_ips=40.0))
    assert rec["state"] == ATTACK
    assert rec["top_features"][0][0] == "n_new_ext_dst_ips"


def test_full_rule_raises_drift_notice_and_blocks():
    make, made = factory()
    pcfg = PipelineConfig(update_rule="full", quarantine={"t_delay_s": W, "purge_k": 0},
                          budget={"b_daily": 0.5, "b_total": 100.0}, alert_k=1, alert_n=1)
    pipe = DevicePipeline("dev", FEATS + ["fast", "anchor"], make, BOOT, pcfg, 0.5, 0.9, window_s=W)
    recs = [pipe.process(i * W, window(i, bytes_out=500.0)) for i in range(200)]  # benign-scoring but shifted
    assert any(r["drift_notice"] for r in recs)
    assert sum(r["released"]["blocked"] for r in recs) > 0


def test_calibrate_thresholds_from_validation():
    tau_admit, tau_alert = calibrate_thresholds([0.1, 0.2, 0.3, 0.4], 30, 1, 0.5)
    assert tau_admit == pytest.approx(0.25) and tau_alert > 0.4


def test_config_validation():
    with pytest.raises(ValueError):
        PipelineConfig(update_rule="sometimes")
    with pytest.raises(ValueError):
        PipelineConfig(alert_k=4, alert_n=3)


@pytest.mark.parametrize("rule", ["naive", "gated", "full"])
def test_end_to_end_on_synthetic_device(tmp_path, rule):
    recs, labels = _device_stream()
    packets = tmp_path / "dev.parquet"
    pq.write_table(records_to_table(recs), packets)
    cfg = {
        "experiment": f"toy_pipeline_{rule}", "out_dir": str(tmp_path / "results"), "device": "toy",
        "packets": str(packets),
        "features": {"exclude": ["tod_sin", "tod_cos", "is_weekend"]},
        "detector": {"name": "mad", "params": {}},
        "split": {"bootstrap_windows": 60, "validation_windows": 40},
        "pipeline": {"update_rule": rule, "quarantine": {"t_delay_s": 300, "purge_k": 3},
                     "budget": {"b_daily": 5.0, "b_total": 10.0}, "alert_k": 1, "alert_n": 1},
    }
    res = run_pipeline(cfg)
    out = tmp_path / "results" / cfg["experiment"]
    for name in ("windows.jsonl", "summary_pipeline.csv", "summary_pipeline.md", "config.yaml", "meta.json"):
        assert (out / name).exists(), name
    df = res["records"]
    assert len(df) == N_WINDOWS - 100
    attack = df["t"] >= df["t"].iloc[0] + (ATTACK_FROM - 100) * W
    assert df.loc[attack, "alert"].all()
    assert (df.loc[attack, "state"] == ATTACK).all()  # the ARP sweep is a diversity jump
    if rule != "naive":
        outcome = res["pipeline"].quarantine.outcome
        assert all(outcome[t] != COMMITTED for t in df.loc[attack, "t"])
        cache = res["pipeline"].profile_cache
        assert not cache.has_dst_port(23)  # the telnet scan never reached the profile cache
    else:
        assert res["pipeline"].profile_cache.has_dst_port(23)  # naive updating learns the attack


def test_budget_calibration_from_benign_days():
    """D42: budgets are factor x the observed benign day-to-day (and from-day-0) median shift."""
    import numpy as np

    from rad.pipeline.run import calibrate_budgets
    rng = np.random.default_rng(0)
    days = {d: (rng.normal(size=(200, 2)) + [0.1 * d, 0]).tolist() for d in range(3)}
    b_daily, b_total = calibrate_budgets(days, 2.0)
    assert 0.0 < b_daily <= b_total
    assert b_total < 2.0 * 0.6  # two days of 0.1-sigma drift in one feature stays well under 1 IQR unit
