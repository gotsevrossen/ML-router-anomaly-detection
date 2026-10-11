# regress_i3_unsw_late_netatmo_camera

Windows: {'windows': 18436, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 9706, 'test_attack': 126, 'excluded': 24}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/9706 = 0.000103; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 1 | 0 | 0.9843 | 0.9984 | 0.5607 | 1.484 | 0.9921 | 0 | 1 | 6 | 0.09589 | 0.004515 | 0.334 |
| mad_tail_slog | 1 | 0 | 0.9841 | 0.9983 | 0.5814 | 1.484 | 1 | 0 | 1 | 6 | 0.04822 | 0.01032 | 0.2969 |
| autoencoder_slog | 1 | 0.8016 | 0.9974 | 0.9997 | 0.006757 | 3.264 | 1 | 0 | 1 | 6 | 1.82 | 0.01163 | 2.852 |
| iforest_ext_sparse_slog | 1 | 0.8254 | 0.9979 | 0.9998 | 0.532 | 2.967 | 1 | 0 | 1 | 6 | 0.419 | 0.4551 | 770.6 |
| hst_slog | 0.8889 | 0.5 | 0.9839 | 0.9983 | 0.8348 | 1.187 | 0.8889 | 30 | 1 | 6 | 0.6901 | 0.06004 | 550 |
| kitnet | 0.9603 | 0 | 0.965 | 0.9775 | 0.2619 | 2.077 | 0.9603 | 30 | 1 | 6 | 2.141 | 0.18 | 1.918 |
