# regress_ref_kitsune_suite_os_scan

Windows: {'windows': 105, 'bootstrap': 44, 'validation': 26, 'test_benign': 32, 'test_attack': 3}. Window length 30 s; features (28): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets.

FPR resolution on test = 1/32 = 0.0312; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 1 | 1 | 1 | 1 | 0.5818 | 270 | 1 | 0 | 0.001479 | 0.004334 | 0.2461 |
| mad_tail_slog | 1 | 1 | 1 | 1 | 0.605 | 90 | 1 | 0 | 0.0008308 | 0.01113 | 0.2188 |
| autoencoder_slog | 1 | 1 | 1 | 1 | 0.006402 | 270 | 1 | 0 | 1.746 | 0.006199 | 2.109 |
| iforest_ext_sparse_slog | 1 | 1 | 1 | 1 | 0.5075 | 180 | 1 | 0 | 0.06153 | 0.2558 | 230.8 |
| hst_slog | 1 | 1 | 1 | 1 | 0.6403 | 270 | 1 | 0 | 0.3375 | 0.06827 | 549.9 |
| kitnet | 1 | 1 | 1 | 1 | 0.1661 | 360 | 1 | 0 | 0.03182 | 0.3698 | 2.02 |
