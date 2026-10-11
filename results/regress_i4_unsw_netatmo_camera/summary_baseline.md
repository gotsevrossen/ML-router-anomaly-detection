# regress_i4_unsw_netatmo_camera

Windows: {'windows': 15537, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 6582, 'test_attack': 315, 'excluded': 60}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/6582 = 0.000152; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.9937 | 0.1968 | 0.9905 | 0.9974 | 0.5607 | 2.188 | 0.9937 | 0 | 1 | 15 | 0.06395 | 0.00305 | 0.334 |
| mad_tail_slog | 0.9968 | 0 | 0.986 | 0.9983 | 0.5814 | 2.625 | 0.9968 | 0 | 1 | 15 | 0.04899 | 0.00947 | 0.2969 |
| autoencoder_slog | 0.9968 | 0.2063 | 0.9833 | 0.998 | 0.006757 | 6.126 | 0.9968 | 0 | 1 | 15 | 1.868 | 0.01177 | 2.852 |
| iforest_ext_sparse_slog | 0.9841 | 0 | 0.983 | 0.9982 | 0.532 | 4.376 | 0.9937 | 30 | 1 | 15 | 0.3966 | 0.3879 | 770.6 |
| hst_slog | 0.7048 | 0 | 0.9113 | 0.9384 | 0.8348 | 3.938 | 0.8667 | 30 | 1 | 15 | 0.472 | 0.05095 | 550 |
| kitnet | 0.9778 | 0.2 | 0.981 | 0.988 | 0.2619 | 2.188 | 0.9778 | 0 | 1 | 15 | 1.606 | 0.1472 | 1.918 |
