"""End-to-end streaming run on one device's packets (Phase 2d).

Usage:
  python -m rad.pipeline.run --config configs/pipeline_kitsune_mirai.yaml

Packets stream through the window extractor and the pipeline together, so the
profile cache behind the "new ..." features is committed only by the update
rule (D10, D18), exactly as it would be on the router.

Phases of the stream (time order):
  bootstrap   first `bootstrap_windows`: assumed clean; committed to the profile
              cache, then used to bootstrap the detector(s)
  validation  next `validation_windows`: scored by the bootstrapped detector,
              never learned; they set tau_alert (target alarms/day) and tau_admit
              (a validation-score quantile). Benign data only, no attack labels.
  live        everything after: the configured update rule runs, and one output
              record per window is written

Outputs in results/<experiment>/: windows.jsonl (one record per live window),
summary_pipeline.md / .csv (decision, state and alert counts), config.yaml, meta.json.
"""

from __future__ import annotations

import argparse
import json
import logging
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from rad.eval.baseline import select_features
from rad.features.extract import read_records
from rad.features.profile_cache import ProfileCache
from rad.features.window_features import FEATURE_NAMES, WindowFeatureExtractor
from rad.models import build_detector
from rad.pipeline.alarm import StrictDualAlarm, calibrate_strict_dual
from rad.pipeline.stream import DevicePipeline, PipelineConfig, calibrate_thresholds
from rad.utils.config import load_config, save_resolved_config
from rad.utils.log import setup_logging
from rad.utils.run_meta import run_metadata
from rad.utils.seed import set_seed

log = logging.getLogger(__name__)

DEFAULTS: dict[str, Any] = {
    "out_dir": "results",
    "seed": 0,
    "window_s": 30,
    "features": {"exclude": []},
    "profile_cache": {},
    "calibration": {"alarms_per_day": 1.0, "admit_quantile": 0.9},
    "extractor": {},
}


def resolve_config(cfg: dict[str, Any]) -> dict[str, Any]:
    resolved = {**DEFAULTS, **cfg}
    for key in ("features", "calibration"):
        resolved[key] = {**DEFAULTS[key], **(cfg.get(key) or {})}
    missing = [k for k in ("experiment", "device", "packets", "detector", "split", "pipeline") if not resolved.get(k)]
    if missing:
        raise ValueError(f"Config is missing required keys: {missing}")
    return resolved


def calibrate_budgets(days: dict[int, list[list[float]]], factor: float, measure: str = "sum",
                      cap: float = 3.0) -> tuple[float, float]:
    """Drift budgets from benign data only (D42): `factor` x the largest day-to-day median shift
    (daily) and x the largest shift of any benign day from the first day (total), in the drift
    budget's units (sum over features of |median shift| / bootstrap IQR). Needs >= 2 days."""
    from rad.continual.profile_stats import robust_scale

    keys = sorted(k for k, v in days.items() if len(v) >= 60)  # skip slivers of a day
    if len(keys) < 2:
        raise ValueError("budget calibration needs at least two benign days")
    from rad.continual.sketch import FeatureHistograms

    mats = {k: np.asarray(days[k], dtype=float) for k in keys}
    boot = np.vstack([mats[k] for k in keys[:-1]])
    scale = robust_scale(boot)
    # Daily medians with the same 64-bin histograms the budget uses at run time (edges from the bootstrap),
    # so the calibrated budget includes the binning jumps the run-time measure will see.
    names = [str(j) for j in range(boot.shape[1])]
    med = {}
    for k, m in mats.items():
        h = FeatureHistograms(names, boot.min(axis=0), boot.max(axis=0))
        for v in m:
            h.add_vec(v)
        med[k] = h.median()
    from rad.continual.drift_budget import drift_measure

    shift = lambda a, b: drift_measure(med[a], med[b], scale, measure, cap)  # noqa: E731
    daily = max(shift(a, b) for a, b in zip(keys, keys[1:]))
    total = max(shift(k, keys[0]) for k in keys[1:])
    return factor * daily, factor * max(total, daily)


