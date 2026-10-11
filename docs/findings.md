# Research findings (working notes for the paper)

This is the paper-facing record of what the experiments have shown so far. Each finding gives:
- the claim in plain words;
- the numbers behind it;
- where the evidence lives (result folder, commit);
- its caveats;
- the research question it serves.

Design decisions are explained in [decisions.md](decisions.md) (D1–D29). The build log and the deviations from the plan are in [README.md](../README.md) §5–6.

**Status labels**
- **Solid:** held-out evidence, current protocol.
- **Preliminary:** development-set evidence only, small test sets, or produced under the old threshold rule.
- **Pending:** a run is in progress.
- **Negative:** something that did not work. Kept, because negative results are part of the paper.

**Last updated:** 2026-10-11 13:30, after the multi-seed check, the Kitsune suite, the first UNSW run and the regression suite (ref → i3).

---

## 1. Setup in brief (needed to read the numbers)

**Data**
- **Kitsune Mirai capture.** One infected device, real pcap, parsed by our own pipeline into 30 s windows with 28 window features (31 minus the 3 time-of-day features). It has 239 windows:

  | Part | Windows | Length |
  |---|---|---|
  | Bootstrap | 60 | 30 min |
  | Validation | 45 | |
  | Test, benign | 44 | 22 min |
  | Test, attack | 90 | |

  This is the *primary* (router-equivalent) feature path.
- **N-BaIoT, 9 devices** (secondary benchmark). The dataset ships only pre-extracted per-packet-snapshot features (115 per row) and no pcaps. Our window features therefore cannot be computed on it, and its results are **per row**, not per 30 s window. They cannot be converted to false alarms per day.
  - Benign rows are split in time order: 50% bootstrap, 20% validation, 30% test.
  - Up to 10 attack files per device (5 Gafgyt and 5 Mirai). Ennio Doorbell and Samsung Webcam have no Mirai files.
  - 2,000 rows are sampled per attack file (seeded).
- **Kitsune dataset, the 8 other captures** (independent test, D29). For each capture:
  - The monitored device is the MAC involved in the most attack-labelled frames.
  - The first 50% of its pre-attack windows bootstrap the detectors, the next 30% validate, and the rest are test.

**Protocol rules (all experiments)**
- **Unsupervised.** Models train on benign data only. Labels are used only for scoring the results, and in D29 to pick which device to watch.
- **Frozen after bootstrap** for these baseline tables. The continual-learning rule is evaluated separately.
- **Thresholds are set on benign validation data only**, for a target false-positive rate of 0.1%. N-BaIoT uses an FPR target of 1e-3; the window datasets use 1 alarm/day.
- **Metrics** (never accuracy):
  - **TPR at FPR 1e-3 and 1e-4.** This is a *test-set* operating point: it measures ranking quality.
  - **pAUC** at 0.01 and 0.1 (McClish-standardised; 0.5 = random).
  - **Attacks caught at the validation threshold** ("detection rate@tau"). This is the deployable number.
  - **Test false-positive rate at that threshold.**
  - False alarms per day (windows only), time to detect, fit time, scoring time, and model size (estimated C-port memory, D26).
- **Development vs held-out.** Danmini Doorbell (N-BaIoT) and Kitsune Mirai were inspected while designing the fixes, so they are **development sets**. The other 8 N-BaIoT devices were run only after each configuration was frozen; they are **held out**. The 8 extra Kitsune captures have never been used for anything: they are **independent**.

---

## 2. Findings

### F1. The pipeline works end to end, and window features make attacks obvious on real pcap data. [Solid, RQ1 / RQ2 prerequisite]
- The streaming parser → 30 s windows → 31 features → detector → update rule → output record pipeline runs on the Kitsune Mirai pcap with bounded memory.
- Shifts in the median window, benign → attack, on the Mirai device:
  - ARP requests 2 → 6,404;
  - distinct ARP targets 2 → 240;
  - failed-TCP index 6 → 168;
  - connection attempts 6 → 94;
  - top-3-port share 1.0 → 0.13.
- External destination IPs stay at 3, because this Mirai instance scans the LAN, not the internet.
- ARP decoding was essential: about 96% of the scanning was ARP, and a pure-IP parser would have discarded it (D8).
- Evidence: README log 13–15; `data/processed/`.
- Caveat: one device, about 2 h of capture, only about 75 min of it benign.

### F2. On window features, the Mirai attack is easy for every model except packet-level Kitsune. [Preliminary: tiny test set]
- Attacks caught at the validation threshold:

  | Model | Caught |
  |---|---|
  | Autoencoder | 100% |
  | Isolation Forest | 100% |
  | HST | 98.9% |
  | MAD | 98.9% |
  | Kitsune (raw packets, max score per window) | 54.4% |

- Every window detector raised exactly **one** false alarm, and it was on the same benign window, at 68.5 min. Several features sit at their bootstrap maxima together there.
- That one alarm is "65 alarms/day" only because the benign test set is 22 minutes long. The number is statistically meaningless.
- With slog preprocessing, HST raised **0** false alarms and caught 100% (`baseline_kitsune_mirai_improved`).
- Evidence: `results/baseline_kitsune_mirai/`, commit `f773176`; `results/baseline_kitsune_mirai_improved/`.
- Paper use: shows that window-level features plus a simple detector suffice for scanning malware. The Kitsune comparison must note that Kitsune scores packets with its own features, aligned to windows by the max.

### F3. Textbook Isolation Forest and textbook MAD fail completely on N-BaIoT, for two identifiable reasons. [Solid: diagnosed on data, Negative]
- On Danmini, TPR at FPR 1e-3 was:

  | Model | TPR at FPR 1e-3 | pAUC@0.01 |
  |---|---|---|
  | Isolation Forest (sklearn) | 0.00 | 0.68 |
  | MAD (CLAUDE.md formula) | 0.0016 | 0.50, i.e. random |
  | KitNET | 0.80 | |
  | Autoencoder | 0.58 | |
  | HST | 0.34 | |

