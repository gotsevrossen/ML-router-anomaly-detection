"""Regression suite: one detector set on every dataset, compared with a reference run.

Usage:
  python -m rad.eval.regress --config configs/regress.yaml --tag <name> [--ref <old tag>] [--only mirai nbaiot ...]

Any change to a detector or to the features must not make an older dataset worse
while it improves a new one. This runner re-runs the same detector block on:
  mirai          Kitsune Mirai device, 30 s windows (development set)
  nbaiot         the 9 N-BaIoT devices, per row, seed 0 (Danmini = development)
  kitsune_suite  the 5 usable Kitsune captures, 30 s windows (D29)
  unsw           the 5 UNSW IoT devices, 30 s windows (D30)
  unsw_oct       5 other UNSW devices, October 2018 (D36)
  unsw_late      the June devices' later attack days (D38)
Window features are re-extracted under `windows_tag` when the feature code changes,
so stored windows from older feature versions are never mixed in.

Outputs (results/regress_<tag>/): summary_regress.csv (one row per dataset, unit and
detector), summary_regress.md (means per dataset and detector, and the change
against --ref, with drops flagged).
"""

from __future__ import annotations

import argparse
import copy
import logging
from pathlib import Path
from typing import Any

import pandas as pd

from rad.eval.baseline import _markdown_table, run_baseline
from rad.features.extract import extract_windows
from rad.utils.config import load_config, save_resolved_config
from rad.utils.log import setup_logging

log = logging.getLogger(__name__)
METRICS = ("detection_rate@tau", "event_detection@tau", "test_fpr@tau", "false_alarms_per_day", "tpr@fpr=0.001",
           "pauc@0.01")
# A drop in attacks caught (percentage points) or a rise in false positives that is flagged.
FLAG_CAUGHT_PTS = 2.0
FLAG_FPR_REL = 0.5


def _tagged(cfg: dict[str, Any], tag: str) -> dict[str, Any]:
    c = copy.deepcopy(cfg)
    c["experiment"] = f"regress_{tag}_{c['experiment']}"
    return c


def _exclude(cfg: dict[str, Any], rc: dict[str, Any]) -> None:
    """Add the suite's `exclude_features` (e.g. to reproduce an older feature set) to a window config."""
    extra = list(rc.get("exclude_features") or [])
    if extra:
        feats = cfg.setdefault("features", {})
        feats["exclude"] = list(feats.get("exclude") or []) + extra


def run_mirai(rc: dict[str, Any], dets: dict, tag: str) -> list[pd.DataFrame]:
    fcfg = load_config(rc["features_config"])
    wtag = rc.get("windows_tag", "")
    fcfg["name"] = f"{fcfg['name']}{wtag}"
    win = Path(fcfg["out_dir"]) / f"{fcfg['name']}.parquet"
    if not win.exists():
        extract_windows(fcfg)
    bcfg = _tagged(load_config(rc["baseline_config"]), tag)
    bcfg.update({"windows": str(win), "detectors": dets})
    _exclude(bcfg, rc)
    t = run_baseline(bcfg)["table"]
    t.insert(0, "unit", "kitsune_mirai")
    return [t]


def run_nbaiot_all(rc: dict[str, Any], dets: dict, tag: str) -> list[pd.DataFrame]:
    from rad.eval.nbaiot import run_nbaiot
    base = load_config(rc["config"])
    out = []
    for dev in rc["devices"]:
        c = _tagged(base, tag)
        c["device_dir"] = str(Path(base["device_dir"]).parent / dev)
        c["experiment"] = f"{c['experiment']}_{dev}"
        c["detectors"] = {k: v for k, v in dets.items() if k != "kitsune"}
        t = run_nbaiot(c)["table"]
        t.insert(0, "unit", dev)
        out.append(t)
    return out


def run_kitsune_suite(rc: dict[str, Any], dets: dict, tag: str) -> list[pd.DataFrame]:
    from rad.eval.kitsune_suite import run_capture
    base = _tagged(load_config(rc["config"]), tag)
    base["detectors"] = dets
    base["windows_tag"] = rc.get("windows_tag", "")
    _exclude(base, rc)
    out = []
    for name, cap in base["captures"].items():
        r = run_capture(name, cap, base)
        if "table" in r:
            t = r["table"]
            t.insert(0, "unit", name)
            out.append(t)
    return out


