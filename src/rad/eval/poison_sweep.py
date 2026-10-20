"""RQ3: how much chaff, and how many days, until boiling-frog poisoning works (Phase 3d; D51).

Usage:
  python -m rad.eval.poison_sweep --config configs/poison_sweep_unsw.yaml [--only <device> ...]
                                  [--variants <name> ...] [--jobs N]

This is ANTIDOTE's metric (Rubinstein et al., IMC 2009) in its boiling-frog form: the false-negative
rate (FNR) on a fixed real attack as a function of how long, and with how much chaff, the model was
poisoned first. For every device x variant x launch day d (`launch_days`) x update rule, the stream is
2 bootstrap days, 1 validation day, d chaff days (the `start_frac` schedule of
rad.attacks.boiling_frog, so the chaff history does not depend on d), then the attack at rate R on
day d + 1. d = 0 is the unpoisoned reference, and it must be in `launch_days`.

Curve (one row per run):
  chaff_packets   injected chaff packets before the attack day
  chaff_frac      chaff packets / benign packets of the same days
  chaff_committed chaff windows the rule learned
  window_fnr      attack windows without an alert (k-of-n smoothed, as the user sees it)
  event_fnr       attack bursts (24 a day) with no alert at all
Crossings (per device x variant x rule x metric x level q in `fnr_levels`):
  status    reached | not_reached (within the sampled launch days) |
            baseline (FNR >= q already at d = 0, with no chaff: the attack is missed anyway, or, under naive,
            teaches itself; with RobustZ's running-extreme scales one learned attack window is enough)
  day       first sampled launch day with FNR >= q; the true crossing lies in (prev_day, day]
  chaff_packets, chaff_frac at that launch day
Outputs in results/<experiment>_summary/: curves_*.csv, crossings_*.csv, summary_*.md, fnr_*.png,
config_*.yaml, meta_*.json. Labels (the schedule) are used for evaluation only.
"""

from __future__ import annotations

import argparse
import json
import logging
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any, Sequence

import numpy as np
import pandas as pd

from rad.attacks.boiling_frog import SECONDS_PER_DAY, FrogConfig, build_stream
from rad.eval.baseline import _markdown_table
from rad.eval.poison import run_rule
from rad.utils.config import load_config, save_resolved_config
from rad.utils.log import setup_logging
from rad.utils.run_meta import run_metadata

log = logging.getLogger(__name__)

FNR_METRICS = ("window_fnr", "event_fnr")
RULE_ORDER = ("frozen", "naive", "gated", "full")


def fnr_crossings(curve: pd.DataFrame, levels: Sequence[float], metrics: Sequence[str] = FNR_METRICS) -> pd.DataFrame:
    """First sampled launch day at which each FNR metric reaches each level, for one run group.

    `curve` has one row per launch day (columns launch_day, chaff_packets, chaff_frac and the metrics)
    and must include launch day 0, the reference without chaff. Levels already reached at day 0 are
    `baseline`: nothing can be attributed to the chaff (the attack is missed anyway, or teaches itself).
    """
    c = curve.sort_values("launch_day").reset_index(drop=True)
    if c["launch_day"].iat[0] != 0:
        raise ValueError("launch day 0 (no chaff) is needed as the reference")
    days = c["launch_day"].to_numpy()
    rows = []
    for m in metrics:
        fnr = c[m].to_numpy(float)
        for q in levels:
            row: dict[str, Any] = {"metric": m, "level": float(q), "fnr_at_0": float(fnr[0]), "day": np.nan,
                                   "prev_day": np.nan, "chaff_packets": np.nan, "chaff_frac": np.nan}
            hit = np.flatnonzero(fnr >= q)
            if fnr[0] >= q:
                row["status"] = "baseline"
            elif len(hit):
                i = hit[0]
                row.update(status="reached", day=int(days[i]), prev_day=int(days[i - 1]),
                           chaff_packets=float(c["chaff_packets"].iat[i]), chaff_frac=float(c["chaff_frac"].iat[i]))
            else:
                row["status"] = "not_reached"
            rows.append(row)
    return pd.DataFrame(rows)


