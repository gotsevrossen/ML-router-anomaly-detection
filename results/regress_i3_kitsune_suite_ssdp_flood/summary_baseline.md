# regress_i3_kitsune_suite_ssdp_flood

Windows: {'windows': 82, 'bootstrap': 39, 'validation': 23, 'test_benign': 17, 'test_attack': 3}. Window length 30 s; features (33): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts.

FPR resolution on test = 1/17 = 0.0588; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 1 | 1 | 1 | 1 | 0.5518 | 0 | 1 | 0 | 0.001311 | 0.002984 | 0.29 |
| mad_tail_slog | 1 | 1 | 1 | 1 | 0.5809 | 169.4 | 1 | 0 | 0.0004866 | 0.00647 | 0.2578 |
| autoencoder_slog | 1 | 1 | 1 | 1 | 0.04782 | 2541 | 1 | 0 | 1.226 | 0.007049 | 2.48 |
| iforest_ext_sparse_slog | 1 | 1 | 1 | 1 | 0.5233 | 2372 | 1 | 0 | 0.06841 | 0.1696 | 240 |
| hst_slog | 0.6667 | 0.6667 | 0.8325 | 0.8968 | 0.8205 | 1355 | 1 | 0 | 0.3407 | 0.04176 | 549.9 |
| kitnet | 1 | 1 | 1 | 1 | 0.3706 | 2711 | 1 | 0 | 0.01673 | 0.1768 | 2.041 |
