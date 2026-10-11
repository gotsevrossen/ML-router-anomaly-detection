# regress_i2_kitsune_suite_ssdp_flood

Windows: {'windows': 82, 'bootstrap': 39, 'validation': 23, 'test_benign': 17, 'test_attack': 3}. Window length 30 s; features (31): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, n_in_peers, n_new_in_peers, n_in_ports.

FPR resolution on test = 1/17 = 0.0588; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 1 | 1 | 1 | 1 | 0.5518 | 0 | 1 | 0 | 0.0006605 | 0.002294 | 0.2725 |
| mad_tail_slog | 1 | 1 | 1 | 1 | 0.5809 | 169.4 | 1 | 0 | 0.0003679 | 0.004904 | 0.2422 |
| autoencoder_slog | 1 | 1 | 1 | 1 | 0.04641 | 2711 | 1 | 0 | 1.321 | 0.007234 | 2.332 |
| iforest_ext_sparse_slog | 1 | 1 | 1 | 1 | 0.4996 | 2711 | 1 | 0 | 0.09641 | 0.1868 | 243.9 |
| hst_slog | 1 | 1 | 1 | 1 | 0.9273 | 169.4 | 1 | 0 | 0.1689 | 0.04713 | 549.9 |
| kitnet | 1 | 1 | 1 | 1 | 0.3932 | 2711 | 1 | 0 | 0.01256 | 0.2042 | 1.885 |
