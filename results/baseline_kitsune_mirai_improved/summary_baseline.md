# baseline_kitsune_mirai_improved

Windows: {'windows': 239, 'bootstrap': 60, 'validation': 45, 'test_benign': 44, 'test_attack': 90}. Window length 30 s; features (28): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets.

FPR resolution on test = 1/44 = 0.0227; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|
| hst_slog | 1 | 1 | 1 | 1 | 0.9242 | 0 | 1 | 0 | 1.622 | 0.1797 | 549.9 |
| hst_proj | 1 | 1 | 1 | 1 | 0.9535 | 65.45 | 1 | 0 | 0.5607 | 0.1701 | 553.6 |
| autoencoder_slog | 1 | 1 | 1 | 1 | 0.01299 | 65.45 | 1 | 0 | 11.63 | 0.02492 | 2.109 |
| iforest_ext_slog | 1 | 1 | 1 | 1 | 0.5056 | 65.45 | 1 | 0 | 0.5858 | 0.305 | 761.2 |
| iforest_ext_sparse_slog | 1 | 1 | 1 | 1 | 0.4957 | 65.45 | 1 | 0 | 0.3103 | 0.3241 | 253.7 |
| mad_tail_slog | 1 | 1 | 1 | 1 | 0.613 | 65.45 | 1 | 0 | 0.001607 | 0.02329 | 0.2188 |
| kitnet_windows | 1 | 1 | 1 | 1 | 0.3137 | 65.45 | 1 | 0 | 0.1397 | 0.541 | 1.379 |
| fusion | 1 | 1 | 1 | 1 | 0.766 | 65.45 | 1 | 0 | 2.578 | 0.2222 | 556.1 |
