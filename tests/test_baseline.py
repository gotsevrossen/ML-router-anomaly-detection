"""End-to-end baseline run on a synthetic device: quiet benign traffic, then an ARP/telnet scan."""

from __future__ import annotations

import gzip
import json

import pandas as pd
import pyarrow.parquet as pq
import pytest

from rad.eval.baseline import main, run_baseline, select_features, split_labels
from rad.eval.labels import load_frame_labels
from rad.features.extract import extract_windows
from rad.features.packet_schema import ARP_REQUEST, TCP_ACK, TCP_SYN, ARROW_SCHEMA, PacketRecord, records_to_table

W = 30.0
T0 = 1_700_000_010.0  # a multiple of 30 s, so window k starts at T0 + 30 k
N_WINDOWS, ATTACK_FROM = 160, 130
DEV, ROUTER = "02:00:00:00:00:01", "02:00:00:00:00:fe"


def _device_stream() -> tuple[list[PacketRecord], list[int]]:
    """Records of one device plus per-frame labels (frames == records here)."""
    recs, labels = [], []

    def add(ts, label, **kw):
        base = dict(pkt_index=len(recs), ts=ts, cap_len=80, ip_len=66, src_mac=DEV, dst_mac=ROUTER, ip_version=4,
                    src_ip="192.168.1.50", dst_ip="93.184.216.34", ip_proto=6, src_port=40000, dst_port=443,
                    tcp_flags=TCP_ACK, direction="out", peer_ip="93.184.216.34")
        base.update(kw)
        recs.append(PacketRecord(**base))
        labels.append(label)

    for k in range(N_WINDOWS):
        t = T0 + k * W
        attack = int(k >= ATTACK_FROM)
        for j in range(4):  # steady benign heartbeat, with small variation
            add(t + 1 + j * 5 + (k % 3), attack, ip_len=60 + (k + j) % 7)
        if attack:
            for j in range(40):  # ARP sweep and telnet SYNs to new LAN hosts
                add(t + 2 + j * 0.5, 1, ip_version=0, ip_proto=-1, src_port=-1, dst_port=-1, tcp_flags=-1,
                    dst_ip=f"192.168.1.{j + 100}", peer_ip=f"192.168.1.{j + 100}", peer_is_lan=True,
                    dst_mac="ff:ff:ff:ff:ff:ff", ip_len=28, arp_op=ARP_REQUEST)
                add(t + 2.2 + j * 0.5, 1, dst_ip=f"192.168.1.{j + 100}", peer_ip=f"192.168.1.{j + 100}",
                    peer_is_lan=True, dst_port=23, src_port=50000 + j, tcp_flags=TCP_SYN)
    return recs, labels


@pytest.fixture
def baseline_inputs(tmp_path):
    recs, labels = _device_stream()
    packets = tmp_path / "dev.parquet"
    pq.write_table(records_to_table(recs), packets)
    labels_path = tmp_path / "labels.csv.gz"
    with gzip.open(labels_path, "wt") as fh:
        fh.write("\n".join(map(str, labels)))
    extract_windows({"input": str(packets), "name": "dev_w30", "out_dir": str(tmp_path / "processed"),
                     "profile": {"bootstrap_windows": 60}})
    return {
        "experiment": "toy",
        "out_dir": str(tmp_path / "results"),
        "windows": str(tmp_path / "processed" / "dev_w30.parquet"),
        "packets": str(packets),
        "labels": str(labels_path),
        "features": {"exclude": ["tod_sin", "tod_cos", "is_weekend"]},
        "split": {"bootstrap_windows": 60, "validation_windows": 40},
        "detectors": {
            "hst": {"n_trees": 10, "height": 6, "window_size": 50, "seed": 0},
            "iforest": {"n_estimators": 50, "seed": 0},
            "autoencoder": {"bootstrap_steps": 300, "seed": 0},
            "mad": {},
            "kitsune": {"max_autoencoder_size": 5},
        },
    }


def test_end_to_end_table_and_outputs(baseline_inputs, tmp_path):
    res = run_baseline(baseline_inputs)
    assert res["counts"] == {"windows": 160, "bootstrap": 60, "validation": 40, "test_benign": 30, "test_attack": 30}
    table = res["table"].set_index("detector")
    assert list(table.index) == ["hst", "iforest", "autoencoder", "mad", "kitsune"]
    # The scan is blatant: every detector separates it and catches it immediately.
    assert (table["pauc@0.1"] > 0.9).all()
    assert (table["time_to_detect_s"] == 0).all()

    out = tmp_path / "results" / "toy"
    for name in ("summary_baseline.csv", "summary_baseline.md", "scores.csv", "scores.png", "config.yaml", "meta.json"):
        assert (out / name).exists(), name
    scores = pd.read_csv(out / "scores.csv")
    assert scores["label"].sum() == 30 and set(scores["split"]) == {"bootstrap", "validation", "test"}
    meta = json.loads((out / "meta.json").read_text(encoding="utf-8"))
    assert "is_weekend" not in meta["features"] and "git_commit" in meta["run"]

    # A second run reuses the cached Kitsune scores and gives the same table.
    assert len(list((out / "cache").glob("kitsune_*.npy"))) == 1
    again = run_baseline(baseline_inputs)["table"].set_index("detector")
    pd.testing.assert_frame_equal(again.drop(columns=["fit_s", "score_ms_per_window"]),
                                  table.drop(columns=["fit_s", "score_ms_per_window"]))


def test_cli_matches_function(baseline_inputs, tmp_path):
    import yaml

    cfg = {**baseline_inputs, "experiment": "toy_cli", "detectors": {"mad": {}}}
    path = tmp_path / "b.yaml"
    path.write_text(yaml.safe_dump(cfg))
    assert main(["--config", str(path), "--log-level", "WARNING"]) == 0
    assert (tmp_path / "results" / "toy_cli" / "summary_baseline.csv").exists()


def test_select_features_and_split():
    assert select_features(["a", "b", "c"], None, ["b"]) == ["a", "c"]
    assert select_features(["a", "b", "c"], ["c", "a"], []) == ["c", "a"]
    with pytest.raises(ValueError):
        select_features(["a"], None, ["zzz"])
    assert list(split_labels(5, 2, 1)) == ["bootstrap", "bootstrap", "validation", "test", "test"]
    with pytest.raises(ValueError):
        split_labels(3, 2, 1)


def test_label_loader_accepts_headered_files(tmp_path):
    p = tmp_path / "l.csv"
    p.write_text(",x\n0,0\n1,1\n2,1\n")
    assert load_frame_labels(p).tolist() == [0, 1, 1]
