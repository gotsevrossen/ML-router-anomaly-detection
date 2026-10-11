"""Streaming fixed-window features for one device (Phase 1b).

`FEATURE_NAMES` is the contract with the detectors and the Phase 4 C port: the
order is fixed and every definition is below. Only append new features, and
record the change in docs/decisions.md.

A window is [start, start + window_s) with start a multiple of window_s since
the Unix epoch. "Records" are the device's rows from Phase 1a (IP and ARP).

Volume
  bytes_out, bytes_in        sum of ip_len over records sent / received
  pkts_out, pkts_in          number of records sent / received
  out_byte_frac              bytes_out / (bytes_out + bytes_in); 0 for an empty window
Packet shape
  pkt_size_mean, pkt_size_var  mean and population variance of ip_len over all records
  iat_mean, iat_var          gap to the device's previous record, which may lie in an
                             earlier window; out-of-order (negative) gaps count as 0
Destinations
  n_ext_dst_ips              distinct non-LAN peer IPs of sent IP packets
  n_new_ext_dst_ips          of those, how many are not in the committed profile
  n_ext_dst_prefixes         distinct /24 (IPv4) or /48 (IPv6) prefixes of those peers
  lan_byte_frac              bytes exchanged with LAN peers / all bytes (ARP counts as LAN)
Ports / services
  n_dst_ports                distinct destination ports of sent TCP/UDP packets
  n_new_dst_ports            of those, how many are not in the committed profile
  tcp_frac, udp_frac, icmp_frac  share of IP packets (both directions) by protocol;
                             ICMPv6 counts as ICMP
  top3_port_frac             share of TCP/UDP packets whose service port (the lower of
                             src/dst port) is one of the profile's top-3 service ports
DNS (UDP port 53 only, D1)
  dns_queries                queries sent
  n_domains, n_new_domains   distinct names queried; of those, how many are not in the profile
  nxdomain                   NXDOMAIN responses received
Connections (TCP)
  n_new_conns                SYN-without-ACK packets in either direction (connection attempts)
  n_failed_tcp               unanswered SYNs per direction (SYNs minus SYN/ACKs coming back,
                             floored at 0) plus RST packets
  conn_dur_mean              mean SYN-to-first-FIN/RST time of connections closed in the window
ARP (D8)
  arp_req_out                ARP requests sent
  n_arp_targets              distinct IPs asked about in those requests
Context
  tod_sin, tod_cos           time of day of the window start (UTC + tz_offset_h)
  is_weekend                 1.0 on Saturday or Sunday, else 0.0
Inbound (D31, appended after the context features)
  n_in_peers                 distinct sender IPs of received IP packets (LAN or not)
  n_new_in_peers             of those, how many are not in the committed profile; spoofed or
                             randomised sources (floods) make nearly every sender new
  n_in_ports                 distinct local destination ports of received TCP/UDP packets
ARP spoofing (D34, appended)
  arp_rep_in                 ARP replies received
  n_arp_conflicts            sender IPs of received ARP packets claimed by a MAC other than the
                             committed profile's binding for that IP, or by 2+ MACs in the window
                             (the gateway's IP suddenly answered by the attacker's MAC)
Service and LAN-peer novelty (D37, appended; IoT devices serve few local ports and talk to few LAN hosts)
  n_new_in_ports             local TCP/UDP ports that received traffic and never did in the profile
  n_lan_peers                distinct LAN peer IPs of IP packets in either direction
  n_new_lan_peers            of those, how many are not in the committed profile

Distinct counts saturate at `window_set_cap`. Every profile lookup happens when
the window closes, so a window is always compared with the profile as committed
at that moment, and never with its own traffic.
"""

from __future__ import annotations

import ipaddress
import logging
import math
from dataclasses import asdict, dataclass
from typing import Iterable, Iterator

from rad.features.packet_schema import (
    ARP_REPLY,
    ARP_REQUEST,
    DNS_RCODE_NXDOMAIN,
    TCP_ACK,
    TCP_FIN,
    TCP_RST,
    TCP_SYN,
    PacketRecord,
)
from rad.features.profile_cache import CappedSet, ProfileCache, WindowObservation

