# CLAUDE.md — Poisoning-Resistant Continual Anomaly Detection on a Consumer Router

Undergraduate research project (Purdue, advisor: Prof. Esmaeili). This file tells Claude Code what to build, in what order, and what rules to follow. Read it fully before writing code.

> Implementation log and deviations from this plan are recorded in README.md §5–6.

## 1. What this project is

A streaming, **unsupervised** anomaly detector that watches **one device's** traffic on a **consumer/home OpenWrt router**, keeps learning that device's normal behavior, and **refuses to learn slow ("boiling-frog") poisoning as normal**.

- **Primary model:** Half-Space Trees (HST) — streaming, one-class, constant memory.
- **Baselines (required):** Kitsune/KitNET, Isolation Forest (sliding-window retrain), shallow autoencoder (25→8→25), robust-statistics MAD/boxplot detector.
- **The novelty is the update rule, not the detector:**
  1. **Quarantine buffer** — gated, delayed-commit updates.
  2. **Drift budget + anchor model** — bounded daily profile shift; alert when fast and anchor models diverge.
  3. **Drift-vs-attack disambiguation** — volume-shift vs. diversity-shift heuristic → three-state output.
- **Evaluated on real router-class hardware** with measured CPU, RAM, latency, throughput.

### Research questions (every experiment must map to one)
- **RQ1 Feasibility:** how small can the detector be (trees, depth, window, features) and what does it cost on a router?
- **RQ2 Adaptation:** does gated updating keep false positives low through benign drift vs. frozen and naive-update models?
- **RQ3 Poisoning resistance:** how much more chaff / how many more days does boiling-frog poisoning need against the full system?
- **RQ4 Disambiguation:** how well does the three-state output separate benign drift from attacks?

## 2. Hard constraints (do not violate)

- **Single device only.** One model instance per device (keyed by MAC). Do not build multi-device or network-wide logic; leave clean seams for it.
- **Unsupervised only.** No training on attack labels. Labels are used **only for evaluation**. No Hoeffding/online decision trees (they need labels).
- **No payload inspection.** Headers/flow metadata only (privacy + works on encrypted traffic).
- **Window-level, not per-packet, features.** ~25 features per 30 s window.
- **Router-friendly design from day one.** Avoid anything that can't be ported to C with fixed-point math, static memory, and bounded state. No deep models in the main detector.
- **Never report accuracy as a headline metric.** Use TPR at fixed low FPR, partial AUC, false alarms/day.
- **Reproducibility:** fixed random seeds everywhere; every experiment driven by a config file; results written to disk with the config that produced them.
- **Attack traffic only in isolated lab networks / offline pcaps.** Never generate scanning, brute-force, or flood traffic against anything outside the isolated testbed.

## 3. Repository layout (create this)

```
router-anomaly/
├── CLAUDE.md
├── README.md
├── pyproject.toml / environment.yml
├── configs/                  # YAML experiment configs
├── data/
│   ├── raw/                  # pcaps, N-BaIoT CSVs (gitignored)
│   ├── interim/              # parsed per-device packet tables
│   └── processed/            # windowed feature matrices (parquet)
├── src/rad/                  # "router anomaly detection" package
│   ├── features/             # pcap parsing, windowing, feature extraction
│   ├── models/               # hst.py, iforest.py, autoencoder.py, mad.py, kitsune_wrapper.py
│   ├── continual/            # quarantine.py, anchor.py, drift_budget.py, disambiguation.py
│   ├── pipeline/             # streaming loop that wires features → model → update rule → outputs
│   ├── attacks/              # boiling-frog injector, benign-drift simulator
│   ├── eval/                 # metrics, ablation runner, plots
│   └── utils/
├── notebooks/                # exploration only; no logic that isn't also in src/
├── tests/                    # pytest
├── results/                  # experiment outputs (gitignored except summaries)
└── c/                        # Phase 4: C port + OpenWrt package
    ├── src/
    ├── include/
    ├── tests/
    └── openwrt/router-ids/Makefile
```

## 4. Tech stack

