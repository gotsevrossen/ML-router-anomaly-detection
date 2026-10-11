# regress_i3_kitsune_suite_video_injection

Windows: {'windows': 72, 'bootstrap': 30, 'validation': 18, 'test_benign': 13, 'test_attack': 11}. Window length 30 s; features (33): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts.

FPR resolution on test = 1/13 = 0.0769; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.9091 | 0.9091 | 0.9543 | 0.9522 | 0.5384 | 0 | 0.9091 | 30 | 1 | 1 | 0.0007763 | 0.003757 | 0.29 |
| mad_tail_slog | 0.9091 | 0.9091 | 0.9543 | 0.9522 | 0.4992 | 221.5 | 0.9091 | 30 | 1 | 1 | 0.0004895 | 0.007821 | 0.2578 |
| autoencoder_slog | 1 | 1 | 1 | 1 | 0.01718 | 0 | 0.9091 | 30 | 1 | 1 | 1.039 | 0.008222 | 2.48 |
| iforest_ext_sparse_slog | 0.9091 | 0.9091 | 0.9543 | 0.9632 | 0.417 | 221.5 | 0.9091 | 30 | 1 | 1 | 0.04721 | 0.186 | 177 |
| hst_slog | 0.9091 | 0.9091 | 0.9543 | 0.9632 | 0.7088 | 221.5 | 0.9091 | 30 | 1 | 1 | 0.3165 | 0.07671 | 549.9 |
| kitnet | 1 | 1 | 1 | 1 | 0.1961 | 221.5 | 1 | 0 | 1 | 1 | 0.01877 | 0.2236 | 2.17 |
