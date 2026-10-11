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
