"""Synthetic captures with known contents, built with dpkt (no real data needed for tests)."""

from __future__ import annotations

import gzip
import shutil
import socket
import struct
from pathlib import Path

import dpkt
import pytest

DEVICE_MAC = "02:00:00:00:00:01"
DEVICE_IP = "192.168.1.50"
DEVICE_IP6 = "fe80::1"
ROUTER_MAC = "02:00:00:00:00:fe"
ROUTER_IP = "192.168.1.1"
OTHER_MAC = "02:00:00:00:00:02"
OTHER_IP = "192.168.1.60"
BCAST_MAC = "ff:ff:ff:ff:ff:ff"
MDNS6_MAC = "33:33:00:00:00:fb"

T0 = 1_700_000_000.0
DT = 0.25  # exactly representable, so pcap (us) and pcapng timestamps round-trip

# Frame indices of the standard stream and what each one is.
IDX_SYN, IDX_SYNACK, IDX_RST, IDX_DNS_Q, IDX_DNS_NX, IDX_ICMP = 0, 1, 2, 3, 4, 5
IDX_ARP, IDX_IPV6_MDNS, IDX_VLAN_TELNET, IDX_TRUNCATED_IP = 6, 7, 8, 9
IDX_OTHER_DEVICE, IDX_OTHER_BCAST, IDX_TRUNCATED_TCP = 10, 11, 12
DEVICE_INDICES = [0, 1, 2, 3, 4, 5, 7, 8, 12]


def mac(m: str) -> bytes:
    return bytes(int(x, 16) for x in m.split(":"))


def ip4(a: str) -> bytes:
    return socket.inet_pton(socket.AF_INET, a)


def ip6(a: str) -> bytes:
    return socket.inet_pton(socket.AF_INET6, a)


def ipv4_packet(src: str, dst: str, l4: dpkt.Packet, proto: int) -> dpkt.ip.IP:
    pkt = dpkt.ip.IP(src=ip4(src), dst=ip4(dst), p=proto, ttl=64, data=l4)
    pkt.len = len(pkt)
    return pkt


def eth(src: str, dst: str, payload: dpkt.Packet | bytes, etype: int = dpkt.ethernet.ETH_TYPE_IP) -> bytes:
    return bytes(dpkt.ethernet.Ethernet(src=mac(src), dst=mac(dst), type=etype, data=payload))


def tcp(sport: int, dport: int, flags: int) -> dpkt.tcp.TCP:
    return dpkt.tcp.TCP(sport=sport, dport=dport, flags=flags, seq=1, win=1024)


def udp(sport: int, dport: int, payload: bytes) -> dpkt.udp.UDP:
    u = dpkt.udp.UDP(sport=sport, dport=dport, data=payload)
    u.ulen = len(u)
    return u


def dns_query(name: str) -> bytes:
    q = dpkt.dns.DNS(id=1, qd=[dpkt.dns.DNS.Q(name=name, type=dpkt.dns.DNS_A, cls=dpkt.dns.DNS_IN)])
    q.qr = dpkt.dns.DNS_Q
    return bytes(q)


def dns_nxdomain(name: str) -> bytes:
    r = dpkt.dns.DNS(id=2, qd=[dpkt.dns.DNS.Q(name=name, type=dpkt.dns.DNS_A, cls=dpkt.dns.DNS_IN)])
    r.qr = dpkt.dns.DNS_R
    r.rcode = dpkt.dns.DNS_RCODE_NXDOMAIN
    return bytes(r)


