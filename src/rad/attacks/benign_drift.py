"""Benign drift simulator (Phase 3b, CLAUDE.md 3b; D46).

Scripted benign events injected at the packet level into a device's replayed benign days
(same stream layout as rad.attacks.boiling_frog: 2 bootstrap days, 1 validation day, then
`n_days` replayed days). Each event starts on replay day `event_day` at `event_hour` (UTC).

  firmware_update  DNS query for a new update host, a `download_mb` download over 10 minutes
                   from a new server, then - permanently - a heartbeat to a second new server
                   every 60 s (persistent diversity shift + transient volume spike)
  app_reinstall    a 5-minute burst: DNS queries for 8 new domains and short TLS exchanges with
                   8 new servers (transient diversity shift)
  usage_increase   from the event on, every packet of the device's own traffic appears twice
                   (persistent volume shift)

Returns (records, events) where events lists every injected interval with its kind and whether
it is the transient part or the persistent tail (labels for evaluation only).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import pandas as pd

from rad.attacks.boiling_frog import SECONDS_PER_DAY, local_days

TCP_ACK, TCP_SYN, TCP_PSH = 0x10, 0x02, 0x08


@dataclass
class DriftConfig:
    kind: str = "firmware_update"
    n_days: int = 7
    event_day: int = 2          # replay day of the event (1 = first replayed day)
    event_hour: int = 3
    download_mb: float = 20.0


def _pkt(ts, dev, peer, out, proto=6, sport=40_100, dport=443, size=60, flags=TCP_ACK, qname="", dns_resp=-1):
    src, dst = (dev["ip"], peer) if out else (peer, dev["ip"])
    smac, dmac = (dev["mac"], dev["gw_mac"]) if out else (dev["gw_mac"], dev["mac"])
    return {"pkt_index": -1, "ts": float(ts), "cap_len": size + 14, "ip_len": size, "src_mac": smac, "dst_mac": dmac,
            "ip_version": 4, "src_ip": src, "dst_ip": dst, "ip_proto": proto,
            "src_port": sport if out else dport, "dst_port": dport if out else sport,
            "tcp_flags": flags if proto == 6 else -1, "icmp_type": -1, "dns_is_response": dns_resp,
            "dns_qname": qname, "dns_rcode": 0 if dns_resp == 1 else -1, "direction": "out" if out else "in",
            "peer_ip": peer, "peer_is_lan": False, "arp_op": -1}


def _dns(ts, dev, name, resolver):
    return [_pkt(ts, dev, resolver, True, 17, 53_000, 53, 70, qname=name, dns_resp=0),
            _pkt(ts + 0.02, dev, resolver, False, 17, 53_000, 53, 120, qname=name, dns_resp=1)]


def _tls_exchange(t0, dev, server, n_in, n_out, dur, sport):
    rows = [_pkt(t0, dev, server, True, sport=sport, flags=TCP_SYN), _pkt(t0 + 0.05, dev, server, False, sport=sport,
                                                                          flags=TCP_SYN | TCP_ACK)]
    for ts in t0 + 0.1 + np.linspace(0, dur, n_in, endpoint=False):
        rows.append(_pkt(ts, dev, server, False, sport=sport, size=1400, flags=TCP_ACK | TCP_PSH))
    for ts in t0 + 0.1 + np.linspace(0, dur, n_out, endpoint=False):
        rows.append(_pkt(ts, dev, server, True, sport=sport, size=60))
    return rows


def build_drift_stream(benign: pd.DataFrame, cfg: DriftConfig, day_offset_h: float = 0.0
                       ) -> tuple[pd.DataFrame, pd.DataFrame]:
    days = [d for d in local_days(benign, day_offset_h) if len(d)]
    days = [d for d in days if d["ts"].iat[-1] - d["ts"].iat[0] >= 0.9 * SECONDS_PER_DAY]
    if len(days) < 3:
        raise ValueError("need at least 3 complete benign days")
    out_rows = benign[benign["direction"] == "out"]
    dev = {"mac": out_rows["src_mac"].mode().iat[0], "gw_mac": out_rows["dst_mac"].mode().iat[0],
           "ip": out_rows["src_ip"].mode().iat[0]}
    dns_rows = benign[(benign["dns_is_response"] == 0) & (benign["direction"] == "out")]
    resolver = dns_rows["peer_ip"].mode().iat[0] if len(dns_rows) else "192.168.1.1"
    first_day = math.floor((days[0]["ts"].iat[0] + day_offset_h * 3600) / SECONDS_PER_DAY)

    def day_start(k: int) -> float:
        return (first_day + k) * SECONDS_PER_DAY - day_offset_h * 3600

    parts, events = list(days[:3]), []
    ev_t = day_start(2 + cfg.event_day) + cfg.event_hour * 3600
    end_t = day_start(3 + cfg.n_days)
    for k in range(1, cfg.n_days + 1):
        src = days[(k - 1) % len(days)]
        src_start = day_start(int(math.floor((src["ts"].iat[0] + day_offset_h * 3600) / SECONDS_PER_DAY)) - first_day)
        shifted = src.assign(ts=src["ts"] + (day_start(2 + k) - src_start))
        parts.append(shifted)
        if cfg.kind == "usage_increase":
            dup = shifted[shifted["ts"] >= ev_t]
            if len(dup):
                parts.append(dup.assign(ts=dup["ts"] + 0.001))  # every packet appears twice
    rows: list[dict] = []
    if cfg.kind == "firmware_update":
        rows += _dns(ev_t, dev, "fw.update-vendor.example", resolver)
        n_in = int(cfg.download_mb * 1e6 / 1400)
        rows += _tls_exchange(ev_t + 1, dev, "192.0.2.80", n_in, n_in // 2, 600.0, 41_000)
        events.append({"start": ev_t, "end": ev_t + 601, "part": "transient"})
        for i, ts in enumerate(np.arange(ev_t + 660, end_t, 60.0)):  # permanent heartbeat to a new server
            rows += [_pkt(ts, dev, "192.0.2.81", True, sport=42_000 + i % 1000, size=120, flags=TCP_ACK | TCP_PSH),
                     _pkt(ts + 0.08, dev, "192.0.2.81", False, sport=42_000 + i % 1000, size=90,
                          flags=TCP_ACK | TCP_PSH)]
        events.append({"start": ev_t + 660, "end": end_t, "part": "persistent"})
    elif cfg.kind == "app_reinstall":
        for j in range(8):
            t = ev_t + j * 35.0
            rows += _dns(t, dev, f"api{j}.app-cloud.example", resolver)
            rows += _tls_exchange(t + 0.5, dev, f"192.0.2.{100 + j}", 40, 20, 20.0, 43_000 + j)
        events.append({"start": ev_t, "end": ev_t + 300, "part": "transient"})
    elif cfg.kind == "usage_increase":
        events.append({"start": ev_t, "end": end_t, "part": "persistent"})
    else:
        raise ValueError(f"unknown drift kind {cfg.kind!r}")
    if rows:
        parts.append(pd.DataFrame(rows))
    rec = pd.concat(parts, ignore_index=True).sort_values("ts", kind="stable").reset_index(drop=True)
    rec["pkt_index"] = np.arange(len(rec))
    return rec, pd.DataFrame(events).assign(kind=cfg.kind)
