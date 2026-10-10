from __future__ import annotations

import struct
from pathlib import Path

import dpkt
import pytest

from conftest import (
    DEVICE_IP,
    DEVICE_MAC,
    IDX_DNS_NX,
    IDX_DNS_Q,
    IDX_ICMP,
    IDX_IPV6_MDNS,
    IDX_SYN,
    IDX_SYNACK,
    IDX_TRUNCATED_TCP,
    IDX_VLAN_TELNET,
    ROUTER_MAC,
    T0,
    ipv4_packet,
    mac,
    tcp,
    write_pcap,
)
from rad.features.packet_schema import TCP_ACK, TCP_SYN
from rad.features.pcap_reader import ParseStats, iter_packets, normalize_mac


def _by_index(path: Path) -> tuple[dict[int, object], ParseStats]:
    stats = ParseStats()
    recs = {r.pkt_index: r for r in iter_packets(path, stats)}
    return recs, stats


def test_stats_count_every_skip_reason(pcap_path):
    _, stats = _by_index(pcap_path)
    assert stats.frames_total == 13
    assert stats.decoded_ip == 11
    assert stats.skipped_non_ip == 1  # ARP
    assert stats.skipped_malformed == 1  # truncated IPv4 header
    assert stats.l4_undecoded == 1  # truncated TCP header
    assert stats.dns_undecoded == 0
    assert stats.out_of_order_ts == 0


def test_tcp_fields(pcap_path):
    recs, _ = _by_index(pcap_path)
    syn = recs[IDX_SYN]
    assert syn.ts == T0
    assert (syn.src_mac, syn.dst_mac) == (DEVICE_MAC, ROUTER_MAC)
    assert (syn.src_ip, syn.dst_ip) == (DEVICE_IP, "93.184.216.34")
    assert (syn.ip_version, syn.ip_proto) == (4, 6)
    assert (syn.src_port, syn.dst_port) == (40000, 443)
    assert syn.tcp_flags == TCP_SYN
    assert syn.ip_len == 40  # 20 IP + 20 TCP
    assert syn.cap_len == 54  # + 14 Ethernet
    assert syn.icmp_type == -1 and syn.dns_is_response == -1 and syn.dns_rcode == -1
    assert recs[IDX_SYNACK].tcp_flags == TCP_SYN | TCP_ACK


def test_dns_fields(pcap_path):
    recs, _ = _by_index(pcap_path)
    q, nx = recs[IDX_DNS_Q], recs[IDX_DNS_NX]
    assert (q.dns_is_response, q.dns_qname, q.dns_rcode) == (0, "example.com", 0)
    assert (nx.dns_is_response, nx.dns_qname, nx.dns_rcode) == (1, "nonexistent.example", 3)
    assert q.tcp_flags == -1 and q.dst_port == 53


def test_icmp_ipv6_vlan_and_truncated_l4(pcap_path):
    recs, _ = _by_index(pcap_path)
    assert recs[IDX_ICMP].icmp_type == 8 and recs[IDX_ICMP].src_port == -1

    v6 = recs[IDX_IPV6_MDNS]
    assert (v6.ip_version, v6.ip_proto, v6.dst_ip, v6.dst_port) == (6, 17, "ff02::fb", 5353)
    assert v6.dns_is_response == -1  # mDNS (5353) is not counted as DNS

    vlan = recs[IDX_VLAN_TELNET]
    assert (vlan.dst_ip, vlan.dst_port, vlan.tcp_flags) == ("203.0.113.5", 23, TCP_SYN)
    assert (vlan.src_mac, vlan.dst_mac) == (DEVICE_MAC, ROUTER_MAC)

    cut = recs[IDX_TRUNCATED_TCP]
    assert (cut.ip_proto, cut.src_port, cut.dst_port, cut.tcp_flags) == (6, -1, -1, -1)
    assert cut.ip_len == 40  # from the IP header, despite the snaplen cut


def test_pcap_pcapng_and_gzip_give_identical_records(pcap_path, pcapng_path, pcap_gz_path):
    a = [r.as_tuple() for r in iter_packets(pcap_path)]
    b = [r.as_tuple() for r in iter_packets(pcapng_path)]
    c = [r.as_tuple() for r in iter_packets(pcap_gz_path)]
    assert a == b == c
    assert len(a) == 11


def test_capture_order_preserved_and_out_of_order_counted(tmp_path, frames):
    # Swap timestamps of frames 3 and 4 so one goes backwards; order must not change.
    shuffled = list(frames)
    shuffled[3], shuffled[4] = (frames[4][0], frames[3][1]), (frames[3][0], frames[4][1])
    path = write_pcap(tmp_path / "ooo.pcap", shuffled)
    stats = ParseStats()
    indices = [r.pkt_index for r in iter_packets(path, stats)]
    assert indices == sorted(indices)
    assert stats.out_of_order_ts == 1


def test_raw_ip_linktype(tmp_path):
    ip_bytes = bytes(ipv4_packet(DEVICE_IP, "8.8.8.8", tcp(1234, 80, dpkt.tcp.TH_SYN), 6))
    path = write_pcap(tmp_path / "raw.pcap", [(T0, ip_bytes)], linktype=101)
    (rec,) = list(iter_packets(path))
    assert (rec.src_mac, rec.dst_mac, rec.src_ip, rec.dst_port) == ("", "", DEVICE_IP, 80)


def test_linux_sll_linktype(tmp_path):
    ip_bytes = bytes(ipv4_packet(DEVICE_IP, "8.8.8.8", tcp(1234, 80, dpkt.tcp.TH_SYN), 6))
    # SLL header: packet type 4 (outgoing), ARPHRD_ETHER, addr len 6, addr padded to 8, ethertype
    sll = struct.pack("!HHH", 4, 1, 6) + mac(DEVICE_MAC) + b"\x00\x00" + struct.pack("!H", 0x0800)
    path = write_pcap(tmp_path / "sll.pcap", [(T0, sll + ip_bytes)], linktype=113)
    (rec,) = list(iter_packets(path))
    assert (rec.src_mac, rec.dst_mac, rec.dst_ip) == (DEVICE_MAC, "", "8.8.8.8")


def test_rejects_non_capture_file(tmp_path):
    bogus = tmp_path / "notes.txt"
    bogus.write_text("hello, not a pcap")
    with pytest.raises(ValueError, match="not a pcap"):
        list(iter_packets(bogus))


@pytest.mark.parametrize("raw", ["02:00:00:00:00:01", "02-00-00-00-00-01", "020000000001", "02:00:00:00:00:01".upper()])
def test_normalize_mac(raw):
    assert normalize_mac(raw) == "02:00:00:00:00:01"


def test_normalize_mac_rejects_garbage():
    with pytest.raises(ValueError):
        normalize_mac("02:00:00:00:00")
