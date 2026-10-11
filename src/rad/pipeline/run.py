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

import pandas as pd

from rad.eval.baseline import select_features
from rad.features.extract import read_records
from rad.features.profile_cache import ProfileCache
from rad.features.window_features import FEATURE_NAMES, WindowFeatureExtractor
from rad.models import build_detector
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
    window_s = float(cfg["window_s"])
    profile_cache = ProfileCache(**cfg["profile_cache"])
    extractor = WindowFeatureExtractor(profile_cache, window_s=window_s, **cfg["extractor"])
    pcfg = PipelineConfig.from_dict(cfg["pipeline"])

    boot_rows: list[dict[str, float]] = []
    val_scores: list[float] = []
    fast = None
    pipe: DevicePipeline | None = None
    n = 0
    thresholds: dict[str, float] = {}
    with open(out / "windows.jsonl", "w", encoding="utf-8") as fh:
        records = read_records(cfg["packets"], 65_536)
        for res in extractor.run(records):
            x = {f: res.features[f] for f in features}
            if n < n_boot:
                boot_rows.append(x)
                profile_cache.commit(res.observation)  # bootstrap is assumed clean (CLAUDE.md §8)
            elif n < n_boot + n_val:
                if fast is None:
                    fast = factory()
                    fast.bootstrap(boot_rows)
                val_scores.append(float(fast.score_one(x)))
            else:
                if pipe is None:
                    tau_admit, tau_alert = calibrate_thresholds(val_scores, window_s,
                                                                float(cfg["calibration"]["alarms_per_day"]),
                                                                float(cfg["calibration"]["admit_quantile"]))
                    thresholds = {"tau_admit": tau_admit, "tau_alert": tau_alert}
                    log.info("Calibrated on %d validation windows: tau_admit=%.4f tau_alert=%.4f",
                             len(val_scores), tau_admit, tau_alert)
                    pipe = DevicePipeline(cfg["device"], features, factory, boot_rows, pcfg, tau_admit, tau_alert,
                                          window_s=window_s, profile_cache=profile_cache, bootstrapped_fast=fast)
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
