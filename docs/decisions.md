# Design decisions

This file records choices that affect the research claims or that the C port has to reproduce. Each entry gives the decision, why it was made, and its consequence.

## Phase 1a: parsing

**D1. DNS question name and rcode are read; nothing else in any payload is.**
"No payload inspection" (CLAUDE.md §2) rules out reading application data. The DNS feature group (queries, distinct domains, new domains, NXDOMAIN) still needs the query name and response code. These are plaintext protocol metadata that any router resolver already sees. Only UDP port 53 is decoded.
*Limitation:* DNS over TCP, DoT and DoH are invisible, so DNS features undercount for devices that use encrypted DNS. mDNS (5353) is not counted as DNS.

**D2. A packet belongs to the device iff the device's MAC is the Ethernet source ("out") or destination ("in").**
Broadcast or multicast frames that the device only *receives* are dropped, because they are not the device's conversation and would make features depend on other hosts. Frames the device *sends* to broadcast or multicast addresses are kept. An optional `target_ip` fallback exists for captures without usable MACs (raw IP, Linux SLL, captures upstream of the device).

**D3. "LAN peer" is an explicit, fixed list of ranges** (`device_filter.LAN_NETWORKS`): RFC 1918, IPv4 link-local, loopback, IPv4 multicast and limited broadcast, IPv6 ULA, link-local, multicast and loopback.
We do not use Python's `ipaddress.is_private`, because its definition changes between Python versions and the C port must match exactly. CGNAT space (100.64.0.0/10) counts as *not* LAN.

**D4. Volume is measured from the IP header length (`ip_len`), not the captured frame length.**
`ip_len` survives snaplen truncation and matches what conntrack-style router counters report. `cap_len` is kept for diagnostics only.

**D5. Out-of-order timestamps: keep capture order, count them, warn.**
Packets are never re-sorted, because re-sorting would require looking ahead (streaming rule). Phase 1b windowing must define how such a packet is assigned. Proposed rule: put it in the currently open window and never reopen a closed one.

**D6. `pkt_index` is the 0-based frame index in the original capture.**
It counts every frame, including skipped ones, so dataset per-packet labels can be joined by row number. It exists **only for evaluation** and must never be a model input.

**D7. Non-first IP fragments and snaplen-truncated L4 headers are kept with ports and flags set to -1.**
They still carry volume and destination information. Dropping them would bias volume features. They are counted in `stats.l4_undecoded`.

**D8. Ethernet/IPv4 ARP frames are kept as packet records** (`ip_version` 0, sender/target IPs in `src_ip`/`dst_ip`, opcode in `arp_op`).
In the Kitsune Mirai capture the infected device (`3c:33:00:98:ee:fd`) sent about 552k ARP frames during the attack against only 23.5k IP packets: Mirai's LAN scanning shows up mostly as ARP. An IP-only parser would hide most of the infection. ARP is header-only link-layer metadata, so this stays within "no payload inspection".
*Consequences for Phase 1b:* ARP records have no ports, flags or L4 protocol, so protocol fractions and port features must use IP records only, while volume and destination counts may include ARP. Phase 1b should add ARP features (e.g. ARP requests sent, distinct ARP target IPs) to the diversity group. Other ARP variants (non-Ethernet hardware, non-IPv4 protocol) are still counted in `skipped_non_ip`.

## Phase 1b: window features

The authoritative definitions of all 31 features, in order, are in the docstring of [window_features.py](../src/rad/features/window_features.py). The entries below cover choices that go beyond the CLAUDE.md feature table.

**D9. Windows are aligned to the Unix epoch** (`start = k * window_s`), not to the first packet. Windows with no traffic inside the capture span are emitted as all-zero vectors (context features still set).
Epoch alignment makes window boundaries identical across runs, captures and the C port. Empty windows are kept because silence is itself behaviour; skipping them would make the time axis depend on traffic. A late packet (timestamp before the open window) is counted in the open window and never reopens a closed one (completes D5).

**D10. Profile-dependent features are evaluated when a window closes, against the profile as committed at that moment.**
The extractor never writes to the profile cache. Each window returns a `WindowObservation` (its external IPs, destination ports, domains and service-port counts), and the update rule decides whether to `commit` it. Until Phase 2 exists, `CommitPolicy` provides `bootstrap` (first N windows, then frozen; the default), `always` (naive) and `never`. This is the seam the quarantine buffer will use, so the cache cannot be poisoned through a side door (CLAUDE.md §8).

