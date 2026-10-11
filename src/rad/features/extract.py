"""Phase 1b CLI: per-device packet table -> fixed-window feature matrix (parquet).

Usage:
  python -m rad.features.extract --config configs/features_kitsune_mirai.yaml

Config keys:
  input            per-device packet parquet from Phase 1a (rows in capture order)
  name             output file stem
  out_dir          default "data/processed"
  window_s         window length in seconds, default 30
  tz_offset_h      hours added to UTC for the time-of-day features, default 0
  emit_empty       emit windows with no traffic inside the capture span, default true
  window_set_cap   cap on per-window distinct counts, default 4096
  conn_table_size  max TCP connections tracked for conn_dur_mean, default 1024
  conn_timeout_s   forget a tracked connection after this long without FIN/RST, default 300
  batch_size       parquet rows read at a time, default 65536
  profile:
    max_ips, max_ports, max_domains, top_k_ports   profile cache bounds
    update             bootstrap | always | never  (see window_features.CommitPolicy)
    bootstrap_windows  windows committed in "bootstrap" mode, default 120 (1 h)

Outputs (in out_dir):
  <name>.parquet    one row per window: window_start, window_end, n_records,
                    first_pkt_index, last_pkt_index, then FEATURE_NAMES in order
  <name>.meta.json  resolved config, run metadata, feature names, extractor and profile stats
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Any, Iterator

import pyarrow as pa
import pyarrow.parquet as pq

from rad.features.packet_schema import PacketRecord
from rad.features.profile_cache import ProfileCache
from rad.features.window_features import FEATURE_NAMES, CommitPolicy, WindowFeatureExtractor, WindowResult
from rad.utils.config import load_config
from rad.utils.log import setup_logging
from rad.utils.run_meta import run_metadata

log = logging.getLogger(__name__)

DEFAULTS: dict[str, Any] = {
    "out_dir": "data/processed",
    "window_s": 30,
    "tz_offset_h": 0,
    "emit_empty": True,
    "window_set_cap": 4096,
    "conn_table_size": 1024,
    "conn_timeout_s": 300,
    "batch_size": 65_536,
}
PROFILE_DEFAULTS: dict[str, Any] = {
    "max_ips": 4096,
    "max_ports": 1024,
    "max_domains": 2048,
    "top_k_ports": 3,
    "update": "bootstrap",
    "bootstrap_windows": 120,
}

META_COLUMNS: tuple[tuple[str, pa.DataType], ...] = (
    ("window_start", pa.float64()),
    ("window_end", pa.float64()),
    ("n_records", pa.int64()),
    ("first_pkt_index", pa.int64()),
    ("last_pkt_index", pa.int64()),
)
WINDOW_SCHEMA = pa.schema(list(META_COLUMNS) + [(name, pa.float64()) for name in FEATURE_NAMES])
_WRITE_EVERY = 10_000  # windows buffered per parquet write


def resolve_config(cfg: dict[str, Any]) -> dict[str, Any]:
    resolved = {**DEFAULTS, **cfg}
    resolved["profile"] = {**PROFILE_DEFAULTS, **(cfg.get("profile") or {})}
    missing = [k for k in ("input", "name") if not resolved.get(k)]
    if missing:
        raise ValueError(f"Config is missing required keys: {missing}")
    return resolved


def read_records(path: str | Path, batch_size: int) -> Iterator[PacketRecord]:
    """Stream Phase 1a rows back as PacketRecords without loading the whole file."""
    for batch in pq.ParquetFile(path).iter_batches(batch_size=batch_size):
        for row in batch.to_pylist():
            yield PacketRecord(**row)


def _rows_to_table(results: list[WindowResult]) -> pa.Table:
    columns: dict[str, list] = {name: [] for name in WINDOW_SCHEMA.names}
    for res in results:
        columns["window_start"].append(res.start)
        columns["window_end"].append(res.end)
        columns["n_records"].append(res.n_records)
        columns["first_pkt_index"].append(res.first_pkt_index)
        columns["last_pkt_index"].append(res.last_pkt_index)
        for name in FEATURE_NAMES:
            columns[name].append(res.features[name])
    return pa.Table.from_pydict(columns, schema=WINDOW_SCHEMA)


def extract_windows(cfg: dict[str, Any]) -> dict[str, Any]:
    """Stream one device's packet table into window features. Returns the meta dict."""
    cfg = resolve_config(cfg)
    pcfg = cfg["profile"]
    out_dir = Path(cfg["out_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{cfg['name']}.parquet"
    meta_path = out_dir / f"{cfg['name']}.meta.json"

    profile = ProfileCache(max_ips=int(pcfg["max_ips"]), max_ports=int(pcfg["max_ports"]),
                           max_domains=int(pcfg["max_domains"]), top_k_ports=int(pcfg["top_k_ports"]))
    policy = CommitPolicy(pcfg["update"], int(pcfg["bootstrap_windows"]))
    extractor = WindowFeatureExtractor(
        profile,
        window_s=float(cfg["window_s"]),
        tz_offset_h=float(cfg["tz_offset_h"]),
        emit_empty=bool(cfg["emit_empty"]),
        window_set_cap=int(cfg["window_set_cap"]),
        conn_table_size=int(cfg["conn_table_size"]),
        conn_timeout_s=float(cfg["conn_timeout_s"]),
    )

    buffer: list[WindowResult] = []
    n_windows = 0
    first_start: float | None = None
    last_start: float | None = None
    records = read_records(cfg["input"], int(cfg["batch_size"]))
    with pq.ParquetWriter(out_path, WINDOW_SCHEMA) as writer:
        for res in extractor.run(records, commit=policy):
            buffer.append(res)
            n_windows += 1
            first_start = res.start if first_start is None else first_start
            last_start = res.start
            if len(buffer) >= _WRITE_EVERY:
                writer.write_table(_rows_to_table(buffer))
                buffer.clear()
        if buffer:
            writer.write_table(_rows_to_table(buffer))

    meta = {
        "config": cfg,
        "run": run_metadata(),
        "output": str(out_path),
        "n_windows": n_windows,
        "first_window_start": first_start,
        "last_window_start": last_start,
        "feature_names": list(FEATURE_NAMES),
        "extractor_stats": extractor.stats.as_dict(),
        "profile_stats": profile.stats(),
    }
    with open(meta_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2)
    log.info("Done: %d windows (%d empty) -> %s", n_windows, extractor.stats.empty_windows, out_path)
    if extractor.stats.saturated_windows:
        log.warning("%d windows hit window_set_cap=%d; distinct counts there are lower bounds",
                    extractor.stats.saturated_windows, cfg["window_set_cap"])
    return meta


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m rad.features.extract", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", required=True, help="YAML config (see module docstring)")
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args(argv)
    setup_logging(args.log_level)
    extract_windows(load_config(args.config))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
