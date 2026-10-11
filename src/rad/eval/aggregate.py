"""Aggregate per-device N-BaIoT summaries into one cross-device table.

Usage:
  python -m rad.eval.aggregate --prefix nbaiot_fixes --metric detection_rate@tau test_fpr@tau tpr@fpr=0.001

Reads results/<prefix>*/summary_nbaiot.csv and writes results/<prefix>_summary/
summary_<metric>.csv and summary_aggregate.md (devices x detectors, plus the mean
and median over devices).
"""

from __future__ import annotations

import argparse
import logging
import re
from pathlib import Path

import pandas as pd

from rad.eval.baseline import _markdown_table
from rad.utils.log import setup_logging

log = logging.getLogger(__name__)


def aggregate(results_dir: Path, prefix: str, metrics: list[str]) -> dict[str, pd.DataFrame]:
    tables = {}
    rows = []
    for path in sorted(results_dir.glob(f"{prefix}*/summary_nbaiot.csv")):
        exp = path.parent.name
        if exp.endswith("_summary"):
            continue
        device = exp[len(prefix):].lstrip("_") or "dev(Danmini_Doorbell)"
        df = pd.read_csv(path)
        df["device"] = device
        rows.append(df)
    if not rows:
        raise FileNotFoundError(f"no {prefix}*/summary_nbaiot.csv under {results_dir}")
    allrows = pd.concat(rows, ignore_index=True)
    for metric in metrics:
        t = allrows.pivot(index="device", columns="detector", values=metric)
        t = t[list(dict.fromkeys(allrows["detector"]))]
        held_out = t.drop(index=[i for i in t.index if i.startswith("dev(")], errors="ignore")
        t.loc["mean (held-out)"] = held_out.mean()
        t.loc["median (held-out)"] = held_out.median()
        tables[metric] = t
    return tables


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m rad.eval.aggregate", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--prefix", required=True)
    ap.add_argument("--metric", nargs="+", default=["detection_rate@tau", "test_fpr@tau", "tpr@fpr=0.001"])
    ap.add_argument("--results", default="results")
    args = ap.parse_args(argv)
    setup_logging("INFO")
    out = Path(args.results) / f"{args.prefix}_summary"
    out.mkdir(parents=True, exist_ok=True)
    tables = aggregate(Path(args.results), args.prefix, args.metric)
    with open(out / "summary_aggregate.md", "w", encoding="utf-8") as fh:
        for metric, t in tables.items():
            safe = re.sub(r"[^A-Za-z0-9_.=-]", "_", metric)
            t.to_csv(out / f"summary_{safe}.csv")
            fh.write(f"## {metric}\n\n{_markdown_table(t.reset_index())}\n\n")
    log.info("Aggregate -> %s", out / "summary_aggregate.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
