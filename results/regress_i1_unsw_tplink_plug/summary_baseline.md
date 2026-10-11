# regress_i1_unsw_tplink_plug

Windows: {'windows': 15531, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 6426, 'test_attack': 441, 'excluded': 84}. Window length 30 s; features (33): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports.

FPR resolution on test = 1/6426 = 0.000156; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.8798 | 0.6553 | 0.9598 | 0.9803 | 0.5809 | 11.2 | 0.9569 | 240 | 0.06631 | 0.003065 | 0.29 |
| mad_tail_slog | 0.8617 | 0.2857 | 0.9685 | 0.9951 | 0.5954 | 13 | 0.9955 | 30 | 0.03859 | 0.007961 | 0.2578 |
| autoencoder_slog | 0.8526 | 0.1701 | 0.9363 | 0.9874 | 0.04658 | 4.482 | 0.8617 | 240 | 1.37 | 0.008249 | 2.48 |
| iforest_ext_sparse_slog | 0.7574 | 0.02948 | 0.897 | 0.9799 | 0.6946 | 10.31 | 0.8322 | 240 | 0.3088 | 0.2713 | 412.6 |
| hst_slog | 0.1497 | 0 | 0.6592 | 0.8186 | 0.9832 | 7.171 | 0.1497 | 2.568e+04 | 0.543 | 0.04813 | 549.9 |
| kitnet | 0.9456 | 0.1769 | 0.9711 | 0.9882 | 0.2885 | 6.723 | 0.9592 | 240 | 1.738 | 0.169 | 1.846 |