**D11. All "distinct" counts and the profile cache are capped, first-seen-wins sets** (`CappedSet`): per window `window_set_cap` (4096); in the profile `max_ips`, `max_ports` and `max_domains`. Once a set is full, new items are dropped and counted as overflow, which is reported in meta.json.
This keeps memory static for the C port. An exact capped set was chosen over a Bloom filter because a Bloom filter's false positives would silently hide "new" destinations. First-seen order makes saturation deterministic.

**D12. Feature interpretations the plan left open:**
- *Out/in byte ratio* is `out_byte_frac = bytes_out / (bytes_out + bytes_in)`. It stays in [0, 1] instead of becoming unbounded when nothing comes in, which suits HST and a fixed-point C port.
- *Inter-arrival time* is measured to the device's previous packet even if that packet is in an earlier window, so a window holding one packet still has a meaningful gap.
- *External destination IPs* are non-LAN peers of packets the device **sends**. LAN scanning is captured by the ARP features (D8) and `lan_byte_frac`.
- *Prefixes* are /24 for IPv4 and /48 for IPv6.
- *Top-3 historical ports* use the **service port**, the lower of source and destination port. A device acting as a server (for example a camera serving RTSP) is then ranked by its own listening port rather than random client ports. Ties break toward the lower port number. Counts are cumulative over committed windows with no decay yet; revisit in Phase 2.
- *New connections* are TCP SYN-without-ACK packets in either direction. UDP "connections" are not counted.
- *Failed/half-open TCP* is `max(0, SYN_out − SYN/ACK_in) + max(0, SYN_in − SYN/ACK_out) + RST packets` within the window. It is an index of failure, not an exact count (a refused SYN counts once as unanswered and once for its RST), and it needs no lookahead.
- *Connection duration* is the time from the first SYN to the first FIN or RST on the same (local port, peer IP, remote port), for connections that closed in the window. Tracking is bounded by `conn_table_size` (1024) and `conn_timeout_s` (300 s).
- *Time of day* uses UTC plus a configured `tz_offset_h`, because pcaps carry no timezone. The weekday comes from integer day arithmetic (1970-01-01 was a Thursday) so the C port matches exactly.

## Phase 1c: detectors and baseline protocol

**D13. Baseline protocol: frozen detectors, a time-ordered split, and thresholds from benign validation only.**
Windows are split in time order into bootstrap (training), validation and test. Every detector is trained on bootstrap and then frozen; naive and gated updating are Phase 2/3 ablations. The alert threshold `tau` is the validation-score quantile that gives a target false-alarm rate (default 1/day). When validation is too short to resolve that rate, `tau` sits just above the highest validation score. Attack labels are used only for test metrics. They are never used for training, the threshold or the split.
Two settings are specific to the 2-hour Kitsune Mirai capture:
- *Time-of-day features are excluded.* Within 2 hours, time only increases, so a detector trained on the first 30 minutes would flag every later window for its clock alone. They belong back in on multi-day data.
- *HST `window_size` is 50 instead of 250.* river's HST scores 0 until its first reference window is full, so `window_size` must not exceed the 60 bootstrap windows.

A caveat follows from the data size. With roughly 45 benign test windows, the FPR resolution is about 0.02, so "TPR at FPR = 1e-3" is really TPR at zero false positives, and false alarms/day is measured on about 22 minutes. These numbers show that the pipeline works; they are not evidence of a low false-alarm rate.

**D14. Scaled detectors keep headroom around the bootstrap range** (`margin`, default 0.25: bootstrap [min, max] maps to [0.25, 0.75], clipped to [0, 1]).
With plain min-max scaling and clipping, a value far beyond anything seen in bootstrap is clipped onto the bootstrap maximum. HST then puts it in the same leaf as the most extreme benign window and cannot tell them apart (found by a test; see `test_hst_separates_values_far_beyond_bootstrap_range`). With headroom, novel magnitudes reach leaves that bootstrap left empty. The autoencoder uses the same scaling. Bounds are still fixed after bootstrap, as the C port needs.

