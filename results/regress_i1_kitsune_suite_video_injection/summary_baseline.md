# regress_i1_kitsune_suite_video_injection

Windows: {'windows': 72, 'bootstrap': 30, 'validation': 18, 'test_benign': 13, 'test_attack': 11}. Window length 30 s; features (31): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, n_in_peers, n_new_in_peers, n_in_ports.

FPR resolution on test = 1/13 = 0.0769; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.8182 | 0.8182 | 0.9086 | 0.9043 | 0.5913 | 0 | 0.6364 | 60 | 0.001183 | 0.004794 | 0.2725 |
| mad_tail_slog | 0.8182 | 0.8182 | 0.9086 | 0.9043 | 0.6291 | 0 | 0.8182 | 30 | 0.0005819 | 0.008968 | 0.2422 |
| autoencoder_slog | 0.7273 | 0.7273 | 0.863 | 0.8565 | 0.01805 | 0 | 0.5455 | 150 | 1.86 | 0.01485 | 2.332 |
| iforest_ext_sparse_slog | 0.8182 | 0.8182 | 0.9086 | 0.9153 | 0.4886 | 0 | 0.4545 | 150 | 0.0983 | 0.2068 | 191.4 |
| hst_slog | 0.6364 | 0.6364 | 0.8173 | 0.8086 | 0.7808 | 0 | 0.3636 | 30 | 0.3949 | 0.08122 | 549.9 |
| kitnet | 0.9091 | 0.9091 | 0.9543 | 0.9522 | 0.2032 | 0 | 0.9091 | 0 | 0.01996 | 0.2729 | 1.939 |
