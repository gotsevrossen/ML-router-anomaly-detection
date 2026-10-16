"""RQ3: boiling-frog poisoning against each update rule (Phase 3a/3c; D45).

Usage:
  python -m rad.eval.poison --config configs/poison_unsw.yaml [--only <device> ...] [--variants <name> ...]

Per device x variant (rad.attacks.boiling_frog) x update rule, the streaming pipeline runs
over: 2 bootstrap days, 1 validation day, N chaff days with geometrically growing injected
traffic, then the real attack day. Measured (labels only for evaluation):
  chaff_detected_first / _last   share of chaff windows alerted on the first / last chaff day
  chaff_committed                chaff windows the rule learned (poisoning success)
  attack_window_det              attack-day windows alerted
  attack_event_det               attack-day bursts with at least one alert (24 per day)
  false_alarms_per_day           alerts on benign windows of the replayed days
  drift_notices                  budget notices raised
A per-day curve (chaff detection, chaff commits) is written for every run.
"""

from __future__ import annotations

import argparse
import copy
import logging
from pathlib import Path

import numpy as np
import pandas as pd

from rad.attacks.boiling_frog import SECONDS_PER_DAY, FrogConfig, build_stream
from rad.eval import metrics as M
from rad.eval.baseline import _markdown_table
from rad.pipeline.run import run_pipeline
from rad.utils.config import load_config, save_resolved_config
from rad.utils.log import setup_logging

log = logging.getLogger(__name__)