**D15. Score normalisation.** HST (river) and Isolation Forest (original-paper score, `-score_samples`) are naturally in [0, 1]. Unbounded scores (autoencoder MSE, MAD's max robust z, KitNET RMSE) go through `L / (1 + L)` with `L = log(1 + r)`. This is monotone, so ranks and every reported metric are unchanged; it only puts all detectors on one scale for plots and later score fusion. The log matters: the first version used `r / (1 + r)`, which rounds every r above about 1e16 to exactly 1.0. On N-BaIoT, MAD's robust z over near-constant features reaches such values, so 59% of benign test rows tied at 1.0 and MAD's partial AUC fell to 0.49 because of ties, not because of the method (`test_squash_keeps_huge_scores_apart`).

**D16. Kitsune is fed only the target device's packets, and its window score is the maximum packet score in the window.**
This keeps the single-device scope (CLAUDE.md §2). Kitsune normally watches a whole network segment, which is a difference from its paper setting. The device's packets go to the vendored netStat/KitNET unmodified, with fields mapped exactly as Kitsune's own scapy parser maps them. KitNET trains on the packets of the bootstrap windows: the first 10% learn the feature map and the rest train the autoencoders. It is frozen afterwards, as Kitsune does by default. Kitsune-py runs at about 300–500 packets/s here, so its window scores are cached on disk. RQ1 should compare against Kitsune's published C++ throughput, not this Python port.

**D17. N-BaIoT is a per-row secondary benchmark on its own 115 features.** It has no timestamps or pcaps, so window features, false alarms/day and time to detect do not apply. Benign rows in file order are split 50/20/30 into bootstrap, validation and test. 2,000 rows are sampled (seeded) from each attack file. The threshold is set for FPR 1e-3 on validation.

## Phase 2: continual learning

**D18. Quarantine semantics** ([continual/quarantine.py](../src/rad/continual/quarantine.py)). These choices define what "committed" means in every RQ2/RQ3 result.
- *Order per window:* first release queued windows that are due (older than `t_delay_s`), then score the new window, then gate it. A window is always scored before anything learns from it.
- *Gating:* `score < tau_admit` → quarantined; `tau_admit ≤ score < tau_alert` → rejected (never learned, no alert); `score ≥ tau_alert` → alert, rejected.
- *The alert used for gating is the raw per-window score*, not the k-of-n smoothed alert of 2d. Gating should be conservative: one suspicious window is enough to stop learning, even if it is not enough to page the user.
- *On alert:* the `purge_k` most recently queued windows are purged immediately (the pre-attack ramp-up). With `taint_on_alert` (default, the literal reading of rule 4: "only if no alert fired during their stay") every other queued window is marked and purged when it falls due. A single alert therefore discards up to `t_delay_s` of queued learning. That is the price of the guarantee, and it is what RQ2 measures.
- *The profile cache is committed in the same step as the detector*, from the same queued item.
- *Bounded:* the queue holds at most `ceil(t_delay_s / window_s) + 1` windows (a static ring buffer in C). If irregular spacing ever fills it, the oldest item is released early and counted in `forced_releases`.

**D19. Drift budget and anchor model** ([drift_budget.py](../src/rad/continual/drift_budget.py), [anchor.py](../src/rad/continual/anchor.py), [sketch.py](../src/rad/continual/sketch.py)).
- *Drift* is `D(m) = Σ_j |m_j − median_anchor_j| / scale_j`. `scale` is the bootstrap IQR, falling back to a normal-equivalent mean absolute deviation and then 1.0 for constant features (same chain as MAD).
- *Medians are tracked with fixed-bin histograms*, with bins fixed at bootstrap (64 bins over the bootstrap range ± 50%, plus under/overflow bins). These are static arrays in C. A shift beyond the binned range saturates at the range edge, so measured drift has a ceiling; for budgets of a few IQR units that ceiling is never reached.
- *The fast profile is a decayed histogram* of bootstrap plus committed windows (half-life 1 day by default), so it follows what the fast model learned recently rather than its whole history.
- *Two budgets are checked before every commit.* Daily: the shift of the fast median since the start of the day must stay within `b_daily`. Cumulative: the shift against the anchor median must stay within `b_total`. A commit that would break either is refused and undone exactly (histogram counts are additive). Commits then stop, until the next day (daily) or until `rebase` (cumulative: anchor update or operator review). A `possible_slow_poisoning_or_major_change` notice is raised.
- *Refused windows get the outcome `blocked`*, a fifth outcome next to committed, quarantined, rejected and purged. It is kept separate because RQ3 needs to count what the budget stopped. Blocked windows are dropped, not re-queued, because re-queuing would only postpone the same shift.
- *The anchor is a second detector instance*, frozen at bootstrap by default. With `update_every_s` (e.g. weekly), it learns a period's committed windows at the period boundary, and only if that period had no alert and no drift notice. A weekly anchor that absorbs a slow attack is exactly the failure mode RQ3 should quantify against the frozen default.
- *The budget values are placeholders* until they are tuned on benign data only (Phase 3), e.g. as the largest daily and cumulative shifts seen in benign validation, plus a margin.

**D20. Disambiguation details** ([disambiguation.py](../src/rad/continual/disambiguation.py), [profile_stats.py](../src/rad/continual/profile_stats.py)). CLAUDE.md calls this a hypothesis under test, so these choices are what RQ4 evaluates.
- *Robust z is measured against the committed profile*: the decayed committed-data median (the same `RobustProfile` the drift budget uses) divided by the bootstrap-fixed scale. A z of 5 always means "5 bootstrap IQRs from what was recently committed".
- *Groups.* `F_vol` = bytes and packets in and out. `F_div` = new external IPs, new destination ports, new domains, the failed-TCP index, distinct external prefixes, and distinct ARP targets (added per D8).
- *Aggregation.* `z_vol` is the maximum |z| (a volume drop can be benign too, e.g. a camera switched off). `z_div` is the maximum upward z (less diversity is not attack-like).
- *Tie-breaks.* An alert with `z_div > tau_div` is an attack, otherwise an alert where volume dominates is benign drift. An alert that neither rule explains is called `suspected_attack`: the fail-safe is to never label an unexplained alert benign.
- *Top features* rank all features by |z| against the same profile, so explanations and states use the same reference.

**D21. Pipeline and output record** ([pipeline/stream.py](../src/rad/pipeline/stream.py), [pipeline/run.py](../src/rad/pipeline/run.py)).
- *The stream has three phases.* Bootstrap windows are committed to the profile cache and bootstrap the detector(s). Validation windows are scored by the bootstrapped detector and never learned; they set `tau_alert` (target alarms/day) and `tau_admit` (a validation-score quantile, default 0.9). Live windows run the update rule.
- *Under `full`, gating uses max(fast, anchor)*, and `divergence` marks windows the frozen anchor flags but the fast model does not. That is the signature of a fast model that has been taught the attack.
- *Smoothing and threat.* `alert` is k-of-n smoothed (default 2 of 3) over raw window alerts. `threat_score = persistence × magnitude`: the share of the last n windows at or above `tau_alert`, times `(score − tau_admit) / (1 − tau_admit)` clipped to [0, 1]. Gating itself uses the raw per-window alert (D18).
- *`update_decision` is the decision when the window arrives* (quarantined or rejected; committed under `naive`; rejected under `frozen`, where nothing is learned). The final outcome (committed, purged or blocked) is known only later and is kept in the quarantine log and the run summary.
- *Known rough edge.* A feature whose bootstrap IQR is tiny (e.g. `conn_dur_mean` on the Mirai device) gets z-scores in the thousands. That is correct by the definition but makes `top_features` noisy. Revisit in Phase 3, for example with a scale floor tuned on benign data.

## Branch fix/iforest-mad-extrapolation: making IForest and MAD work on both datasets

**How these fixes were developed (read before citing the numbers).** Both failures were diagnosed on N-BaIoT Danmini doorbell and the Kitsune Mirai device, whose test results had already been seen. So those two are *development* sets for these fixes. All new parameter values were fixed before any run with them, and none was tuned on attack data. The Isolation Forest needed two attempts on the development set (headroom alone, then Extended IF). The evidence that the fixes generalise is the eight N-BaIoT devices that were never inspected (held-out), run once each with the same configuration (`configs/nbaiot_fixes.yaml`).

**D22. Isolation Forest variants** (`margin`, `hyperplane` in [iforest.py](../src/rad/models/iforest.py)). The sklearn version is unchanged and kept as the textbook baseline.
- *Headroom (`margin: 0.25`, `extra_depth: 4`).* Textbook IF draws each split between the node's training min and max, so a point far beyond the range shares a leaf with the most extreme training point. On Danmini, every attack row was outside the training range in at least one feature, yet every attack scored below the highest benign validation score. Headroom draws splits from the node range widened by 25% on each side; the 4 extra levels make up for splits that fall outside the data. On its own this barely helped on Danmini (0% → 0.15% detected).
- *Why headroom was not enough:* a typical attack row is out of range in only 23 of 115 features, so an axis-parallel split looks at a relevant feature only about 20% of the time.
- *Extended IF (`hyperplane: true`, Hariri et al. 2019).* Each split is a random hyperplane over all features, with the same headroom on the projected range, so every split sees every feature. Features are first standardised with the D23 tail-calibrated robust scale, so no single feature's units dominate the projection.
- *Cost.* About 10× slower to score than sklearn in this numpy version (≈1 ms/row with 115 features), and each node stores one normal vector of F floats. That is fine for 28 window features on a router; it needs measuring in Phase 4.

**D23. MAD with a tail-calibrated scale floor** (`tail_quantile: 0.999`, `tail_z: 3.0`): `scale_j ≥ Q_0.999(|x_j − median_j|) / 3` on training data.
- 22 of 115 N-BaIoT features have near-zero MAD, so their tiny benign fluctuations produced robust z around 1e36 and took over the maximum over features.
- With the floor, a feature's own extreme training deviation maps to about 3 units, so "how unusual" is comparable across features.
- This changes MAD from CLAUDE.md's literal formula, so the original stays the default and the floor is opt-in.

**Held-out check of D22/D23 (8 never-inspected N-BaIoT devices, one run each).** Mean attacks caught at the validation threshold: Extended IF 74.5% (sklearn IF 6.9%), MAD with tail floor 77.2% (MAD 0.004%). Mean benign test FPR at the threshold: 0.09% and 0.12% (target 0.1%). The fixes generalise; they are not artefacts of the development devices. Many devices top out at about 80% or 60%: that is the two Gafgyt floods (tcp, udp) that no detector catches, out of 10 (or 5) attack files.

## Router-friendly improvements for every detector (D24-D26)

Same rules as D22/D23: every value was fixed in the configs (`nbaiot_improved.yaml`, `baseline_kitsune_mirai_improved.yaml`) before any run, nothing was tuned on attack data, and the evidence is the held-out devices.

**D24. Preprocessing wrappers usable with any detector** ([preprocess.py](../src/rad/models/preprocess.py)), frozen after bootstrap.
- `slog`: x → sign(x)·log(1 + |x|). Window counts jump 100–1000× under attack, which squashes benign variation into a sliver of a linear range. In C: a lookup table.
- `project`: robust standardisation (the D23 scale), then 32 seeded random unit directions. Every projected feature mixes all inputs, so HST's single-feature cuts see attack shifts in any feature, for the same reason Extended IF works. In C: one fixed 32×F matrix-vector product per window (3,680 multiply-adds for N-BaIoT's 115 features, 896 for our 28).

