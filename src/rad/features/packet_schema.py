"""Per-packet record produced by Phase 1a parsing.

The column order below is part of the contract with Phase 1b (windowing) and
the Phase 4 C port: do not reorder columns, only append new ones.

Columns (in order):
  pkt_index        int64   0-based index of the frame in the original capture
                           (counts every frame, including skipped ones), so
                           per-packet dataset labels can be joined at evaluation
                           time only. Never used as a model input.
  ts               float64 packet timestamp in seconds (capture clock, not wall clock)
  cap_len          int32   captured frame length in bytes (may be < on-wire if snaplen cut it)
  ip_len           int32   IP-layer length from the IP header (IPv4 total length,
                           IPv6 payload length + 40). Used for volume features
                           because it survives snaplen truncation.
  src_mac          string  "aa:bb:cc:dd:ee:ff" ("" if the link layer has none)
  dst_mac          string  as above
  ip_version       int8    4 or 6
  src_ip           string
  dst_ip           string
  ip_proto         int16   IP protocol / IPv6 next header (6 TCP, 17 UDP, 1 ICMP, 58 ICMPv6, ...)
  src_port         int32   -1 if not TCP/UDP or the L4 header could not be decoded
  dst_port         int32   -1 as above
  tcp_flags        int16   raw TCP flag byte; -1 if not TCP
  icmp_type        int16   ICMP / ICMPv6 type; -1 otherwise
  dns_is_response  int8    1 response, 0 query, -1 not a DNS packet (UDP port 53 only)
  dns_qname        string  first question name, lower-cased, no trailing dot; "" if none
  dns_rcode        int16   DNS response code (3 = NXDOMAIN); -1 if not DNS
  direction        string  "out" (device is sender) or "in" (device is receiver);
                           set by the device filter
  peer_ip          string  the other endpoint's IP; set by the device filter
  peer_is_lan      bool    peer is in a local-scope range (see device_filter.LAN_NETWORKS)
"""

from __future__ import annotations

from dataclasses import dataclass, fields

import pyarrow as pa

# TCP flag bits (same values as the TCP header byte).
TCP_FIN = 0x01
TCP_SYN = 0x02
TCP_RST = 0x04
TCP_PSH = 0x08
TCP_ACK = 0x10

DNS_RCODE_NXDOMAIN = 3


@dataclass(slots=True)
class PacketRecord:
    pkt_index: int
    ts: float
    cap_len: int
    ip_len: int
    src_mac: str
    dst_mac: str
    ip_version: int
    src_ip: str
    dst_ip: str
    ip_proto: int
    src_port: int = -1
    dst_port: int = -1
    tcp_flags: int = -1
    icmp_type: int = -1
    dns_is_response: int = -1
    dns_qname: str = ""
    dns_rcode: int = -1
    direction: str = ""
    peer_ip: str = ""
    peer_is_lan: bool = False

    def as_tuple(self) -> tuple:
        return tuple(getattr(self, name) for name in COLUMNS)


COLUMNS: tuple[str, ...] = tuple(f.name for f in fields(PacketRecord))

ARROW_SCHEMA = pa.schema(
    [
        ("pkt_index", pa.int64()),
        ("ts", pa.float64()),
        ("cap_len", pa.int32()),
        ("ip_len", pa.int32()),
        ("src_mac", pa.string()),
        ("dst_mac", pa.string()),
        ("ip_version", pa.int8()),
        ("src_ip", pa.string()),
        ("dst_ip", pa.string()),
        ("ip_proto", pa.int16()),
        ("src_port", pa.int32()),
        ("dst_port", pa.int32()),
        ("tcp_flags", pa.int16()),
        ("icmp_type", pa.int16()),
        ("dns_is_response", pa.int8()),
        ("dns_qname", pa.string()),
        ("dns_rcode", pa.int16()),
        ("direction", pa.string()),
        ("peer_ip", pa.string()),
        ("peer_is_lan", pa.bool_()),
    ]
)

assert tuple(ARROW_SCHEMA.names) == COLUMNS, "ARROW_SCHEMA must match PacketRecord field order"


def records_to_table(records: list[PacketRecord]) -> pa.Table:
    """Convert a chunk of records to an Arrow table with the fixed schema."""
    columns = list(zip(*(r.as_tuple() for r in records))) if records else [[] for _ in COLUMNS]
    arrays = [pa.array(col, type=field.type) for col, field in zip(columns, ARROW_SCHEMA)]
    return pa.Table.from_arrays(arrays, schema=ARROW_SCHEMA)
