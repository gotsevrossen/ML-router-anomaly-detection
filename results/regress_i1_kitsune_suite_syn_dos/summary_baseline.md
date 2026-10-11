# regress_i1_kitsune_suite_syn_dos

Windows: {'windows': 106, 'bootstrap': 50, 'validation': 30, 'test_benign': 21, 'test_attack': 5}. Window length 30 s; features (31): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, n_in_peers, n_new_in_peers, n_in_ports.

FPR resolution on test = 1/21 = 0.0476; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.8 | 0.8 | 0.8995 | 0.8997 | 0.5665 | 411.4 | 1 | 0 | 0.001347 | 0.003976 | 0.2725 |
| mad_tail_slog | 0.8 | 0.8 | 0.8995 | 0.8997 | 0.5813 | 411.4 | 1 | 0 | 0.000704 | 0.007102 | 0.2422 |
| autoencoder_slog | 0.8 | 0.8 | 0.8995 | 0.8947 | 0.01599 | 137.1 | 0.8 | 30 | 1.408 | 0.007958 | 2.332 |
| iforest_ext_sparse_slog | 0.8 | 0.8 | 0.8995 | 0.8997 | 0.4671 | 411.4 | 1 | 0 | 0.1472 | 0.2562 | 256.1 |
| hst_slog | 0.4 | 0.4 | 0.6985 | 0.7995 | 0.8012 | 548.6 | 1 | 0 | 0.509 | 0.0865 | 549.9 |
| kitnet | 0.8 | 0.8 | 0.8995 | 0.8997 | 0.2038 | 548.6 | 1 | 0 | 0.03385 | 0.3593 | 2.127 |
