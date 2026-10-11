# regress_i1_baseline_kitsune_mirai_improved

Windows: {'windows': 239, 'bootstrap': 60, 'validation': 45, 'test_benign': 44, 'test_attack': 90}. Window length 30 s; features (31): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, n_in_peers, n_new_in_peers, n_in_ports.

FPR resolution on test = 1/44 = 0.0227; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 1 | 1 | 1 | 1 | 0.5986 | 65.45 | 1 | 0 | 0.0009596 | 0.003444 | 0.2725 |
| mad_tail_slog | 1 | 1 | 1 | 1 | 0.613 | 65.45 | 1 | 0 | 0.001193 | 0.005136 | 0.2422 |
| autoencoder_slog | 1 | 1 | 1 | 1 | 0.02679 | 65.45 | 1 | 0 | 6.406 | 0.01139 | 2.332 |
| iforest_ext_sparse_slog | 1 | 1 | 1 | 1 | 0.4963 | 65.45 | 1 | 0 | 0.3319 | 0.1698 | 259.3 |
| hst_slog | 0.9889 | 0.9889 | 0.9944 | 0.9987 | 0.8861 | 65.45 | 1 | 0 | 0.7925 | 0.06688 | 549.9 |
| kitnet | 1 | 1 | 1 | 1 | 0.2964 | 65.45 | 1 | 0 | 0.05789 | 0.1244 | 1.631 |
