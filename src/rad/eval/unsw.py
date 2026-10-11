"""UNSW IoT attack dataset (ACM SOSR 2019): multi-day, multi-device benchmark (D30).

Usage:
  python -m rad.eval.unsw --config configs/unsw.yaml [--only <device> ...]

Data (iotanalytics.unsw.edu.au/attack-data.html, MIT-0): one pcap per day of the
whole lab network, plus per-device annotation files listing each attack's start
and end (Unix seconds) and type, e.g. `ArpSpoof100L2D` (ARP spoofing, 100 pkt/s,
LAN to device).

Per device, in order (each step is skipped when its output already exists):
  1. Parse every configured day's pcap for the device's MAC (rad.features.parse),
     days in parallel worker processes, then concatenate the days in time order.
  2. Build 30 s windows (rad.features.extract) with the profile cache bootstrapped on
     the bootstrap period.
  3. Label windows from the annotation intervals (labels are used for evaluation only).
     Benign windows that end within `guard_after_s` after an attack are excluded from
     validation and test, because a device can stay disturbed for a while after an attack.
  4. Split by time: the first `bootstrap_days` days bootstrap the detectors, the next
     `validation_days` set the thresholds, everything later is test.
  5. Run rad.eval.baseline with the frozen detector configs.

Outputs: results/<experiment>_<device>/ (as rad.eval.baseline, plus per-attack
detection) and results/<experiment>_summary/ across devices.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from rad.eval.baseline import _markdown_table, run_baseline
from rad.features.extract import extract_windows
from rad.features.parse import parse_capture
from rad.utils.config import load_config, save_resolved_config
from rad.utils.log import setup_logging

log = logging.getLogger(__name__)
SECONDS_PER_DAY = 86_400


def load_intervals(path: str | Path) -> pd.DataFrame:
    """Annotation file -> DataFrame(start, end, attack) in Unix seconds, sorted by start."""
    df = pd.read_csv(path, header=None, names=["start", "end", "flows", "attack"])
    return df[["start", "end", "attack"]].sort_values("start").reset_index(drop=True)


def attack_family(label: str) -> str:
    """`TcpSynReflection10W2D2W` -> `TcpSynReflection`: the attack without its rate and path."""
    m = re.match(r"([A-Za-z]+?)(\d+)", label)
    return m.group(1) if m else label


def window_interval_labels(starts: np.ndarray, window_s: float, iv: pd.DataFrame,
                           guard_after_s: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Per window: attack fraction (overlap seconds / window_s), attack name, guard flag.

    The guard flag marks windows that overlap (end, end + guard_after_s] of some attack.
    """
    frac = np.zeros(len(starts))
    name = np.full(len(starts), "", dtype=object)
    guard = np.zeros(len(starts), dtype=bool)
    ends = starts + window_s
    for s, e, a in iv[["start", "end", "attack"]].itertuples(index=False):
        ov = np.clip(np.minimum(ends, e) - np.maximum(starts, s), 0, None)
        hit = ov > 0
        frac[hit] += ov[hit] / window_s
        name[hit & (name == "")] = a
        guard |= (ends > e) & (starts < e + guard_after_s)
    return np.minimum(frac, 1.0), name, guard


def _parse_one(job: tuple[str, str, str, str]) -> str:
    pcap, dev_name, mac, out_dir = job
    if not (Path(out_dir) / f"{dev_name}.parquet").exists():
        setup_logging("WARNING")
        parse_capture({"input": pcap, "device_name": dev_name, "target_mac": mac, "out_dir": out_dir})
    return dev_name


def parse_days(cfg: dict[str, Any], devices: dict[str, str]) -> None:
    """Parse each (day, device) pair once, in parallel worker processes."""
    work = Path(cfg["work_dir"])
    jobs = []
    for dev, mac in devices.items():
        (work / dev).mkdir(parents=True, exist_ok=True)
        for day in cfg["days"]:
            pcap = Path(cfg["data_dir"]) / f"{day}.pcap"
            jobs.append((str(pcap), Path(day).name, mac, str(work / dev)))
    todo = [j for j in jobs if not (Path(j[3]) / f"{j[1]}.parquet").exists()]
    log.info("Parsing %d of %d (day, device) pairs with %d workers", len(todo), len(jobs), cfg["workers"])
    with ProcessPoolExecutor(max_workers=int(cfg["workers"])) as ex:
        for name in ex.map(_parse_one, todo):
            log.info("parsed %s", name)


def concat_days(cfg: dict[str, Any], dev: str) -> Path:
    work = Path(cfg["work_dir"]) / dev
    out = work / f"{dev}_all.parquet"
    if out.exists():
        return out
    parts = [work / f"{Path(day).name}.parquet" for day in cfg["days"]]
    with pq.ParquetWriter(out, pq.read_schema(parts[0])) as w:
        for p in parts:
            for batch in pq.ParquetFile(p).iter_batches(batch_size=262_144):
                w.write_batch(batch)
    return out


