from __future__ import annotations

import pytest

from conftest import (
    DEVICE_INDICES,
    DEVICE_IP,
    DEVICE_MAC,
    IDX_DNS_NX,
    IDX_ARP,
    IDX_DNS_Q,
    IDX_IPV6_MDNS,
    IDX_SYN,
    IDX_SYNACK,
    IDX_VLAN_TELNET,
    OTHER_MAC,
    ROUTER_IP,
    ROUTER_MAC,
)
from rad.features.device_filter import DeviceFilter, is_lan_ip, list_devices
from rad.features.pcap_reader import iter_packets


def _device_records(path, **kwargs):
    return {r.pkt_index: r for r in DeviceFilter(**kwargs).filter(iter_packets(path))}


def test_keeps_only_target_device_packets(pcap_path):
    recs = _device_records(pcap_path, target_mac=DEVICE_MAC)
    assert sorted(recs) == DEVICE_INDICES


def test_target_mac_accepts_any_format(pcap_path):
    recs = _device_records(pcap_path, target_mac=DEVICE_MAC.upper().replace(":", "-"))
    assert sorted(recs) == DEVICE_INDICES


def test_direction_and_peer(pcap_path):
    recs = _device_records(pcap_path, target_mac=DEVICE_MAC)
    assert (recs[IDX_SYN].direction, recs[IDX_SYN].peer_ip, recs[IDX_SYN].peer_is_lan) == ("out", "93.184.216.34", False)
    assert (recs[IDX_SYNACK].direction, recs[IDX_SYNACK].peer_ip) == ("in", "93.184.216.34")
    assert (recs[IDX_DNS_Q].direction, recs[IDX_DNS_Q].peer_ip, recs[IDX_DNS_Q].peer_is_lan) == ("out", ROUTER_IP, True)
    assert (recs[IDX_DNS_NX].direction, recs[IDX_DNS_NX].peer_ip) == ("in", ROUTER_IP)
    assert (recs[IDX_IPV6_MDNS].direction, recs[IDX_IPV6_MDNS].peer_is_lan) == ("out", True)
    assert (recs[IDX_VLAN_TELNET].direction, recs[IDX_VLAN_TELNET].peer_ip) == ("out", "203.0.113.5")
    # ARP to the broadcast MAC: the peer is the IP being asked about.
    assert (recs[IDX_ARP].direction, recs[IDX_ARP].peer_ip, recs[IDX_ARP].peer_is_lan) == ("out", ROUTER_IP, True)


def test_target_ip_fallback(pcap_path):
    recs = _device_records(pcap_path, target_mac=None, target_ip=DEVICE_IP)
    # IPv4 only: the IPv6 mDNS frame uses a different address and is not matched.
    assert sorted(recs) == [i for i in DEVICE_INDICES if i != IDX_IPV6_MDNS]
    assert recs[IDX_SYNACK].direction == "in"


def test_requires_a_target():
    with pytest.raises(ValueError):
        DeviceFilter(target_mac=None, target_ip=None)


@pytest.mark.parametrize(
    "ip,expected",
    [
        ("192.168.1.1", True), ("10.1.2.3", True), ("172.16.0.1", True), ("172.32.0.1", False),
        ("169.254.1.1", True), ("239.255.255.250", True), ("255.255.255.255", True),
        ("8.8.8.8", False), ("100.64.0.1", False),
        ("fe80::1", True), ("fd00::1", True), ("ff02::fb", True), ("2001:4860::8888", False),
        ("not-an-ip", False),
    ],
)
def test_is_lan_ip(ip, expected):
    assert is_lan_ip(ip) is expected


def test_list_devices_counts(pcap_path):
    devices = {d.mac: d for d in list_devices(pcap_path)}
    # Broadcast / multicast MACs are never listed.
    assert set(devices) == {DEVICE_MAC, ROUTER_MAC, OTHER_MAC}
    dev = devices[DEVICE_MAC]
    assert (dev.packets_sent, dev.packets_received) == (8, 2)  # sends 0,2,3,5,6,7,8,12; receives 1,4
    assert DEVICE_IP in dev.ips
    other = devices[OTHER_MAC]
    assert (other.packets_sent, other.packets_received) == (2, 0)
    router = devices[ROUTER_MAC]
    assert (router.packets_sent, router.packets_received) == (2, 7)
