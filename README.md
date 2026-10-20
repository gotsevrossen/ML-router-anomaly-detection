# Poisoning-Resistant Continual Anomaly Detection on a Consumer Router

Undergraduate research project (Purdue, advisor: Prof. Esmaeili). The authoritative build spec is [CLAUDE.md](CLAUDE.md). This README explains the model in plain terms, says how to run what exists so far, and **logs every implementation step and every deviation from the plan**.

**Status:** Phase 1 (parsing, window features, five detectors, baseline tables) and Phase 2 (quarantine, drift budget + anchor, disambiguation, streaming pipeline) are implemented and tested. Phase 3 (attack/drift simulation and ablations) is next.

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
uv pip install torch --index-url https://download.pytorch.org/whl/cpu   # CPU-only torch (~200 MB)
uv pip install -e ".[dev,models]"   # + river, scikit-learn, matplotlib, cython
```

Run things with `uv run ...`, or activate the venv first (`.venv\Scripts\activate` on Windows).

**OneDrive caveat.** The repo sits in a OneDrive folder, and OneDrive interferes with `.venv`: it refuses hardlinks (fixed by `link-mode = "copy"` in `pyproject.toml`) and sometimes locks files during reinstalls ("Access is denied" on `rad-0.1.0.dist-info`). If that happens, delete that folder and re-run `uv pip install -e ".[dev,models]"`. `uv run --no-sync ...` skips the automatic reinstall that `uv run` does after `pyproject.toml` changes. Moving the project out of OneDrive avoids the problem entirely.

**Kitsune baseline.** Kitsune-py is vendored unmodified under [third_party/kitsune_py/](third_party/kitsune_py/) (MIT, pinned commit in `VENDORED.md`). It needs `cython`, which is in the `models` extra.

## 3. Usage (what works today)

```bash
uv run pytest                                                     # 151 tests
uv run python -m rad.features.parse --list-devices data/raw/<capture>   # which MACs, how much traffic
uv run python -m rad.features.parse --config configs/parse_kitsune_mirai.yaml
uv run python -m rad.features.extract --config configs/features_kitsune_mirai.yaml   # Phase 1b
uv run python -m rad.eval.baseline --config configs/baseline_kitsune_mirai.yaml      # Phase 1c baseline table
uv run python -m rad.eval.nbaiot --config configs/nbaiot_danmini_doorbell.yaml       # N-BaIoT secondary benchmark
uv run python -m rad.pipeline.run --config configs/pipeline_kitsune_mirai.yaml       # Phase 2 streaming pipeline
```

Output: `data/interim/<device>.parquet` holds one row per packet of the target device, in capture order. Columns are documented in [packet_schema.py](src/rad/features/packet_schema.py). Next to it, `<device>.meta.json` records the config, git commit, package versions, and counters for every skipped frame. Data download steps are in [data/README.md](data/README.md).

Phase 1b output: `data/processed/<name>.parquet` holds one row per 30 s window. The first five columns are window bookkeeping (`window_start`, `window_end`, `n_records`, `first_pkt_index`, `last_pkt_index`; the pkt indices are only for joining labels at evaluation time). The 31 features follow in `FEATURE_NAMES` order. A `meta.json` next to it records the config, git commit, and extractor and profile-cache counters.

Phase 1c output: `results/<experiment>/` holds `summary_baseline.csv`/`.md` (the table, committed to git), `scores.csv` (every window's score per detector, split and label), `scores.png` (one panel per detector), the resolved `config.yaml` and `meta.json` (git commit, counts). Kitsune scores are cached in `cache/`, because Kitsune-py takes over an hour on the Mirai capture (D16).

Phase 2 output: `results/<experiment>/windows.jsonl` has one record per live window, in the CLAUDE.md §5 2d format (`score`, `state`, `alert`, `threat_score`, `top_features`, `update_decision`, `drift_notice`, plus `fast_score`, `anchor_score`, `divergence`, `released`). `summary_pipeline.md` counts alerts, states and final update outcomes.

Speed: about 13k frames/s on this laptop, so the roughly 760k-packet Kitsune Mirai capture takes about a minute.

## 4. Code map (Phases 1–2)

| File | What it does |
|---|---|
| [src/rad/features/pcap_reader.py](src/rad/features/pcap_reader.py) | Streaming reader for pcap, pcapng and `.gz` (detected from magic bytes). Header-only decode: Ethernet, 802.1Q, Linux SLL/SLL2, raw IP, IPv4/IPv6, TCP/UDP/ICMP, and the DNS qname and rcode. Bad frames are counted, never fatal. |
| [src/rad/features/device_filter.py](src/rad/features/device_filter.py) | Keeps one device's packets by MAC (with an optional IP fallback) and sets direction, peer IP and the LAN-peer flag. `list_devices()` summarises the MACs in a capture. |
| [src/rad/features/packet_schema.py](src/rad/features/packet_schema.py) | `PacketRecord` plus the fixed Arrow schema. Column order is a contract for Phase 1b and the C port. |
| [src/rad/features/parse.py](src/rad/features/parse.py) | CLI: streams into chunked parquet and writes meta.json. |
| [src/rad/features/window_features.py](src/rad/features/window_features.py) | **The feature contract.** `FEATURE_NAMES` (31 features in a fixed order, each defined in the module docstring) and the streaming `WindowFeatureExtractor`, which emits one vector each time a window closes. `CommitPolicy` decides which windows update the profile cache until Phase 2 replaces it. |
| [src/rad/features/profile_cache.py](src/rad/features/profile_cache.py) | Bounded profile cache (seen IPs, ports, domains, service-port counts) behind the "new …" features. It changes only through `commit()`, the hook for the Phase 2 quarantine. |
| [src/rad/features/extract.py](src/rad/features/extract.py) | CLI: per-device packet parquet → window feature parquet + meta.json. |
| [src/rad/models/](src/rad/models/) | The five detectors behind one interface (`base.Detector`: `bootstrap`, `score_one`, `learn_one`): `hst.py` (river Half-Space Trees, bootstrap-frozen scaling with headroom, D14), `iforest.py` (sliding-window retrain), `autoencoder.py` (d→8→d), `mad.py` (max robust z), `kitsune_wrapper.py` (vendored Kitsune fed our packets, max score per window, D16). |
| [src/rad/eval/](src/rad/eval/) | `metrics.py` (TPR at fixed FPR, partial AUC, validation-set thresholds, false alarms/day, time to detect; never accuracy), `labels.py` (per-window ground truth, evaluation only), `baseline.py` (the one-command baseline table), `nbaiot.py` (N-BaIoT secondary benchmark). |
| [src/rad/continual/](src/rad/continual/) | **The novelty.** `quarantine.py` (gated, delayed-commit updates; D18), `drift_budget.py` (daily and cumulative shift budgets, notices; D19), `anchor.py` (frozen or slow, gated anchor model), `profile_stats.py` + `sketch.py` (committed-profile medians in fixed-bin histograms, bootstrap-fixed scales), `disambiguation.py` (volume vs diversity → three states; D20). |
| [src/rad/pipeline/](src/rad/pipeline/) | `stream.py`: `DevicePipeline`, which runs one device under a frozen, naive, gated or full update rule and emits the output record. `run.py`: the packets → extractor → pipeline CLI, with the profile cache committed only by the update rule (D21). |
| [third_party/kitsune_py/](third_party/kitsune_py/) | Kitsune-py, vendored unmodified (MIT); see `VENDORED.md`. |
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
12. Downloaded the Kitsune and N-BaIoT datasets (N-BaIoT confirmed CSV-only). Identified the Mirai-infected device in the Kitsune Mirai capture as `3c:33:00:98:ee:fd` (192.168.2.110) from its ARP scanning burst, and parsed it.
13. Added ARP decoding to the parser (D8): the infected device's scanning was ~96% ARP and was being discarded. New `arp_op` column appended to the packet schema; tests added.
14. **Phase 1b.** Built the streaming 30 s window extractor with 31 features (`window_features.py`), the bounded profile cache (`profile_cache.py`) and the `extract` CLI. Decisions are recorded as D9–D12. Added 24 tests, including one that checks windows before *k* stay identical whatever traffic follows.
15. Ran Phase 1b on the Kitsune Mirai device: 239 windows, none saturated, profile bootstrapped on the first 60 windows (30 min). Median per window, benign → attack: ARP requests 2 → 6,404, distinct ARP targets 2 → 240, failed-TCP index 6 → 168, connection attempts 6 → 94, top-3-port share 1.0 → 0.13. External destination IPs stay at 3, because this Mirai instance scans the LAN, not the internet.
16. **Phase 1c setup.** Installed the `models` extra (river 0.26.1, scikit-learn 1.9.1, torch 2.14.1+cpu, matplotlib 3.11.2, cython 3.3.0). Vendored Kitsune-py at commit `7c8ea51` into `third_party/kitsune_py/`; a smoke test confirmed netStat (100 features per packet) and KitNET run. The 2018 code uses `np.Inf`, which NumPy 2 removed, so the wrapper will restore that alias before import rather than edit vendored code. Extracted the 16 N-BaIoT attack `.rar` archives with Windows' built-in `tar`.
17. **Phase 1c.** Five detectors behind one interface, low-FPR metrics, and two one-command runners (`rad.eval.baseline`, `rad.eval.nbaiot`). Tests exposed two real flaws, both fixed with regression tests: min-max clipping made far-out values indistinguishable from the bootstrap maximum for HST (D14), and `r/(1+r)` rounded huge MAD scores to exactly 1.0, creating ties (D15). Run metadata is now captured when a run starts, so edits during a run cannot mark it dirty.
18. N-BaIoT Danmini doorbell (secondary benchmark, 115 features, commit `dad15d7`): TPR at FPR 1e-3 is KitNET 0.80, autoencoder 0.58, HST 0.34, Isolation Forest 0.00 and MAD 0.00. pAUC@0.01 is 0.92, 0.96, 0.91, 0.68 and 0.50. MAD's max-over-115-features is dominated by near-constant features that also fluctuate in benign traffic. No detector catches the Gafgyt `tcp`/`udp` floods on these features. Full table: `results/nbaiot_danmini_doorbell/summary_nbaiot.md`.
19. **Phase 2.** Quarantine buffer (D18), drift budget + anchor model + histogram sketches (D19), disambiguation on a shared committed-profile `RobustProfile` (D20), and the streaming pipeline with the output record (D21). The required checks are tests: an obviously anomalous window is never committed, the windows before an alert are purged, and the drift budget halts commits once exceeded (including a boiling-frog ramp that only the cumulative budget catches). End-to-end tests show that under `gated` and `full` a scan never reaches the detector or the profile cache, while `naive` learns it.
20. Ran the full pipeline (HST, full rule, compressed 10 min quarantine) on the Kitsune Mirai device: all ~88 attack windows alert as `suspected_attack` and none is committed, with explanations such as "ARP requests +5,149 IQRs". 13 benign windows were committed, and 29 were purged when the attack's alert tainted the quarantine. Summary: `results/pipeline_kitsune_mirai_hst_full/summary_pipeline.md`.
21. Mirai baseline table complete (commit `f773176`; Kitsune scores from the eed5359 run, converted exactly to the raw cache format). Test set: 44 benign and 90 attack windows. Attacks caught at the validation threshold: autoencoder 100%, Isolation Forest 100%, HST 98.9%, MAD 98.9%, Kitsune 54.4%. Every detector raised exactly one false alarm, on the same benign window at 68.5 min, where several features sit at their bootstrap maxima together. With 22 minutes of benign test data that is 65 alarms/day, which is meaningless statistically. Table: `results/baseline_kitsune_mirai/summary_baseline.md`.
22. Why Isolation Forest and MAD fail on N-BaIoT but not on Mirai (diagnosed on the data). *Isolation Forest:* every attack row lies outside the training range in at least one feature, and 80% lie more than 10 ranges beyond it. Yet the attack scores (median 0.689, max 0.790) all stay below the highest benign validation score (0.833). sklearn splits between each node's training min and max, so a point far beyond the range lands in the same leaf as the most extreme benign point: the same blind spot D14 fixed for HST. *MAD:* 22 of the 115 features have a near-zero scale (< 1e-6) in the training data, e.g. `HH_L1_pcc`. Their tiny benign fluctuations give robust z-scores around 1e36 (benign median), larger than the attacks' (median 6.7e11), so the maximum over features is taken over by noise. On Mirai's 28 window features neither problem appears, and the attacks move features by thousands of IQRs.
23. **Branch `fix/iforest-mad-extrapolation`, 2026-10-10/11.** Model fixes and new detectors, all developed on Danmini and Mirai and checked on held-out devices:
    - Extended IF with headroom (D22) and the MAD tail floor (D23);
    - slog and projection preprocessing (D24), min-p fusion (D25), C-layout model sizes (D26);
    - RobustZ (D27), tie-safe thresholds (D28);
    - ECOD-tail with a router sketch (D39).
24. Robustness checks: 3 seeds (spread ≤ 0.38 points); the artefact check of the Gafgyt flood signal (real spoofed sources, but fragile); the independent Kitsune suite (D29).
25. New data: UNSW IoT traces. June (5 devices, D30), October (5 unseen devices, D36) and a temporal hold-out (D38), about 38 GB in `AI reserch data/unsw-iot-sosr2019`. Fixes found on it: capture gaps, annotation commas, truncated pcapng, buffer sizes (D35).
26. Features 31 → 39: inbound senders and ports (D31), ARP spoofing (D34), service and LAN-peer novelty (D37). Resolution floor (D32).
27. One-command regression suite over every dataset (`rad.eval.regress`, D33), per-attack metric, and persistence / dual-channel alarms (D40). Best configuration: `configs/regress_i8.yaml`.
28. Update rules on real days (`rad.eval.adapt`, D41–D44): naive learns every attack window (detection 84% → 31%); gated and full commit none. Budget estimator bug fixed; capped-mean measure; monotone scales.
29. Boiling-frog injector and RQ3 runner (`rad.attacks.boiling_frog`, `rad.eval.poison`, D45).
30. **2026-10-16.** Chaff-to-FNR sweep (`rad.eval.poison_sweep`, D51): chaff schedule independent of the launch day, 160 runs on 2 UNSW devices. Gated and full were never poisoned within 15 days; naive is poisoned by a single learned attack window (F37). Branch pushed to GitHub (it existed only in this OneDrive copy).
31. **2026-10-19.** Explanation z-scores fixed (D52): `top_features` and the three-state label used raw values over raw IQRs, which gave |z| > 10 on every ordinary window. RQ4 re-measured (F38) with a reproducible confusion matrix in `rad.eval.adapt`: firmware updates are now recognised as drift, and F32's attack-label rate was partly an artefact.
32. **2026-10-19.** Target >= 99% of attacks at FPR < 0.1% (D53, regress_i9): per-protocol packet counts, direction-aware ECOD/RobustZ, strict dual alarms. ECOD meets it on the UNSW June devices (100% / 0.091%), their later days (100% / 0.000%) and Mirai; it fails on the unseen October devices (12.2% FPR, behaviour shift) (F39).
33. **2026-10-19.** Model-specific work (D54, D55, regress_i10): N-BaIoT's AfterImage jitter columns leak timestamps, and ECOD relied on them (86.7% -> 80.0% without; RobustZ unaffected at 88.8%). RobustZ with 99.5th-percentile scales on windows: UNSW June 96.4% / 0.081%, later days 100% / 0.002% (F40).
34. **2026-10-19.** Improvements round (D56-D58): the strict dual alarm now runs in the router pipeline; ECOD there catches 100% of attacks at 0.092% FPR frozen and learns no attack window under gated/full; in the boiling-frog sweep no attack burst is missed. ECOD rebuilds batched (`refit_every`) and the poisoning sweep is resumable. Rejected: model ensembles, n-invariant tails, sliding memory (F41).

Findings for the paper: [docs/findings.md](docs/findings.md) (F1–F41).

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
| 9 | Per-packet table from IP packets (feature table lists IP-level features only) | Ethernet/IPv4 ARP frames are also kept, with a new `arp_op` column | Mirai's LAN scanning is mostly ARP; dropping it hid most of the infection in the Kitsune Mirai capture (D8). |
| 10 | ~25 features, "out/in byte ratio" | 31 features: the CLAUDE.md table plus `arp_req_out` and `n_arp_targets` (D8); the ratio is `out_byte_frac` in [0, 1] | ARP carries the LAN scanning. A bounded ratio suits HST and fixed-point C (D12). |
| 11 | Profile cache obeys quarantine/commit rules | The extractor never writes the cache. A `CommitPolicy` stand-in (bootstrap / always / never) decides until the Phase 2 quarantine replaces it | Keeps Phase 1b free of Phase 2 logic while leaving the exact seam the quarantine needs (D10). |
| 12 | HST `window_size=250`; min-max scaler fit on bootstrap | `window_size` is a config value (50 for the 2-hour Mirai capture); the bootstrap range maps to [0.25, 0.75] instead of [0, 1] | river's HST scores 0 until its first window fills, and plain clipping made far-out values indistinguishable from the bootstrap maximum (D13, D14). |
| 13 | Shallow autoencoder 25→8→25 | d→8→d, with d = the number of selected features (28 on Mirai, 115 on N-BaIoT), trained on the bootstrap set and then by replay | The feature count grew to 31 (deviation 10) and some experiments exclude features. |
| 14 | Kitsune on raw packets | Kitsune is fed only the target device's packets (parsed by us, mapped to its inputs exactly as its own parser does) | Single-device scope; avoids scapy/tshark (D16). |
| 15 | Phase 1 done on an N-BaIoT device | Primary table on the Kitsune Mirai device; N-BaIoT (Danmini doorbell) is a per-row secondary benchmark on its own 115 features | N-BaIoT has no pcaps or timestamps (deviation 4, D17). |
| 16 | Update decisions: committed / quarantined / rejected / purged | Adds a fifth outcome, `blocked` (due and clean, but refused by the drift budget) | RQ3 needs to count what the budget stopped, separately from what an alert purged (D19). |
| 17 | 24 h quarantine delay, daily budgets | The Mirai pipeline demo uses a 10 min delay and placeholder budgets | The capture lasts ~2 h; with a 24 h delay nothing would ever commit. Defaults stay 24 h / per day (D21). |
| 18 | Phase 2 done when the pipeline runs end-to-end on N-BaIoT | Runs end-to-end on the Kitsune Mirai pcap | N-BaIoT has no packets, so the profile cache and window features cannot be computed from it (deviation 15). |
| 19 | MAD = max over features of \|x − median\| / (1.4826·MAD) | Kept as the baseline. The portfolio adds MAD+tail floor+slog (D23/D24), RobustZ (D27) and ECOD-tail (D39). | The literal formula fails on near-constant features (F3). Simple robust statistics still win (F9). |
| 20 | Thresholds: k-th highest validation score | Tie-safe cut (D28) | Ties at the cut alerted together and broke the false-positive budget. |
| 21 | ~25 features | 39 (D31, D34, D37 appended) | Spoofed floods, ARP spoofing and LAN attacks were invisible to destination-only features. |
| 22 | Drift = Σ_j \|Δmedian_j\| / IQR_j | Option: mean_j min(\|Δmedian_j\| / IQR_j, 3) (D43); budgets calibrated on benign days (D42) | The sum is dominated by near-constant features (budgets 0.03–475 across devices). |
| 23 | Quarantine: commit only if no alert during the stay | Also a k-purge variant (D41) | With ~1 false alarm/day and a 24 h delay, the strict rule commits almost nothing (F30). |
| 24 | Primary model HST | HST kept, but RobustZ is the most stable model (F15, F27) | HST is weak on N-BaIoT and UNSW. Decision for the paper pending. |

---

## 7. Next steps

- **Data:** the Mirai capture has only ~75 min of benign traffic, too little for reliable false-alarm rates or for the day-scale drift budget. The own testbed (2–4 weeks) is the main fix; a longer public capture would help in the meantime.
- **Phase 3:** the boiling-frog injector (volumetric and behavioral, geometric growth), the benign-drift simulator (firmware update, app reinstall, schedule shift), and the one-command ablation matrix over update rules × detectors × feature sets. Also: tune `b_daily`/`b_total`, `tau_div` and a z-scale floor on benign data only (D19–D21).
