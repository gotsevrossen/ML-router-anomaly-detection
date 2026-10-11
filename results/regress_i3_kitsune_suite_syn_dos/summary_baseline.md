# regress_i3_kitsune_suite_syn_dos

Windows: {'windows': 106, 'bootstrap': 50, 'validation': 30, 'test_benign': 21, 'test_attack': 5}. Window length 30 s; features (33): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts.

FPR resolution on test = 1/21 = 0.0476; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.8 | 0.8 | 0.8995 | 0.8947 | 0.5809 | 0 | 0.8 | 30 | 1 | 1 | 0.0008284 | 0.004597 | 0.29 |
| mad_tail_slog | 0.8 | 0.8 | 0.8995 | 0.8998 | 0.5813 | 137.1 | 0.8 | 30 | 1 | 1 | 0.0008452 | 0.007203 | 0.2578 |
| autoencoder_slog | 0.8 | 0.8 | 0.8995 | 0.8947 | 0.02149 | 274.3 | 0.8 | 30 | 1 | 1 | 1.24 | 0.01112 | 2.48 |
| iforest_ext_sparse_slog | 0.8 | 0.8 | 0.8995 | 0.8947 | 0.5384 | 137.1 | 0.8 | 30 | 1 | 1 | 0.07031 | 0.1716 | 263.6 |
| hst_slog | 0 | 0 | 0.4975 | 0.6992 | 0.7167 | 685.7 | 1 | 0 | 1 | 1 | 0.3371 | 0.08192 | 549.9 |
| kitnet | 0.8 | 0.8 | 0.8995 | 0.8997 | 0.1993 | 548.6 | 1 | 0 | 1 | 1 | 0.02578 | 0.2259 | 2.369 |
