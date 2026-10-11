"""Window features on hand-built record streams with known answers."""

from __future__ import annotations

import math
import random
from datetime import datetime, timezone

import pytest

from rad.features.device_filter import is_lan_ip
from rad.features.packet_schema import ARP_REQUEST, TCP_ACK, TCP_FIN, TCP_RST, TCP_SYN, PacketRecord
from rad.features.profile_cache import ProfileCache
from rad.features.window_features import FEATURE_NAMES, CommitPolicy, WindowFeatureExtractor, ip_prefix

DEV_IP = "192.168.1.50"
W = 30.0
# 2024-01-06 is a Saturday; start the stream at 06:00 UTC that day.
T0 = datetime(2024, 1, 6, 6, 0, tzinfo=timezone.utc).timestamp()


def rec(ts: float, direction: str = "out", *, peer: str = "93.184.216.34", ip_len: int = 100,
        proto: int = 6, lport: int = 40000, rport: int = 443, flags: int = -1, idx: int = 0,
        arp_op: int = -1, dns_resp: int = -1, qname: str = "", rcode: int = -1) -> PacketRecord:
    out = direction == "out"
    is_arp = arp_op >= 0
    has_ports = proto in (6, 17) and not is_arp
    return PacketRecord(
        pkt_index=idx, ts=ts, cap_len=ip_len + 14, ip_len=ip_len,
        src_mac="", dst_mac="", ip_version=0 if is_arp else 4,
        src_ip=DEV_IP if out else peer, dst_ip=peer if out else DEV_IP,
        ip_proto=-1 if is_arp else proto,
        src_port=(lport if out else rport) if has_ports else -1,
        dst_port=(rport if out else lport) if has_ports else -1,
        tcp_flags=flags if proto == 6 and not is_arp else -1,
        dns_is_response=dns_resp, dns_qname=qname, dns_rcode=rcode,
        direction=direction, peer_ip=peer, peer_is_lan=is_lan_ip(peer), arp_op=arp_op,
    )


def run(records, profile=None, commit=None, **kwargs):
    ex = WindowFeatureExtractor(profile or ProfileCache(), window_s=W, **kwargs)
    return list(ex.run(records, commit=commit)), ex


def test_feature_names_are_unique_and_in_result_order():
    assert len(FEATURE_NAMES) == len(set(FEATURE_NAMES)) == 34
    (res,), _ = run([rec(T0)])
    assert tuple(res.features) == FEATURE_NAMES


def test_volume_and_shape():
    (res,), _ = run([rec(T0, ip_len=100), rec(T0 + 2, ip_len=300), rec(T0 + 6, "in", ip_len=200)])
    f = res.features
    assert (f["bytes_out"], f["bytes_in"], f["pkts_out"], f["pkts_in"]) == (400, 200, 2, 1)
    assert f["out_byte_frac"] == pytest.approx(400 / 600)
    assert f["pkt_size_mean"] == pytest.approx(200)
    assert f["pkt_size_var"] == pytest.approx((100**2 + 0 + 100**2) / 3)
    assert f["iat_mean"] == pytest.approx(3.0)  # gaps 2 and 4
    assert f["iat_var"] == pytest.approx(1.0)


def test_windows_are_epoch_aligned_and_gaps_emit_empty_windows():
    records = [rec(T0 + 1), rec(T0 + 95)]
    results, ex = run(records)
    assert [r.start - T0 for r in results] == [0, 30, 60, 90]
    assert [r.n_records for r in results] == [1, 0, 0, 1]
    empty = results[1].features
    assert empty["bytes_out"] == 0 and empty["iat_mean"] == 0 and empty["out_byte_frac"] == 0
    assert ex.stats.empty_windows == 2

    results, _ = run(records, emit_empty=False)
    assert [r.start - T0 for r in results] == [0, 90]
    # IAT carries across windows: the second record's gap is to the first one.
    assert results[1].features["iat_mean"] == pytest.approx(94)


def test_late_record_stays_in_open_window():
    results, ex = run([rec(T0 + 1), rec(T0 + 31), rec(T0 + 29), rec(T0 + 32)])
    assert [r.n_records for r in results] == [1, 3]
    assert ex.stats.late_records == 1