**D25. Min-p fusion** ([fusion.py](../src/rad/models/fusion.py)). Members (MAD+tail+slog, HST on projections, AE+slog) train on the first 80% of the bootstrap windows. The last 20%, which they never saw, calibrate each member's score to a benign p-value: empirical below the 90th percentile, an exponential tail above it (peaks-over-threshold, in the style of SPOT, Siffer et al. 2017), so scores beyond the calibration maximum keep their order. The combined score is squash(−log min(1, m·min_i p_i)), computed in log space. It is unsupervised and benign-only. Cost: the members plus a sorted calibration array per member.

**D26. Size and speed are reported for every model.** `model_bytes()` estimates the C-port memory of the *scoring* state.
- HST: per node two uint32 masses; per internal node a uint16 feature and a float32 cut.
- Isolation Forest: about 18 bytes per node, plus (uint16 index + float32 weight) per non-zero hyperplane weight.
- Autoencoder and KitNET: float32 weights and biases.
- MAD: one median and one scale per feature.

Learning buffers are not counted, because the C port would use the D19 sketches instead. Sparse Extended IF (`hyperplane_features: sqrt`, about √F weights per split) cuts the forest to roughly a third of its dense size.

## RobustZ: the router-ready robust-statistics detector (D27-D28)

**D27. RobustZ** ([robust_z.py](../src/rad/models/robust_z.py)) is MAD+tail floor+slog, rebuilt around three findings on the development sets (Danmini, Mirai).
- *Two-sided, range-calibrated scales.* N-BaIoT rows from the two Gafgyt floods (tcp, udp) are outside the benign training range in about 5 features each (0.0–0.1% of them lie inside it, against 99.6% of benign test rows). Yet with one symmetric scale per feature their z was only about 5.94, because where the training range ends differs wildly between features: anywhere from z = 0 to z = 2,435. For `MI_dir_L0.01_weight` it is +0.6 above the median and −5.94 below. RobustZ gives each side of each feature its own scale, `s = max(MAD-type scale, extreme training deviation on that side / 3)`, so the training range ends at z ≤ 3 on every side, and a long tail on one side no longer inflates the other side's scale. Dropping the robust floor (so the edge lands at exactly z = 3) was slightly worse on the development sets (Danmini TPR@1e-3 0.80 instead of 1.00; Mirai 2/44 false alarms instead of 1/44), so the floor stays. A test caught the original description ("exactly z = 3") being wrong. Danmini attacks caught at the validation threshold went from 80% to 100%, and pAUC@0.01 from 0.958 to 0.989.
- *Mean of the 3 largest z instead of the maximum.* An attack pushes several features out of range; a benign outlier usually pushes one. Pre-declared options were max, 2nd-largest and top-3 mean. The declared rule (best development pAUC) would have picked 2nd-largest, but its validation threshold did not transfer (22% test FPR on Danmini), so top-3 mean was chosen instead. This is a documented deviation from the declared rule, made because of the false-positive priority.
- *Router state.* Scoring needs a median and two reciprocal scales per feature: 3F float32, or 3F int16 mantissas plus 3F int8 exponents (`precision: int16`, 9 bytes per feature, so 252 B for our 28 features). Learning with `stats: sketch` keeps one 64-bin histogram per feature plus running per-side extremes (about 7.7 KB for 28 features) instead of a 2,880-row window (about 315 KB in float32), and refreshes parameters lazily. On the development sets, sketch and int16 parameters were as accurate as exact float32.
- *Per-window cost:* F × (log lookup, subtract, multiply, compare) plus a partial top-3. About 1–1.6 µs per window for 28 features in vectorised numpy; a C loop should be faster still.
- *Remaining false positives are drift, not the scores.* 0.37% of Danmini's later benign test rows fall outside the bootstrap range, so any detector frozen after bootstrap that asks "outside the training range?" has that floor. Continual learning through the quarantine (D18) is what addresses it.