def run_pipeline(cfg: dict[str, Any]) -> dict[str, Any]:
    cfg = resolve_config(cfg)
    run = run_metadata()
    set_seed(int(cfg["seed"]))
    out = Path(cfg["out_dir"]) / cfg["experiment"]
    out.mkdir(parents=True, exist_ok=True)

    features = select_features(FEATURE_NAMES, cfg["features"].get("include"), cfg["features"].get("exclude") or [])
    det_name, det_params = cfg["detector"]["name"], cfg["detector"].get("params") or {}
    if det_name == "kitsune":
        raise ValueError("Kitsune is packet-level; it is evaluated in rad.eval.baseline, not in the window pipeline")

    def factory():
        return build_detector(det_name, features, det_params)

    n_boot, n_val = int(cfg["split"]["bootstrap_windows"]), int(cfg["split"]["validation_windows"])
    # Multi-day data (rad.eval.adapt): split by time, and skip capture-gap windows (no device had traffic).
    t_boot, t_val = cfg["split"].get("boot_end_ts"), cfg["split"].get("val_end_ts")
    skip = set(float(t) for t in (cfg.get("skip_starts") or []))
    window_s = float(cfg["window_s"])
    profile_cache = ProfileCache(**cfg["profile_cache"])
    extractor = WindowFeatureExtractor(profile_cache, window_s=window_s, **cfg["extractor"])
    pipe_dict = {**cfg["pipeline"], "budget": dict(cfg["pipeline"].get("budget") or {})}
    budget_factor = pipe_dict["budget"].pop("calibrate_factor", None)  # D42: budgets from benign day-to-day drift
    pcfg = PipelineConfig.from_dict(pipe_dict)

    boot_rows: list[dict[str, float]] = []
    val_scores: list[float] = []
    boot_starts: list[float] = []
    val_starts: list[float] = []
    benign_days: dict[int, list[list[float]]] = {}  # day index -> bootstrap/validation rows (D42)
    t_first: float | None = None
    fast = None
    pipe: DevicePipeline | None = None
    n = 0
    thresholds: dict[str, float] = {}
    with open(out / "windows.jsonl", "w", encoding="utf-8") as fh:
        records = read_records(cfg["packets"], 65_536)
        for res in extractor.run(records):
            if res.start in skip:
                continue
            x = {f: res.features[f] for f in features}
            in_boot = res.start < t_boot if t_boot is not None else n < n_boot
            in_val = res.start < t_val if t_val is not None else n < n_boot + n_val
            if in_val:  # bootstrap or validation: benign by assumption
                t_first = res.start if t_first is None else t_first
                benign_days.setdefault(int((res.start - t_first) // 86_400), []).append([x[f] for f in features])
            if in_boot:
                boot_rows.append(x)
                boot_starts.append(res.start)
                profile_cache.commit(res.observation)  # bootstrap is assumed clean (CLAUDE.md §8)
            elif in_val:
                if fast is None:
                    fast = factory()
                    fast.bootstrap(boot_rows)
                val_scores.append(float(fast.score_one(x)))
                val_starts.append(res.start)
            else:
                if pipe is None:
                    tau_admit, tau_alert = calibrate_thresholds(val_scores, window_s,
                                                                float(cfg["calibration"]["alarms_per_day"]),
                                                                float(cfg["calibration"]["admit_quantile"]))
                    if cfg["calibration"].get("above_bootstrap"):
                        # D47: a window as normal as the most extreme bootstrap window never alarms. RobustZ's
                        # in-range scores share a ceiling (z = 3 on the top features), and a threshold sitting
                        # exactly on it made windows that merely touch their training extremes alarm.
                        from rad.models.base import score_many
                        boot_max = float(np.max(score_many(fast, boot_rows)))
                        tau_alert = max(tau_alert, float(np.nextafter(boot_max, np.inf)))
                    if cfg["calibration"].get("strict"):
                        # D48: alert only strictly above the threshold, so a window tying with the most extreme
                        # validation window (e.g. RobustZ's in-range ceiling, z = 3 on the top features) never
                        # alarms; anything beyond the learned range still does.
                        tau_alert = float(np.nextafter(tau_alert, np.inf))
                    thresholds = {"tau_admit": tau_admit, "tau_alert": tau_alert}
                    if budget_factor is not None:
                        b_daily, b_total = calibrate_budgets(benign_days, float(budget_factor),
                                                             pcfg.budget.get("measure", "sum"),
                                                             float(pcfg.budget.get("cap", 3.0)))
                        pcfg.budget = {**pcfg.budget, "b_daily": b_daily, "b_total": b_total}
                        thresholds.update({"b_daily": b_daily, "b_total": b_total})
                    log.info("Calibrated on %d validation windows: tau_admit=%.4f tau_alert=%.4f",
                             len(val_scores), tau_admit, tau_alert)
                    alarm = None
                    if pcfg.alarm.get("mode", "k_of_n") == "strict_dual":  # D53
                        from rad.models.base import score_many
                        k, margin = int(pcfg.alarm.get("k", 8)), float(pcfg.alarm.get("margin", 0.0))
                        t_per, t_raw = calibrate_strict_dual(
                            boot_starts, score_many(fast, boot_rows), val_starts, val_scores, k, window_s,
                            float(cfg["calibration"]["alarms_per_day"]), margin)
                        alarm = StrictDualAlarm(k, t_per, t_raw, window_s)
                        alarm.prime(val_starts, val_scores)  # live windows continue the validation history
                        thresholds.update({"t_per": t_per, "t_raw": t_raw})
                    pipe = DevicePipeline(cfg["device"], features, factory, boot_rows, pcfg, tau_admit, tau_alert,
                                          window_s=window_s, profile_cache=profile_cache, bootstrapped_fast=fast,
                                          alarm=alarm)
                rec = pipe.process(res.start, x, res.observation)
                fh.write(json.dumps(rec) + "\n")
            n += 1
    if pipe is None:
        raise ValueError(f"stream has {n} windows; need more than bootstrap ({n_boot}) + validation ({n_val})")

    recs = pd.read_json(out / "windows.jsonl", lines=True)
    final = Counter(pipe.quarantine.outcome.values()) if pipe.quarantine is not None else \
        Counter(recs["update_decision"])
    summary = {
        "experiment": cfg["experiment"], "update_rule": pcfg.update_rule, "detector": det_name,
        "live_windows": len(recs), **thresholds,
        "alerts": int(recs["alert"].sum()), "raw_alerts": int(recs["raw_alert"].sum()),
        "drift_notices": int(recs["drift_notice"].sum()), "divergence": int(recs["divergence"].sum()),
        **{f"state_{k}": int(v) for k, v in Counter(recs["state"]).items()},
        **{f"final_{k}": int(v) for k, v in final.items()},
    }
    pd.DataFrame([summary]).to_csv(out / "summary_pipeline.csv", index=False)
    with open(out / "summary_pipeline.md", "w", encoding="utf-8") as fh:
        fh.write(f"# {cfg['experiment']}\n\n")
        fh.write("| key | value |\n|---|---|\n")
        for k, v in summary.items():
            fh.write(f"| {k} | {v:.4g} |\n" if isinstance(v, float) else f"| {k} | {v} |\n")
    save_resolved_config(cfg, out / "config.yaml")
    meta = {"run": run, "features": features, "window_s": window_s, "thresholds": thresholds,
            "profile_cache": profile_cache.stats(), "extractor": extractor.stats.as_dict(),
            "quarantine": None if pipe.quarantine is None else pipe.quarantine.stats.__dict__,
            "drift_notices": [] if pipe.budget is None else [n.__dict__ for n in pipe.budget.notices]}
    with open(out / "meta.json", "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2, default=str)
    log.info("Pipeline (%s) -> %s: %s", pcfg.update_rule, out, summary)
    return {"summary": summary, "records": recs, "pipeline": pipe, "out": str(out)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m rad.pipeline.run", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", required=True)
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args(argv)
    setup_logging(args.log_level)
    run_pipeline(load_config(args.config))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