log = logging.getLogger(__name__)

FEATURE_NAMES: tuple[str, ...] = (
    # volume
    "bytes_out", "bytes_in", "pkts_out", "pkts_in", "out_byte_frac",
    # packet shape
    "pkt_size_mean", "pkt_size_var", "iat_mean", "iat_var",
    # destinations
    "n_ext_dst_ips", "n_new_ext_dst_ips", "n_ext_dst_prefixes", "lan_byte_frac",
    # ports / services
    "n_dst_ports", "n_new_dst_ports", "tcp_frac", "udp_frac", "icmp_frac", "top3_port_frac",
    # DNS
    "dns_queries", "n_domains", "n_new_domains", "nxdomain",
    # connections
    "n_new_conns", "n_failed_tcp", "conn_dur_mean",
    # ARP
    "arp_req_out", "n_arp_targets",
    # context
    "tod_sin", "tod_cos", "is_weekend",
    # inbound (D31; appended so the order above is unchanged)
    "n_in_peers", "n_new_in_peers", "n_in_ports",
    # ARP spoofing (D34)
    "arp_rep_in", "n_arp_conflicts",
    # service and LAN-peer novelty (D37)
    "n_new_in_ports", "n_lan_peers", "n_new_lan_peers",
)

IP_PROTO_TCP, IP_PROTO_UDP, IP_PROTO_ICMP, IP_PROTO_ICMP6 = 6, 17, 1, 58
_SECONDS_PER_DAY = 86_400
_EPOCH_WEEKDAY = 3  # 1970-01-01 was a Thursday (Monday = 0)


class _Welford:
    """Streaming mean / population variance (C port: three scalars)."""

    __slots__ = ("n", "mean", "m2")

    def __init__(self) -> None:
        self.n, self.mean, self.m2 = 0, 0.0, 0.0

    def add(self, x: float) -> None:
        self.n += 1
        delta = x - self.mean
        self.mean += delta / self.n
        self.m2 += delta * (x - self.mean)

    @property
    def var(self) -> float:
        return self.m2 / self.n if self.n else 0.0


def ip_prefix(ip: str) -> str:
    """/24 for IPv4, /48 for IPv6, as a string key."""
    if ":" in ip:
        return ipaddress.IPv6Address(ip).exploded[:14] + "::/48"
    return ip.rsplit(".", 1)[0] + ".0/24"


class _Window:
    """Accumulators for one open window."""

    def __init__(self, k: int, window_s: float, cap: int) -> None:
        self.k = k
        self.start = k * window_s
        self.end = (k + 1) * window_s
        self.cap = cap
        self.n_records = 0
        self.first_pkt_index = -1
        self.last_pkt_index = -1
        self.bytes_out = self.bytes_in = self.pkts_out = self.pkts_in = 0
        self.size = _Welford()
        self.iat = _Welford()
        self.ext_dst_ips = CappedSet(cap)
        self.ext_prefixes = CappedSet(cap)
        self.lan_bytes = 0
        self.dst_ports = CappedSet(cap)
        self.ip_pkts = self.tcp = self.udp = self.icmp = 0
        self.service_ports: dict[int, int] = {}
        self.service_port_overflow = 0
        self.dns_queries = self.nxdomain = 0
        self.domains = CappedSet(cap)
        self.syn_out = self.syn_in = self.synack_out = self.synack_in = self.rst = 0
        self.conn_dur = _Welford()
        self.arp_req_out = 0
        self.arp_targets = CappedSet(cap)
        self.in_peers = CappedSet(cap)
        self.in_ports = CappedSet(cap)
        self.arp_rep_in = 0
        self.lan_peers = CappedSet(cap)
        self.arp_claims: dict[str, set[str]] = {}  # sender IP -> sender MACs of received ARP (<= cap IPs)

    def count_service_port(self, port: int) -> None:
        if port in self.service_ports or len(self.service_ports) < self.cap:
            self.service_ports[port] = self.service_ports.get(port, 0) + 1
        else:
            self.service_port_overflow += 1

    @property
    def saturated(self) -> bool:
        sets = (self.ext_dst_ips, self.ext_prefixes, self.dst_ports, self.domains, self.arp_targets,
                self.in_peers, self.in_ports, self.lan_peers)
        return self.service_port_overflow > 0 or any(s.overflow for s in sets)