**D28. Tie-safe thresholds** (`metrics.threshold_for_fpr`). The old rule cut at the floor(fpr·n)-th highest validation score. When several validation scores tied at that cut, all of them alerted, so the real validation false-positive rate could far exceed the target. Discrete features make ties common: many benign rows sit exactly at a training extreme, so they score exactly z = 3. The cut now moves to the next distinct score whenever ties would break the budget. Every detector benefits. Results produced before this fix overstate false positives wherever ties occurred.

## Robustness checks, new data and the regression rule (D29-D33)

**D29. Independent test on the unused Kitsune captures** ([kitsune_suite.py](../src/rad/eval/kitsune_suite.py)). Rules fixed before the run:
- The monitored device is the MAC involved in the most attack-labelled frames. Labels pick the device; they never train or threshold anything.
- The device's benign windows before the first attack window are split 50% bootstrap and 30% validation; the rest is test. A capture is skipped if that gives fewer than 20 bootstrap or 10 validation windows. That rule skipped active wiretap, ARP MitM and fuzzing (21–34 pre-attack windows).
- Time-of-day features are excluded (captures are under 1 h).

Result:
- The frozen models caught the attacks on all 5 usable captures (video injection: 45–82%).
- False alarms were high on the steady devices: benign traffic drifted slowly out of a 10–20 minute bootstrap range (packet size 771 → 788 bytes, UDP share 0.76 → 0.72). These were not labelling errors.
- This motivated D32 and is evidence for the continual-learning premise (RQ2).
- These captures are now development data for anything changed after D29.

