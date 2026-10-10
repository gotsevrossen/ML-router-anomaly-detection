"""Streaming pcap / pcapng reader and header-only packet decoder.

Design rules this module follows (CLAUDE.md §2, §5 Phase 1a):
  * Streaming: frames are yielded one at a time in capture order; the whole
    file is never loaded and packets are never re-ordered.
  * Headers only: Ethernet / IP / TCP / UDP / ICMP headers are decoded. The
    one exception is DNS (UDP port 53), where the question name and response
    code are read because the DNS feature group needs them (see
    docs/decisions.md). No other payload byte is inspected.
  * Never crash on bad input: malformed frames are counted and skipped.
"""

from __future__ import annotations

import gzip
import logging
import socket
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import BinaryIO, Iterator

import dpkt

from rad.features.packet_schema import PacketRecord

log = logging.getLogger(__name__)

# Link types we can decode (see https://www.tcpdump.org/linktypes.html).
DLT_EN10MB = 1
DLT_RAW = 101
DLT_RAW_ALT = (12, 14)  # OS-specific aliases for raw IP
DLT_LINUX_SLL = 113
DLT_LINUX_SLL2 = 276

_PCAP_MAGICS = {
    b"\xd4\xc3\xb2\xa1", b"\xa1\xb2\xc3\xd4",  # microsecond, LE / BE
    b"\x4d\x3c\xb2\xa1", b"\xa1\xb2\x3c\x4d",  # nanosecond, LE / BE
}
_PCAPNG_MAGIC = b"\x0a\x0d\x0d\x0a"
_GZIP_MAGIC = b"\x1f\x8b"

ETH_TYPE_IP = 0x0800
ETH_TYPE_IP6 = 0x86DD
DNS_PORT = 53


@dataclass
class ParseStats:
    """Counters reported in the run's meta.json so data loss is never silent."""

    frames_total: int = 0
    decoded_ip: int = 0
    skipped_non_ip: int = 0  # e.g. ARP, LLDP, EAPOL
    skipped_malformed: int = 0  # claimed IP but header could not be decoded
    l4_undecoded: int = 0  # IP ok, but TCP/UDP/ICMP header truncated or a non-first fragment
    dns_undecoded: int = 0  # UDP/53 payload that is not a parseable DNS message
    out_of_order_ts: int = 0  # timestamp earlier than the previous frame's

    def as_dict(self) -> dict[str, int]:
        return asdict(self)


def _open_maybe_gzip(path: Path) -> BinaryIO:
    with open(path, "rb") as fh:
        magic = fh.read(2)
    if magic == _GZIP_MAGIC:
        return gzip.open(path, "rb")  # type: ignore[return-value]
    return open(path, "rb")


def open_capture(path: str | Path) -> tuple[BinaryIO, "dpkt.pcap.Reader | dpkt.pcapng.Reader"]:
    """Open a pcap / pcapng (optionally gzipped) file; format is detected from magic bytes."""
    path = Path(path)
    fh = _open_maybe_gzip(path)
    magic = fh.read(4)
    # Re-open rather than seek: gzip streams seek slowly and some readers need offset 0.
    fh.close()
    fh = _open_maybe_gzip(path)
    if magic == _PCAPNG_MAGIC:
        return fh, dpkt.pcapng.Reader(fh)
    if magic in _PCAP_MAGICS:
        return fh, dpkt.pcap.Reader(fh)
    fh.close()
    raise ValueError(f"{path}: not a pcap or pcapng file (magic={magic.hex()})")


def iter_frames(path: str | Path) -> Iterator[tuple[int, float, bytes, int]]:
    """Yield (pkt_index, ts, frame_bytes, linktype) for every frame, in capture order."""
    fh, reader = open_capture(path)
    linktype = reader.datalink()
    try:
        for idx, (ts, buf) in enumerate(reader):
            yield idx, float(ts), buf, linktype
    finally:
        fh.close()


def mac_str(raw: bytes) -> str:
    return ":".join(f"{b:02x}" for b in raw)


def normalize_mac(mac: str) -> str:
    """Accept aa:bb:.., aa-bb-.., or aabb.. in any case; return lower-case colon form."""
    hex_only = mac.replace(":", "").replace("-", "").replace(".", "").lower()
    if len(hex_only) != 12 or any(c not in "0123456789abcdef" for c in hex_only):
        raise ValueError(f"Invalid MAC address: {mac!r}")
    return ":".join(hex_only[i : i + 2] for i in range(0, 12, 2))