- **Isolation Forest blind spot.**
  - Every attack row is outside the training range in at least one feature, and 80% are more than 10 ranges beyond it.
  - Yet every attack scores below the highest benign validation score: median 0.689, max 0.790, against 0.833.
  - The reason: sklearn draws each split between the node's training min and max, so a far-out point lands in the same leaf as the most extreme benign point.
  - It's the same blind spot that min-max clipping created for HST (D14).
- **MAD noise takeover.**
  - 22 of the 115 features have a near-zero MAD in training (e.g. `HH_L1_pcc`).
  - Their tiny benign fluctuations give z ≈ 1e36 (benign median), which is larger than the attacks' z (median 6.7e11).
  - So the maximum over features is taken over by noise.
- On Mirai's 28 window features neither problem appears (F2).
- Evidence: README log 18 and 22; `results/nbaiot_danmini_doorbell/`.
- Paper use: a concrete, reproducible explanation of *why* simple baselines can look broken. It connects to Arp et al.'s warning that baselines are often misconfigured.

### F4. Two principled fixes make both models work, and the fixes generalise to held-out devices. [Solid]
- **Isolation Forest (D22).**
  - Headroom alone (splits drawn from a range widened 25%, plus 4 extra levels) barely helped: 0% → 0.15% on Danmini.
  - The reason: an attack row is out of range in only about 23 of 115 features, so an axis-parallel split rarely tests a relevant feature.
  - **Extended IF** (random hyperplane splits, Hariri et al. 2019) with headroom fixed it.
- **MAD (D23).** A tail-calibrated scale floor: `scale_j ≥ Q_0.999(|x_j − median_j|)/3`.
- Mean over the 8 held-out devices, one run each, commit `1b5c0c3`, old threshold rule:

  | Model | Attacks caught at threshold | Benign test FPR |
  |---|---|---|
  | sklearn IF | 6.9% | |
  | **Extended IF** | **74.5%** | 0.09% |
  | MAD | 0.004% | |
  | **MAD + tail floor** | **77.2%** | 0.12% |

- Evidence: `results/nbaiot_fixes_summary/summary_aggregate.md`.
- Caveat: produced before the tie-safe threshold fix (F6), so the false-positive rates are slightly optimistic for the threshold side and the detection rates slightly inflated. The direction of the result is not in doubt.

### F5. The log transform ("slog") helped only MAD. For the other models it was neutral or slightly harmful. [Solid, partly Negative]
- `slog(x) = sign(x)·log(1+|x|)`, frozen and cheap (a lookup table in C, D24).
- Held-out mean attacks caught at the threshold (old threshold rule):

  | Model | Without slog | With slog |
  |---|---|---|
  | MAD + tail | 77.2% | **87.3%** |
  | Extended IF | 74.5% | 70.1% |
  | Autoencoder | 76.6% | 73.4% |
  | HST | 23.0% | 21.3% |

- Evidence: `results/nbaiot_fixes_summary/`, `results/nbaiot_improved_summary/`, commit `0661d0b`.
- Paper use: the preprocessing is not a universal win. Report it per model.

### F6. A threshold-setting bug inflated false positives wherever scores tie, and it is easy to miss. [Solid: methodological finding]
- The standard "take the k-th highest validation score" rule lets every validation score tied at the cut alert. So the real false-positive rate can far exceed the target.
- Ties are common with discrete features and with robust detectors: many benign rows sit exactly at a training extreme and score exactly z = 3.
- The fix (D28) moves the cut to the next distinct score.
- Effect on MAD + tail + slog: mean attacks caught fell from 87.3% (old rule, held-out) to 82.1% (new rule, all 9 devices, seed 0), with correspondingly honest false-positive rates.
- All results before commit `da863a3` are **indicative only** wherever ties occurred.
- Paper use: a short methods note. Many anomaly-detection papers threshold this way, and the bias is in the optimistic direction.

### F7. RobustZ catches the hardest N-BaIoT attacks (the Gafgyt TCP/UDP floods) on 5 of 9 devices; no previous model caught them anywhere. [Solid on seed 0; multi-seed Pending]
- RobustZ = MAD + tail + slog, with three changes (D27):
  1. a separate scale for each side of each feature;
  2. the mean of the 3 largest z instead of the maximum;
  3. a router build with histogram statistics and int16 parameters.
- Seed 0, tie-safe threshold, all 9 devices (`results/nbaiot_frontrunners_s0_*`), mean attacks caught at the validation threshold:

  | Model | Mean | Median | Min | Max |
  |---|---|---|---|---|
  | **RobustZ router** | **88.9%** | 99.95% | 60.0% | 100% |
  | MAD + tail + slog | 82.1% | 80.0% | 60.0% | 99.98% |
  | KitNET | 79.9% | 80.0% | 60.0% | 99.99% |
  | Autoencoder + slog | 71.2% | 77.0% | 42.4% | 91.7% |

- Gafgyt TCP/UDP floods caught (mean over 9 devices / devices with ≥90% caught):

  | Model | Mean caught | Devices ≥90% |
  |---|---|---|
  | RobustZ | 55.5% | 5 of 9 |
  | MAD + tail + slog | 33.3% | 3 of 9 |
  | KitNET | 22.2% | 2 of 9 |
  | Autoencoder + slog | 11.1% | 1 of 9 |

  On the original Danmini table, *no* detector caught them at all.
- The other 8 attack types (Gafgyt combo, junk and scan; the 5 Mirai types) are caught at ≥98.9% on average by RobustZ, MAD + tail + slog and KitNET.
- Caveat: designed on Danmini and Mirai (development sets). Danmini is included in these means. The held-out-only means will be reported with the multi-seed results.

