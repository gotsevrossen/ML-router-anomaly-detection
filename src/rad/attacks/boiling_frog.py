"""Boiling-frog injector (Phase 3a, CLAUDE.md 3a; D45).

Builds a long packet stream for one device from its real benign days and injects synthetic
attack packets whose rate grows geometrically, so that each day looks only slightly worse
than the one before. Injection happens at the packet level, so every feature (including the
profile-cache novelty counts that behavioural poisoning targets) is computed by the normal
extractor.

Stream layout (days are capture days: midnight at UTC + `day_offset_h`; UNSW's daily pcaps are UTC days):
  days 1-2       original benign days    (bootstrap)
  day 3          original benign day     (validation)
  days 4..3+N    benign days replayed in a cycle, plus chaff at rate r_k = R * (1 + alpha)^(k - N - 1)
  day 4+N        benign day replayed, plus the real attack at the full rate R
Chaff and attack run in bursts of `burst_s` seconds starting at minute `burst_minute` of every
hour (24 bursts a day).

Variants:
  volumetric   UDP from the device to one external target, `rate` packets/s
  behavioral   TCP SYN to port 23 of a never-used address per packet (scan of new subnets),
               `rate` new destinations/s
The schedule and every injected window are returned for evaluation (labels only).
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass

import numpy as np
import pandas as pd

SECONDS_PER_DAY = 86_400
TCP_SYN = 0x02
log = logging.getLogger(__name__)


@dataclass
class FrogConfig:
    kind: str = "volumetric"        # volumetric | behavioral
    final_rate: float = 10.0        # R: packets/s (volumetric) or new destinations/s (behavioral)
    alpha: float = 0.05             # daily growth of the chaff
    n_days: int = 14                # chaff days before the real attack
    burst_s: float = 300.0          # active seconds per hour
    burst_minute: int = 15
    target_ip: str = "203.0.113.50"  # "known": the device's most used external destination (stealthier)


def local_days(df: pd.DataFrame, day_offset_h: float) -> list[pd.DataFrame]:
    """Split a device's benign records into local calendar days (complete or not), in order."""
    day = np.floor((df["ts"].to_numpy() + day_offset_h * 3600) / SECONDS_PER_DAY).astype(int)
    return [g for _, g in df.groupby(day, sort=True)]


def _new_ip(i: int) -> str:
    """The i-th never-used destination, walking through new /24s of 198.18.0.0/15 (benchmarking range)."""
    net, host = divmod(i, 254)  # hosts .1-.254, then the next /24
    return f"198.{18 + (net >> 8) % 2}.{net & 255}.{host + 1}"


def _burst_packets(day_start: float, rate: float, cfg: FrogConfig, dev: dict, ip_counter: list[int]) -> pd.DataFrame:
    rows = []
    for hour in range(24):
        t0 = day_start + hour * 3600 + cfg.burst_minute * 60
        n = max(1, int(round(rate * cfg.burst_s)))
        for ts in t0 + (np.arange(n) + 0.5) * (cfg.burst_s / n):
            if cfg.kind == "volumetric":
                peer, proto, dport, flags, size = cfg.target_ip, 17, 9999, -1, 512
            else:
                peer, proto, dport, flags, size = _new_ip(ip_counter[0]), 6, 23, TCP_SYN, 60
                ip_counter[0] += 1
            rows.append({"pkt_index": -1, "ts": float(ts), "cap_len": size + 14, "ip_len": size,
                         "src_mac": dev["mac"], "dst_mac": dev["gw_mac"], "ip_version": 4,
                         "src_ip": dev["ip"], "dst_ip": peer, "ip_proto": proto, "src_port": 40_000,
                         "dst_port": dport, "tcp_flags": flags, "direction": "out", "peer_ip": peer,
                         "peer_is_lan": False, "icmp_type": -1, "dns_is_response": -1, "dns_qname": "",
                         "dns_rcode": -1, "arp_op": -1})
    return pd.DataFrame(rows)


def build_stream(benign: pd.DataFrame, cfg: FrogConfig, day_offset_h: float = 0.0) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (records, schedule). `benign` holds only benign days of one device (packet-table columns).

    schedule: one row per injected burst: start, end, day (1 = first chaff day), phase (chaff|attack), rate.
    """
    days = [d for d in local_days(benign, day_offset_h) if len(d)]
    # Replaying a partial capture day (e.g. a pcap that stops after 13 h) would insert hours of silence
    # every cycle, which the detectors rightly flag. Only days whose packets span >= 90% of 24 h are used.
    full = [d for d in days if d["ts"].iat[-1] - d["ts"].iat[0] >= 0.9 * SECONDS_PER_DAY]
    if len(full) < len(days):
        log.warning("dropping %d partial capture day(s) from the stream", len(days) - len(full))
    days = full
    if len(days) < 3:
        raise ValueError("need at least 3 benign days (2 bootstrap + 1 validation)")
    out_rows = benign[benign["direction"] == "out"]
    dev = {"mac": out_rows["src_mac"].mode().iat[0], "gw_mac": out_rows["dst_mac"].mode().iat[0],
           "ip": out_rows["src_ip"].mode().iat[0]}
    if cfg.target_ip == "known":  # hide in traffic to a destination the profile already knows
        ext = out_rows[~out_rows["peer_is_lan"].astype(bool)]
        cfg = FrogConfig(**{**cfg.__dict__, "target_ip": ext["peer_ip"].mode().iat[0]})
    first_day = math.floor((days[0]["ts"].iat[0] + day_offset_h * 3600) / SECONDS_PER_DAY)

    def day_start(k: int) -> float:  # UTC start of local day k (0 = first original day)
        return (first_day + k) * SECONDS_PER_DAY - day_offset_h * 3600

    parts = list(days[:3])
    sched, counter = [], [0]
    for k in range(1, cfg.n_days + 2):  # chaff days 1..N, then the attack day N+1
        src = days[(k - 1) % len(days)]
        src_start = day_start(int(math.floor((src["ts"].iat[0] + day_offset_h * 3600) / SECONDS_PER_DAY) - first_day))
        tgt_start = day_start(2 + k)
        parts.append(src.assign(ts=src["ts"] + (tgt_start - src_start)))
        rate = cfg.final_rate * (1 + cfg.alpha) ** (k - cfg.n_days - 1)
        inj = _burst_packets(tgt_start, rate, cfg, dev, counter)
        parts.append(inj)
        phase = "attack" if k == cfg.n_days + 1 else "chaff"
        for hour in range(24):
            s = tgt_start + hour * 3600 + cfg.burst_minute * 60
            sched.append({"start": s, "end": s + cfg.burst_s, "day": k, "phase": phase, "rate": rate})
    rec = pd.concat(parts, ignore_index=True).sort_values("ts", kind="stable").reset_index(drop=True)
    rec["pkt_index"] = np.arange(len(rec))
    return rec, pd.DataFrame(sched)
