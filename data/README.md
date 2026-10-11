# Data

Raw data never goes in git. Everything under `raw/`, `interim/` and `processed/` is ignored by `.gitignore`.

| Folder | Contents | Produced by |
|---|---|---|
| `raw/` | Downloaded pcaps / CSVs, untouched | you |
| `interim/` | Per-device packet tables (`<device>.parquet` + `<device>.meta.json`) | `python -m rad.features.parse` (Phase 1a) |
| `processed/` | 30 s windowed feature matrices (`<name>.parquet` + `<name>.meta.json`) | `python -m rad.features.extract` (Phase 1b) |

## 1. Kitsune Network Attack Dataset (primary real-pcap source)

- UCI ML Repository: https://archive.ics.uci.edu/dataset/516/kitsune+network+attack+dataset. It is also mirrored on Kaggle; search "Kitsune Network Attack Dataset".
- It has 9 attack captures (Mirai, SYN DoS, SSDP flood, OS scan, fuzzing, ARP MitM, and others). Each comes as a raw capture plus a per-packet labels CSV.
- Put the capture file in `data/raw/` as-is. `.pcap`, `.pcapng` and gzipped versions all work, so you don't need to decompress.
- **Labels are for evaluation only.** The parser writes `pkt_index` (the 0-based frame index in the capture), so labels can be joined later by row number. Labels are never a model input.
- Start with the **Mirai** capture. It is an IoT network, which fits our single-device scope best.

## 2. N-BaIoT

- UCI ML Repository: https://archive.ics.uci.edu/dataset/442/detection+of+iot+botnet+attacks+n+baiot (also on Kaggle).
- **Confirmed CSV-only (2026-10-10):** the public release ships *pre-extracted CSV features* (115 Kitsune-style features per device), **not raw pcaps**.
  - Those features don't match the 25 window features we compute on the router, so N-BaIoT is a secondary benchmark only (loader planned for Phase 1c).
  - Layout: `raw/detection+of+iot+botnet+attacks+n+baiot/<Device>/benign_traffic.csv`, plus `gafgyt_attacks.rar` and `mirai_attacks.rar`. Extract the `.rar` files with 7-Zip before use.
  - Ennio_Doorbell and Samsung_SNH_1011_N_Webcam have no Mirai capture. That is how the dataset was published; nothing is missing.

## 3. Own testbed (later)

Run `tcpdump -i <iface> -w capture.pcap ether host <DEVICE_MAC>` on the OpenWrt router, or on a mirror port. Captures taken on the router's `any` interface use Linux SLL framing; the parser supports that too.

## Typical workflow

```bash
# Which MACs are in this capture, and how much traffic does each have?
python -m rad.features.parse --list-devices data/raw/Mirai_pcap.pcap

# Copy the device's MAC into configs/parse_kitsune_mirai.yaml, then:
python -m rad.features.parse --config configs/parse_kitsune_mirai.yaml
# -> data/interim/kitsune_mirai_device.parquet
# -> data/interim/kitsune_mirai_device.meta.json (config, git commit, counters)
```

Check `stats` in the meta.json after every parse. Large `skipped_malformed` or `l4_undecoded` counts mean the capture was truncated, often by a small snaplen.
