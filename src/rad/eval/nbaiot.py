"""Secondary benchmark on N-BaIoT's pre-extracted CSV features (Phase 1c).

N-BaIoT ships per-packet snapshots of 115 Kitsune/AfterImage statistics, not
pcaps, so our 30 s window features cannot be computed from it (README deviation
4). This benchmark runs the same detectors on those 115 features to compare
detectors on a second, much larger benign set. Rows carry no timestamps, so the
metrics are per row: no false alarms/day and no time to detect.

Usage:
  python -m rad.eval.nbaiot --config configs/nbaiot_danmini_doorbell.yaml

Protocol: benign rows in file order are split into bootstrap / validation / test
fractions; the threshold is set on validation benign rows for `target_fpr`;
`attack_rows_per_file` rows are sampled (seeded) from every attack CSV for the test set.
Detectors are frozen after bootstrap.

Outputs in results/<experiment>/: summary_nbaiot.csv / .md, summary_nbaiot_per_attack.csv, config.yaml, meta.json.
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from rad.eval import metrics as M
from rad.eval.baseline import _markdown_table, run_window_detector
from rad.utils.config import load_config, save_resolved_config
from rad.utils.log import setup_logging
from rad.utils.run_meta import run_metadata
from rad.utils.seed import set_seed

log = logging.getLogger(__name__)

DEFAULTS: dict[str, Any] = {
    "out_dir": "results",
    "seed": 0,
    "split": {"bootstrap_frac": 0.5, "validation_frac": 0.2},
    "attack_rows_per_file": 2000,
    "threshold": {"target_fpr": 0.001},
    "metrics": {"fpr": [1e-3, 1e-4], "pauc_max_fpr": [0.01, 0.1]},
}


def resolve_config(cfg: dict[str, Any]) -> dict[str, Any]:
    resolved = {**DEFAULTS, **cfg}
    for key in ("split", "threshold", "metrics"):
        resolved[key] = {**DEFAULTS[key], **(cfg.get(key) or {})}
    missing = [k for k in ("experiment", "device_dir", "detectors") if not resolved.get(k)]
    if missing:
        raise ValueError(f"Config is missing required keys: {missing}")
    return resolved


def sample_rows(path: Path, n: int, rng: np.random.Generator) -> pd.DataFrame:
    """Seeded uniform sample of n data rows without loading the whole CSV."""
    with open(path, "rb") as fh:
        total = sum(1 for _ in fh) - 1
    if n >= total:
        return pd.read_csv(path)
    keep = set((rng.choice(total, size=n, replace=False) + 1).tolist())  # +1: line 0 is the header
    return pd.read_csv(path, skiprows=lambda i: i != 0 and i not in keep)


def load_device(device_dir: Path, attack_rows_per_file: int, rng: np.random.Generator
                ) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Benign rows in file order, and sampled attack rows with an `attack` column such as 'mirai/scan'."""
    benign = pd.read_csv(device_dir / "benign_traffic.csv")
    attacks = []
    for csv in sorted(device_dir.glob("*_attacks/*.csv")):
        df = sample_rows(csv, attack_rows_per_file, rng).copy()  # copy consolidates the frame before adding a column
        df["attack"] = f"{csv.parent.name.removesuffix('_attacks')}/{csv.stem}"
        attacks.append(df)
    if not attacks:
        raise FileNotFoundError(f"no extracted attack CSVs under {device_dir} (extract the .rar files first)")
    attack = pd.concat(attacks, ignore_index=True)
    if list(attack.columns[:-1]) != list(benign.columns):
        raise ValueError("attack and benign CSV headers differ")
    return benign, attack


def run_nbaiot(cfg: dict[str, Any]) -> dict[str, Any]:
    cfg = resolve_config(cfg)
    run = run_metadata()  # at start, see baseline.py
    rng = set_seed(int(cfg["seed"]))
    out = Path(cfg["out_dir"]) / cfg["experiment"]
    out.mkdir(parents=True, exist_ok=True)

    benign, attack = load_device(Path(cfg["device_dir"]), int(cfg["attack_rows_per_file"]), rng)
    features = list(benign.columns)
    n = len(benign)
    n_boot = int(cfg["split"]["bootstrap_frac"] * n)
    n_val = int(cfg["split"]["validation_frac"] * n)
    split = np.array(["bootstrap"] * n_boot + ["validation"] * n_val + ["test"] * (n - n_boot - n_val)
                     + ["test"] * len(attack), dtype=object)
    data = pd.concat([benign, attack[features]], ignore_index=True)
    y = np.r_[np.zeros(n, dtype=int), np.ones(len(attack), dtype=int)]
    attack_type = np.r_[np.full(n, "benign", dtype=object), attack["attack"].to_numpy(dtype=object)]
    rows = data.to_dict("records")

    table_rows, per_attack = [], []
    test = split == "test"
    for name, params in cfg["detectors"].items():
        log.info("Running %s", name)
        scores, timing = run_window_detector(name, params or {}, features, rows, split)
        tau = M.threshold_for_fpr(scores[split == "validation"], float(cfg["threshold"]["target_fpr"]))
        y_t, s_t = y[test], scores[test]
        row: dict[str, Any] = {"detector": name}
        for fpr in cfg["metrics"]["fpr"]:
            row[f"tpr@fpr={fpr:g}"] = M.tpr_at_fpr(y_t, s_t, fpr)
        for max_fpr in cfg["metrics"]["pauc_max_fpr"]:
            row[f"pauc@{max_fpr:g}"] = M.partial_auc(y_t, s_t, max_fpr)
        row["tau"] = tau
        row["test_fpr@tau"] = float((s_t[y_t == 0] >= tau).mean())
        row["detection_rate@tau"] = M.detection_rate(s_t[y_t == 1], tau)
        row.update(timing)
        table_rows.append(row)
        for kind in sorted(set(attack["attack"])):
            mask = test & (attack_type == kind)
            per_attack.append({"detector": name, "attack": kind, "detection_rate@tau": M.detection_rate(scores[mask], tau)})

    table = pd.DataFrame(table_rows)
    per_attack_df = pd.DataFrame(per_attack).pivot(index="attack", columns="detector", values="detection_rate@tau")
    per_attack_df = per_attack_df[list(cfg["detectors"])]
    counts = {"benign": n, "bootstrap": n_boot, "validation": n_val, "test_benign": n - n_boot - n_val,
              "test_attack": int(len(attack)), "features": len(features)}

    table.to_csv(out / "summary_nbaiot.csv", index=False)
    per_attack_df.to_csv(out / "summary_nbaiot_per_attack.csv")
    with open(out / "summary_nbaiot.md", "w", encoding="utf-8") as fh:
        fh.write(f"# {cfg['experiment']}\n\nRows: {counts}. Per-row metrics on N-BaIoT's 115 pre-extracted "
                 f"features (secondary benchmark; not our window features).\n\n")
        fh.write(_markdown_table(table) + "\n\n## Detection rate at tau, per attack\n\n")
        fh.write(_markdown_table(per_attack_df.reset_index()) + "\n")
    save_resolved_config(cfg, out / "config.yaml")
    with open(out / "meta.json", "w", encoding="utf-8") as fh:
        json.dump({"run": run, "counts": counts}, fh, indent=2)
    log.info("N-BaIoT table -> %s\n%s\n%s", out / "summary_nbaiot.md", table.to_string(index=False),
             per_attack_df.to_string())
    return {"table": table, "per_attack": per_attack_df, "counts": counts, "out": str(out)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m rad.eval.nbaiot", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", required=True)
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args(argv)
    setup_logging(args.log_level)
    run_nbaiot(load_config(args.config))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