- Python 3.10+, conda env `router-anomaly`.
- `river` (≥0.21) for `anomaly.HalfSpaceTrees`; `scikit-learn` for Isolation Forest + metrics; `torch` for the autoencoder baseline; `pandas`, `numpy`, `pyarrow`; `scapy` or `dpkt` for pcap parsing (prefer `dpkt` for speed); `matplotlib`; `pyyaml`; `pytest`.
- Kitsune baseline: wrap `ymirsky/Kitsune-py` (vendor or submodule; do not rewrite it).
- Phase 4: C99, OpenWrt SDK, `libpcap`, `musl` cross-compile, `iperf3` for throughput tests.

Setup:
```bash
conda create -n router-anomaly python=3.10 -y
conda activate router-anomaly
pip install river scikit-learn pandas numpy pyarrow torch dpkt scapy matplotlib pyyaml pytest jupyterlab
```

## 5. Build order (phases — finish and test each before the next)

### Phase 1 — Data pipeline + baselines (Python)

**1a. Parsing.** Read pcaps (N-BaIoT, Kitsune dataset, own testbed) into a per-packet table filtered to the target device's MAC/IP. N-BaIoT also ships pre-extracted CSV features; support pcaps as the primary path so features match what the router will compute.

**1b. Windowing + features.** Fixed 30 s windows (5 min as optional secondary context). One feature vector per window:

| Group | Features |
|---|---|
| Volume | bytes out, bytes in, packets out, packets in, out/in byte ratio |
| Packet shape | mean & variance of packet size; mean & variance of inter-arrival time |
| Destinations | # distinct external dst IPs; # **new** dst IPs never seen in profile; # distinct /24 prefixes; fraction of traffic to LAN peers |
| Ports/services | # distinct dst ports; # **new** dst ports; TCP/UDP/ICMP fractions; fraction of traffic on device's top-3 historical ports |
| DNS | # queries; # distinct domains; # **new** domains; NXDOMAIN count |
| Connections | # new connections; # failed/half-open TCP (SYN w/o established, RSTs); mean connection duration |
| Context | time-of-day sin/cos; day-of-week flag |

Rules:
- "New" features need a **profile cache** (seen IPs/ports/domains). The cache is part of the device profile and must obey the same quarantine/commit rules as the model — otherwise poisoning just teaches the cache. Use bounded structures (e.g., capped set or Bloom filter) so the C port is possible.
- Feature extractor must be **streaming** (process packets in order, emit a vector when a window closes), not a batch groupby over the whole capture.
- Keep feature definitions in one module with a documented order; the C port must reproduce them exactly.

**1c. Models.** Common interface for every detector:
```python
class Detector(Protocol):
    def score_one(self, x: dict[str, float]) -> float: ...   # higher = more anomalous, normalized to [0,1] where possible
    def learn_one(self, x: dict[str, float]) -> None: ...
```
- HST: `river.anomaly.HalfSpaceTrees(n_trees=25, height=10, window_size=250, seed=...)`. Wrap in `river.compose` with a min-max scaler fit on bootstrap data (HST expects features in [0,1]). Make scaling bounds fixed after bootstrap so the C port can use them.
- Isolation Forest: retrain on a sliding window of recent "accepted" windows.
- Shallow autoencoder: 25→8→25, MSE reconstruction error as score.
- MAD baseline: `score = max_j |x_j − median_j| / (1.4826 · MAD_j)`.
- Kitsune: run on raw packets (it uses its own per-packet features); align its outputs to our 30 s windows (max score per window) for comparison.

**Phase 1 done when:** windowed features for at least one N-BaIoT device are produced, all five detectors score them, and a baseline table (TPR@FPR=1e-3, partial AUC, false alarms/day) is generated by one command.

### Phase 2 — Continual learning core (the novelty)

Implement as wrappers around any `Detector`, so the same update rule can be ablated across models.

**2a. Quarantine buffer (`continual/quarantine.py`)**
1. Score each window **before** any learning.
2. If `score < tau_admit` → push `(x, t)` onto FIFO queue Q.
3. If `score ≥ tau_alert` → raise alert and **purge the last k windows** from Q (pre-attack ramp-up).
4. Items older than `T_delay` (default 24 h of simulated time) are committed via `learn_one` **only if no alert fired during their stay**.
5. Log every window's decision: `committed | quarantined | rejected | purged`.