def _link_decode(buf: bytes, linktype: int) -> tuple[str, str, int, object] | None:
    """Strip the link layer. Returns (src_mac, dst_mac, ethertype, l3) or None if unsupported."""
    if linktype == DLT_EN10MB:
        eth = dpkt.ethernet.Ethernet(buf)  # dpkt strips 802.1Q / QinQ tags itself
        return mac_str(eth.src), mac_str(eth.dst), eth.type, eth.data
    if linktype in (DLT_LINUX_SLL, DLT_LINUX_SLL2):
        sll = dpkt.sll.SLL(buf) if linktype == DLT_LINUX_SLL else dpkt.sll2.SLL2(buf)
        # SLL carries only the sender's address. Packet type 4 = sent by the capturing host.
        src = mac_str(sll.hdr[: sll.hlen]) if sll.hlen == 6 else ""
        return src, "", sll.ethtype, sll.data
    if linktype == DLT_RAW or linktype in DLT_RAW_ALT:
        if not buf:
            return None
        version = buf[0] >> 4
        if version == 4:
            return "", "", ETH_TYPE_IP, dpkt.ip.IP(buf)
        if version == 6:
            return "", "", ETH_TYPE_IP6, dpkt.ip6.IP6(buf)
        return None
    return None


def _decode_dns(payload: bytes, rec: PacketRecord, stats: ParseStats) -> None:
    try:
        msg = dpkt.dns.DNS(payload)
    except (dpkt.UnpackError, IndexError, ValueError):
        stats.dns_undecoded += 1
        return
    rec.dns_is_response = 1 if msg.qr == dpkt.dns.DNS_R else 0
    rec.dns_rcode = int(msg.rcode)
    if msg.qd:
        rec.dns_qname = msg.qd[0].name.lower().rstrip(".")


def decode_frame(
    pkt_index: int, ts: float, buf: bytes, linktype: int, stats: ParseStats
) -> PacketRecord | None:
    """Decode one frame into a PacketRecord, or return None (and count why) if it is skipped."""
    try:
        link = _link_decode(buf, linktype)
    except (dpkt.UnpackError, IndexError, ValueError):
        stats.skipped_malformed += 1
        return None
    if link is None:
        stats.skipped_non_ip += 1
        return None
    src_mac, dst_mac, ethertype, l3 = link

    if isinstance(l3, dpkt.ip.IP):
        ip_version = 4
        src_ip = socket.inet_ntop(socket.AF_INET, l3.src)
        dst_ip = socket.inet_ntop(socket.AF_INET, l3.dst)
        proto = l3.p
        # ip.len == 0 happens with TCP segmentation offload captures; fall back to what we have.
        ip_len = l3.len or (l3.__hdr_len__ + len(l3.opts) + len(l3.data))
    elif isinstance(l3, dpkt.ip6.IP6):
        ip_version = 6
        src_ip = socket.inet_ntop(socket.AF_INET6, l3.src)
        dst_ip = socket.inet_ntop(socket.AF_INET6, l3.dst)
        proto = l3.p  # dpkt walks extension headers; this is the final next-header
        ip_len = l3.plen + 40
    else:
        if ethertype in (ETH_TYPE_IP, ETH_TYPE_IP6):
            stats.skipped_malformed += 1  # claimed IP but dpkt could not parse the header
        else:
            stats.skipped_non_ip += 1
        return None

    stats.decoded_ip += 1
    rec = PacketRecord(
        pkt_index=pkt_index,
        ts=ts,
        cap_len=len(buf),
        ip_len=int(ip_len),
        src_mac=src_mac,
        dst_mac=dst_mac,
        ip_version=ip_version,
        src_ip=src_ip,
        dst_ip=dst_ip,
        ip_proto=int(proto),
    )

    l4 = l3.data
    if isinstance(l4, dpkt.tcp.TCP):
        rec.src_port, rec.dst_port, rec.tcp_flags = l4.sport, l4.dport, l4.flags
    elif isinstance(l4, dpkt.udp.UDP):
        rec.src_port, rec.dst_port = l4.sport, l4.dport
        if DNS_PORT in (l4.sport, l4.dport):
            _decode_dns(bytes(l4.data), rec, stats)
    elif isinstance(l4, (dpkt.icmp.ICMP, dpkt.icmp6.ICMP6)):
        rec.icmp_type = l4.type
    elif proto in (dpkt.ip.IP_PROTO_TCP, dpkt.ip.IP_PROTO_UDP, dpkt.ip.IP_PROTO_ICMP, dpkt.ip.IP_PROTO_ICMP6):
        stats.l4_undecoded += 1  # known L4 protocol but header missing/truncated, or a later fragment
    return rec


def iter_packets(path: str | Path, stats: ParseStats | None = None) -> Iterator[PacketRecord]:
    """Stream decoded IP packets from a capture, in capture order.

    `stats` (if given) is updated in place, so callers can read the counters
    after (or during) iteration.
    """
    stats = stats if stats is not None else ParseStats()
    last_ts = float("-inf")
    for pkt_index, ts, buf, linktype in iter_frames(path):
        stats.frames_total += 1
        if ts < last_ts:
            stats.out_of_order_ts += 1
            if stats.out_of_order_ts <= 5:
                log.warning("Frame %d timestamp %.6f is earlier than previous %.6f (kept in capture order)",
                            pkt_index, ts, last_ts)
        else:
            last_ts = ts
        rec = decode_frame(pkt_index, ts, buf, linktype, stats)
        if rec is not None:
            yield rec