def test_destinations_lan_share_and_arp():
    records = [
        rec(T0, peer="8.8.8.8"), rec(T0 + 1, peer="8.8.8.4"), rec(T0 + 2, peer="1.1.1.1"),
        rec(T0 + 3, "in", peer="9.9.9.9"),  # received: not a destination
        rec(T0 + 4, peer="192.168.1.1", ip_len=200),  # LAN peer: not external
        rec(T0 + 5, peer="192.168.1.7", arp_op=ARP_REQUEST, ip_len=28),
        rec(T0 + 6, peer="192.168.1.8", arp_op=ARP_REQUEST, ip_len=28),
        rec(T0 + 7, peer="192.168.1.8", arp_op=ARP_REQUEST, ip_len=28),
    ]
    (res,), _ = run(records)
    f = res.features
    assert f["n_ext_dst_ips"] == 3 and f["n_new_ext_dst_ips"] == 3
    assert f["n_ext_dst_prefixes"] == 2  # 8.8.8.0/24 and 1.1.1.0/24
    assert f["lan_byte_frac"] == pytest.approx((200 + 3 * 28) / (4 * 100 + 200 + 3 * 28))
    assert (f["arp_req_out"], f["n_arp_targets"]) == (3, 2)
    # ARP is not an IP packet: protocol shares are over the 5 IP packets only.
    assert f["tcp_frac"] == pytest.approx(1.0)


def test_ip_prefix():
    assert ip_prefix("203.0.113.77") == "203.0.113.0/24"
    assert ip_prefix("2001:db8:1:2::1") == "2001:0db8:0001::/48"


def test_new_features_only_see_committed_profile():
    records = [rec(T0, peer="8.8.8.8", rport=23), rec(T0 + 30, peer="8.8.8.8", rport=23)]
    never, _ = run(records, commit=CommitPolicy("never"))
    assert [r.features["n_new_ext_dst_ips"] for r in never] == [1, 1]
    always, _ = run(records, commit=CommitPolicy("always"))
    assert [r.features["n_new_ext_dst_ips"] for r in always] == [1, 0]
    assert [r.features["n_new_dst_ports"] for r in always] == [1, 0]


def test_bootstrap_policy_freezes_the_profile():
    records = [rec(T0 + 30 * i, peer=f"8.8.8.{i}") for i in range(4)] + [rec(T0 + 120, peer="8.8.8.3")]
    profile = ProfileCache()
    results, _ = run(records, profile=profile, commit=CommitPolicy("bootstrap", bootstrap_windows=2))
    assert profile.windows_committed == 2
    assert profile.has_ip("8.8.8.1") and not profile.has_ip("8.8.8.2")
    assert results[-1].features["n_new_ext_dst_ips"] == 1  # 8.8.8.3 was never committed


def test_ports_and_top3_share():
    learn = [rec(T0 + i, rport=p) for i, p in enumerate([443] * 5 + [80] * 3 + [53] * 2 + [8080])]
    probe = [rec(T0 + 30, rport=443), rec(T0 + 31, rport=22), rec(T0 + 32, "in", lport=22, rport=50000)]
    results, _ = run(learn + probe, commit=CommitPolicy("always"))
    f = results[1].features
    assert f["n_dst_ports"] == 2 and f["n_new_dst_ports"] == 1  # 22 is new
    # Service ports: 443, 22, 22 (incoming to the device's port 22). Top-3 is {443, 80, 53}.
    assert f["top3_port_frac"] == pytest.approx(1 / 3)


def test_dns():
    records = [
        rec(T0, proto=17, rport=53, peer="192.168.1.1", dns_resp=0, qname="a.example"),
        rec(T0 + 1, proto=17, rport=53, peer="192.168.1.1", dns_resp=0, qname="a.example"),
        rec(T0 + 2, proto=17, rport=53, peer="192.168.1.1", dns_resp=0, qname="b.example"),
        rec(T0 + 3, "in", proto=17, rport=53, peer="192.168.1.1", dns_resp=1, qname="b.example", rcode=3),
        rec(T0 + 4, "in", proto=17, rport=53, peer="192.168.1.1", dns_resp=1, qname="a.example", rcode=0),
    ]
    (res,), _ = run(records)
    f = res.features
    assert (f["dns_queries"], f["n_domains"], f["n_new_domains"], f["nxdomain"]) == (3, 2, 2, 1)
    assert f["udp_frac"] == 1.0


