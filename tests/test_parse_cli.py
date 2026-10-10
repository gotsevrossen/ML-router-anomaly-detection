from __future__ import annotations

import json

import dpkt
import pandas as pd
import pytest
import yaml

from conftest import DEVICE_INDICES, DEVICE_IP, DEVICE_MAC, ROUTER_MAC, T0, DT, eth, ipv4_packet, tcp, write_pcap
from rad.features.packet_schema import COLUMNS
from rad.features.parse import main, parse_capture


def _cfg(tmp_path, input_path, **overrides):
    cfg = {
        "input": str(input_path),
        "device_name": "testdev",
        "target_mac": DEVICE_MAC,
        "out_dir": str(tmp_path / "interim"),
    }
    cfg.update(overrides)
    return cfg


def test_end_to_end_parquet_and_meta(tmp_path, pcap_path):
    meta = parse_capture(_cfg(tmp_path, pcap_path))
    df = pd.read_parquet(tmp_path / "interim" / "testdev.parquet")
    assert tuple(df.columns) == COLUMNS
    assert df["pkt_index"].tolist() == DEVICE_INDICES
    assert set(df["direction"]) == {"in", "out"}

    with open(tmp_path / "interim" / "testdev.meta.json", encoding="utf-8") as fh:
        on_disk = json.load(fh)
    assert on_disk["rows_kept"] == meta["rows_kept"] == len(DEVICE_INDICES)
    assert on_disk["stats"]["frames_total"] == 13
    assert on_disk["config"]["target_mac"] == DEVICE_MAC
    assert on_disk["first_ts"] == T0
    assert "git_commit" in on_disk["run"]


def test_chunk_size_does_not_change_output(tmp_path, pcap_path):
    parse_capture(_cfg(tmp_path, pcap_path, device_name="big", chunk_size=100_000))
    parse_capture(_cfg(tmp_path, pcap_path, device_name="small", chunk_size=2))
    big = pd.read_parquet(tmp_path / "interim" / "big.parquet")
    small = pd.read_parquet(tmp_path / "interim" / "small.parquet")
    pd.testing.assert_frame_equal(big, small)


def test_prefix_is_independent_of_future_frames(tmp_path, frames):
    """Streaming rule: rows for frames < k must not depend on anything after k."""
    k = 6
    future = [
        (T0 + (k + i) * DT, eth(DEVICE_MAC, ROUTER_MAC, ipv4_packet(DEVICE_IP, f"198.51.100.{i}", tcp(1000 + i, 23, dpkt.tcp.TH_SYN), 6)))
        for i in range(20)
    ]
    original = write_pcap(tmp_path / "a.pcap", frames)
    altered = write_pcap(tmp_path / "b.pcap", frames[:k] + future)

    parse_capture(_cfg(tmp_path, original, device_name="full"))
    parse_capture(_cfg(tmp_path, altered, device_name="altered"))
    parse_capture(_cfg(tmp_path, original, device_name="prefix", max_packets=k))

    full = pd.read_parquet(tmp_path / "interim" / "full.parquet")
    alt = pd.read_parquet(tmp_path / "interim" / "altered.parquet")
    prefix = pd.read_parquet(tmp_path / "interim" / "prefix.parquet")

    expected = full[full["pkt_index"] < k].reset_index(drop=True)
    pd.testing.assert_frame_equal(prefix, expected)
    pd.testing.assert_frame_equal(alt[alt["pkt_index"] < k].reset_index(drop=True), expected)


def test_no_match_writes_empty_table(tmp_path, pcap_path):
    meta = parse_capture(_cfg(tmp_path, pcap_path, target_mac="02:aa:aa:aa:aa:aa"))
    assert meta["rows_kept"] == 0
    df = pd.read_parquet(tmp_path / "interim" / "testdev.parquet")
    assert len(df) == 0 and tuple(df.columns) == COLUMNS


def test_config_validation(tmp_path, pcap_path):
    with pytest.raises(ValueError, match="target_mac"):
        parse_capture(_cfg(tmp_path, pcap_path, target_mac=None))
    with pytest.raises(ValueError, match="device_name"):
        parse_capture(_cfg(tmp_path, pcap_path, device_name=""))


def test_cli_config_and_list_devices(tmp_path, pcap_path, capsys):
    cfg_path = tmp_path / "parse.yaml"
    cfg_path.write_text(yaml.safe_dump(_cfg(tmp_path, pcap_path)))
    assert main(["--config", str(cfg_path), "--log-level", "WARNING"]) == 0
    assert (tmp_path / "interim" / "testdev.parquet").exists()

    assert main(["--list-devices", str(pcap_path)]) == 0
    out = capsys.readouterr().out
    assert "13 frames, 11 IP packets" in out
    assert DEVICE_MAC in out and DEVICE_IP in out