def run_device(dev: str, mac: str, cfg: dict[str, Any]) -> dict[str, Any]:
    work = Path(cfg["work_dir"]) / dev
    packets = concat_days(cfg, dev)
    first_ts = pq.read_table(packets, columns=["ts"]).column("ts")[0].as_py()
    t0 = np.floor(first_ts / cfg["window_s"]) * cfg["window_s"]
    boot_end = t0 + cfg["split"]["bootstrap_days"] * SECONDS_PER_DAY
    val_end = boot_end + cfg["split"]["validation_days"] * SECONDS_PER_DAY
    n_boot = int(round((boot_end - t0) / cfg["window_s"]))

    name = f"{dev}_w30_boot{n_boot}"
    win_path = work / f"{name}.parquet"
    if not win_path.exists():
        extract_windows({"input": str(packets), "name": name, "out_dir": str(work), "window_s": cfg["window_s"],
                         "tz_offset_h": cfg["tz_offset_h"], **cfg.get("extract", {}),
                         "profile": {"update": "bootstrap", "bootstrap_windows": n_boot}})
    w = pd.read_parquet(win_path, columns=["window_start"])
    starts = w["window_start"].to_numpy()
    iv = load_intervals(Path(cfg["annotations_dir"]) / f"{mac.replace(':', '').lower()}.csv")
    frac, att, guard = window_interval_labels(starts, cfg["window_s"], iv, cfg["guard_after_s"])
    n_boot_w = int((starts < boot_end).sum())
    n_val_w = int(((starts >= boot_end) & (starts < val_end)).sum())
    if (frac[: n_boot_w + n_val_w] > 0).any():
        log.warning("[%s] attack windows inside bootstrap/validation", dev)
    exp = f"{cfg['experiment']}_{dev}"
    res = run_baseline({
        "experiment": exp, "out_dir": cfg["out_dir"], "seed": cfg.get("seed", 0),
        "windows": str(win_path), "packets": str(packets),
        "window_labels": {"attack_frac": frac.tolist(), "exclude": (guard & (frac == 0)).tolist()},
        "features": cfg.get("features", {}), "split": {"bootstrap_windows": n_boot_w, "validation_windows": n_val_w},
        "threshold": cfg.get("threshold", {}), "metrics": cfg.get("metrics", {}), "detectors": cfg["detectors"],
    })
    # Per-attack detection at each detector's validation threshold.
    out = Path(res["out"])
    sc = pd.read_csv(out / "scores.csv")
    taus = res["table"].set_index("detector")["tau"]
    test_att = (sc["split"] == "test").to_numpy() & (frac > 0)
    per = []
    for a in sorted(set(att[test_att])):
        m = test_att & (att == a)
        per.append({"attack": a, "family": attack_family(a), "windows": int(m.sum()),
                    **{d: float((sc.loc[m, d] >= taus[d]).mean()) for d in taus.index}})
    pd.DataFrame(per).to_csv(out / "summary_per_attack.csv", index=False)
    return {"device": dev, "mac": mac, **res["counts"], "table": res["table"], "per_attack": pd.DataFrame(per)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m rad.eval.unsw", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", required=True)
    ap.add_argument("--only", nargs="*", help="run only these devices")
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args(argv)
    setup_logging(args.log_level)
    cfg = load_config(args.config)
    cfg.setdefault("workers", 4)
    cfg.setdefault("window_s", 30.0)
    devices = {d: m for d, m in cfg["devices"].items() if not args.only or d in args.only}
    parse_days(cfg, devices)
    out = Path(cfg["out_dir"]) / f"{cfg['experiment']}_summary"
    out.mkdir(parents=True, exist_ok=True)
    save_resolved_config(cfg, out / "config.yaml")
    rows, per, info = [], [], []
    for dev, mac in devices.items():
        r = run_device(dev, mac, cfg)
        t = r.pop("table"); t.insert(0, "device", dev); rows.append(t)
        p = r.pop("per_attack"); p.insert(0, "device", dev); per.append(p)
        info.append(r)
    allrows = pd.concat(rows, ignore_index=True)
    allrows.to_csv(out / "summary_unsw.csv", index=False)
    allper = pd.concat(per, ignore_index=True)
    allper.to_csv(out / "summary_unsw_per_attack.csv", index=False)
    dets = list(cfg["detectors"])
    fam = allper.groupby("family")[dets].mean()
    with open(out / "summary_unsw.md", "w", encoding="utf-8") as fh:
        fh.write(f"# {cfg['experiment']}\n\n")
        for metric, title in (("detection_rate@tau", "Attack windows caught at the validation threshold"),
                              ("false_alarms_per_day", "False alarms per day (benign test windows)"),
                              ("tpr@fpr=0.001", "TPR at test FPR 1e-3"), ("pauc@0.01", "pAUC@0.01")):
            if metric in allrows:
                piv = allrows.pivot(index="device", columns="detector", values=metric)[dets]
                piv.loc["mean"] = piv.mean()
                fh.write(f"## {title}\n\n{_markdown_table(piv.reset_index())}\n\n")
        fh.write(f"## Caught per attack family (mean over devices and rates)\n\n{_markdown_table(fam.reset_index())}\n\n")
        fh.write(f"## Devices\n\n{_markdown_table(pd.DataFrame(info))}\n")
    log.info("UNSW summary -> %s", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
