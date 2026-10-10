# Poisoning-Resistant Continual Anomaly Detection on a Consumer Router

Undergraduate research project (Purdue, advisor: Prof. Esmaeili). The authoritative build spec is [CLAUDE.md](CLAUDE.md). This README explains the model in plain terms, says how to run what exists so far, and **logs every implementation step and every deviation from the plan**.

**Status:** Phase 1a (pcap parsing) is done. Phase 1b (window features) is next.

---

## 1. The model in one page

**Goal.** A small program on a home router watches **one device's** traffic, such as a smart camera. It learns what "normal" looks like for that device, flags behavior that deviates from it, and keeps learning over time **without letting an attacker slowly teach it that an attack is normal** (the "boiling-frog" poisoning attack).

**Pipeline**

```
packets for one MAC ──► 30 s windows ──► ~25 features ──► anomaly detector ──► score
       (Phase 1a)          (1b)              (1b)          (1c: HST + baselines)
                                                                    │
                     gated update rule (Phase 2, the novelty) ◄─────┘
                     ├─ quarantine buffer: learn a window only after 24 h with no alert
                     ├─ drift budget + anchor model: cap how fast "normal" may move per day
                     └─ disambiguation: volume shift → "benign drift", diversity shift → "attack"
                                                                    │
                     output per window: score, state, alert, top-3 reasons, update decision
```

- **Inputs:** header and flow metadata only, never payloads, so it works on encrypted traffic. Features cover volume, packet sizes and timing, destinations (including never-seen-before IPs), ports, DNS, failed connections, and time of day.
- **Primary detector:** **Half-Space Trees (HST).** It is unsupervised (needs no attack labels), streaming (learns one window at a time), uses constant memory, and works by counting, which suits a router CPU and a later C port.
- **Baselines** (to prove the novelty actually helps): Kitsune/KitNET, Isolation Forest, a small 25→8→25 autoencoder, and a robust-statistics (MAD) detector. The MAD detector matters because simple baselines sometimes win (Arp et al. 2022).
- **The novelty is the update rule, not the detector:**
  1. **Quarantine buffer:** a window is scored *before* learning. Only low-scoring windows are queued, and they are committed only after a delay with no alert. When an alert fires, the windows just before it are purged.
  2. **Drift budget + anchor model:** a slow "anchor" copy of the profile is kept. If the fast model drifts from the anchor faster than a daily budget allows, learning stops and a "possible slow poisoning or major change" notice is raised.
  3. **Drift-vs-attack disambiguation:** benign changes (firmware updates) mostly shift *volume*. Attacks raise *diversity* (new IPs, new ports, failed connections). This is a hypothesis we test, not a guarantee.
- **Research questions:**
  - RQ1: how small and cheap can it be on a real router?
  - RQ2: does gated updating keep false alarms low through benign drift?
  - RQ3: how much harder does poisoning become?
  - RQ4: how well does the three-state output separate drift from attacks?
- **Metrics:** TPR at a fixed low FPR, partial AUC, false alarms per day, and chaff needed for 50% false negatives. **Never accuracy.**

**Phases:**
1. Python data pipeline and baselines.
2. Continual-learning core.
3. Attack and drift simulation, plus ablations.
4. C port, OpenWrt package, on-router benchmarks.

---

## 2. Setup

