"""Phase 1c: one-command baseline table for all detectors on one device's windows.

Usage:
  python -m rad.eval.baseline --config configs/baseline_kitsune_mirai.yaml

Protocol (all detectors frozen after bootstrap; update rules come in Phase 2):
  1. Windows are split in time order: the first `bootstrap_windows` train the
     detector, the next `validation_windows` are benign validation, the rest are test.
  2. The alert threshold is set on validation scores only, for a target number of
     false alarms per day (CLAUDE.md §8: never tune on attack data).
  3. Test metrics: TPR at fixed FPR, partial AUC, false alarms/day and detection
     rate at the validation threshold, time to detect. Never accuracy.

Outputs in results/<experiment>/: summary_baseline.csv / .md (the table),
scores.csv (per-window scores), scores.png, config.yaml (resolved), meta.json.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import time
from pathlib import Path
from typing import Any, Sequence

import numpy as np
import pandas as pd

from rad.eval import metrics as M
from rad.eval.labels import load_frame_labels, window_attack_fraction
from rad.features.extract import read_records
from rad.models import build_detector
from rad.models.base import score_many
from rad.models.kitsune_wrapper import kitsune_window_scores
from rad.utils.config import load_config, save_resolved_config
from rad.utils.log import setup_logging
from rad.utils.run_meta import run_metadata
from rad.utils.seed import set_seed

log = logging.getLogger(__name__)

DEFAULTS: dict[str, Any] = {
    "out_dir": "results",
    "seed": 0,
    "features": {"exclude": []},
    "threshold": {"alarms_per_day": 1.0},
    "metrics": {"fpr": [1e-3, 1e-4], "pauc_max_fpr": [0.01, 0.1]},
}
SPLITS = ("bootstrap", "validation", "test")


def resolve_config(cfg: dict[str, Any]) -> dict[str, Any]:
    resolved = {**DEFAULTS, **cfg}
    for key in ("features", "threshold", "metrics"):
        resolved[key] = {**DEFAULTS[key], **(cfg.get(key) or {})}
    missing = [k for k in ("experiment", "windows", "packets", "labels", "split", "detectors") if not resolved.get(k)]
    if missing:
        raise ValueError(f"Config is missing required keys: {missing}")
    return resolved


def select_features(names: Sequence[str], include: Sequence[str] | None, exclude: Sequence[str]) -> list[str]:
    chosen = list(include) if include else list(names)
    unknown = [f for f in [*chosen, *exclude] if f not in names]
    if unknown:
        raise ValueError(f"unknown features in config: {unknown}")
    return [f for f in chosen if f not in set(exclude)]


def split_labels(n: int, bootstrap: int, validation: int) -> np.ndarray:
    if bootstrap + validation >= n:
        raise ValueError(f"bootstrap ({bootstrap}) + validation ({validation}) leaves no test windows out of {n}")
    split = np.full(n, "test", dtype=object)
    split[:bootstrap] = "bootstrap"
    split[bootstrap:bootstrap + validation] = "validation"
    return split


def run_window_detector(name: str, params: dict, features: list[str], rows: list[dict[str, float]],
                        split: np.ndarray) -> tuple[np.ndarray, dict[str, float]]:
    """Bootstrap on the bootstrap split, then score every window without learning (frozen)."""
    det = build_detector(name, features, params)
    t0 = time.perf_counter()
    det.bootstrap([r for r, s in zip(rows, split) if s == "bootstrap"])
    fit_s = time.perf_counter() - t0
    t0 = time.perf_counter()
    scores = score_many(det, rows)
    score_ms = 1000 * (time.perf_counter() - t0) / len(rows)
    return scores, {"fit_s": fit_s, "score_ms_per_window": score_ms}


def run_kitsune(cfg: dict[str, Any], windows: pd.DataFrame, params: dict, cache_dir: Path
                ) -> tuple[np.ndarray, dict[str, float]]:
    """Per-window Kitsune scores, cached on disk: Kitsune-py is slow (~500 packets/s) and deterministic.

    The cache key covers the packet file (path, size, mtime), the window spans, the
    bootstrap length, the parameters and the vendored code version.
    """
    spans = list(zip(windows["first_pkt_index"].tolist(), windows["last_pkt_index"].tolist()))
    n_boot = int(cfg["split"]["bootstrap_windows"])
    st = Path(cfg["packets"]).stat()
    key_src = json.dumps([str(Path(cfg["packets"]).resolve()), st.st_size, st.st_mtime_ns, spans, n_boot,
                          sorted(params.items()), "kitsune-py@7c8ea51"])
    cache = cache_dir / f"kitsune_{hashlib.sha1(key_src.encode()).hexdigest()[:16]}.npy"
    if cache.exists():
        log.info("Kitsune: using cached scores %s", cache)
        return np.load(cache), {"fit_s": float("nan"), "score_ms_per_window": float("nan")}
    t0 = time.perf_counter()
    scores = kitsune_window_scores(read_records(cfg["packets"], 65_536), spans, n_boot, **params)
    elapsed = time.perf_counter() - t0
    cache_dir.mkdir(parents=True, exist_ok=True)
    np.save(cache, scores)
    # Kitsune trains and scores per packet, so report total time per window (no separate fit time).
    return scores, {"fit_s": float("nan"), "score_ms_per_window": 1000 * elapsed / len(spans)}


def evaluate(scores: np.ndarray, y: np.ndarray, split: np.ndarray, starts: np.ndarray, window_s: float,
             cfg: dict[str, Any]) -> dict[str, float]:
    val = split == "validation"
    test = split == "test"
    tau = M.threshold_for_alarm_rate(scores[val], float(cfg["threshold"]["alarms_per_day"]), window_s)
    y_t, s_t = y[test], scores[test]
    row: dict[str, float] = {}
    for fpr in cfg["metrics"]["fpr"]:
        row[f"tpr@fpr={fpr:g}"] = M.tpr_at_fpr(y_t, s_t, fpr)
    for max_fpr in cfg["metrics"]["pauc_max_fpr"]:
        row[f"pauc@{max_fpr:g}"] = M.partial_auc(y_t, s_t, max_fpr)
    row["tau"] = tau
    row["false_alarms_per_day"] = M.false_alarms_per_day(s_t[y_t == 0], tau, window_s)
    row["detection_rate@tau"] = M.detection_rate(s_t[y_t == 1], tau)
    row["time_to_detect_s"] = M.time_to_detect(starts[test], y_t, s_t, tau)
    return row


def plot_scores(path: Path, minutes: np.ndarray, scores: dict[str, np.ndarray], taus: dict[str, float],
                y: np.ndarray, split: np.ndarray, title: str) -> None:
    """Small multiples, one panel per detector: score line, threshold, attack and split context."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    surface, ink, ink2, line, band = "#fcfcfb", "#0b0b0b", "#52514e", "#2a78d6", "#e6e5e1"
    names = list(scores)
    fig, axes = plt.subplots(len(names), 1, figsize=(10, 1.9 * len(names) + 0.6), sharex=True,
                             facecolor=surface, squeeze=False)
    attack = np.flatnonzero(y == 1)
    boot_end = minutes[np.flatnonzero(split != "bootstrap")[0]]
    test_start = minutes[np.flatnonzero(split == "test")[0]]
    for ax, name in zip(axes[:, 0], names):
        ax.set_facecolor(surface)
        if len(attack):
            ax.axvspan(minutes[attack[0]], minutes[attack[-1]], color=band, lw=0, zorder=0)
        for x in (boot_end, test_start):
            ax.axvline(x, color=ink2, lw=0.8, ls=":", zorder=1)
        ax.plot(minutes, scores[name], color=line, lw=2, zorder=3)
        ax.axhline(taus[name], color=ink2, lw=1, ls="--", zorder=2)
        ax.text(minutes[-1], taus[name], " threshold", color=ink2, fontsize=8, va="center", ha="left")
        ax.set_title(name, loc="left", fontsize=10, color=ink)
        ax.set_ylim(-0.02, 1.02)
        ax.tick_params(colors=ink2, labelsize=8)
        ax.grid(axis="y", color=band, lw=0.6)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color(band)
    top = axes[0, 0]
    top.text(boot_end / 2, 1.08, "bootstrap", transform=top.get_xaxis_transform(), ha="center", fontsize=8, color=ink2)
    top.text((boot_end + test_start) / 2, 1.08, "validation", transform=top.get_xaxis_transform(), ha="center",
             fontsize=8, color=ink2)
    if len(attack):
        top.text((minutes[attack[0]] + minutes[attack[-1]]) / 2, 1.08, "attack (labels; grey band)",
                 transform=top.get_xaxis_transform(), ha="center", fontsize=8, color=ink2)
    axes[-1, 0].set_xlabel("minutes since first window", color=ink2, fontsize=9)
    fig.suptitle(title, x=0.01, ha="left", fontsize=11, color=ink)
    fig.tight_layout()
    fig.savefig(path, dpi=130, facecolor=surface)
    plt.close(fig)