def _stream_for(cfg: dict, data: dict, dev: str, vname: str, d: int) -> tuple[Path, pd.DataFrame, dict[str, float]]:
    """Build (or reuse) the injected stream for launch day d; return it with its chaff totals."""
    work = Path(cfg["work_dir"])
    stream, sched_path = work / f"{dev}_{vname}_d{d}.parquet", work / f"{dev}_{vname}_d{d}_schedule.csv"
    if not stream.exists():
        benign = pd.concat([pd.read_parquet(Path(data["work_dir"]) / dev / f"{Path(p).name}.parquet")
                            for p in cfg["benign_days"]], ignore_index=True)
        v = {k: x for k, x in cfg["variants"][vname].items() if k != "launch_days"}
        rec, sched = build_stream(benign, FrogConfig(**{**v, "n_days": d}), float(cfg.get("day_offset_h", 0.0)))
        rec.to_parquet(stream, index=False)
        sched.to_csv(sched_path, index=False)
    sched = pd.read_csv(sched_path)
    chaff = sched[sched["phase"] == "chaff"]
    chaff_pkts = float(chaff["packets"].sum())
    benign_pkts = 0.0
    if d:
        ts = pd.read_parquet(stream, columns=["ts"])["ts"].to_numpy()
        day_off = float(cfg.get("day_offset_h", 0.0))
        s1 = float(chaff["start"].min())  # first burst of chaff day 1; d1 = that local day's midnight
        d1 = np.floor((s1 + day_off * 3600) / SECONDS_PER_DAY) * SECONDS_PER_DAY - day_off * 3600
        in_chaff_days = (ts >= d1) & (ts < d1 + d * SECONDS_PER_DAY)
        benign_pkts = float(in_chaff_days.sum()) - chaff_pkts
    return stream, sched, {"chaff_packets": chaff_pkts, "benign_packets": benign_pkts,
                           "chaff_frac": chaff_pkts / benign_pkts if benign_pkts else 0.0}


def _run_task(cfg: dict, data: dict, dev: str, vname: str, d: int, log_level: str) -> list[dict]:
    """One device x variant x launch day, all update rules (a worker process).

    Each run's curve row is saved to <summary>/rows/<run>.json as soon as it finishes, and a run whose row
    exists is not repeated, so an interrupted sweep resumes where it stopped.
    """
    setup_logging(log_level)
    rows_dir = Path(cfg["out_dir"]) / f"{cfg['experiment']}_summary" / "rows"
    rows_dir.mkdir(parents=True, exist_ok=True)
    mac = data["devices"][dev]
    rows, stream = [], None
    for rule in cfg["update_rules"]:
        exp = f"{cfg['experiment']}_{dev}_{vname}_d{d}_{rule}"
        done = rows_dir / f"{exp}.json"
        if done.exists():
            rows.append(json.loads(done.read_text(encoding="utf-8")))
            continue
        if stream is None:
            stream, sched, totals = _stream_for(cfg, data, dev, vname, d)
        row, _ = run_rule(cfg, data, mac, stream, sched, rule, exp)
        if not cfg.get("keep_windows", False):  # per-window records are large; the curve keeps what RQ3 needs
            (Path(cfg["out_dir"]) / exp / "windows.jsonl").unlink(missing_ok=True)
        out = {"device": dev, "variant": vname, "rule": rule, "launch_day": d, **totals,
               "chaff_committed": row["chaff_committed"], "window_fnr": 1.0 - row["attack_window_det"],
               "event_fnr": 1.0 - row["attack_event_det"], "false_alarms_per_day": row["false_alarms_per_day"],
               "drift_notices": row["drift_notices"]}
        done.write_text(json.dumps(out), encoding="utf-8")
        rows.append(out)
    return rows


