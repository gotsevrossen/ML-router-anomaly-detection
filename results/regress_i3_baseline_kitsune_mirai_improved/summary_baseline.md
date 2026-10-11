# regress_i3_baseline_kitsune_mirai_improved

Windows: {'windows': 239, 'bootstrap': 60, 'validation': 45, 'test_benign': 44, 'test_attack': 90}. Window length 30 s; features (33): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts.

FPR resolution on test = 1/44 = 0.0227; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 1 | 1 | 1 | 1 | 0.5841 | 0 | 1 | 0 | 1 | 1 | 0.0009335 | 0.001918 | 0.29 |
| mad_tail_slog | 1 | 1 | 1 | 1 | 0.5889 | 65.45 | 1 | 0 | 1 | 1 | 0.00105 | 0.004966 | 0.2578 |
| autoencoder_slog | 1 | 1 | 1 | 1 | 0.03439 | 65.45 | 1 | 0 | 1 | 1 | 4.278 | 0.005788 | 2.48 |
| iforest_ext_sparse_slog | 1 | 1 | 1 | 1 | 0.51 | 65.45 | 1 | 0 | 1 | 1 | 0.1769 | 0.07913 | 271 |
| hst_slog | 1 | 1 | 1 | 1 | 0.8724 | 0 | 1 | 0 | 1 | 1 | 0.4711 | 0.04676 | 549.9 |
| kitnet | 1 | 1 | 1 | 1 | 0.2837 | 65.45 | 1 | 0 | 1 | 1 | 0.04142 | 0.1349 | 1.822 |
