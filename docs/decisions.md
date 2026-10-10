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
