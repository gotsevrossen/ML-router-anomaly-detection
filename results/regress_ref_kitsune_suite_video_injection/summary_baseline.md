# regress_ref_kitsune_suite_video_injection

Windows: {'windows': 72, 'bootstrap': 30, 'validation': 18, 'test_benign': 13, 'test_attack': 11}. Window length 30 s; features (28): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets.

FPR resolution on test = 1/13 = 0.0769; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.8182 | 0.8182 | 0.9086 | 0.9043 | 0.5913 | 0 | 0.6364 | 60 | 0.0012 | 0.004297 | 0.2461 |
| mad_tail_slog | 0.8182 | 0.8182 | 0.9086 | 0.9043 | 0.6291 | 0 | 0.8182 | 30 | 0.000343 | 0.004529 | 0.2188 |
| autoencoder_slog | 1 | 1 | 1 | 1 | 0.01066 | 0 | 0.8182 | 30 | 1.928 | 0.007188 | 2.109 |
| iforest_ext_sparse_slog | 0.8182 | 0.8182 | 0.9086 | 0.9043 | 0.4785 | 0 | 0.6364 | 30 | 0.06732 | 0.3673 | 186.7 |
| hst_slog | 0.7273 | 0.7273 | 0.863 | 0.8565 | 0.7644 | 0 | 0.6364 | 30 | 0.3754 | 0.0822 | 549.9 |
| kitnet | 0.9091 | 0.9091 | 0.9543 | 0.9522 | 0.2031 | 0 | 0.8182 | 30 | 0.01676 | 0.3295 | 1.773 |