def test_tcp_attempts_failures_and_duration():
    records = [
        # completed connection: SYN out, SYN/ACK in, FIN out after 4 s
        rec(T0, flags=TCP_SYN, lport=1000),
        rec(T0 + 1, "in", flags=TCP_SYN | TCP_ACK, lport=1000),
        rec(T0 + 4, flags=TCP_FIN | TCP_ACK, lport=1000),
        # refused: SYN out, RST in after 1 s
        rec(T0 + 5, peer="203.0.113.9", rport=23, flags=TCP_SYN, lport=1001),
        rec(T0 + 6, "in", peer="203.0.113.9", rport=23, flags=TCP_RST | TCP_ACK, lport=1001),
        # unanswered SYN
        rec(T0 + 7, peer="203.0.113.10", rport=23, flags=TCP_SYN, lport=1002),
    ]
    (res,), _ = run(records)
    f = res.features
    assert f["n_new_conns"] == 3
    assert f["n_failed_tcp"] == (3 - 1) + 1  # two SYNs without SYN/ACK, one RST
    assert f["conn_dur_mean"] == pytest.approx((4 + 1) / 2)


def test_connection_table_is_bounded_and_times_out():
    syns = [rec(T0 + i, flags=TCP_SYN, lport=2000 + i) for i in range(5)]
    _, ex = run(syns + [rec(T0 + 400)], conn_table_size=3, conn_timeout_s=300)
    assert ex.stats.conn_table_full == 2
    assert ex.stats.conn_timeouts == 3
    assert ex._conns == {}


def test_time_of_day_and_weekend():
    (sat,), _ = run([rec(T0)])
    assert sat.features["tod_sin"] == pytest.approx(1.0)  # 06:00
    assert sat.features["tod_cos"] == pytest.approx(0.0, abs=1e-12)
    assert sat.features["is_weekend"] == 1.0
    # +20 h shifts local time to 02:00 Sunday; +44 h to 02:00 Monday.
    (sun,), _ = run([rec(T0)], tz_offset_h=20)
    (mon,), _ = run([rec(T0)], tz_offset_h=44)
    assert sun.features["is_weekend"] == 1.0 and mon.features["is_weekend"] == 0.0
    assert mon.features["tod_sin"] == pytest.approx(math.sin(2 * math.pi * 2 / 24))


def test_window_set_cap_saturates_counts():
    records = [rec(T0 + i * 0.1, peer=f"8.8.{i}.1") for i in range(10)]
    (res,), ex = run(records, window_set_cap=4)
    assert res.features["n_ext_dst_ips"] == 4
    assert ex.stats.saturated_windows == 1


def test_future_records_do_not_change_past_windows():
    """Streaming rule (CLAUDE.md §7): shuffling or replacing later traffic leaves earlier windows alone."""
    def stream(seed: int) -> list[PacketRecord]:
        r = random.Random(seed)
        out = []
        for i in range(400):
            ts = T0 + i * 0.5
            if ts >= T0 + 90:  # everything after the first three windows depends on the seed
                peer = f"{r.randint(1, 223)}.{r.randint(0, 255)}.0.1"
                flags = r.choice([TCP_SYN, TCP_ACK, TCP_FIN | TCP_ACK, TCP_RST])
                direction = r.choice(["out", "in"])
            else:
                peer, flags, direction = f"8.8.{i % 7}.8", TCP_SYN if i % 3 == 0 else TCP_FIN, "out"
            out.append(rec(ts, direction, peer=peer, flags=flags, lport=3000 + i % 11, idx=i))
        return out

    a, _ = run(stream(1), commit=CommitPolicy("always"))
    b, _ = run(stream(2), commit=CommitPolicy("always"))
    assert a[:3] == b[:3]
    assert a[3:] != b[3:]


def test_inbound_peers_new_peers_and_ports():
    """D31: senders of received packets, how many the profile has never seen, and local ports hit."""
    learn = [rec(T0 + 1, "in", peer="203.0.113.1", lport=80), rec(T0 + 2, "in", peer="192.168.1.9", lport=80)]
    flood = [rec(T0 + 30 + i * 0.1, "in", peer=f"198.51.100.{i}", proto=17, lport=1000 + i % 3) for i in range(20)]
    flood += [rec(T0 + 40, "in", peer="203.0.113.1", lport=80), rec(T0 + 41, "out", peer="203.0.113.1")]
    results, _ = run(learn + flood, commit=CommitPolicy("bootstrap", bootstrap_windows=1))
    f0, f1 = results[0].features, results[1].features
    assert (f0["n_in_peers"], f0["n_new_in_peers"], f0["n_in_ports"]) == (2, 2, 1)  # nothing committed yet
    assert f1["n_in_peers"] == 21 and f1["n_new_in_peers"] == 20  # 203.0.113.1 was committed in window 0
    assert f1["n_in_ports"] == 4  # 1000, 1001, 1002 and 80; outgoing packets do not count