The project uses [uv](https://docs.astral.sh/uv/) and a Python 3.12 virtual environment (see Deviation 2).

```bash
uv python install 3.12
uv venv --python 3.12
uv pip install -e ".[dev]"          # Phase 1a deps + pytest
# later (Phase 1c): uv pip install -e ".[dev,models]"   # river, scikit-learn, torch, matplotlib
```

Run things with `uv run ...`, or activate the venv first (`.venv\Scripts\activate` on Windows).

## 3. Usage (what works today)

```bash
uv run pytest                                                     # 40 tests
uv run python -m rad.features.parse --list-devices data/raw/<capture>   # which MACs, how much traffic
uv run python -m rad.features.parse --config configs/parse_kitsune_mirai.yaml
```

Output: `data/interim/<device>.parquet` holds one row per packet of the target device, in capture order. Columns are documented in [packet_schema.py](src/rad/features/packet_schema.py). Next to it, `<device>.meta.json` records the config, git commit, package versions, and counters for every skipped frame. Data download steps are in [data/README.md](data/README.md).

Speed: about 13k frames/s on this laptop, so the roughly 760k-packet Kitsune Mirai capture takes about a minute.

## 4. Code map (Phase 1a)

| File | What it does |
|---|---|
| [src/rad/features/pcap_reader.py](src/rad/features/pcap_reader.py) | Streaming reader for pcap, pcapng and `.gz` (detected from magic bytes). Header-only decode: Ethernet, 802.1Q, Linux SLL/SLL2, raw IP, IPv4/IPv6, TCP/UDP/ICMP, and the DNS qname and rcode. Bad frames are counted, never fatal. |
| [src/rad/features/device_filter.py](src/rad/features/device_filter.py) | Keeps one device's packets by MAC (with an optional IP fallback) and sets direction, peer IP and the LAN-peer flag. `list_devices()` summarises the MACs in a capture. |
| [src/rad/features/packet_schema.py](src/rad/features/packet_schema.py) | `PacketRecord` plus the fixed Arrow schema. Column order is a contract for Phase 1b and the C port. |
| [src/rad/features/parse.py](src/rad/features/parse.py) | CLI: streams into chunked parquet and writes meta.json. |
| [src/rad/utils/](src/rad/utils/) | YAML config load/save, logging setup, seeding, run metadata (git hash, versions). |
| [tests/](tests/) | Synthetic captures built in-test with known answers, including a check that past rows never depend on future frames. |
| [docs/decisions.md](docs/decisions.md) | Design decisions that affect results or the C port. |

---

## 5. Implementation log

### 2026-10-09: Phase 1a (parsing)

1. Checked the environment: the workspace was empty, conda was not installed, system Python was 3.14, and uv 0.12 was available.
2. `git init` on branch `main`. Created the CLAUDE.md §3 directory layout (`src/rad/{features,models,continual,pipeline,attacks,eval,utils}`, `configs/`, `data/{raw,interim,processed}`, `tests/`, `results/`, `docs/`, `c/`). Added a `.gitignore` that keeps data and results out of git.
3. Installed Python 3.12 with uv, created `.venv`, and wrote `pyproject.toml` (src layout, `dev` and `models` extras).
4. Wrote `utils/`: config, logging, seed, and run metadata.
5. Defined the per-packet schema (20 columns, fixed order).
6. Wrote the streaming pcap/pcapng reader and the header-only decoder, with counters for every skip reason.
7. Wrote the device filter (direction, peer, LAN flag) and the `list_devices` helper.
8. Wrote the `python -m rad.features.parse` CLI: chunked parquet output with bounded memory, plus meta.json.
9. Wrote 40 pytest tests on synthetic captures. They cover every decode path, pcap = pcapng = gzip equivalence, order preservation, out-of-order counting, raw-IP and SLL link types, the device filter, LAN ranges, MAC formats, and end-to-end CLI output. One test checks that rows for frames before *k* are identical no matter what comes after *k* (the streaming rule). All pass.
10. Benchmarked a 260k-frame synthetic capture at about 20 s end to end.
11. Wrote this README, [data/README.md](data/README.md) and [docs/decisions.md](docs/decisions.md).

---

## 6. Deviations from the plan (CLAUDE.md / proposal)

| # | Plan said | What was done | Why |
|---|---|---|---|
| 1 | Repo root is a `router-anomaly/` folder | Repo root is this workspace folder | The workspace was empty and dedicated to this project, so an extra nesting level added nothing. Layout inside is unchanged. |
| 2 | conda env `router-anomaly`, Python 3.10+ | uv-managed `.venv` with Python 3.12 | conda is not installed and uv is. System Python 3.14 is too new for reliable `river`/`torch` wheels, and 3.12 is well supported. `requires-python` is `>=3.10,<3.13`. |
| 3 | Install everything up front (incl. scapy) | Only Phase 1a deps installed; `river`, `scikit-learn`, `torch` and `matplotlib` declared as a `models` extra; scapy dropped | Keeps the environment small until it's needed. dpkt does all parsing (and is faster); test pcaps are also built with dpkt. |
| 4 | N-BaIoT pcaps as a primary parse source | Kitsune dataset pcaps are the primary real-pcap source; an N-BaIoT CSV loader is deferred to 1c | The public N-BaIoT release is pre-extracted CSVs, not pcaps (confirmed on download, 2026-10-10). See data/README.md. |
| 5 | Per-packet table (columns unspecified) | Added `pkt_index`, `cap_len` *and* `ip_len`, `icmp_type`, DNS `qname`/`rcode`/`is_response` | `pkt_index` lets dataset labels join for evaluation only. `ip_len` survives snaplen truncation (D4). `icmp_type` will help detect failed connections (ICMP unreachable). DNS fields feed the DNS feature group (D1). |
| 6 | Filter by MAC | MAC filter plus an optional `target_ip` fallback; Linux SLL/SLL2 and raw-IP link types supported | Captures taken on a router (`tcpdump -i any`) or upstream of a device often lack a usable destination MAC. |
| 7 | `utils/logging.py` implied by "use logging" | Named `utils/log.py` | Avoids confusion with the standard-library `logging` module. |
| 8 | Folders for later phases | Created with placeholder `__init__.py` only, no code | CLAUDE.md: "begin with Phase 1a and do not jump ahead." |

---

## 7. Next steps

- **You:** download the Kitsune Mirai capture into `data/raw/`, run `--list-devices`, put the device MAC in `configs/parse_kitsune_mirai.yaml`, parse it, and check `stats` in the meta.json.
- **Phase 1b:** streaming 30 s window feature extractor (~25 features) with a bounded profile cache for the "new IP / port / domain" features. The cache must later go through the same quarantine as the model.
- **Phase 1c:** the five detectors behind a common `Detector` interface, plus a one-command baseline table (TPR@FPR=1e-3, partial AUC, false alarms per day).
