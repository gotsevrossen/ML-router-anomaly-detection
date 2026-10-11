"""RQ2/RQ3 on real multi-day data: update rules compared on the UNSW devices (D41).

Usage:
  python -m rad.eval.adapt --config configs/adapt_unsw.yaml [--only <device> ...]

For every device x detector x update rule (frozen | naive | gated | full) the streaming
pipeline (rad.pipeline) runs over the device's whole capture: bootstrap and validation
days as in rad.eval.unsw, then every later window is scored, alerted (k-of-n), and -
depending on the rule - learned. Labels (annotation intervals) are joined afterwards for
evaluation only:
  false_alarms_per_day   alerts on benign windows (post-attack guard windows excluded)
  event_detection        attack episodes with at least one alert while they run
  window_detection       attack windows that alert
  attack_committed       attack windows the rule let into the model (poisoning; should be 0)
  benign_committed       benign windows learned (adaptation)
Outputs: results/<experiment>_<device>_<detector>_<rule>/ (pipeline outputs) and
results/<experiment>_summary/summary_adapt.csv / .md.
"""

from __future__ import annotations

import argparse
import copy
import logging
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from rad.eval import metrics as M
from rad.eval.baseline import _markdown_table
from rad.eval.unsw import SECONDS_PER_DAY, capture_gap_starts, concat_days, load_intervals, window_interval_labels
from rad.pipeline.run import run_pipeline
from rad.utils.config import load_config, save_resolved_config
from rad.utils.log import setup_logging

log = logging.getLogger(__name__)


def evaluate_records(recs: pd.DataFrame, final: pd.Series, iv: pd.DataFrame, window_s: float,
                     guard_after_s: float) -> dict[str, float]:
    """`final`: each window's final update decision (after the quarantine delay), aligned with `recs`."""
    starts = recs["t"].to_numpy(dtype=float)
    frac, _, guard = window_interval_labels(starts, window_s, iv, guard_after_s)
    y = (frac > 0).astype(int)
    alert = recs["alert"].to_numpy(dtype=bool)
    benign = (y == 0) & ~guard
    days = benign.sum() * window_s / SECONDS_PER_DAY
    committed = final.astype(str).eq("committed").to_numpy()
    rate, n_ev = M.event_detection_rate(starts, y, alert.astype(float), 0.5, window_s)
    return {
        "false_alarms_per_day": float(alert[benign].sum() / days) if days else float("nan"),
        "event_detection": rate, "n_events": n_ev,
        "window_detection": float(alert[y == 1].mean()) if y.any() else float("nan"),
        "attack_windows": int(y.sum()),
        "attack_committed": int((committed & (y == 1)).sum()),
        "benign_committed": int((committed & (y == 0)).sum()),
        "drift_notices": int(recs["drift_notice"].sum()),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m rad.eval.adapt", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", required=True)
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args(argv)
    setup_logging(args.log_level)
    cfg = load_config(args.config)
    data = load_config(cfg["data_config"])  # the rad.eval.unsw config: days, devices, annotations, tz
    ws = float(data.get("window_s", 30))
    gaps = sorted(capture_gap_starts(data))
    tag = "_" + "_".join(args.only) if args.only else ""  # parallel per-device runs write separate summaries
    out = Path(cfg["out_dir"]) / f"{cfg['experiment']}_summary"
    out.mkdir(parents=True, exist_ok=True)
    save_resolved_config(cfg, out / "config.yaml")
    rows = []
    for dev, mac in data["devices"].items():
        if args.only and dev not in args.only:
            continue
        packets = concat_days(data, dev)
        first_ts = pd.read_parquet(packets, columns=["ts"])["ts"].iloc[0]
        t0 = np.floor(first_ts / ws) * ws
        boot_end = t0 + data["split"]["bootstrap_days"] * SECONDS_PER_DAY
        val_end = boot_end + data["split"]["validation_days"] * SECONDS_PER_DAY
        iv = load_intervals(Path(data["annotations_dir"]) / f"{mac.replace(':', '').lower()}.csv")
        for det_name, det in cfg["detectors"].items():
            for rule in cfg["update_rules"]:
                pcfg = copy.deepcopy(cfg["pipeline"])
                pcfg["update_rule"] = rule
                exp = f"{cfg['experiment']}_{dev}_{det_name}_{rule}"
                log.info("=== %s", exp)
                res = run_pipeline({
                    "experiment": exp, "seed": cfg.get("seed", 0), "out_dir": cfg["out_dir"], "device": mac,
                    "packets": str(packets), "window_s": ws, "features": cfg.get("features", {}),
                    "detector": {"name": det["type"], "params": {k: v for k, v in det.items() if k != "type"}},
                    "split": {"bootstrap_windows": 0, "validation_windows": 0,
                              "boot_end_ts": float(boot_end), "val_end_ts": float(val_end)},
                    "skip_starts": gaps, "calibration": cfg["calibration"], "pipeline": pcfg,
                    "extractor": {"tz_offset_h": data["tz_offset_h"]},
                })
                recs, q = res["records"], res["pipeline"].quarantine
                final = recs["t"].map(q.outcome).fillna(recs["update_decision"]) if q is not None                     else recs["update_decision"]
                ev = evaluate_records(recs, final, iv, ws, float(data["guard_after_s"]))
                s = res["summary"]
                rows.append({"device": dev, "detector": det_name, "rule": rule, **ev,
                             "final_committed": s.get("final_committed", np.nan),
                             "final_purged": s.get("final_purged", 0), "final_blocked": s.get("final_blocked", 0)})
                pd.DataFrame(rows).to_csv(out / f"summary_adapt{tag}.csv", index=False)
    df = pd.DataFrame(rows)
    with open(out / f"summary_adapt{tag}.md", "w", encoding="utf-8") as fh:
        fh.write(f"# {cfg['experiment']}\n\n")
        for metric in ("false_alarms_per_day", "event_detection", "window_detection", "attack_committed",
                       "benign_committed", "drift_notices"):
            piv = df.pivot_table(index=["detector", "rule"], columns="device", values=metric)
            piv["mean"] = piv.mean(axis=1)
            fh.write(f"## {metric}\n\n{_markdown_table(piv.reset_index())}\n\n")
    log.info("Adaptation summary -> %s", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
