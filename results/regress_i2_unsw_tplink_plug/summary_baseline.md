# regress_i2_unsw_tplink_plug

Windows: {'windows': 15531, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 6426, 'test_attack': 441, 'excluded': 84}. Window length 30 s; features (33): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports.

FPR resolution on test = 1/6426 = 0.000156; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.873 | 0.8435 | 0.9629 | 0.9799 | 0.5809 | 11.2 | 0.9546 | 390 | 0.07031 | 0.002671 | 0.29 |
| mad_tail_slog | 0.5692 | 0.5624 | 0.9604 | 0.9943 | 0.5954 | 13 | 0.9955 | 30 | 0.06339 | 0.008017 | 0.2578 |
| autoencoder_slog | 0.8526 | 0.1701 | 0.9363 | 0.9874 | 0.04658 | 4.482 | 0.8617 | 240 | 1.472 | 0.008795 | 2.48 |
| iforest_ext_sparse_slog | 0.7324 | 0.1587 | 0.8856 | 0.9792 | 0.682 | 6.723 | 0.7392 | 2.568e+04 | 0.2601 | 0.2813 | 425.6 |
| hst_slog | 0.1497 | 0 | 0.6592 | 0.8186 | 0.9832 | 7.171 | 0.1497 | 2.568e+04 | 0.5723 | 0.0466 | 549.9 |
| kitnet | 0.9456 | 0.1769 | 0.9711 | 0.9882 | 0.2885 | 6.723 | 0.9592 | 240 | 1.71 | 0.1705 | 1.846 |
