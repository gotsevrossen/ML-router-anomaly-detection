from __future__ import annotations

import numpy as np

from conftest import DEVICE_MAC, OTHER_MAC, ROUTER_MAC
from rad.eval.kitsune_suite import mac_attack_counts


def test_device_choice_counts_attack_frames_per_unicast_mac(pcap_path):
    labels = np.zeros(13, dtype=np.int8)
    labels[[0, 1, 2, 3]] = 1  # frames 0-3 involve the device and the router
    labels[10] = 1  # another device's frame to the router
    counts = mac_attack_counts(pcap_path, labels)
    assert "ff:ff:ff:ff:ff:ff" not in counts.index  # group MACs are never candidates
    assert counts.loc[ROUTER_MAC, "attack_frames"] == 5
    assert counts.loc[DEVICE_MAC, "attack_frames"] == 4
    assert counts.loc[OTHER_MAC, "attack_frames"] == 1
    assert counts.index[0] == ROUTER_MAC  # sorted by attack frames, then frames