def standard_frames() -> list[tuple[float, bytes]]:
    """13 frames covering every decode path; see the IDX_* constants."""
    F = dpkt.tcp
    frames: list[bytes] = []
    # 0-2: a refused TCP connection from the device to the internet
    frames.append(eth(DEVICE_MAC, ROUTER_MAC, ipv4_packet(DEVICE_IP, "93.184.216.34", tcp(40000, 443, F.TH_SYN), 6)))
    frames.append(eth(ROUTER_MAC, DEVICE_MAC, ipv4_packet("93.184.216.34", DEVICE_IP, tcp(443, 40000, F.TH_SYN | F.TH_ACK), 6)))
    frames.append(eth(DEVICE_MAC, ROUTER_MAC, ipv4_packet(DEVICE_IP, "93.184.216.34", tcp(40000, 443, F.TH_RST), 6)))
    # 3-4: DNS query to the router, NXDOMAIN response
    frames.append(eth(DEVICE_MAC, ROUTER_MAC, ipv4_packet(DEVICE_IP, ROUTER_IP, udp(5000, 53, dns_query("Example.COM")), 17)))
    frames.append(eth(ROUTER_MAC, DEVICE_MAC, ipv4_packet(ROUTER_IP, DEVICE_IP, udp(53, 5000, dns_nxdomain("NonExistent.example")), 17)))
    # 5: ICMP echo request
    echo = dpkt.icmp.ICMP(type=dpkt.icmp.ICMP_ECHO, data=dpkt.icmp.ICMP.Echo(id=1, seq=1))
    frames.append(eth(DEVICE_MAC, ROUTER_MAC, ipv4_packet(DEVICE_IP, "1.1.1.1", echo, 1)))
    # 6: ARP broadcast (non-IP, skipped)
    arp = dpkt.arp.ARP(sha=mac(DEVICE_MAC), spa=ip4(DEVICE_IP), tha=b"\x00" * 6, tpa=ip4(ROUTER_IP))
    frames.append(eth(DEVICE_MAC, BCAST_MAC, arp, dpkt.ethernet.ETH_TYPE_ARP))
    # 7: IPv6 mDNS to a multicast group
    u6 = udp(5353, 5353, b"\x00" * 12)
    v6 = dpkt.ip6.IP6(src=ip6(DEVICE_IP6), dst=ip6("ff02::fb"), nxt=17, hlim=255, plen=len(u6), data=u6)
    frames.append(eth(DEVICE_MAC, MDNS6_MAC, v6, dpkt.ethernet.ETH_TYPE_IP6))
    # 8: 802.1Q VLAN-tagged telnet SYN (built by hand: dst, src, 0x8100, TCI, 0x0800, IP)
    ip_bytes = bytes(ipv4_packet(DEVICE_IP, "203.0.113.5", tcp(40001, 23, F.TH_SYN), 6))
    frames.append(mac(ROUTER_MAC) + mac(DEVICE_MAC) + struct.pack("!HHH", 0x8100, 10, 0x0800) + ip_bytes)
    # 9: Ethernet header claiming IPv4 but only 10 bytes of IP header (malformed, skipped)
    frames.append(mac(ROUTER_MAC) + mac(DEVICE_MAC) + struct.pack("!H", 0x0800) + ip_bytes[:10])
    # 10-11: another device's traffic (filtered out)
    frames.append(eth(OTHER_MAC, ROUTER_MAC, ipv4_packet(OTHER_IP, "8.8.8.8", tcp(50000, 80, F.TH_SYN), 6)))
    frames.append(eth(OTHER_MAC, BCAST_MAC, ipv4_packet(OTHER_IP, "255.255.255.255", udp(68, 67, b"\x00" * 8), 17)))
    # 12: device packet whose TCP header is cut short by the snaplen (kept, ports unknown)
    full = bytes(ipv4_packet(DEVICE_IP, "93.184.216.34", tcp(40002, 443, F.TH_ACK), 6))
    frames.append(eth(DEVICE_MAC, ROUTER_MAC, b"")[:14] + full[:26])
    return [(T0 + i * DT, f) for i, f in enumerate(frames)]


def write_pcap(path: Path, frames: list[tuple[float, bytes]], linktype: int = dpkt.pcap.DLT_EN10MB) -> Path:
    with open(path, "wb") as fh:
        w = dpkt.pcap.Writer(fh, linktype=linktype)
        for ts, buf in frames:
            w.writepkt(buf, ts=ts)
    return path


def write_pcapng(path: Path, frames: list[tuple[float, bytes]]) -> Path:
    with open(path, "wb") as fh:
        w = dpkt.pcapng.Writer(fh)
        for ts, buf in frames:
            w.writepkt(buf, ts=ts)
    return path


def gzip_file(src: Path, dst: Path) -> Path:
    with open(src, "rb") as fin, gzip.open(dst, "wb") as fout:
        shutil.copyfileobj(fin, fout)
    return dst


@pytest.fixture
def frames() -> list[tuple[float, bytes]]:
    return standard_frames()


@pytest.fixture
def pcap_path(tmp_path: Path, frames) -> Path:
    return write_pcap(tmp_path / "stream.pcap", frames)


@pytest.fixture
def pcapng_path(tmp_path: Path, frames) -> Path:
    return write_pcapng(tmp_path / "stream.pcapng", frames)


@pytest.fixture
def pcap_gz_path(tmp_path: Path, pcap_path: Path) -> Path:
    return gzip_file(pcap_path, tmp_path / "stream.pcap.gz")
