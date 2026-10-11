# regress_ref_baseline_kitsune_mirai_improved

Windows: {'windows': 239, 'bootstrap': 60, 'validation': 45, 'test_benign': 44, 'test_attack': 90}. Window length 30 s; features (28): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets.

FPR resolution on test = 1/44 = 0.0227; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 1 | 1 | 1 | 1 | 0.5986 | 65.45 | 1 | 0 | 0.001057 | 0.001941 | 0.2461 |
| mad_tail_slog | 1 | 1 | 1 | 1 | 0.613 | 65.45 | 1 | 0 | 0.001268 | 0.00428 | 0.2188 |
| autoencoder_slog | 1 | 1 | 1 | 1 | 0.01478 | 65.45 | 1 | 0 | 4.772 | 0.0123 | 2.109 |
| iforest_ext_sparse_slog | 1 | 1 | 1 | 1 | 0.4957 | 65.45 | 1 | 0 | 0.1953 | 0.08786 | 253.7 |
| hst_slog | 1 | 1 | 1 | 1 | 0.9242 | 0 | 1 | 0 | 0.5155 | 0.04821 | 549.9 |
| kitnet | 1 | 1 | 1 | 1 | 0.3137 | 65.45 | 1 | 0 | 0.03949 | 0.1115 | 1.379 |