**D30. UNSW IoT attack traces as the next held-out dataset** ([unsw.py](../src/rad/eval/unsw.py), `configs/unsw.yaml`).
- Source: Hamza et al., ACM SOSR 2019, MIT-0 licence, iotanalytics.unsw.edu.au/attack-data.html. Real consumer devices, one pcap per day, per-device annotation intervals.
- Used: 5 devices (WEMO motion sensor, WEMO switch, Samsung camera, TP-Link plug, Netatmo camera); benign days 2018-05-28 to 05-31; attack days 06-01 and 06-02.
- 9 attack families at 1, 10 and 100 packets/s: ARP spoofing, TCP SYN, SYN reflection, Smurf, SNMP, SSDP, UDP, ping of death.
- Fixed before the first run:
  - split by time: 2 days bootstrap, 1 day validation, the rest test;
  - labels: a window is attack if it overlaps an annotated interval;
  - benign windows ending within 120 s after an attack are excluded;
  - `tz_offset_h = 10`; `is_weekend` excluded (weekday bootstrap, weekend attack day);
  - detector settings copied from earlier configs.
- `rad.eval.baseline` accepts per-window labels (`window_labels`) for interval-annotated data.

**D31. Inbound features** (`n_in_peers`, `n_new_in_peers`, `n_in_ports`, appended to `FEATURE_NAMES`).
- The artefact check showed that N-BaIoT's Gafgyt floods come from never-seen (spoofed or randomised) sources. Our window features only counted *destinations* the device contacts, so a flood *into* the device was invisible except through volume.
- `n_new_in_peers` counts senders absent from the committed profile, using a new bounded `in_peers` set. Like the other profile sets, it is committed only through the update rule.
- `n_in_ports` counts the local ports that received traffic (floods and scans aimed at the device).
- Feature count is now 34. Window files from before D31 lack these columns and are re-extracted under a `windows_tag`.

