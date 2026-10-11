# regress_i7_unsw_oct_hue_bulb

Windows: {'windows': 20724, 'bootstrap': 5760, 'validation': 2873, 'test_benign': 12091, 'test_attack': 0, 'excluded': 0}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/12091 = 8.27e-05; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | nan | nan | nan | nan | -1.11e-16 | 66.69 | nan | nan | nan | 0 | 0.06931 | 0.004001 | 0.334 |
| mad_tail_slog | nan | nan | nan | nan | -1.11e-16 | 72.65 | nan | nan | nan | 0 | 0.05411 | 0.008737 | 0.2969 |
| autoencoder_slog | nan | nan | nan | nan | -8.674e-19 | 91.23 | nan | nan | nan | 0 | 1.674 | 0.01727 | 2.852 |
| iforest_ext_sparse_slog | nan | nan | nan | nan | -5.551e-17 | 84.32 | nan | nan | nan | 0 | 0.3775 | 0.3494 | 817.7 |
| hst_slog | nan | nan | nan | nan | -1.11e-16 | 71.46 | nan | nan | nan | 0 | 0.4463 | 0.06059 | 550 |
| kitnet | nan | nan | nan | nan | -5.551e-17 | 9.528 | nan | nan | nan | 0 | 1.986 | 0.2 | 2.18 |
| ecod_tail | nan | nan | nan | nan | -1.11e-16 | 69.55 | nan | nan | nan | 0 | 0.024 | 0.007062 | 855.3 |
