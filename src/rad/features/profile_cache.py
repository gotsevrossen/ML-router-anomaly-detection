"""Bounded profile cache behind the "new IP / port / domain" features (Phase 1b).

The cache is part of the device profile, so it must obey the same commit rules
as the model (CLAUDE.md §5 1b, §8 "profile cache poisoning"). The window
extractor only *reads* it; each closed window hands back a `WindowObservation`,
and the update rule decides whether and when to `commit` it. In Phase 2 the
quarantine buffer holds observations next to feature vectors and commits both
together.

Every structure has a fixed capacity so the C port can use static arrays
(see docs/decisions.md D11).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Hashable, Iterator


class CappedSet:
    """Insertion-ordered set that stops growing at `cap` items.

    Items offered after the cap is reached are dropped and counted in
    `overflow`; membership stays exact for the items that were admitted.
    C port: a fixed-size hash table that refuses inserts when full.
    """

    def __init__(self, cap: int) -> None:
        if cap < 1:
            raise ValueError(f"cap must be >= 1, got {cap}")
        self.cap = cap
        self._items: dict[Hashable, None] = {}
        self.overflow = 0

    def add(self, item: Hashable) -> bool:
        """Insert `item`; return True only if it was newly admitted."""
        if item in self._items:
            return False
        if len(self._items) >= self.cap:
            self.overflow += 1
            return False
        self._items[item] = None
        return True

    def __contains__(self, item: object) -> bool:
        return item in self._items

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator:
        return iter(self._items)


@dataclass(frozen=True)
class WindowObservation:
    """What one window would add to the profile if committed. All tuples are in first-seen order."""

    window_start: float
    dst_ips: tuple[str, ...] = ()
    dst_ports: tuple[int, ...] = ()
    domains: tuple[str, ...] = ()
    service_ports: tuple[tuple[int, int], ...] = ()  # (service port, packets)
    in_peers: tuple[str, ...] = ()  # senders of received IP packets, LAN or not (D31)
    arp_bindings: tuple[tuple[str, str], ...] = ()  # (IP, MAC) claimed by one MAC in received ARP (D34)


class ProfileCache:
    """Committed destinations, ports, domains and service-port counts of one device."""

    def __init__(self, max_ips: int = 4096, max_ports: int = 1024, max_domains: int = 2048,
                 top_k_ports: int = 3) -> None:
        self.ips = CappedSet(max_ips)
        self.dst_ports = CappedSet(max_ports)
        self.domains = CappedSet(max_domains)
        self.in_peers = CappedSet(max_ips)
        self.max_ips = max_ips
        self._arp: dict[str, str] = {}  # IP -> MAC last committed (bounded by max_ips)
        self.arp_overflow = 0
        self.max_ports = max_ports
        self.top_k_ports = top_k_ports
        self.service_port_counts: dict[int, int] = {}
        self.service_port_overflow = 0
        self._top: tuple[int, ...] = ()
        self.windows_committed = 0

    def has_ip(self, ip: str) -> bool:
        return ip in self.ips

    def arp_binding(self, ip: str) -> str | None:
        return self._arp.get(ip)

    def has_in_peer(self, ip: str) -> bool:
        return ip in self.in_peers

    def has_dst_port(self, port: int) -> bool:
        return port in self.dst_ports

    def has_domain(self, domain: str) -> bool:
        return domain in self.domains

    def top_ports(self) -> tuple[int, ...]:
        """The device's most used service ports so far (ties broken by lower port number)."""
        return self._top

    def commit(self, obs: WindowObservation) -> None:
        """Learn one window's observations. Only the update rule should call this."""
        for ip in obs.dst_ips:
            self.ips.add(ip)
        for ip in obs.in_peers:
            self.in_peers.add(ip)
        for ip, mac in obs.arp_bindings:
            if ip in self._arp or len(self._arp) < self.max_ips:
                self._arp[ip] = mac  # a committed (gated) window may legitimately rebind an IP
            else:
                self.arp_overflow += 1
        for port in obs.dst_ports:
            self.dst_ports.add(port)
        for domain in obs.domains:
            self.domains.add(domain)
        for port, packets in obs.service_ports:
            if port in self.service_port_counts or len(self.service_port_counts) < self.max_ports:
                self.service_port_counts[port] = self.service_port_counts.get(port, 0) + packets
            else:
                self.service_port_overflow += 1
        ranked = sorted(self.service_port_counts.items(), key=lambda kv: (-kv[1], kv[0]))
        self._top = tuple(port for port, _ in ranked[: self.top_k_ports])
        self.windows_committed += 1

    def stats(self) -> dict[str, object]:
        """Sizes and overflow counters, written to meta.json so saturation is never silent."""
        return {
            "windows_committed": self.windows_committed,
            "ips": len(self.ips),
            "ips_overflow": self.ips.overflow,
            "dst_ports": len(self.dst_ports),
            "dst_ports_overflow": self.dst_ports.overflow,
            "domains": len(self.domains),
            "domains_overflow": self.domains.overflow,
            "in_peers": len(self.in_peers),
            "in_peers_overflow": self.in_peers.overflow,
            "arp_bindings": len(self._arp),
            "arp_overflow": self.arp_overflow,
            "service_ports": len(self.service_port_counts),
            "service_ports_overflow": self.service_port_overflow,
            "top_ports": list(self._top),
        }