def label_windows(t: np.ndarray, ws: float, sched: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Per window start: injected day (0 = none) and phase ('' | chaff | attack)."""
    day = np.zeros(len(t), dtype=int)
    phase = np.full(len(t), "", dtype=object)
    for s, e, d, ph in sched[["start", "end", "day", "phase"]].itertuples(index=False):
        hit = (t < e) & (t + ws > s)
        day[hit], phase[hit] = d, ph
    return day, phase


def run_rule(cfg: dict, data: dict, mac: str, stream: Path, sched: pd.DataFrame, rule: str,
             exp: str) -> tuple[dict, pd.DataFrame]:
    """Run the pipeline on one injected stream under one update rule and score it against the schedule.

    Returns the summary row (metrics only) and the per-chaff-day curve (chaff_detected, chaff_committed).
    """
    ws, tz = float(data.get("window_s", 30)), float(data["tz_offset_h"])
    day_off = float(cfg.get("day_offset_h", 0.0))  # capture-day boundaries (UNSW pcaps: UTC days)
    first = pd.read_parquet(stream, columns=["ts"])["ts"].iloc[0]
    d0 = np.floor((first + day_off * 3600) / SECONDS_PER_DAY) * SECONDS_PER_DAY - day_off * 3600
    pcfg = copy.deepcopy(cfg["pipeline"])
    pcfg["update_rule"] = rule
    det = cfg["detector"]
    log.info("=== %s", exp)
    res = run_pipeline({
        "experiment": exp, "seed": cfg.get("seed", 0), "out_dir": cfg["out_dir"], "device": mac,
        "packets": str(stream), "window_s": ws, "features": cfg.get("features", {}),
        "detector": {"name": det["type"], "params": {k: x for k, x in det.items() if k != "type"}},
        "split": {"bootstrap_windows": 0, "validation_windows": 0,
                  "boot_end_ts": float(d0 + 2 * SECONDS_PER_DAY),
                  "val_end_ts": float(d0 + 3 * SECONDS_PER_DAY)},
        "calibration": cfg["calibration"], "pipeline": pcfg, "extractor": {"tz_offset_h": tz},
    })
    recs, q = res["records"], res["pipeline"].quarantine
    final = recs["t"].map(q.outcome).fillna(recs["update_decision"]) if q is not None \
        else recs["update_decision"]
    t = recs["t"].to_numpy(float)
    day, phase = label_windows(t, ws, sched)
    alert = recs["alert"].to_numpy(bool)
    committed = final.astype(str).eq("committed").to_numpy()
    chaff = phase == "chaff"
    per_day = (pd.DataFrame({"day": day[chaff], "alert": alert[chaff], "committed": committed[chaff]})
               .groupby("day").agg(chaff_detected=("alert", "mean"), chaff_committed=("committed", "sum"))
               .reset_index())
    att = phase == "attack"
    keep = att | (phase == "")
    ev, _ = M.event_detection_rate(t[keep], att[keep].astype(int), alert[keep].astype(float), 0.5, ws)
    # Benign = no injection, after validation, and not within guard_after_s of a burst end
    # (k-of-n smoothing keeps an alert for a window or two after the burst stops).
    after = np.zeros(len(t), dtype=bool)
    for e in sched["end"].to_numpy():
        after |= (t + ws > e) & (t < e + float(data["guard_after_s"]))
    benign = (phase == "") & ~after & (t >= d0 + 3 * SECONDS_PER_DAY)
    days_b = benign.sum() * ws / SECONDS_PER_DAY
    nan = float("nan")
    row = {"chaff_detected_first": float(per_day.chaff_detected.iloc[0]) if len(per_day) else nan,
           "chaff_detected_last": float(per_day.chaff_detected.iloc[-1]) if len(per_day) else nan,
           "chaff_committed": int(committed[chaff].sum()),
           "attack_window_det": float(alert[att].mean()), "attack_event_det": ev,
           "false_alarms_per_day": float(alert[benign].sum() / days_b) if days_b else nan,
           "drift_notices": int(recs["drift_notice"].sum())}
    return row, per_day


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m rad.eval.poison", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", required=True)
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--variants", nargs="*")
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args(argv)
    setup_logging(args.log_level)
    cfg = load_config(args.config)
    data = load_config(cfg["data_config"])
    day_off = float(cfg.get("day_offset_h", 0.0))  # capture-day boundaries (UNSW pcaps: UTC days)
    work = Path(cfg["work_dir"])
    work.mkdir(parents=True, exist_ok=True)
    tag = "_".join(args.variants) if args.variants else "all"
    out = Path(cfg["out_dir"]) / f"{cfg['experiment']}_summary"
    out.mkdir(parents=True, exist_ok=True)
    save_resolved_config(cfg, out / f"config_{tag}.yaml")
    rows, curves = [], []
    for dev in cfg["devices"]:
        if args.only and dev not in args.only:
            continue
        mac = data["devices"][dev]
        benign_days = pd.concat([pd.read_parquet(Path(data["work_dir"]) / dev / f"{Path(d).name}.parquet")
                                 for d in cfg["benign_days"]], ignore_index=True)
        for vname, v in cfg["variants"].items():
            if args.variants and vname not in args.variants:
                continue
            stream = work / f"{dev}_{vname}.parquet"
            sched_path = work / f"{dev}_{vname}_schedule.csv"
            if not stream.exists():
                rec, sched = build_stream(benign_days, FrogConfig(**v), day_off)
                rec.to_parquet(stream, index=False)
                sched.to_csv(sched_path, index=False)
            sched = pd.read_csv(sched_path)
            for rule in cfg["update_rules"]:
                exp = f"{cfg['experiment']}_{dev}_{vname}_{rule}"
                row, per_day = run_rule(cfg, data, mac, stream, sched, rule, exp)
                rows.append({"device": dev, "variant": vname, "rule": rule, **row})
                curves.append(per_day.assign(device=dev, variant=vname, rule=rule))
                pd.DataFrame(rows).to_csv(out / f"summary_poison_{tag}.csv", index=False)
                pd.concat(curves).to_csv(out / f"curves_poison_{tag}.csv", index=False)
    df = pd.DataFrame(rows)
    with open(out / f"summary_poison_{tag}.md", "w", encoding="utf-8") as fh:
        fh.write(f"# {cfg['experiment']} ({tag})\n\n{_markdown_table(df.round(3))}\n")
    log.info("Poisoning summary -> %s", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