**D32. Resolution floor `min_scale`** (RobustZ, MAD, Extended IF standardisation; off by default).
- The scale is floored at `min_scale` in the detector's input units. With slog, 0.05 means a change of about 5% is one robust unit.
- Without it, a very steady device's tiny training spread turns ordinary slow drift into many units (D29).
- The value 0.05 was declared before any run with it. An attack's shift (×10 to ×1000, i.e. 2.3–6.9 slog units) is unaffected.

**D33. Regression rule** ([regress.py](../src/rad/eval/regress.py)).
- Every change is re-run on every dataset (Kitsune Mirai, 9 N-BaIoT devices, 5 Kitsune captures, UNSW) and compared with the previous reference.
- A drop of more than 2 points in attacks caught, or a rise of more than 50% in false positives, is flagged.
- The reference variant reproduces the pre-D31 feature set by excluding the new features (`exclude_features`), so it can be checked against the committed results.
- The detector portfolio (RobustZ, MAD+tail+slog, AE+slog, sparse Extended IF, HST+slog, KitNET) is improved and reported together, so several options remain for testbed experiments.

**D34. ARP-spoofing features** (`arp_rep_in`, `n_arp_conflicts`, appended; 36 features).
- On UNSW, ARP spoofing was caught at most 45% of the time. The window features counted only ARP requests the device *sends*, not the forged replies it *receives*.
- `n_arp_conflicts` counts sender IPs of received ARP packets claimed by a MAC other than the profile's committed binding, or by two or more MACs within one window.
- The binding map is bounded (`max_ips`) and is committed only through the update rule, like every profile set.
- *Status:* designed after seeing UNSW, so UNSW is now a development set for D34. Confirmation needs the next new dataset.

**D35. Detector buffers must cover the bootstrap.**
- The regression suite first ran one shared detector block, and MAD and Extended IF then kept their default 2,880-row buffers. On N-BaIoT (about 25k bootstrap rows) and UNSW (5,760 windows) they learned only the latest part of the bootstrap. MAD fell to 21% on N-BaIoT, against 82% in its own config.
- `detector_overrides` per dataset now set the buffers: 50,000 for N-BaIoT, as in its original configs, and 5,760 for UNSW.
- This was a configuration bug, not a tuning choice.
- On UNSW it raised MAD from 44% to 72% caught and Extended IF from 45% to 50%.

**Regression outcome (ref → i3 = D31 + D32 + D34)**, mean attacks caught at the validation threshold:

| Dataset | Change |
|---|---|
| UNSW | MAD 72→85, RobustZ 70→81, KitNET 70→79, AE 58→69, HST 2→12, EIF 50→47 |
| Kitsune suite | 5 of 6 models up (KitNET 96→100, HST 91→97). MAD 93→89, but with false alarms down from 795 to 160 per day; RobustZ false alarms down from 894 to 180 per day. |
| Mirai | Unchanged (100%); RobustZ's single false alarm removed |
| N-BaIoT | D31 and D34 do not apply. D32 is neutral, or +5.6 points for EIF. |

Flagged items, accepted and documented:
- MAD on the Kitsune suite: −3.8 points with 5× fewer false alarms, on 14 attack windows.
- EIF on UNSW: −2.6 points.

## Unseen devices, persistence and a rank-based model (D36-D40)

**D36. UNSW October batch: 5 unseen devices** (Hue bulb, Amazon Echo, Chromecast, iHome, LIFX bulb; `configs/unsw_oct.yaml`).
- The pcaps are not listed on the UNSW page but are served at the same URL pattern; they were verified as pcapng, and a made-up date returns NoSuchKey.
- Same rules as D30, with tz +11 (Sydney daylight time).
- The 10-24 pcap is truncated after frame 607,503. The reader now stops at a truncated record with a warning instead of crashing. The Hue bulb's attacks fall in the lost part, so it has no test attacks.
- On these devices, the October attack days show behaviour absent from the benign days. iHome has about 20-minute bursts every 2 hours from the first attack day on; LIFX has a 2 h silence. These raise false alarms for every model. They may be unlabelled activity of the lab setup. They are reported, not tuned away.

