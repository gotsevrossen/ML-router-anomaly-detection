from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from rad.attacks.boiling_frog import SECONDS_PER_DAY, FrogConfig, build_stream

T0 = 1_527_400_800.0  # 2018-05-27 06:00 UTC = 16:00 Sydney (UTC+10)


def _benign(days=4):
    rows = []
    for d in range(days):
        for i in range(48):  # one packet every 30 min, alternating direction
            out = i % 2 == 0
            rows.append({"pkt_index": 0, "ts": T0 + d * SECONDS_PER_DAY + i * 1800.0, "cap_len": 114, "ip_len": 100,
                         "src_mac": "aa:aa:aa:aa:aa:01" if out else "bb:bb:bb:bb:bb:01",
                         "dst_mac": "bb:bb:bb:bb:bb:01" if out else "aa:aa:aa:aa:aa:01", "ip_version": 4,
                         "src_ip": "192.168.1.5" if out else "8.8.8.8", "dst_ip": "8.8.8.8" if out else "192.168.1.5",
                         "ip_proto": 17, "src_port": 5000, "dst_port": 53, "tcp_flags": -1, "icmp_type": -1,
                         "dns_is_response": -1, "dns_qname": "", "dns_rcode": -1,
                         "direction": "out" if out else "in", "peer_ip": "8.8.8.8", "peer_is_lan": False, "arp_op": -1})
    return pd.DataFrame(rows)


@pytest.mark.parametrize("kind", ["volumetric", "behavioral"])
def test_stream_layout_growth_and_labels(kind):
    cfg = FrogConfig(kind=kind, final_rate=1.0, alpha=0.5, n_days=3, burst_s=60.0)
    rec, sched = build_stream(_benign(), cfg, day_offset_h=10)
    assert not rec.isna().any().any()
    assert (np.diff(rec["ts"].to_numpy()) >= 0).all()
    rates = sched.groupby("day").rate.first().to_numpy()
    assert np.allclose(rates, [1.5 ** -3, 1.5 ** -2, 1.5 ** -1, 1.0])  # geometric, reaching R on the attack day
    assert list(sched.phase.unique()) == ["chaff", "attack"] and len(sched) == 4 * 24
    injected = rec[rec["src_port"] == 40_000]
    assert len(injected) == sum(max(1, round(r * 60)) * 24 for r in rates)
    # The injection starts after the 3 original local calendar days (2 bootstrap + 1 validation).
    first_midnight = np.floor((T0 + 36_000) / SECONDS_PER_DAY) * SECONDS_PER_DAY - 36_000
    assert injected["ts"].min() >= first_midnight + 3 * SECONDS_PER_DAY
    if kind == "behavioral":
        assert injected["peer_ip"].is_unique  # every scanned address is new
