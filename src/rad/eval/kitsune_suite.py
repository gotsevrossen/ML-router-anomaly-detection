"""Independent test on the Kitsune captures: parse -> windows -> frozen detectors (D29).

Usage:
  python -m rad.eval.kitsune_suite --config configs/kitsune_suite.yaml

Per capture, in order (each step is skipped when its output already exists):
  1. Count, per unicast MAC, the frames it sends or receives and how many of them
     are labelled attack. The monitored device is the MAC involved in the most
     attack frames. Labels choose *which device to evaluate*; they never train,
     tune or threshold anything.
  2. Parse that device's packets (rad.features.parse) and build 30 s windows
     (rad.features.extract), with the same feature code as everywhere else.
  3. Split the device's benign windows before the first attack window: the first
     `bootstrap_frac` bootstrap the detectors, the next `validation_frac` set the
     thresholds, everything later is test.
  4. Run rad.eval.baseline with the frozen detector configs.

Outputs: results/<experiment>_<capture>/ per capture (as rad.eval.baseline), plus
results/<experiment>_summary/summary_suite.csv / .md across captures.
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

from rad.eval.baseline import _markdown_table, run_baseline
from rad.eval.labels import load_frame_labels, window_attack_fraction
from rad.features.extract import extract_windows
from rad.features.parse import parse_capture
from rad.features.pcap_reader import _link_decode, iter_frames
from rad.utils.config import load_config, save_resolved_config
from rad.utils.log import setup_logging

log = logging.getLogger(__name__)


def _is_group(mac: str) -> bool:
    return not mac or int(mac[:2], 16) & 1 == 1


def mac_attack_counts(pcap: str | Path, labels: np.ndarray) -> pd.DataFrame:
    """Frames and attack-labelled frames per unicast MAC (sent or received)."""
    frames: Counter[str] = Counter()
    attack: Counter[str] = Counter()
    for idx, _ts, buf, linktype in iter_frames(pcap):
        try:
            link = _link_decode(buf, linktype)
        except Exception:  # noqa: BLE001 - malformed frames are skipped, as in the parser
            continue
        if link is None:
            continue
        y = int(labels[idx]) if idx < len(labels) else 0
        for mac in {link[0], link[1]}:
            if _is_group(mac):
                continue
            frames[mac] += 1
            attack[mac] += y
    df = pd.DataFrame({"frames": pd.Series(frames), "attack_frames": pd.Series(attack)}).fillna(0).astype(int)
    return df.sort_values(["attack_frames", "frames"], ascending=False)


def run_capture(name: str, cap: dict[str, Any], cfg: dict[str, Any]) -> dict[str, Any]:
    work = Path(cfg["work_dir"])
    work.mkdir(parents=True, exist_ok=True)
    labels = load_frame_labels(cap["labels"])

    choice_path = work / f"{name}.device.json"
    if choice_path.exists():
        choice = json.loads(choice_path.read_text(encoding="utf-8"))
    else:
        log.info("[%s] counting frames per MAC", name)
        counts = mac_attack_counts(cap["pcap"], labels)
        mac = str(counts.index[0])
        choice = {"mac": mac, "frames": int(counts.iloc[0]["frames"]), "attack_frames": int(counts.iloc[0]["attack_frames"]),
                  "top5": counts.head(5).reset_index(names="mac").to_dict("records")}
        choice_path.write_text(json.dumps(choice, indent=2), encoding="utf-8")
    log.info("[%s] monitored device %s (%d frames, %d attack)", name, choice["mac"], choice["frames"], choice["attack_frames"])

    packets = work / f"{name}_device.parquet"
    if not packets.exists():
        parse_capture({"input": cap["pcap"], "device_name": f"{name}_device", "target_mac": choice["mac"],
                       "out_dir": str(work)})
    windows = work / f"{name}_device_w30.parquet"
    if not windows.exists():
        extract_windows({"input": str(packets), "name": f"{name}_device_w30", "out_dir": str(work),
                         "profile": {"update": "never"}})

    w = pd.read_parquet(windows)
    y = window_attack_fraction(w, packets, labels) > 0
    if not y.any():
        log.warning("[%s] no attack windows for the monitored device; skipped", name)
        return {"capture": name, "skipped": "no attack windows"}
    n_benign_pre = int(np.argmax(y))  # windows before the first attack window
    n_boot = int(cfg["split"]["bootstrap_frac"] * n_benign_pre)
    n_val = int(cfg["split"]["validation_frac"] * n_benign_pre)
    if n_boot < cfg["split"]["min_bootstrap"] or n_val < cfg["split"]["min_validation"]:
        log.warning("[%s] only %d benign windows before the attack; skipped", name, n_benign_pre)
        return {"capture": name, "skipped": f"{n_benign_pre} pre-attack windows"}
    # Profile-cache "new" features: the bootstrap windows are the clean profile, as in the pipeline.
    extract_cfg = {"input": str(packets), "name": f"{name}_device_w30_boot{n_boot}", "out_dir": str(work),
                   "profile": {"update": "bootstrap", "bootstrap_windows": n_boot}}
    win_boot = work / f"{extract_cfg['name']}.parquet"
    if not win_boot.exists():
        extract_windows(extract_cfg)
    res = run_baseline({
        "experiment": f"{cfg['experiment']}_{name}", "out_dir": cfg["out_dir"], "seed": cfg.get("seed", 0),
        "windows": str(win_boot), "packets": str(packets), "labels": cap["labels"],
        "features": cfg.get("features", {}), "split": {"bootstrap_windows": n_boot, "validation_windows": n_val},
        "threshold": cfg.get("threshold", {}), "metrics": cfg.get("metrics", {}), "detectors": cfg["detectors"],
    })
    return {"capture": name, "device": choice["mac"], "pre_attack_windows": n_benign_pre, **res["counts"],
            "table": res["table"]}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m rad.eval.kitsune_suite", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", required=True)
    ap.add_argument("--only", nargs="*", help="run only these captures")
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args(argv)
    setup_logging(args.log_level)
    cfg = load_config(args.config)
    cfg.setdefault("work_dir", "data/interim/kitsune_suite")
    out = Path(cfg["out_dir"]) / f"{cfg['experiment']}_summary"
    out.mkdir(parents=True, exist_ok=True)
    save_resolved_config(cfg, out / "config.yaml")
    rows, info = [], []
    for name, cap in cfg["captures"].items():
        if args.only and name not in args.only:
            continue
        r = run_capture(name, cap, cfg)
        if "table" in r:
            t = r.pop("table")
            t.insert(0, "capture", name)
            rows.append(t)
        info.append(r)
    pd.DataFrame(info).to_csv(out / "summary_suite_captures.csv", index=False)
    if rows:
        allrows = pd.concat(rows, ignore_index=True)
        allrows.to_csv(out / "summary_suite.csv", index=False)
        piv = allrows.pivot(index="capture", columns="detector", values="detection_rate@tau")
        fpd = allrows.pivot(index="capture", columns="detector", values="false_alarms_per_day")
        with open(out / "summary_suite.md", "w", encoding="utf-8") as fh:
            fh.write(f"# {cfg['experiment']}\n\n## Attacks caught at the validation threshold\n\n")
            fh.write(_markdown_table(piv.reset_index()) + "\n\n## False alarms per day\n\n")
            fh.write(_markdown_table(fpd.reset_index()) + "\n\n## Captures\n\n")
            fh.write(_markdown_table(pd.DataFrame(info)) + "\n")
    log.info("Suite summary -> %s", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
