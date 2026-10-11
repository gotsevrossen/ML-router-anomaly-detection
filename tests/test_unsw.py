from __future__ import annotations

import numpy as np
import pandas as pd

from rad.eval.unsw import attack_family, load_intervals, window_interval_labels


def test_interval_labels_overlap_name_and_guard():
    starts = np.arange(0, 300, 30, dtype=float)  # 10 windows
    iv = pd.DataFrame({"start": [45.0], "end": [120.0], "attack": ["ArpSpoof10L2D"]})
    frac, name, guard = window_interval_labels(starts, 30.0, iv, guard_after_s=60.0)
    assert np.allclose(frac[:5], [0, 0.5, 1, 1, 0])  # [30,60) half covered; [120,150) only touches the end
    assert list(name[1:4]) == ["ArpSpoof10L2D"] * 3 and name[0] == "" and name[4] == ""
    # Guard covers windows overlapping (120, 180]: [90,120) ends at 120 (not after), [120,150) and [150,180) do.
    assert list(np.flatnonzero(guard)) == [4, 5]


def test_attack_family_strips_rate_and_path():
    assert attack_family("TcpSynReflection100W2D2W") == "TcpSynReflection"
    assert attack_family("ArpSpoof1L2D") == "ArpSpoof"
    assert attack_family("Smurf10L2D2L") == "Smurf"


def test_annotations_with_a_comma_inside_the_flows_field(tmp_path):
    f = tmp_path / "a.csv"
    f.write_text("20,30,Localfeatures|Arpfeatures,ArpSpoof1L2D
"
                 "5,9,localIcmpPortAllIP192.168.1.1,Icmpfeatures|Localfeatures,PingOfDeath1L2D
", encoding="utf-8")
    iv = load_intervals(f)
    assert list(iv.attack) == ["PingOfDeath1L2D", "ArpSpoof1L2D"] and list(iv.start) == [5.0, 20.0]
