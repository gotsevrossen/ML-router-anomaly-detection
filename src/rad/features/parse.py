"""Phase 1a CLI: pcap -> per-device packet table (parquet).

Usage:
  python -m rad.features.parse --list-devices data/raw/capture.pcap
  python -m rad.features.parse --config configs/parse_kitsune_mirai.yaml

Config keys:
  input        path to a .pcap / .pcapng (optionally .gz)
  device_name  output file stem, e.g. "kitsune_mirai_cam"
  target_mac   device MAC (preferred)
  target_ip    optional IP fallback (see device_filter.py)
  out_dir      default "data/interim"
  chunk_size   rows buffered before each parquet write (bounds memory), default 100000
  max_packets  optional: stop after this many capture frames (quick looks / tests)

Outputs (in out_dir):
  <device_name>.parquet     rows in capture order, columns per packet_schema.py
  <device_name>.meta.json   resolved config, run metadata, ParseStats counters
"""

from __future__ import annotations

import argparse
import itertools
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pyarrow.parquet as pq

from rad.features.device_filter import DeviceFilter, list_devices
from rad.features.packet_schema import ARROW_SCHEMA, PacketRecord, records_to_table
from rad.features.pcap_reader import ParseStats, iter_packets
from rad.utils.config import load_config
from rad.utils.log import setup_logging
from rad.utils.run_meta import run_metadata

log = logging.getLogger(__name__)

DEFAULTS: dict[str, Any] = {
    "target_ip": None,
    "out_dir": "data/interim",
    "chunk_size": 100_000,
    "max_packets": None,
}


def resolve_config(cfg: dict[str, Any]) -> dict[str, Any]:
    resolved = {**DEFAULTS, **cfg}
    missing = [k for k in ("input", "device_name") if not resolved.get(k)]
    if missing:
        raise ValueError(f"Config is missing required keys: {missing}")
    if not resolved.get("target_mac") and not resolved.get("target_ip"):
        raise ValueError("Config needs target_mac and/or target_ip")
    return resolved


def parse_capture(cfg: dict[str, Any]) -> dict[str, Any]:
    """Stream one capture through the device filter into parquet. Returns the meta dict."""
    cfg = resolve_config(cfg)
    run = run_metadata()  # at start: the code that produced the output
    out_dir = Path(cfg["out_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{cfg['device_name']}.parquet"
    meta_path = out_dir / f"{cfg['device_name']}.meta.json"

    stats = ParseStats()
    dev_filter = DeviceFilter(cfg.get("target_mac"), cfg.get("target_ip"))
    packets = iter_packets(cfg["input"], stats)
    if cfg["max_packets"] is not None:
        # Bound by capture frame index (not decoded-packet count) so the output is
        # exactly the prefix of a full run. pkt_index is increasing, so stop reading early.
        limit = int(cfg["max_packets"])
        packets = itertools.takewhile(lambda p: p.pkt_index < limit, packets)

    chunk: list[PacketRecord] = []
    rows = 0
    first_ts: float | None = None
    last_ts: float | None = None
    with pq.ParquetWriter(out_path, ARROW_SCHEMA) as writer:
        for rec in dev_filter.filter(packets):
            chunk.append(rec)
            if first_ts is None:
                first_ts = rec.ts
            last_ts = rec.ts
            if len(chunk) >= int(cfg["chunk_size"]):
                writer.write_table(records_to_table(chunk))
                rows += len(chunk)
                log.info("Wrote %d rows (%d frames read)", rows, stats.frames_total)
                chunk.clear()
        if chunk:
            writer.write_table(records_to_table(chunk))
            rows += len(chunk)

    meta = {
        "config": cfg,
        "run": run,
        "output": str(out_path),
        "rows_kept": rows,
        "first_ts": first_ts,
        "last_ts": last_ts,
        "first_ts_utc": _utc(first_ts),
        "last_ts_utc": _utc(last_ts),
        "stats": stats.as_dict(),
    }
    with open(meta_path, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2)
    log.info("Done: %d of %d frames belong to the device -> %s", rows, stats.frames_total, out_path)
    if rows == 0:
        log.warning("No packets matched target_mac=%s target_ip=%s. Use --list-devices to find the MAC.",
                    cfg.get("target_mac"), cfg.get("target_ip"))
    return meta


def _utc(ts: float | None) -> str | None:
    if ts is None:
        return None
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat(timespec="seconds")


def format_device_table(path: str | Path, top: int) -> str:
    stats = ParseStats()
    devices = list_devices(path, top=top, stats=stats)
    lines = [
        f"{stats.frames_total} frames, {stats.decoded_ip} IP + {stats.decoded_arp} ARP packets in {path}",
        f"{'MAC':<19}{'pkts_out':>10}{'pkts_in':>10}{'bytes_out':>13}{'bytes_in':>13}{'hours':>8}  IPs",
    ]
    for d in devices:
        hours = (d.last_ts - d.first_ts) / 3600 if d.packets else 0.0
        ips = ",".join(sorted(d.ips))
        lines.append(
            f"{d.mac:<19}{d.packets_sent:>10}{d.packets_received:>10}"
            f"{d.bytes_sent:>13}{d.bytes_received:>13}{hours:>8.2f}  {ips}"
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m rad.features.parse", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--config", help="YAML config (see module docstring)")
    group.add_argument("--list-devices", metavar="PCAP", help="summarise MACs in a capture and exit")
    ap.add_argument("--top", type=int, default=20, help="rows to show with --list-devices")
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args(argv)
    setup_logging(args.log_level)

    if args.list_devices:
        # The device table is the command's output, so it goes to stdout rather than the log.
        print(format_device_table(args.list_devices, args.top))
        return 0
    parse_capture(load_config(args.config))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
