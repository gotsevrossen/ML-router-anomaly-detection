"""Keep only the target device's packets and label each with direction and peer.

Single-device rule (CLAUDE.md §2): one profile per device, keyed by MAC. A
packet belongs to the device's conversation iff the device's MAC is the
Ethernet source ("out") or destination ("in"). Broadcast / multicast frames
the device merely *receives* are not its conversation and are dropped; frames
it *sends* to a broadcast/multicast address are kept (direction "out").

`target_ip` is a fallback for captures with no usable MACs (raw-IP or SLL
captures, or traffic recorded upstream of the device): a packet whose MAC does
not match is still kept if its IP matches.
"""

from __future__ import annotations

import ipaddress
from collections import defaultdict
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Iterator

from rad.features.packet_schema import PacketRecord
from rad.features.pcap_reader import ParseStats, iter_packets, normalize_mac

# Local-scope ranges, listed explicitly (not via ipaddress.is_private, whose
# definition changes between Python versions) so the C port can copy them.
LAN_NETWORKS = tuple(
    ipaddress.ip_network(n)
    for n in (
        "10.0.0.0/8",
        "172.16.0.0/12",
        "192.168.0.0/16",
        "169.254.0.0/16",  # IPv4 link-local
        "127.0.0.0/8",
        "224.0.0.0/4",  # multicast (SSDP, mDNS, ...) never leaves the LAN
        "255.255.255.255/32",
        "fc00::/7",  # IPv6 unique local
        "fe80::/10",  # IPv6 link-local
        "ff00::/8",  # IPv6 multicast
        "::1/128",
    )
)


@lru_cache(maxsize=65536)
def is_lan_ip(ip: str) -> bool:
    """True if `ip` is in a local-scope range (see LAN_NETWORKS)."""
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return False
    return any(addr.version == net.version and addr in net for net in LAN_NETWORKS)


class DeviceFilter:
    """Selects one device's packets and sets direction / peer_ip / peer_is_lan in place."""

    def __init__(self, target_mac: str | None, target_ip: str | None = None) -> None:
        if not target_mac and not target_ip:
            raise ValueError("DeviceFilter needs target_mac, target_ip, or both")
        self.target_mac = normalize_mac(target_mac) if target_mac else None
        self.target_ip = str(ipaddress.ip_address(target_ip)) if target_ip else None

    def apply(self, rec: PacketRecord) -> PacketRecord | None:
        """Return the labelled record if it belongs to the device, else None."""
        if self.target_mac is not None and rec.src_mac == self.target_mac:
            direction = "out"
        elif self.target_mac is not None and rec.dst_mac == self.target_mac:
            direction = "in"
        elif self.target_ip is not None and rec.src_ip == self.target_ip:
            direction = "out"
        elif self.target_ip is not None and rec.dst_ip == self.target_ip:
            direction = "in"
        else:
            return None
        rec.direction = direction
        rec.peer_ip = rec.dst_ip if direction == "out" else rec.src_ip
        rec.peer_is_lan = is_lan_ip(rec.peer_ip)
        return rec

    def filter(self, records: Iterable[PacketRecord]) -> Iterator[PacketRecord]:
        for rec in records:
            out = self.apply(rec)
            if out is not None:
                yield out


def _is_group_mac(mac: str) -> bool:
    """Broadcast / multicast MACs have the least-significant bit of the first octet set."""
    return bool(mac) and int(mac[:2], 16) & 1 == 1


@dataclass
class DeviceSummary:
    mac: str
    packets_sent: int = 0
    packets_received: int = 0
    bytes_sent: int = 0
    bytes_received: int = 0
    first_ts: float = float("inf")
    last_ts: float = float("-inf")
    ips: set[str] = field(default_factory=set)

    @property
    def packets(self) -> int:
        return self.packets_sent + self.packets_received


_MAX_IPS_PER_MAC = 8  # bounded: enough to recognise a device, not a full inventory


def list_devices(path: str | Path, top: int = 20, stats: ParseStats | None = None) -> list[DeviceSummary]:
    """Stream a capture and summarise unicast MACs by traffic, to help pick `target_mac`."""
    devices: dict[str, DeviceSummary] = defaultdict(lambda: DeviceSummary(mac=""))
    for rec in iter_packets(path, stats):
        for mac, sent in ((rec.src_mac, True), (rec.dst_mac, False)):
            if not mac or _is_group_mac(mac):
                continue
            d = devices[mac]
            d.mac = mac
            if sent:
                d.packets_sent += 1
                d.bytes_sent += rec.ip_len
                if len(d.ips) < _MAX_IPS_PER_MAC:
                    d.ips.add(rec.src_ip)
            else:
                d.packets_received += 1
                d.bytes_received += rec.ip_len
            d.first_ts = min(d.first_ts, rec.ts)
            d.last_ts = max(d.last_ts, rec.ts)
    ranked = sorted(devices.values(), key=lambda d: (-d.packets, d.mac))
    return ranked[:top]
