# regress_i2_kitsune_suite_video_injection

Windows: {'windows': 72, 'bootstrap': 30, 'validation': 18, 'test_benign': 13, 'test_attack': 11}. Window length 30 s; features (31): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, n_in_peers, n_new_in_peers, n_in_ports.

FPR resolution on test = 1/13 = 0.0769; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.2727 | 0.2727 | 0.6345 | 0.6283 | 0.5384 | 0 | 0 | nan | 0.002674 | 0.008426 | 0.2725 |
| mad_tail_slog | 0.2727 | 0.2727 | 0.636 | 0.6328 | 0.4992 | 0 | 0.2727 | 30 | 0.00125 | 0.01875 | 0.2422 |
| autoencoder_slog | 0.7273 | 0.7273 | 0.863 | 0.8565 | 0.01805 | 0 | 0.5455 | 150 | 1.43 | 0.01134 | 2.332 |
| iforest_ext_sparse_slog | 0.8182 | 0.8182 | 0.9086 | 0.9043 | 0.4171 | 0 | 0.4545 | 0 | 0.04895 | 0.1644 | 182.7 |
| hst_slog | 0.6364 | 0.6364 | 0.8173 | 0.8086 | 0.7808 | 0 | 0.3636 | 30 | 0.1294 | 0.04657 | 549.9 |
| kitnet | 0.9091 | 0.9091 | 0.9543 | 0.9522 | 0.2032 | 0 | 0.9091 | 0 | 0.0146 | 0.1787 | 1.939 |