def plot_curves(path: Path, curves: pd.DataFrame, metric: str, level: float) -> None:
    """Small multiples (device x variant): FNR on the final attack against the launch day, one line per rule."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    surface, ink, ink2, band = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e1"
    colors = dict(zip(RULE_ORDER, ("#2a78d6", "#eb6834", "#1baf7a", "#eda100")))  # validated, fixed order
    markers = dict(zip(RULE_ORDER, ("o", "s", "^", "D")))  # second encoding: identity is never colour alone
    # Rules often coincide exactly (frozen = gated = full when nothing is learned): nested sizes, largest
    # underneath, keep every rule visible where the lines overlap.
    sizes = dict(zip(RULE_ORDER, ((11, 4.5), (9, 3.5), (7, 2.5), (4.5, 1.5))))
    devs, vars_ = list(dict.fromkeys(curves["device"])), list(dict.fromkeys(curves["variant"]))
    fig, axes = plt.subplots(len(devs), len(vars_), figsize=(3.2 * len(vars_), 2.4 * len(devs) + 0.8),
                             sharey=True, facecolor=surface, squeeze=False)
    for i, dev in enumerate(devs):
        for j, var in enumerate(vars_):
            ax = axes[i, j]
            ax.set_facecolor(surface)
            ax.axhline(level, color=ink2, lw=1, ls="--", zorder=1)
            sub = curves[(curves["device"] == dev) & (curves["variant"] == var)]
            for z, rule in enumerate([r for r in RULE_ORDER if r in set(sub["rule"])]):
                s = sub[sub["rule"] == rule].sort_values("launch_day")
                ms, lw = sizes[rule]
                ax.plot(s["launch_day"], s[metric], color=colors[rule], lw=lw, marker=markers[rule], ms=ms,
                        mec=surface, mew=1.0, label=rule, zorder=3 + z)
            ax.set_xticks(sorted(sub["launch_day"].unique()))
            ax.set_ylim(-0.04, 1.04)
            ax.set_title(f"{dev} · {var}", loc="left", fontsize=9, color=ink)
            ax.tick_params(colors=ink2, labelsize=8)
            ax.grid(axis="y", color=band, lw=0.6)
            for side in ("top", "right"):
                ax.spines[side].set_visible(False)
            for side in ("left", "bottom"):
                ax.spines[side].set_color(band)
            if i == len(devs) - 1:
                ax.set_xlabel("chaff days before the attack", color=ink2, fontsize=8)
            if j == 0:
                ax.set_ylabel(metric.replace("_", " "), color=ink2, fontsize=8)
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper right", ncol=len(labels), frameon=False, fontsize=8, labelcolor=ink2)
    fig.suptitle(f"FNR on the final attack after boiling-frog poisoning (dashed: {level:.0%})", x=0.01, ha="left",
                 fontsize=10, color=ink)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(path, dpi=130, facecolor=surface)
    plt.close(fig)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m rad.eval.poison_sweep", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", required=True)
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--variants", nargs="*")
    ap.add_argument("--jobs", type=int, default=1)
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args(argv)
    setup_logging(args.log_level)
    cfg = load_config(args.config)
    data = load_config(cfg["data_config"])
    run = run_metadata()  # at start: the commit that produced the results
    Path(cfg["work_dir"]).mkdir(parents=True, exist_ok=True)
    devices = [d for d in cfg["devices"] if not args.only or d in args.only]
    variants = [v for v in cfg["variants"] if not args.variants or v in args.variants]
    tag = "_".join(([*args.only] if args.only else []) + ([*args.variants] if args.variants else [])) or "all"
    out = Path(cfg["out_dir"]) / f"{cfg['experiment']}_summary"
    out.mkdir(parents=True, exist_ok=True)
    save_resolved_config(cfg, out / f"config_{tag}.yaml")

    tasks = []
    for dev in devices:
        for v in variants:
            days = sorted(int(d) for d in cfg["variants"][v]["launch_days"])
            if 0 not in days:
                raise ValueError(f"variant {v}: launch_days must include 0 (the unpoisoned reference)")
            tasks += [(dev, v, d) for d in days]
    log.info("%d runs (%d tasks x %d rules), %d jobs", len(tasks) * len(cfg["update_rules"]), len(tasks),
             len(cfg["update_rules"]), args.jobs)
    rows: list[dict] = []
    if args.jobs > 1:
        with ProcessPoolExecutor(args.jobs) as pool:
            futs = [pool.submit(_run_task, cfg, data, dev, v, d, args.log_level) for dev, v, d in tasks]
            for f in futs:
                rows += f.result()
    else:
        for dev, v, d in tasks:
            rows += _run_task(cfg, data, dev, v, d, args.log_level)

    curves = pd.DataFrame(rows).sort_values(["device", "variant", "rule", "launch_day"]).reset_index(drop=True)
    levels = [float(q) for q in cfg.get("fnr_levels", [0.1, 0.5, 0.9])]
    cross = pd.concat([fnr_crossings(g, levels).assign(device=dev, variant=v, rule=r)
                       for (dev, v, r), g in curves.groupby(["device", "variant", "rule"], sort=False)],
                      ignore_index=True)
    cross = cross[["device", "variant", "rule", "metric", "level", "status", "day", "prev_day", "chaff_packets",
                   "chaff_frac", "fnr_at_0"]]
    curves.to_csv(out / f"curves_{tag}.csv", index=False)
    cross.to_csv(out / f"crossings_{tag}.csv", index=False)
    for m in FNR_METRICS:
        plot_curves(out / f"{m}_{tag}.png", curves, m, 0.5)

    pivot = curves.pivot_table(index=["device", "variant", "rule"], columns="launch_day", values="window_fnr")
    pivot.columns = [f"d{c}" for c in pivot.columns]
    half = cross[(cross["metric"] == "window_fnr") & (cross["level"] == 0.5)]
    with open(out / f"summary_{tag}.md", "w", encoding="utf-8") as fh:
        fh.write(f"# {cfg['experiment']} ({tag})\n\n")
        fh.write("Window FNR on the final attack, by number of chaff days before it (d0 = no chaff):\n\n")
        fh.write(_markdown_table(pivot.reset_index().round(3)) + "\n\n")
        fh.write("Window FNR reaching 50% (day = first sampled launch day; the crossing lies in (prev_day, day]):\n\n")
        fh.write(_markdown_table(half.drop(columns=["metric", "level"]).round(4)) + "\n\n")
        fh.write("All levels and the event-level FNR: `crossings_" + tag + ".csv`; per-run values: `curves_"
                 + tag + ".csv`.\n")
    with open(out / f"meta_{tag}.json", "w", encoding="utf-8") as fh:
        json.dump({"run": run, "tasks": len(tasks), "levels": levels}, fh, indent=2)
    log.info("Poisoning sweep -> %s", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