**2b. Anchor model + drift budget (`continual/anchor.py`, `drift_budget.py`)**
- `M_fast`: updated from committed quarantine output.
- `M_anchor`: frozen to bootstrap, or updated on a much slower schedule (weekly), also gated.
- Each simulated day compute
  `D_drift = Σ_j |median_fast(f_j) − median_anchor(f_j)| / IQR_anchor(f_j)`
  over committed data (track medians/quantiles with streaming sketches, e.g., P² or fixed histograms).
- If a day's commits would push the shift beyond `B_daily`, **stop committing** for that day and raise a `possible_slow_poisoning_or_major_change` notice. Do not silently adapt.
- Track cumulative drift vs. anchor too, so many small within-budget days still trigger a notice.

**2c. Disambiguation (`continual/disambiguation.py`)**
- Split features into volume group `F_vol` and diversity group `F_div` (new IPs, new ports, new domains, failed SYNs, distinct /24s).
- Compute robust z-scores per group (`z_vol`, `z_div`).
- State:
  - `normal` if `score < tau_alert`
  - `suspected_attack` if `score ≥ tau_alert` and `z_div > tau_div`
  - `suspected_benign_drift` if `score ≥ tau_alert` and `z_vol` dominates `z_div`
- This is a **hypothesis under test**, not a guaranteed result. Keep it simple and report where it fails.

**2d. Per-window output record**
```json
{"t": ..., "device": "...", "score": 0.0, "state": "normal|suspected_benign_drift|suspected_attack",
 "alert": false, "threat_score": 0.0, "top_features": [["new_dst_ips", 12.3], ...],
 "update_decision": "committed|quarantined|rejected|purged", "drift_notice": false}
```
- Alerts use persistence smoothing (k-of-n windows). Threat score combines magnitude and persistence.
- `top_features`: the 3 features with largest robust z-score vs. the committed profile, so alerts read like "camera is contacting 140 new IPs on port 23".

All thresholds (`tau_admit`, `tau_alert`, `tau_div`, `k`, `T_delay`, `B_daily`, k-of-n) live in config, never hard-coded.

**Phase 2 done when:** unit tests show (a) an obviously anomalous window is never committed, (b) windows before an alert are purged, (c) the drift budget halts commits when exceeded, and the full pipeline runs end-to-end on N-BaIoT.

### Phase 3 — Attack simulation + ablations

**3a. Boiling-frog injector (`attacks/boiling_frog.py`)**
- Mix attack windows into benign streams with geometric growth `V(t) = V0 · (1 + α)^t`, α ∈ [0.01, 0.05] per day.
- Two variants: volumetric (flood volume ramps) and behavioral (scan rate toward new subnets ramps).
- Also test one-shot contamination during bootstrap.
- Operate on feature windows **and** optionally on pcaps (mix attack packets from N-BaIoT Mirai/BASHLITE captures), with the mixing schedule logged.

**3b. Benign drift simulator (`attacks/benign_drift.py`)**
- Scripted events: firmware update (new update-server destinations + temporary volume spike), app reinstall, new usage schedule (time-of-day shift).

**3c. Ablation matrix** — run every combination with one command (`python -m rad.eval.ablate --config configs/ablation.yaml`):
- Update rules: frozen / naive always-update / gated (quarantine only) / full (quarantine + anchor + budget)
- Detectors: HST / IForest / AE / MAD / Kitsune (Kitsune only frozen + naive, since it has its own training mode)
- Feature-set size: full ~25 vs. reduced subsets (for RQ1)

**3d. Metrics (`eval/metrics.py`)**
- Detection: TPR at FPR = 1e-3 and 1e-4, partial AUC, mean time-to-detect, false alarms/day.
- Adaptation: FPR before/after each benign drift event; recovery time (windows until FPR returns to baseline).
- Poisoning: chaff needed to reach 50% false-negative rate (ANTIDOTE metric); days to successful poisoning; evasion success after poisoning.
- Disambiguation: confusion matrix of the three states vs. ground truth event type.
- Save tables as CSV + plots as PNG under `results/<experiment_name>/` along with the resolved config and git commit hash.

### Phase 4 — C port + OpenWrt deployment

Start only after Phase 3 shows which configuration is worth porting.