**D37. Service and LAN-peer novelty** (`n_new_in_ports`, `n_lan_peers`, `n_new_lan_peers`; 39 features).
- IoT devices serve few local ports and talk to few LAN hosts (the MUD idea of the dataset's authors).
- The features alone gave small gains (EIF +7, KitNET +2 points on UNSW). The z-score models scale these sparse counts by rare training bursts. That motivated D39 and D40.

**D38. Temporal hold-out** (`configs/unsw_late.yaml`): the June devices' later attack days (06-03, 06-05, 06-06). They were never inspected and were configured before download.

**D39. ECOD-tail detector** ([ecod.py](../src/rad/models/ecod.py)).
- Per feature, the two-sided empirical tail probability under the training data (Li et al., TKDE 2022), plus RobustZ's exponential tail beyond the training range. Score = top-3 mean.
- It ranks sparse novelty counts by rarity instead of by their largest training value.
- Exact mode stores the sorted training values. A router version would keep a quantile sketch plus the exact count of each feature's most common value (future work).

**D40. Persistence and dual-channel alarms** (evaluation and alert rule, every detector alike).
- `persistence: {k: 3}`: causal minimum over the last 3 contiguous windows. Isolated benign spikes vanish; sustained attacks keep their level from their 3rd window on.
- That alone lost short attacks (1–2 windows; Kitsune suite 100% → 67–83%) and lowered thresholds on quiet validation days.
- `mode: dual`: two channels, raw and 3-window minimum, each thresholded on benign validation at half the alarm budget. An alert is raised if either fires. This recovered the short attacks and kept the sustained-attack gains. It implements CLAUDE.md §5 2d's persistence smoothing in the benchmark. On a router: a ring buffer of 2 scores per device.
- All settings were declared before their runs.

**Per-attack (event) metric.** An attack episode (a contiguous run of attack windows) counts as detected if any of its windows alerts. It is reported next to per-window detection. The user's target is at least 95% detection at the benign-only threshold.

## Update rule on real days (D41-D43)

**D41. RQ2/RQ3 runner** ([adapt.py](../src/rad/eval/adapt.py)).
- Setup: UNSW June devices; RobustZ router and HST; rules frozen, naive, gated, full; 24 h quarantine; k-of-n alerts 2-of-3.
- Labels are joined afterwards for evaluation only. Capture gaps are skipped.
- Two quarantine variants, both declared before running:
  - *strict:* any alert during a window's stay purges it (CLAUDE.md's wording);
  - *k-purge:* an alert purges only the 10 windows before it.

**D42. Drift budgets calibrated on benign days.** `b_daily` = 2× the largest day-to-day median shift among the bootstrap and validation days; `b_total` = 2× the largest shift of any such day from day 1.

**D43. Capped-mean drift measure, and an estimator fix.**
- *Measure* (option, deviation from CLAUDE.md 2b): `mean_j min(|Δmedian_j| / IQR_j, 3)` instead of the sum. Calibrated sum-budgets ranged from 0.03 to 475 across five devices because near-constant features dominate the sum.
- *Bug fixed:* the cumulative check compared the exact bootstrap median (anchor) with a 64-bin histogram median (fast profile). The binning error alone measured as 0.7–1.4 units of "drift", so every device was blocked at its first commit. The anchor and the calibration now use the same histogram medians; a test asserts zero drift with no commits.
- *Result:* the full rule now commits 826–1,244 benign windows per device with RobustZ, commits 0 attack windows, and raises no notices on benign days.
- *Open:* the boiling-frog experiment (Phase 3) is what tests whether these budgets stop slow poisoning.

**D44. RobustZ `monotone_scales`** (option, used with learning).
- A side's scale never falls below its bootstrap value.
- RobustZ's upper scale is the distance from the median to the largest training value, so learning windows that raise the median shrank it, and the model became more sensitive than at bootstrap (Netatmo: 1.8 → 33 false alarms per day).
- With the option, adaptation can widen "normal" but not narrow it. How far it widens is bounded by the drift budget.
- Declared before the run that showed Netatmo back at 1.75 per day.
