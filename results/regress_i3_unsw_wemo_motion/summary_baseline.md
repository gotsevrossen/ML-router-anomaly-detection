# regress_i3_unsw_wemo_motion

Windows: {'windows': 15537, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 6358, 'test_attack': 503, 'excluded': 96}. Window length 30 s; features (35): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts.

FPR resolution on test = 1/6358 = 0.000157; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.672 | 0.5308 | 0.8391 | 0.8757 | 0.5971 | 0.453 | 0.6024 | 0 | 0.05781 | 0.00243 | 0.3076 |
| mad_tail_slog | 0.8608 | 0 | 0.9238 | 0.9506 | 0.6442 | 2.265 | 0.829 | 270 | 0.03941 | 0.007274 | 0.2734 |
| autoencoder_slog | 0.159 | 0.1272 | 0.681 | 0.9183 | 0.02231 | 0.9059 | 0.1372 | 0 | 1.503 | 0.01893 | 2.629 |
| iforest_ext_sparse_slog | 0.33 | 0.1869 | 0.7154 | 0.9004 | 0.6551 | 0 | 0.1193 | 240 | 0.2352 | 0.2561 | 571.6 |
| hst_slog | 0.01988 | 0.003976 | 0.5235 | 0.6432 | 0.9808 | 1.359 | 0.01988 | 270 | 0.452 | 0.05104 | 549.9 |
| kitnet | 0.6103 | 0.1252 | 0.8113 | 0.8097 | 0.3023 | 0.453 | 0.5547 | 0 | 1.728 | 0.1666 | 1.861 |