def _markdown_table(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        cells = [f"{v:.4g}" if isinstance(v, float) else str(v) for v in r]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def run_baseline(cfg: dict[str, Any]) -> dict[str, Any]:
    cfg = resolve_config(cfg)
    set_seed(int(cfg["seed"]))
    out = Path(cfg["out_dir"]) / cfg["experiment"]
    out.mkdir(parents=True, exist_ok=True)

    windows = pd.read_parquet(cfg["windows"])
    with open(Path(cfg["windows"]).with_suffix(".meta.json"), encoding="utf-8") as fh:
        feat_meta = json.load(fh)
    window_s = float(feat_meta["config"]["window_s"])
    features = select_features(feat_meta["feature_names"], cfg["features"].get("include"),
                               cfg["features"].get("exclude") or [])
    rows = windows[features].to_dict("records")
    split = split_labels(len(windows), int(cfg["split"]["bootstrap_windows"]), int(cfg["split"]["validation_windows"]))

    attack_frac = window_attack_fraction(windows, cfg["packets"], load_frame_labels(cfg["labels"]))
    y = (attack_frac > 0).astype(int)
    if y[split == "validation"].any() or y[split == "bootstrap"].any():
        log.warning("Labelled attack windows fall inside bootstrap/validation; the split assumes they are benign.")
    starts = windows["window_start"].to_numpy()
    minutes = (starts - starts[0]) / 60

    all_scores: dict[str, np.ndarray] = {}
    timing: dict[str, dict[str, float]] = {}
    for name, params in cfg["detectors"].items():
        log.info("Running %s", name)
        if name == "kitsune":
            all_scores[name], timing[name] = run_kitsune(cfg, windows, params or {}, out / "cache")
        else:
            all_scores[name], timing[name] = run_window_detector(name, params or {}, features, rows, split)

    table_rows = []
    taus: dict[str, float] = {}
    for name, scores in all_scores.items():
        row = {"detector": name, **evaluate(scores, y, split, starts, window_s, cfg), **timing[name]}
        taus[name] = row["tau"]
        table_rows.append(row)
    table = pd.DataFrame(table_rows)

    test = split == "test"
    counts = {
        "windows": int(len(windows)),
        "bootstrap": int((split == "bootstrap").sum()),
        "validation": int((split == "validation").sum()),
        "test_benign": int((test & (y == 0)).sum()),
        "test_attack": int((test & (y == 1)).sum()),
    }
    table.to_csv(out / "summary_baseline.csv", index=False)
    with open(out / "summary_baseline.md", "w", encoding="utf-8") as fh:
        fh.write(f"# {cfg['experiment']}\n\n")
        fh.write(f"Windows: {counts}. Window length {window_s:g} s; features ({len(features)}): {', '.join(features)}.\n\n")
        fh.write(f"FPR resolution on test = 1/{counts['test_benign']} = {1 / max(1, counts['test_benign']):.3g}; "
                 "TPR at smaller FPR targets is TPR at zero false positives.\n\n")
        fh.write(_markdown_table(table) + "\n")
    score_df = pd.DataFrame({"window_start": starts, "minutes": minutes, "split": split,
                             "attack_frac": attack_frac, "label": y, **all_scores})
    score_df.to_csv(out / "scores.csv", index=False)
    plot_scores(out / "scores.png", minutes, all_scores, taus, y, split, cfg["experiment"])
    save_resolved_config(cfg, out / "config.yaml")
    meta = {"run": run_metadata(), "counts": counts, "features": features, "window_s": window_s,
            "features_meta_run": feat_meta.get("run")}
    with open(out / "meta.json", "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2)
    log.info("Baseline table -> %s\n%s", out / "summary_baseline.md", table.to_string(index=False))
    return {"table": table, "counts": counts, "out": str(out)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m rad.eval.baseline", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", required=True)
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args(argv)
    setup_logging(args.log_level)
    run_baseline(load_config(args.config))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