- C99, no `malloc` in the hot path; static arrays for trees, node masses, feature vectors, quarantine queue, and profile cache.
- HST cut points generated at init from a fixed seed (or exported from Python) — the C and Python models must produce **identical scores** on the same input; write a cross-check test that feeds the same feature vectors to both.
- Node masses as `uint32_t`; fixed-point features (scale bounds fixed after bootstrap).
- Capture with `libpcap`, BPF filter `ether host <TARGET_MAC>`, aggregate into 30 s windows.
- Package for OpenWrt SDK under `c/openwrt/router-ids/` (`DEPENDS:=+libpcap +libpthread`), build `.ipk`, install with `opkg`.
- Benchmarks (RQ1): CPU % mean/peak, RSS from `/proc/<pid>/status`, per-window latency via `clock_gettime(CLOCK_MONOTONIC)`, `iperf3` forwarding throughput with detector on vs. off, model size in KB. Targets: <15% of one core, <10 MB RAM, <5 ms per window. Also run on a Raspberry Pi for comparison with Kitsune's published numbers.

## 6. Datasets

- **Primary:** own testbed — one IoT device behind an OpenWrt router, 2–4 weeks continuous capture with scripted benign drift and controlled attacks in an isolated lab network.
- **Public per-device:** N-BaIoT (9 devices, benign + Mirai/BASHLITE), Kitsune dataset.
- **Secondary only:** UNSW-NB15 and **corrected** CIC-IDS2017 (Engelen et al. 2021 fixes). Filter to single hosts; treat results as supplementary.
- Raw data never goes in git. Document download steps in `data/README.md`.

## 7. Coding conventions

- Type hints everywhere; docstrings on public functions explaining the *why* when non-obvious.
- Every module in `features/` and `continual/` gets pytest coverage; use small synthetic streams with known answers.
- Streaming correctness first: no function may look at future windows. Add a test that shuffling future data doesn't change past scores.
- Configs in YAML; CLI entry points via `python -m rad.<module>`.
- Log, don't print. Use the `logging` module.
- Keep notebooks thin — import from `src/rad`, never define core logic there.
- When a design choice affects the research claims (thresholds, what counts as "committed", how drift is measured), add a short note to `docs/decisions.md`.

## 8. Things to watch out for

- **The simple baseline might win.** Arp et al. (USENIX Sec 2022) showed a boxplot method beat Kitsune at low FPR. Always include MAD in comparisons and report honestly.
- **Cold start:** bootstrap data is assumed clean. Measure sensitivity to bootstrap contamination rather than assuming it away.
- **Profile cache poisoning:** the "new destination/port/domain" caches can be poisoned just like the model; they must go through quarantine.
- **Threshold leakage:** never tune thresholds on the test attack data. Tune on benign validation data only (e.g., set `tau_alert` for a target false-alarm rate).
- **Mimicry/evasion attacks** are out of scope beyond a basic test; note it as a limitation.
- **Time:** use packet timestamps, not wall clock, so replays are deterministic.

## 9. Key references (for context, not to reimplement)

- Kitsune — Mirsky et al., NDSS 2018 (baseline; lists contamination filtering as future work)
- N-BaIoT — Meidan et al., IEEE Pervasive Computing 2018 (per-device modeling, dataset)
- Half-Space Trees — Tan, Ting, Liu, IJCAI 2011 (core algorithm)
- ANTIDOTE — Rubinstein et al., IMC 2009 (boiling-frog threat model, chaff-to-50%-FNR metric)
- Casting out Demons — Cretu et al., IEEE S&P 2008 (training-data sanitization → quarantine idea)
- OWAD — Han et al., NDSS 2023 (normality shift detection)
- Dos and Don'ts of ML in Security — Arp et al., USENIX Security 2022 (simple baselines, low-FPR metrics)

## 10. Timeline (for prioritizing)

| Weeks | Milestone |
|---|---|
| 1–3 | Data pipeline + all baselines on N-BaIoT |
| 4–6 | Quarantine buffer, anchor + drift budget, disambiguation |
| 7–9 | Boiling-frog + benign-drift experiments, ablation tables (RQ2–RQ4) |
| 10–12 | C port + OpenWrt SDK build |
| 13–14 | On-router profiling (RQ1) |

If asked to "start", begin with Phase 1a and do not jump ahead.