### F8. RobustZ's lead comes partly from a higher false-positive rate on test. At matched false positives, MAD + tail + slog ranks attacks better. [Solid on seed 0: important nuance]
- Benign test FPR at the validation threshold (target 0.1%), seed 0:

  | Model | Mean | Max | Devices above 0.15% |
  |---|---|---|---|
  | MAD + tail + slog | **0.06%** | 0.14% | **0** |
  | Autoencoder + slog | 0.08% | 0.16% | 1 |
  | KitNET | 0.10% | 0.46% (Ecobee) | 1 |
  | RobustZ | 0.12% | 0.32% (Ennio) | 2 (Ennio 0.32%, SimpleHome 1002 0.18%) |

- TPR at a *fixed* test FPR of 0.1% (ranking quality, same false positives for everyone): MAD + tail + slog **88.8%**, KitNET 82.2%, RobustZ 82.2%, AE + slog 72.0%.
  - MAD + tail + slog ranks the floods above the benign tail on Samsung, SimpleHome 1002 and SimpleHome 1003 (about 99.9%).
  - But its validation threshold is too conservative there (Samsung's realised FPR is 0.01%), so at the deployable threshold it misses them.
- pAUC@0.01 is a tie: RobustZ 0.979, MAD + tail + slog 0.979, KitNET 0.920, AE + slog 0.909.
- **Interpretation:**
  - RobustZ is better at the *deployable* operating point on average.
  - MAD + tail + slog has better ranking and better-controlled false positives.
  - Neither dominates. The deciding factor is **threshold transfer** from validation to test, not the score itself.
- Paper use: report both operating points. Don't claim RobustZ is "better" without this qualification.

### F9. "The simple baseline wins": 1 KB robust-statistics detectors match or beat KitNET and the autoencoder at low false-positive rates. [Solid]
- On N-BaIoT (seed 0, 9 devices), RobustZ and MAD + tail + slog beat KitNET on attacks caught, on TPR at FPR 1e-3 and on pAUC@0.01.
- They are 6–7× smaller and 10–30× faster to score (F12).
- This replicates the warning of Arp et al. (USENIX Security 2022) on a different dataset and with a router-oriented model: a well-configured boxplot/MAD-style detector beats Kitsune at low FPR.
- Paper use: the main "detector" result. It supports making the detector simple and focusing the novelty on the update rule, which is the project's thesis.

### F10. The flood detection is real attack behaviour, not a recording artefact, but it sits exactly on the edge of normal, so it is fragile. [Solid]
- Question: RobustZ's flood detections are driven by `MI_dir_L0.01_weight` (a decayed count of recent packets from the same source). Was a low value a counter-restart artefact at the start of each attack file?
- Check: the median of that feature, and of its faster-decaying versions L5, L1 and L0.1, in the first 1%, the middle 1% and the last 1% of each Gafgyt TCP and UDP file, on 4 devices (2 caught, 2 missed).
- Result:
  - The value is **exactly 1.00 throughout every file**, from start to end, about 92k–111k rows per file. Every packet comes from a never-seen source, which is spoofed or randomized source addresses.
  - An artefact would recover after the first rows.
  - Benign traffic at the start of its file matches the rest of benign traffic (e.g. Danmini 29.9 against a median of 30.3), so file starts are not artificially low.
- Fragility:
  - The benign *training minimum* is also 1.0 on all four devices, so 0% of flood rows fall *below* the training range. They sit exactly at its edge (z ≈ 3).
  - Whether a device alerts then depends on other features adding to the top-3 mean. That happens on Danmini and Ennio, not on Ecobee and Samsung, even though the feature looks identical on all four.
- Implication: a per-window **count of new source addresses** (the "new destination IPs" feature, mirrored for sources) would put floods far outside normal. Improvement I1.

### F11. The "80% / 60%" ceilings in the N-BaIoT tables are structural. [Solid: needed to read every table]
- Each device has 10 attack files (5 Gafgyt + 5 Mirai), or 5 for Ennio and Samsung, which have no Mirai files. The 2,000 rows sampled per file weight every file equally.
- Missing only the two Gafgyt floods (TCP and UDP) therefore gives exactly 80%, or 60% on Ennio and Samsung.
- Most of the differences between models in the cross-device tables are "caught the floods on this device or not".
- Paper use: say this explicitly, and show the per-attack table next to the summary table.

### F12. Every front-runner is far inside the router budget for scoring cost and size. [Preliminary: laptop Python, not router C]
- Seed 0, 9 devices, one scoring call per row/window:

  | Model | Scoring time | Training time | Size (estimated C memory) |
  |---|---|---|---|
  | **RobustZ router** | **0.010–0.013 ms** | 0.15–1.8 s | **1.0 KB** (115 features; 252 B for our 28) |
  | MAD + tail + slog | 0.026–0.032 ms | 0.2–3.0 s | 0.9 KB |
  | Autoencoder + slog | 0.030–0.039 ms | 5.6–10.7 s | 8.6 KB |
  | KitNET | 0.27–0.47 ms | 4–58 s | 6.0–7.1 KB |

  Reference points on window features (Mirai): HST 550 KB, Extended IF 254–774 KB.
- The target is under 5 ms per window, scored once per 30 s, so RobustZ has about 400× headroom on the laptop. Even at a pessimistic 10–50× slower router CPU, RobustZ and MAD stay under 1 ms. KitNET could reach about 20 ms.
- The detector is not in the forwarding path. The per-packet cost is only the feature counters plus the "seen before?" lookups, which are **not measured yet**.
- Evidence: `fit_s`, `score_ms_per_window` and `model_kb` columns in every `summary_*.csv`.
- RQ1: real numbers need Phase 4 (C port, OpenWrt, CPU/RSS/latency/iperf3).

### F13. The router build of RobustZ (64-bin histograms, int16 parameters) is as accurate as exact float32. [Preliminary: development sets]
- Scoring state: 9 bytes per feature (252 B for 28 features). Learning state: about 7.7 KB of histograms, against about 315 KB for a 2,880-row float32 window.
- Same accuracy as exact float32 on Danmini and Mirai (D27).
- The 9-device seed-0 results above *are* the router build, so the held-out devices support this too.

### F14. Score fusion did not beat its best member. [Negative, old threshold rule]
- Min-p fusion (D25) of MAD + tail + slog, HST on projections and AE + slog, with benign-calibrated p-values: held-out mean 80.0% against 87.3% for MAD + tail + slog alone.
- The weak members (HST) dilute the strong one.
- Paper use: report as tried-and-rejected. It supports "simple wins".

### F15. HST, the planned primary model, is strong on window features but weak on N-BaIoT's per-row features. [Solid, Negative for N-BaIoT]
- Mirai windows: 98.9% caught (100% with slog, 0 false alarms).
- N-BaIoT, held-out mean: 23.0% (plain), 21.3% (slog), 36.3% (random projections, D24).
- Likely reason: HST cuts one feature at a time over 115 correlated features. N-BaIoT also has many near-constant features, which waste cuts.
- Open decision for the paper: keep HST as the primary model for the *window* features (where it works and matches the plan), or move RobustZ to primary. This must be decided before Phase 3, because the ablation matrix uses the primary model.

### F16. The update rule (Phase 2) behaves as designed on real data: the attack is never learned, and the ramp-up before the alert is purged. [Preliminary: one capture, compressed time]
- Unit tests prove the required properties:
  - an obviously anomalous window is never committed;
  - windows before an alert are purged;
  - the drift budget halts commits when exceeded, including a boiling-frog ramp that only the *cumulative* budget catches;
  - under `gated` and `full` a scan never reaches the detector or the profile cache, while `naive` learns it.
- Full pipeline on Mirai (HST, full rule, 10 min quarantine instead of 24 h):
  - 134 live windows; 88 alerts after k-of-n smoothing (90 raw);
  - all attack windows labelled `suspected_attack`, **0 committed**;
  - 13 benign windows committed, 29 purged by the alert's taint, 92 rejected;
  - 0 drift notices.
- Explanations read like "ARP requests +5,149 IQRs".
- Evidence: `results/pipeline_kitsune_mirai_hst_full/`, README log 19–20.
- Caveats:
  - The capture is too short for day-scale budgets, so the drift budget is not really exercised.
  - No benign drift event, so RQ4's `suspected_benign_drift` state is untested on real data.

### F17. Most remaining false positives come from benign drift, which motivates the update rule. [Solid on Danmini]
- 0.37% of Danmini's *later* benign test rows fall outside the bootstrap range. Any model frozen after bootstrap that asks "is this outside what I've seen?" has a false-positive floor of about that size.
- Continual learning through the quarantine (D18) is the intended remedy. This links the detector results to RQ2.

### F18. Independent test on the unused Kitsune captures: attacks are caught, but frozen models raise many false alarms on very steady devices, because the benign traffic drifts slowly out of a narrow bootstrap range. [Solid for what it shows; small samples]
- Setup: frozen front-runners plus HST; all rules fixed before the run (D29); 28 window features.
- **3 of 8 captures were skipped by the pre-declared rule.** Active wiretap, ARP MitM and fuzzing have only 21–34 benign windows before the attack, fewer than the 40 needed for 20 bootstrap and 10 validation windows at a 50/30 split.
- Attacks caught at the validation threshold (share of attack windows):

  | Capture | Benign test / attack windows | RobustZ | MAD + tail + slog | AE + slog | KitNET | HST |
  |---|---|---|---|---|---|---|
  | OS scan | 32 / 3 | 100% | 100% | 100% | 100% | 100% |
  | SSDP flood | 17 / 3 | 100% | 100% | 100% | 100% | 100% |
  | SSL renegotiation | 8 / 38 | 92.1% | 81.6% | 94.7% | 100% | 92.1% |
  | SYN DoS | 21 / 5 | 100% | 100% | 80% | 100% | 100% |
  | Video injection | 13 / 11 | 63.6% | 81.8% | 63.6% | 81.8% | 45.5% |

- False alarms per day:

  | Capture | RobustZ | MAD + tail + slog | AE + slog | KitNET | HST |
  |---|---|---|---|---|---|
  | OS scan | 270 | 90 | 270 | 360 | 270 |
  | SSDP flood | 2,711 | 2,033 | 2,711 | 2,711 | 1,864 |
  | SSL renegotiation | 1,080 | 1,440 | 1,080 | 1,800 | 360 |
  | SYN DoS | 411 | 411 | 137 | 686 | 960 |
  | Video injection | 0 | 0 | 0 | 0 | 0 |

  With 8–32 benign test windows, one false alarm is 90–360 per day, so these numbers are very coarse.
- **Why the false alarms (diagnosed on SSDP, then SSL).**
  - In SSDP, all 17 benign test windows come *before* the attack, so this is not post-attack traffic.
  - RobustZ's score climbs steadily from the start of validation to the attack: about 0.48 in bootstrap, 0.62 in validation, 0.76 in test benign, 0.87 in the attack.
  - The features that move are small, smooth shifts:
    - packet size mean 771 → 788 bytes;
    - UDP share 0.76 → 0.72;
    - mean inter-arrival 0.86 → 1.10 ms;
    - top-3-port share 0.73 → 0.86.
  - These are not labelling errors: attack fraction is 0 in every one of these windows. This camera's video stream is so steady that 20 minutes of bootstrap give an extremely narrow normal range, and ordinary slow drift leaves it within minutes.
  - SSL renegotiation shows the same pattern. On OS scan and SYN DoS the false alarms are isolated windows instead.
- **Interpretation.** A frozen model with a short bootstrap cannot tell a steady device's slow drift from an attack. The attacks are still separated from benign traffic in ranking terms (e.g. SSDP attack windows score 0.86–0.88 against at most 0.77 for benign). The failure is the frozen threshold and the narrow scales. This is direct, independent evidence for the project's premise (RQ2): the model must keep learning, safely.
- **Caveat for the update rule.** With the current gate, drifted windows scoring above `tau_admit` are never committed, so a slow benign drift like this could be locked out. Measuring that is improvement I3.
- Evidence: `results/kitsune_suite_<capture>/`, `results/kitsune_suite_summary/`.

### F19. Are the models memorising? Not in the usual sense. The real risks are design overfitting and dataset artefacts, and each has a check. [Analysis]
- **Why this isn't ordinary memorisation.**
  - Models never see attack data.
  - Splits are in time order, so no future data is used.
  - Thresholds come from benign validation data only.
  - Configurations are frozen before held-out runs.
  - There is a test that shuffling future data doesn't change past scores.
- **Risk 1, design overfitting.**
  - Danmini and Mirai shaped D22–D27.
  - Mitigation: the 8 held-out N-BaIoT devices (F4, F7) and the 8 independent Kitsune captures (F18).
  - One documented deviation: top-3 mean was chosen over the pre-declared winner (2nd-largest) because of false positives (D27).
- **Risk 2, dataset artefacts.**
  - The flood signal was checked and is real (F10).
  - An untested broader risk: N-BaIoT's benign and attack files were recorded in separate sessions, so session differences could be detectable. The independent Kitsune captures, where benign and attack share one session, address this.
- **Risk 3, random-sample noise.** Multi-seed run (Pending).

### F20. Multi-seed check: the differences between models are not sampling noise. [Solid]
- 9 N-BaIoT devices × 3 seeds, tie-safe thresholds. A seed changes which attack rows are sampled (and model initialisation).
- The largest change for any device and model is 0.38 points in attacks caught; false-positive rates do not change.
- Held-out 8 devices, mean over seeds:

  | Model | Caught at the threshold | Test FPR | TPR at FPR 1e-3 | pAUC@0.01 |
  |---|---|---|---|---|
  | RobustZ | 87.5% | 0.13% | 80.0% | 97.7 |
  | MAD + tail + slog | 82.4% | 0.06% | **89.9%** | **98.1** |
  | KitNET | 79.9% | 0.10% | 82.4% | 92.0 |
  | AE + slog | 73.0% | 0.08% | 73.9% | 90.5 |

- The trade-off in F8 holds across seeds.
- Remaining uncertainty is device-to-device, not seed-to-seed.

### F21. New dataset (UNSW IoT, 5 real devices, 6 days): the first run exposed a data artefact, and the cleaned result is harder than N-BaIoT. [Solid; D30]
- **Capture gap.** The first run showed about 590 false alarms per day on two cameras. Cause: a 14 h capture gap between the benign and attack pcaps (2018-05-31 23:00 to 06-01 13:30 local), filled with empty windows. Both cameras went "silent" at exactly the same minutes.
- **Fix.** Windows in which *no* device has traffic are dropped. This is a label-free rule.
- **Cleaned result**, pre-change reference, buffers fixed (D35):
  - attacks caught: RobustZ 70%, KitNET 70%, MAD 72%, AE 58%, EIF 50%, HST 2%;
  - false alarms 1–7 per day.
- **Per attack family:**
  - TCP SYN flood, SYN reflection and Smurf: caught 90–100% by the best models.
  - ARP spoofing: ≤45% (motivated D34).
  - UDP floods and SNMP reflection: **0% for every model**. They reach the device, but at 1–100 packets/s their volume stays inside what these devices do normally. This looks like a limit of 30 s volume features.
- **By attack rate:** 1 pkt/s attacks are caught 55% of the time (RobustZ), against 72–74% at 10–100 pkt/s.

### F22. ARP-spoofing features (D34) give the largest single gain so far on real-device data. [Preliminary: UNSW is now a development set for D34]
- UNSW, i2 → i3: MAD 79→85, RobustZ 70→81, KitNET 69→79, AE 56→69, with about 1–3 more false alarms per day.
- On the Kitsune suite every model improves too (e.g. HST 83→97, AE 87→94). That suite contains ARP MitM-style traffic only in a skipped capture, so this gain comes from the D31 + D34 feature set as a whole.
- Must be confirmed on a new dataset.

### F23. Regression rule (D33): every change re-checked on every dataset. Summary of ref → i3. [Solid]
- See the table under D35 in decisions.md.
- **D32 (resolution floor):** cuts false alarms on steady devices 4–6× (Kitsune suite: MAD 795→160, RobustZ 894→180 per day). It is neutral or positive on N-BaIoT (EIF +5.6 points) and Mirai (RobustZ's one false alarm removed).
- **D31 (inbound features):** mixed on its own (HST up, EIF down). It is kept because i3 as a whole is better or equal on every dataset except two flagged, documented items.
- The regression suite also caught a configuration bug (D35) that had silently cut MAD to 21% on N-BaIoT.

### F24. Model size and per-packet cost (laptop, Python). [Preliminary: RQ1 needs router numbers]
- Scoring state at about 33–36 window features:

  | Model | Size |
  |---|---|
  | RobustZ | 0.3 KB |
  | MAD | 0.27 KB |
  | KitNET | 1.8–2.4 KB |
  | AE | 2.5 KB |
  | EIF | 200–600 KB |
  | HST | 550 KB |

- Score time per 30 s window: RobustZ 3–6 µs, MAD 6–11 µs, AE 8–12 µs, HST 40–70 µs, EIF 0.1–0.3 ms, KitNET 0.2–0.5 ms.
- Per-packet feature update: **2.6 µs per packet** in Python, about 380k packets/s, measured on 500k packets of the busiest UNSW device.

### F25. Unseen devices (UNSW October, D36): RobustZ is the most stable model; the feature changes transfer partially. [Solid: held out]
- Per-window attacks caught, reference → i3:

  | Model | Reference | i3 |
  |---|---|---|
  | RobustZ | 87.6% | 87.7% |
  | KitNET | 74.8% | 80.6% |
  | EIF | 44% | 53% |
  | HST | 29% | 49% |
  | AE | 77% | 70% |
  | MAD | 56% | 35% |

- ARP spoofing was already caught 100% by RobustZ and KitNET on these devices, so D34 adds nothing there (it did lift HST from 37% to 68%).
- Plain MAD breaks down on the Amazon Echo (about 2,470 false alarms per day). RobustZ's top-3 mean does not.
- False alarms are higher on the October attack days for every model; see D36 (unlabelled periodic activity on iHome, a 2 h silence on LIFX).

### F26. Persistence is the biggest single step toward the 95% target. [Solid on the hold-outs; D40]
- Several missed low-rate attacks (UDP floods, SNMP, ping of death) *were* visible: one new LAN peer, new senders, a new local port. But single benign windows like that occur about 3 times a day, the same rate as the alarm budget.
- Persistence separates them: benign novelty lasts one window, an attack's lasts its whole duration.
- Dual-channel alarms (raw OR 3-window minimum, half the budget each), per-attack detection i5 → i7:

  | Dataset | Results |
  |---|---|
  | Temporal hold-out (unsw_late, never inspected) | ECOD 94→100%; RobustZ, KitNET 94→97%; AE 71→97% |
  | UNSW June | ECOD 76→96%; RobustZ 80→94%; EIF 69→94%; AE 68→93% |
  | Unseen October devices | MAD 39→98%, AE 61→98%, RobustZ 94→96%, HST 46→94% |
  | Kitsune suite, Mirai | 100% kept |

- Cost: false alarms rise, roughly ×1–2 on UNSW (2–12 per day) and much more on the October attack days (see D36).

### F27. Where the ≥95% per-attack target stands (i7, benign-only thresholds). [Solid]

| Dataset | ≥95% | Below |
|---|---|---|
| Mirai, Kitsune suite | all 7 models | – |
| Temporal hold-out | ECOD 100, RobustZ 97.1, KitNET 97.1, AE 97.1 | MAD 94.3, EIF 94.3, HST 57 |
| UNSW June (development) | ECOD 95.5 | RobustZ 93.7, EIF 93.7, AE 92.8, MAD 86.5, KitNET 81.1 |
| UNSW October (unseen) | MAD 97.8, AE 97.8, RobustZ 95.7 | ECOD 93.5, HST 93.5, KitNET 89.1, EIF 87.0 |
| N-BaIoT (per row, no persistence) | – | RobustZ 88.9, ECOD 84.4, MAD 82.1, KitNET 79.9 |

- RobustZ is the only model at ≥93.5% on every window dataset. ECOD is the strongest on UNSW but needs a sketch version to fit a router (exact mode is 12 MB on N-BaIoT).
- The remaining misses are mainly UDP floods and SNMP on two June devices.

### F28. ECOD (D39) adds a strong, different model to the portfolio. [Preliminary]
- On window data with persistence it is the best on UNSW and the temporal hold-out.
- On N-BaIoT: 84.4% caught at 0.23% FPR (above the 0.1% target), pAUC@0.01 95.8.
- Scoring 0.03 ms per row. Exact-mode state (sorted training values) is too big for a router; a quantile-sketch variant is needed.
- **Router sketch (i8):** exact distinct-value counts for count features, and 257 quantiles plus 64 exact extremes per side for continuous ones. At most 175 KB (N-BaIoT, 115 features), against 22 MB exact, with the same per-attack detection everywhere: UNSW 95.5%, hold-out 100%, October 93.5%, Mirai and Kitsune 100%. N-BaIoT is even slightly better (86.6% against 84.4%).

### F29. RQ3 on real data: naive updating learns the attacks; the quarantine keeps them out when the detector sees them. [Solid; D41]
- UNSW June devices, real days, 24 h quarantine, alerts 2-of-3.
- **Naive updating** commits all 2,328 attack windows. RobustZ's attack detection falls from 84% to 31%; HST's from 22% to 13%.
- **Gated and full rules with RobustZ** commit **0** attack windows, under every variant (strict, k-purge, calibrated budgets).
- **Bound:** HST under the gated rule committed 114 attack windows (k-purge). The quarantine admits whatever scores below `tau_admit`, so its protection is bounded by the detector's sensitivity. A weak detector lets undetected attacks in.

### F30. RQ2 on real data: the update rule as specified barely adapts. Three concrete causes. [Solid; D41, D42]
1. **Strict quarantine.** "Commit only if no alert fired during the stay", with a 24 h delay and about 1+ false alarm per day, means almost nothing survives. RobustZ committed only 1,071 benign windows over 5 devices.
2. **Drift budgets.** The placeholder budgets (3 per day / 6 total) blocked every commit under `full`. Calibrating them from benign days (D42, 2× observed drift) gives budgets from 0.03 to 475 across devices. The CLAUDE.md drift measure (sum over features of |median shift| / IQR) is dominated by near-constant features, so it is unstable as a budget unit. This needs a robust per-feature-capped measure (D43, a deviation to document).
3. **Learning can raise false alarms.** With k-purge, the Netatmo camera went from 1.8 to 33 false alarms per day after learning (naive: 48). The other devices were unchanged or better. So *what* is learned matters, not just whether attacks are kept out.

The paper's novelty claims (RQ2 to RQ4) depend on fixing these. They are design questions for the update rule, not detector questions.

### F31. Making adaptation safe: scales that only grow (D44), and a fixed drift budget (D43). [Solid on UNSW June]
- Two estimator and modelling problems stopped the full rule:
  1. *The budget compared an exact median with a histogram median*, so binning error looked like drift and blocked the first commit on every device (fixed).
  2. *RobustZ became more sensitive as it learned.* Its scale (median to largest training value) shrinks when learned windows pull the median up. Netatmo went from 1.8 to 33 false alarms per day.
- With histogram-consistent budgets (capped-mean, 2× benign drift) and `monotone_scales` (no scale below its bootstrap value), the full rule learns 961–1,244 benign windows per device, commits **0** attack windows, raises no false drift notices, and false alarms match frozen (5.0 vs 4.8 per day; Netatmo back to 1.75).
- Learning did not *reduce* false alarms on these days. All remaining ones on Samsung and WEMO switch fall in one benign event: the network coming back after the capture gap (ARP replies, failed TCP, new domains), which no past data could have prepared for.

### F32. RQ4 on real data: "suspected attack" is precise, "benign drift" is rarely recognised. [Solid on UNSW June]
- Alerted windows, 5 devices, RobustZ full rule:

  | Truth | → suspected_attack | → suspected_benign_drift |
  |---|---|---|
  | Attack | 1,510 | 207 |
  | Benign | 45 | 10 |
  | Post-attack guard | 30 | 59 |

- Precision of "suspected attack": 95%.
- Only 18% of benign alarms are labelled drift: the reconnection event raises *diversity* features (new domains, failed TCP, ARP replies), which the volume-vs-diversity heuristic reads as an attack.
- This is a documented failure mode of the heuristic (CLAUDE.md: report where it fails). A restart signature (many devices at once, right after a capture/network gap) is a candidate refinement.

### F33. RQ3 boiling-frog experiment: naive updating is fully poisoned; the gated and full rules keep the final attack detected. [Preliminary: 2 devices, replayed days; D45]
- **Setup.** 2 bootstrap days, 1 validation day, 14 replayed benign days with chaff growing ×(1+α) per day, then the real attack at the full rate. Variants: volumetric (10 pkt/s UDP to a new or a known destination) and behavioural (0.2 new destinations/s), each at α = 0.05 (CLAUDE.md range) and α = 0.3 (accelerated). Detector: RobustZ router; full rule as in F31.
- **Naive** learns all 3,360 chaff windows in every variant. Its detection of the final attack falls to 0–12% (frozen detects it at 90% of windows and 100% of bursts on TP-Link, and 90/100% for Samsung's behavioural attack).
- **Gated and full** detect the final attack exactly as well as frozen in every variant. They commit 0 chaff windows when the chaff is visible from day 1 (all α = 0.05 variants: the chaff starts at 48% of the final rate).
- **Drift budget:** with fast behavioural chaff on TP-Link (α = 0.3), the gated rule learned 711 chaff windows and the full rule 214. On Samsung the budget barely mattered (1,671 vs 1,658 learned), and the final attack stayed detected anyway, because new destinations stay new.
- **Limits:**
  - Samsung's own traffic hides a 10 pkt/s volumetric flood even from the frozen model (0%), so nothing can be protected there.
  - Replaying bootstrap days puts windows at the training extremes back in front of the model. On Samsung that alone gives 102 alerts per replay of 2018-05-28, so false alarms in this experiment are not comparable to F26/F31.
  - A single new destination does not change the scores (the "known destination" variant gave identical results), because volume features dominate the top-3.

### F34. RQ2/RQ4 with scripted benign drift (D46): the update rule protects but does not yet adapt usefully. [Preliminary: 3 devices, replayed days]
- **Setup.** 3 events injected at packet level on replay day 2 of 7: a firmware update (download, then a permanent new heartbeat server), an app reinstall (8 new domains and servers in 5 min), and a usage increase (application data ×2 from then on).
- **The changes the frozen model tolerates stay tolerated.**
  - TP-Link, firmware update: 21–24 alarms on the event day, then about 0.7 per day.
  - Usage increase: 0 alarms frozen and under full.
  - WEMO switch: 0 alarms for every event and rule.
- **Learning can *create* alarms on a sparse device.** The TP-Link plug's traffic is mostly keepalives. There, the gated rule went from 0 to 9 alarms per day after the reinstall and from 0 to 12.7 after the usage increase. The full rule went to 23 per day after the reinstall but stayed at 0 for usage. Monotone scales (D44) are not enough: the learned median shift and the sketch estimates on sparse features need investigation.
- **Persistent changes that look unusual are never learned.** The quarantine admits only windows scoring below `tau_admit`. A first usage simulation that also doubled ARP, ICMP and SYN packets gave about 42 alarms per day under every non-naive rule, indefinitely. By design (CLAUDE.md 2b), such changes need an operator decision (notice → rebase).
- **RQ4:** pure benign changes are mostly labelled `suspected_attack` (benign-drift share 4–30% on the TP-Link). Samsung is about 90% drift, but its alarms there are dominated by the replay artefact of F33.
- **Simulation flaws found and fixed** (commit log): the usage increase first duplicated SYN, FIN and RST packets, then ARP and ICMP, which turned volume growth into fake connection and ARP anomalies.
- **Open design questions for the update rule** (affect the RQ2/RQ4 claims):
  1. A pathway for persistent benign change, e.g. accept a shift after N days of consistent drift-labelled alarms, within the budget.
  2. Learning that cannot make a sparse device's model stricter (median as well as scale).
  3. A better drift-vs-attack signal than volume-vs-diversity z-scores.

---

## 3. Methodological lessons (bugs that would have invalidated results)
Each one was found by a test or by inspecting data, and fixed with a regression test. This is worth a short paragraph in the paper.

1. **Min-max clipping (D14).** HST could not tell far-out values from the bootstrap maximum. Fixed with a 25% margin.
2. **Score squash `r/(1+r)` (D15).** This rounded huge MAD scores to exactly 1.0 and created artificial ties. Fixed with `log1p(r)/(1+log1p(r))`.
3. **Tie-unsafe thresholds (D28).** See F6.
4. **Isolation Forest range blind spot (D22).** See F3; the same failure class as (1).
5. **Run metadata.** It was originally recorded at the end of a run, so edits made during a run marked it "dirty". Now it's captured at the start, and generated outputs (results/, data/) are excluded from the dirty check.
6. **Capture gaps in multi-day data (D30).** Concatenated daily pcaps left a 14 h gap that became empty windows.
7. **Shared detector configs lost per-dataset buffer sizes (D35).** Found by the regression suite.
8. **Truncated capture files (D36).** A pcapng cut off mid-record crashed the reader; it now keeps every complete frame.
9. **Kitsune score cache.** It stored squashed values. It was converted exactly to raw RMSE maxima, with no ties introduced.

---

## 4. Threats to validity and limitations (list them all in the paper)
- **N-BaIoT is per row, not per window.** Its features are not ours, and its false-positive rates can't be expressed as alarms per day.
- **Little benign time.**
  - Mirai has about 75 min of benign traffic.
  - The Kitsune captures have 6–13 min of validation data.
  - So false-alarm-per-day numbers on window data are statistically weak.
  - The own-testbed capture (2–4 weeks) is needed.
- **Development-set reuse.** Danmini and Mirai shaped the designs. Report held-out-only numbers as the headline.
- **One run per configuration** so far. Multi-seed is pending, and it only varies the attack-row sample (and model initialisation). The benign split is fixed by time order.
- **Threshold transfer.** Realised test false-positive rates range from 0% to 0.46% against a 0.1% target. Validation sets that are too short or too clean make thresholds miss in both directions.
- **Session artefacts in N-BaIoT** (benign and attack recorded separately).
- **No real benign drift events yet.** RQ2 and RQ4 are untested on real data.
- **No poisoning experiments yet.** RQ3 is Phase 3.
- **Mimicry/evasion is out of scope** beyond a basic test (CLAUDE.md §8).
- **Speed and size are laptop Python estimates.** Router numbers come in Phase 4.
- **Fragile flood detection** (F10).

---

## 5. Research-question status

| RQ | What we have | What's missing |
|---|---|---|
| RQ1 Feasibility | Model sizes 0.25–1 KB (robust stats) to 550 KB (HST); µs-scale scoring on a laptop; a router build of RobustZ with int16 parameters and histogram sketches | C port, OpenWrt measurements (CPU, RSS, latency, iperf3), per-packet feature cost, feature-subset sweep |
| RQ2 Adaptation | Update rule implemented and unit-tested; evidence that false positives are drift-driven (F17) | Benign-drift simulator and long benign data; frozen vs naive vs gated vs full comparison |
| RQ3 Poisoning | Quarantine and budget tested on a synthetic boiling-frog ramp; attack never committed on Mirai (F16) | Boiling-frog injector, chaff-to-50%-FNR, days to poison |
| RQ4 Disambiguation | 88/88 Mirai alert windows → `suspected_attack` | Real benign drift events; confusion matrix |

---

## 6. Deviations from the plan made during this branch (to add to README §6)
- **RobustZ added** as a new detector (D27). It is not in the original plan.
- **Top-3 mean** chosen over the pre-declared winner, because of false positives (D27).
- **Tie-safe thresholds** (D28): changes how every threshold is set.
- **KitNET on N-BaIoT** uses N-BaIoT's 115 features, not raw packets (there are no pcaps).
- **Independent test** on the 8 unused Kitsune captures (D29), with a fixed device-choice rule and split.

---

## 7. Pending and open questions
1. Multi-seed results (seeds 0–2, 9 devices). Is RobustZ's lead at the threshold larger than seed noise? Held-out-only means.
2. Whether the update rule fixes the Kitsune false alarms (F18) without learning the attacks, and whether the 3 skipped captures can be used with a pre-declared shorter split.
3. Primary model for Phase 3: HST (plan) or RobustZ (results) (F15).
4. A threshold-transfer fix: longer validation, or a calibration margin chosen on benign data only (F8).

---

## 8. Candidate paper tables and figures
- **Table:** Mirai window-level baseline, all detectors (F2).
- **Table:** N-BaIoT, front-runners × 9 devices: attacks caught at threshold, test FPR, TPR at FPR 1e-3, pAUC@0.01, with mean ± seed spread (F7, F8).
- **Table:** per-attack detection with the 80%/60% ceiling explained (F7, F11).
- **Table:** before/after the IForest and MAD fixes on held-out devices (F3, F4).
- **Table:** size and speed (F12).
- **Figure:** the `MI_dir_L0.01_weight` distribution, benign against flood, showing the edge-of-range effect (F10).
- **Figure:** RobustZ's two-sided scales against one symmetric scale (D27).
- **Figure:** pipeline timeline on Mirai: score, state, update decision per window (F16).
- **Short methods note:** tie-safe thresholds (F6).

---

## 9. Reproducing
```bash
python -m rad.eval.baseline --config configs/baseline_kitsune_mirai.yaml            # F2
python -m rad.eval.nbaiot --config configs/nbaiot_fixes.yaml --device <Device>       # F3, F4
python -m rad.eval.nbaiot --config configs/nbaiot_frontrunners.yaml --seed 0 --device <Device>   # F7, F8, F12
python -m rad.eval.kitsune_suite --config configs/kitsune_suite.yaml               # F18
python -m rad.pipeline.run --config configs/pipeline_kitsune_mirai.yaml            # F16
python -m rad.eval.aggregate --prefix nbaiot_fixes --metric detection_rate@tau test_fpr@tau tpr@fpr=0.001   # cross-device tables
```
Each result folder holds the resolved config, `meta.json` (git commit, clean flag, versions) and the raw scores.