def run_unsw(rc: dict[str, Any], dets: dict, tag: str) -> list[pd.DataFrame]:
    from rad.eval.unsw import run_device
    base = _tagged(load_config(rc["config"]), tag)
    base["detectors"] = dets
    base["windows_tag"] = rc.get("windows_tag", "")
    _exclude(base, rc)
    out = []
    from rad.eval.unsw import capture_gap_starts
    gaps = capture_gap_starts(base) if base.get("drop_capture_gaps", True) else None
    for dev, mac in base["devices"].items():
        t = run_device(dev, mac, base, gaps)["table"]
        t.insert(0, "unit", dev)
        out.append(t)
    return out


RUNNERS = {"mirai": run_mirai, "nbaiot": run_nbaiot_all, "kitsune_suite": run_kitsune_suite, "unsw": run_unsw,
           "unsw_oct": run_unsw, "unsw_late": run_unsw}


def summarize(df: pd.DataFrame, ref: pd.DataFrame | None) -> str:
    cols = [m for m in METRICS if m in df]
    means = df.groupby(["dataset", "detector"])[cols].mean()
    lines = ["## Means per dataset and detector\n", _markdown_table(means.reset_index()), ""]
    if ref is not None:
        rmeans = ref.groupby(["dataset", "detector"])[[c for c in cols if c in ref]].mean()
        both = means.join(rmeans, rsuffix="_ref", how="inner")
        rows = []
        for (ds, det), r in both.iterrows():
            caught = 100 * (r["detection_rate@tau"] - r["detection_rate@tau_ref"])
            fp_col = "test_fpr@tau" if ds == "nbaiot" else "false_alarms_per_day"
            fp, fp_ref = r.get(fp_col), r.get(f"{fp_col}_ref")
            fp_rise = (fp - fp_ref) / fp_ref if fp_ref else (float("inf") if fp else 0.0)
            flag = "DROP" if caught < -FLAG_CAUGHT_PTS else ""
            flag += (" FP-UP" if fp_rise > FLAG_FPR_REL else "")
            rows.append({"dataset": ds, "detector": det, "caught_change_pts": round(caught, 2),
                         f"fp_now": fp, "fp_ref": fp_ref, "flag": flag.strip()})
        lines += ["## Change against the reference\n", _markdown_table(pd.DataFrame(rows)), ""]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m rad.eval.regress", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", required=True)
    ap.add_argument("--tag", required=True, help="name of this run, e.g. the change being tested")
    ap.add_argument("--ref", help="tag of an earlier regress run to compare with")
    ap.add_argument("--only", nargs="*", choices=sorted(RUNNERS))
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args(argv)
    setup_logging(args.log_level)
    cfg = load_config(args.config)
    out = Path(cfg.get("out_dir", "results")) / f"regress_{args.tag}"
    out.mkdir(parents=True, exist_ok=True)
    save_resolved_config(cfg, out / "config.yaml")
    frames = []
    for ds, rc in cfg["datasets"].items():
        rc = {**rc, "exclude_features": cfg.get("exclude_features") or []}
        if args.only and ds not in args.only:
            continue
        log.info("=== %s", ds)
        # Per-dataset overrides (e.g. HST's window_size must fit the bootstrap) merge into the shared block.
        dets = {k: {**v, **(rc.get("detector_overrides", {}).get(k) or {})} for k, v in cfg["detectors"].items()}
        for t in RUNNERS[ds](rc, dets, args.tag):
            t.insert(0, "dataset", ds)
            frames.append(t)
    df = pd.concat(frames, ignore_index=True)
    prev = out / "summary_regress.csv"
    if args.only and prev.exists():  # partial rerun: keep the other datasets' rows
        old = pd.read_csv(prev)
        df = pd.concat([old[~old.dataset.isin(df.dataset.unique())], df], ignore_index=True)
    df.to_csv(prev, index=False)
    ref = None
    if args.ref:
        ref_path = Path(cfg.get("out_dir", "results")) / f"regress_{args.ref}" / "summary_regress.csv"
        ref = pd.read_csv(ref_path) if ref_path.exists() else None
    with open(out / "summary_regress.md", "w", encoding="utf-8") as fh:
        fh.write(f"# regress {args.tag}" + (f" (reference: {args.ref})" if args.ref else "") + "\n\n")
        fh.write(summarize(df, ref))
    log.info("Regression summary -> %s", out / "summary_regress.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
