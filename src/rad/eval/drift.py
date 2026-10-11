"""RQ2/RQ4: scripted benign drift against each update rule (Phase 3b/3c; D46).

Usage:
  python -m rad.eval.drift --config configs/drift_unsw.yaml [--only <device> ...] [--events <name> ...]

Every window here is benign; the question is how many alarms each rule raises around and after
a benign change, whether alarms fade as the rule adapts, and whether the disambiguation calls
them `suspected_benign_drift`. Measured:
  fa_before          alarms/day on replay days before the event (baseline)
  fa_event_day       alarms on the event day (count)
  fa_after_last3     alarms/day over the last 3 replay days (recovery)
  drift_share        share of alarms from the event on labelled suspected_benign_drift
  committed_after    windows learned after the event (adaptation)
A per-day alarm curve is written for every run.
"""

from __future__ import annotations

import argparse
import copy
import logging
from pathlib import Path

import numpy as np
import pandas as pd

from rad.attacks.benign_drift import DriftConfig, build_drift_stream
from rad.attacks.boiling_frog import SECONDS_PER_DAY
from rad.eval.baseline import _markdown_table
from rad.pipeline.run import run_pipeline
from rad.utils.config import load_config, save_resolved_config
from rad.utils.log import setup_logging

log = logging.getLogger(__name__)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m rad.eval.drift", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", required=True)
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--events", nargs="*")
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args(argv)
    setup_logging(args.log_level)
    cfg = load_config(args.config)
    data = load_config(cfg["data_config"])
    ws, tz = float(data.get("window_s", 30)), float(data["tz_offset_h"])
    day_off = float(cfg.get("day_offset_h", 0.0))
    work = Path(cfg["work_dir"])
    work.mkdir(parents=True, exist_ok=True)
    tag = "_".join(args.events) if args.events else "all"
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
        for ename, e in cfg["events"].items():
            if args.events and ename not in args.events:
                continue
            dc = DriftConfig(**e)
            stream, ev_path = work / f"{dev}_{ename}.parquet", work / f"{dev}_{ename}_events.csv"
            if not stream.exists():
                rec, events = build_drift_stream(benign_days, dc, day_off)
                rec.to_parquet(stream, index=False)
                events.to_csv(ev_path, index=False)
            events = pd.read_csv(ev_path)
            first = pd.read_parquet(stream, columns=["ts"])["ts"].iloc[0]
            d0 = np.floor((first + day_off * 3600) / SECONDS_PER_DAY) * SECONDS_PER_DAY - day_off * 3600
            ev_t = float(events["start"].min())
            for rule in cfg["update_rules"]:
                pcfg = copy.deepcopy(cfg["pipeline"])
                pcfg["update_rule"] = rule
                det = cfg["detector"]
                exp = f"{cfg['experiment']}_{dev}_{ename}_{rule}"
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
                alert = recs["alert"].to_numpy(bool)
                day = ((t - d0) // SECONDS_PER_DAY).astype(int) - 2  # 1 = first replay day
                ev_day = int((ev_t - d0) // SECONDS_PER_DAY) - 2
                n_days = int(day.max())
                per = pd.DataFrame({"day": day, "alert": alert}).query("day >= 1").groupby("day").alert.sum()
                curves.append(per.reset_index().assign(device=dev, event=ename, rule=rule))
                before = (day >= 1) & (day < ev_day)
                last3 = day > n_days - 3
                since = t >= ev_t
                state = recs["state"].to_numpy()
                committed = final.astype(str).eq("committed").to_numpy()
                rows.append({
                    "device": dev, "event": ename, "rule": rule,
                    "fa_before": float(alert[before].sum() / max(1, len(np.unique(day[before])))),
                    "fa_event_day": int(alert[day == ev_day].sum()),
                    "fa_after_last3": float(alert[last3].sum() / 3),
                    "drift_share": float((state[since & alert] == "suspected_benign_drift").mean())
                    if (since & alert).any() else float("nan"),
                    "committed_after": int(committed[since].sum()),
                    "drift_notices": int(recs["drift_notice"].sum()),
                })
                pd.DataFrame(rows).to_csv(out / f"summary_drift_{tag}.csv", index=False)
                pd.concat(curves).to_csv(out / f"curves_drift_{tag}.csv", index=False)
    df = pd.DataFrame(rows)
    with open(out / f"summary_drift_{tag}.md", "w", encoding="utf-8") as fh:
        fh.write(f"# {cfg['experiment']} ({tag})\n\n{_markdown_table(df.round(3))}\n")
    log.info("Drift summary -> %s", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
