from __future__ import annotations

import json

import pandas as pd
import yaml

from conftest import DEVICE_MAC
from rad.features.extract import WINDOW_SCHEMA, extract_windows, main
from rad.features.parse import parse_capture
from rad.features.window_features import FEATURE_NAMES


def _interim(tmp_path, pcap_path):
    parse_capture({"input": str(pcap_path), "device_name": "dev", "target_mac": DEVICE_MAC,
                   "out_dir": str(tmp_path / "interim")})
    return tmp_path / "interim" / "dev.parquet"


def test_end_to_end_from_pcap(tmp_path, pcap_path):
    cfg = {"input": str(_interim(tmp_path, pcap_path)), "name": "dev_w30", "out_dir": str(tmp_path / "processed")}
    meta = extract_windows(cfg)
    df = pd.read_parquet(tmp_path / "processed" / "dev_w30.parquet")
    assert tuple(df.columns) == tuple(WINDOW_SCHEMA.names)
    assert tuple(df.columns[5:]) == FEATURE_NAMES
    # The 13-frame stream spans 3 s, so it is one window holding all 10 device records.
    assert len(df) == meta["n_windows"] == 1
    row = df.iloc[0]
    assert row["n_records"] == 10
    assert (row["dns_queries"], row["nxdomain"], row["arp_req_out"]) == (1, 1, 1)

    with open(tmp_path / "processed" / "dev_w30.meta.json", encoding="utf-8") as fh:
        on_disk = json.load(fh)
    assert on_disk["feature_names"] == list(FEATURE_NAMES)
    assert on_disk["config"]["profile"]["update"] == "bootstrap"
    assert on_disk["profile_stats"]["windows_committed"] == 1
    assert "git_commit" in on_disk["run"]


def test_cli(tmp_path, pcap_path):
    cfg_path = tmp_path / "features.yaml"
    cfg_path.write_text(yaml.safe_dump({
        "input": str(_interim(tmp_path, pcap_path)), "name": "cli", "out_dir": str(tmp_path / "processed"),
        "profile": {"update": "never"},
    }))
    assert main(["--config", str(cfg_path), "--log-level", "WARNING"]) == 0
    with open(tmp_path / "processed" / "cli.meta.json", encoding="utf-8") as fh:
        meta = json.load(fh)
    assert meta["profile_stats"]["windows_committed"] == 0
    assert meta["config"]["profile"]["bootstrap_windows"] == 120  # defaults filled in
