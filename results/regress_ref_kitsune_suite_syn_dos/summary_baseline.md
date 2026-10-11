# regress_ref_kitsune_suite_syn_dos

Windows: {'windows': 106, 'bootstrap': 50, 'validation': 30, 'test_benign': 21, 'test_attack': 5}. Window length 30 s; features (28): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets.

FPR resolution on test = 1/21 = 0.0476; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.8 | 0.8 | 0.8995 | 0.8997 | 0.5665 | 411.4 | 1 | 0 | 0.001583 | 0.004141 | 0.2461 |
| mad_tail_slog | 0.8 | 0.8 | 0.8995 | 0.8997 | 0.5813 | 411.4 | 1 | 0 | 0.0007476 | 0.008701 | 0.2188 |
| autoencoder_slog | 0.8 | 0.8 | 0.8995 | 0.8947 | 0.01871 | 0 | 0.8 | 30 | 2.026 | 0.01225 | 2.109 |
| iforest_ext_sparse_slog | 0.8 | 0.8 | 0.8995 | 0.8997 | 0.4878 | 274.3 | 1 | 0 | 0.1257 | 0.28 | 260.4 |
| hst_slog | 0 | 0 | 0.4975 | 0.599 | 0.6937 | 1097 | 1 | 0 | 0.2048 | 0.07157 | 549.9 |
| kitnet | 0.8 | 0.8 | 0.8995 | 0.8997 | 0.2091 | 685.7 | 1 | 0 | 0.03092 | 0.3355 | 1.883 |
