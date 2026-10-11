# regress_i1_unsw_netatmo_camera

Windows: {'windows': 15537, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 6582, 'test_attack': 315, 'excluded': 60}. Window length 30 s; features (33): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports.

FPR resolution on test = 1/6582 = 0.000152; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.9778 | 0 | 0.9793 | 0.9919 | 0.5607 | 2.188 | 0.9778 | 30 | 0.05572 | 0.002746 | 0.29 |
| mad_tail_slog | 0.8952 | 0.04127 | 0.9677 | 0.9905 | 0.5814 | 2.625 | 0.8952 | 180 | 0.04829 | 0.008919 | 0.2578 |
| autoencoder_slog | 0.9683 | 0.2032 | 0.978 | 0.9959 | 0.009727 | 3.5 | 0.9841 | 30 | 1.386 | 0.007067 | 2.48 |
| iforest_ext_sparse_slog | 0.9778 | 0 | 0.9834 | 0.9982 | 0.5167 | 4.813 | 0.9937 | 30 | 0.2854 | 0.2927 | 660.6 |
| hst_slog | 0.4952 | 0 | 0.7335 | 0.8247 | 0.9464 | 4.376 | 0.4952 | 270 | 0.4124 | 0.04455 | 549.9 |
| kitnet | 0.8444 | 0 | 0.9369 | 0.9575 | 0.2769 | 2.188 | 0.8444 | 1740 | 1.198 | 0.1162 | 1.619 |
