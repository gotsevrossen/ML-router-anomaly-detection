# regress_i3_kitsune_suite_os_scan

Windows: {'windows': 105, 'bootstrap': 44, 'validation': 26, 'test_benign': 32, 'test_attack': 3}. Window length 30 s; features (33): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts.

FPR resolution on test = 1/32 = 0.0312; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 1 | 1 | 1 | 1 | 0.2122 | 180 | 1 | 0 | 1 | 2 | 0.001678 | 0.004263 | 0.29 |
| mad_tail_slog | 1 | 1 | 1 | 1 | 0.1021 | 270 | 1 | 0 | 1 | 2 | 0.0007452 | 0.008854 | 0.2578 |
| autoencoder_slog | 1 | 1 | 1 | 1 | 0.008566 | 180 | 1 | 0 | 1 | 2 | 2.047 | 0.008797 | 2.48 |
| iforest_ext_sparse_slog | 1 | 1 | 1 | 1 | 0.4958 | 270 | 1 | 0 | 1 | 2 | 0.09068 | 0.2426 | 200.4 |
| hst_slog | 1 | 1 | 1 | 1 | 0.6044 | 180 | 1 | 0 | 1 | 2 | 0.3519 | 0.04766 | 549.9 |
| kitnet | 1 | 1 | 1 | 1 | 0.1455 | 360 | 1 | 0 | 1 | 2 | 0.01956 | 0.2314 | 2.689 |