@dataclass
class WindowResult:
    """One closed window: its features plus what it would add to the profile."""

    start: float
    end: float
    n_records: int
    first_pkt_index: int  # -1 for an empty window; for joining labels at evaluation time only
    last_pkt_index: int
    features: dict[str, float]
    observation: WindowObservation


@dataclass
class ExtractorStats:
    windows: int = 0
    empty_windows: int = 0
    late_records: int = 0  # timestamp before the open window's start; counted in the open window (D5)
    saturated_windows: int = 0  # some distinct count hit window_set_cap
    conn_table_full: int = 0  # connection attempts not tracked because the table was full
    conn_timeouts: int = 0  # tracked connections dropped after conn_timeout_s without FIN/RST

    def as_dict(self) -> dict[str, int]:
        return asdict(self)


class WindowFeatureExtractor:
    """Turns one device's records (in capture order) into fixed-window feature vectors.

    Usage: call `push(rec)` for every record and `flush()` at the end; both return
    the windows that closed. Commit a window's `observation` to the profile (or not)
    before pushing more records, so later windows see it.
    """

    def __init__(self, profile: ProfileCache, window_s: float = 30.0, tz_offset_h: float = 0.0,
                 emit_empty: bool = True, window_set_cap: int = 4096, conn_table_size: int = 1024,
                 conn_timeout_s: float = 300.0) -> None:
        if window_s <= 0:
            raise ValueError("window_s must be positive")
        self.profile = profile
        self.window_s = float(window_s)
        self.tz_offset_s = float(tz_offset_h) * 3600.0
        self.emit_empty = emit_empty
        self.window_set_cap = window_set_cap
        self.conn_table_size = conn_table_size
        self.conn_timeout_s = float(conn_timeout_s)
        self.stats = ExtractorStats()
        self._win: _Window | None = None
        self._last_ts: float | None = None
        # (local port, peer ip, remote port) -> SYN time. Bounded; C port: fixed array.
        self._conns: dict[tuple[int, str, int], float] = {}

    def push(self, rec: PacketRecord) -> list[WindowResult]:
        closed: list[WindowResult] = []
        k = math.floor(rec.ts / self.window_s)
        if self._win is None:
            self._win = _Window(k, self.window_s, self.window_set_cap)
        elif k > self._win.k:
            closed.append(self._close(self._win))
            if self.emit_empty:
                for gap_k in range(self._win.k + 1, k):
                    closed.append(self._close(_Window(gap_k, self.window_s, self.window_set_cap)))
            self._win = _Window(k, self.window_s, self.window_set_cap)
        elif k < self._win.k:
            self.stats.late_records += 1  # never reopen a closed window (D5)
        self._add(self._win, rec)
        return closed

    def flush(self) -> list[WindowResult]:
        """Close the open window (end of input)."""
        if self._win is None:
            return []
        win, self._win = self._win, None
        return [self._close(win)]

    def run(self, records: Iterable[PacketRecord], commit: "CommitPolicy | None" = None) -> Iterator[WindowResult]:
        """Convenience loop: yields windows and lets `commit(result)` decide on profile updates."""
        for rec in records:
            for res in self.push(rec):
                if commit is not None and commit(res):
                    self.profile.commit(res.observation)
                yield res
        for res in self.flush():
            if commit is not None and commit(res):
                self.profile.commit(res.observation)
            yield res

    # -- per record -----------------------------------------------------------------

    def _add(self, w: _Window, r: PacketRecord) -> None:
        w.n_records += 1
        if w.first_pkt_index < 0:
            w.first_pkt_index = r.pkt_index
        w.last_pkt_index = r.pkt_index
        out = r.direction == "out"
        if out:
            w.bytes_out += r.ip_len
            w.pkts_out += 1
        else:
            w.bytes_in += r.ip_len
            w.pkts_in += 1
        w.size.add(r.ip_len)
        if self._last_ts is not None:
            w.iat.add(max(0.0, r.ts - self._last_ts))
        self._last_ts = r.ts if self._last_ts is None else max(self._last_ts, r.ts)
        if r.peer_is_lan:
            w.lan_bytes += r.ip_len

        if r.ip_version == 0:  # ARP (D8): no ports, flags or L4 protocol
            if out and r.arp_op == ARP_REQUEST:
                w.arp_req_out += 1
                w.arp_targets.add(r.dst_ip)
            elif not out and r.src_ip and r.src_mac:
                w.arp_rep_in += r.arp_op == ARP_REPLY
                if r.src_ip in w.arp_claims or len(w.arp_claims) < w.cap:
                    w.arp_claims.setdefault(r.src_ip, set()).add(r.src_mac)
            return

        w.ip_pkts += 1
        proto = r.ip_proto
        if proto == IP_PROTO_TCP:
            w.tcp += 1
        elif proto == IP_PROTO_UDP:
            w.udp += 1
        elif proto in (IP_PROTO_ICMP, IP_PROTO_ICMP6):
            w.icmp += 1

        if r.peer_is_lan:
            w.lan_peers.add(r.peer_ip)
        if not out:
            w.in_peers.add(r.peer_ip)
            if proto in (IP_PROTO_TCP, IP_PROTO_UDP) and r.dst_port >= 0:
                w.in_ports.add(r.dst_port)
        if out and not r.peer_is_lan:
            w.ext_dst_ips.add(r.peer_ip)
            w.ext_prefixes.add(ip_prefix(r.peer_ip))

        if proto in (IP_PROTO_TCP, IP_PROTO_UDP) and r.dst_port >= 0:
            if out:
                w.dst_ports.add(r.dst_port)
            w.count_service_port(min(r.src_port, r.dst_port))

        if out and r.dns_is_response == 0:
            w.dns_queries += 1
            if r.dns_qname:
                w.domains.add(r.dns_qname)
        elif not out and r.dns_is_response == 1 and r.dns_rcode == DNS_RCODE_NXDOMAIN:
            w.nxdomain += 1

        if proto == IP_PROTO_TCP and r.tcp_flags >= 0:
            self._add_tcp(w, r, out)

    def _add_tcp(self, w: _Window, r: PacketRecord, out: bool) -> None:
        flags = r.tcp_flags
        key = (r.src_port, r.peer_ip, r.dst_port) if out else (r.dst_port, r.peer_ip, r.src_port)
        if flags & TCP_SYN:
            if flags & TCP_ACK:
                if out:
                    w.synack_out += 1
                else:
                    w.synack_in += 1
            else:
                if out:
                    w.syn_out += 1
                else:
                    w.syn_in += 1
                if key not in self._conns:  # a retransmitted SYN keeps the first start time
                    if len(self._conns) < self.conn_table_size:
                        self._conns[key] = r.ts
                    else:
                        self.stats.conn_table_full += 1
        if flags & (TCP_FIN | TCP_RST):
            if flags & TCP_RST:
                w.rst += 1
            started = self._conns.pop(key, None)
            if started is not None:
                w.conn_dur.add(max(0.0, r.ts - started))

    # -- per window -----------------------------------------------------------------

    def _close(self, w: _Window) -> WindowResult:
        cutoff = w.end - self.conn_timeout_s
        expired = [key for key, started in self._conns.items() if started < cutoff]
        for key in expired:
            del self._conns[key]
        self.stats.conn_timeouts += len(expired)

        self.stats.windows += 1
        if w.n_records == 0:
            self.stats.empty_windows += 1
        if w.saturated:
            self.stats.saturated_windows += 1

        p = self.profile
        total_bytes = w.bytes_out + w.bytes_in
        service_pkts = sum(w.service_ports.values())
        top = p.top_ports()
        local = w.start + self.tz_offset_s
        hour = (local % _SECONDS_PER_DAY) / 3600.0
        weekday = (math.floor(local / _SECONDS_PER_DAY) + _EPOCH_WEEKDAY) % 7

        values = (
            w.bytes_out, w.bytes_in, w.pkts_out, w.pkts_in,
            w.bytes_out / total_bytes if total_bytes else 0.0,
            w.size.mean, w.size.var, w.iat.mean, w.iat.var,
            len(w.ext_dst_ips), sum(1 for ip in w.ext_dst_ips if not p.has_ip(ip)),
            len(w.ext_prefixes), w.lan_bytes / total_bytes if total_bytes else 0.0,
            len(w.dst_ports), sum(1 for port in w.dst_ports if not p.has_dst_port(port)),
            w.tcp / w.ip_pkts if w.ip_pkts else 0.0,
            w.udp / w.ip_pkts if w.ip_pkts else 0.0,
            w.icmp / w.ip_pkts if w.ip_pkts else 0.0,
            sum(w.service_ports.get(port, 0) for port in top) / service_pkts if service_pkts else 0.0,
            w.dns_queries, len(w.domains), sum(1 for d in w.domains if not p.has_domain(d)), w.nxdomain,
            w.syn_out + w.syn_in,
            max(0, w.syn_out - w.synack_in) + max(0, w.syn_in - w.synack_out) + w.rst,
            w.conn_dur.mean,
            w.arp_req_out, len(w.arp_targets),
            math.sin(2 * math.pi * hour / 24), math.cos(2 * math.pi * hour / 24),
            1.0 if weekday >= 5 else 0.0,
            len(w.in_peers), sum(1 for ip in w.in_peers if not p.has_in_peer(ip)), len(w.in_ports),
            w.arp_rep_in,
            sum(1 for ip, macs in w.arp_claims.items()
                if len(macs) > 1 or (p.arp_binding(ip) is not None and p.arp_binding(ip) not in macs)),
            sum(1 for port in w.in_ports if not p.has_in_port(port)),
            len(w.lan_peers), sum(1 for ip in w.lan_peers if not p.has_lan_peer(ip)),
        )
        features = {name: float(v) for name, v in zip(FEATURE_NAMES, values, strict=True)}
        observation = WindowObservation(
            window_start=w.start,
            dst_ips=tuple(w.ext_dst_ips),
            dst_ports=tuple(w.dst_ports),
            domains=tuple(w.domains),
            service_ports=tuple(w.service_ports.items()),
            in_peers=tuple(w.in_peers),
            in_ports=tuple(w.in_ports),
            lan_peers=tuple(w.lan_peers),
            arp_bindings=tuple((ip, min(macs)) for ip, macs in w.arp_claims.items() if len(macs) == 1),
        )
        return WindowResult(w.start, w.end, w.n_records, w.first_pkt_index, w.last_pkt_index,
                            features, observation)


class CommitPolicy:
    """Stand-in for the Phase 2 update rule: decides which windows reach the profile cache.

    modes: "bootstrap" (first `bootstrap_windows` windows, then frozen),
           "always" (naive: every window), "never" (profile stays empty).
    """

    MODES = ("bootstrap", "always", "never")

    def __init__(self, mode: str = "bootstrap", bootstrap_windows: int = 120) -> None:
        if mode not in self.MODES:
            raise ValueError(f"profile update mode must be one of {self.MODES}, got {mode!r}")
        self.mode = mode
        self.bootstrap_windows = bootstrap_windows
        self.seen = 0

    def __call__(self, res: WindowResult) -> bool:
        self.seen += 1
        if self.mode == "always":
            return True
        if self.mode == "bootstrap":
            return self.seen <= self.bootstrap_windows
        return False
