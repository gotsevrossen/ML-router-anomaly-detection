# regress_i1_unsw_wemo_switch

Windows: {'windows': 15535, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 6505, 'test_attack': 378, 'excluded': 72}. Window length 30 s; features (33): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports.

FPR resolution on test = 1/6505 = 0.000154; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.1772 | 0.1349 | 0.7899 | 0.9128 | 0.5915 | 9.297 | 0.4921 | 210 | 0.07367 | 0.003273 | 0.29 |
| mad_tail_slog | 0.2143 | 0.172 | 0.8198 | 0.9195 | 0.6724 | 8.855 | 0.6825 | 180 | 0.04368 | 0.006018 | 0.2578 |
| autoencoder_slog | 0.1508 | 0.09524 | 0.7775 | 0.9112 | 0.03494 | 8.855 | 0.3862 | 210 | 1.282 | 0.006481 | 2.48 |
| iforest_ext_sparse_slog | 0.08201 | 0.03704 | 0.7717 | 0.9196 | 0.6576 | 5.313 | 0.246 | 1800 | 0.2687 | 0.2314 | 695.4 |
| hst_slog | 0.07407 | 0.005291 | 0.743 | 0.8885 | 0.9719 | 0 | 0.005291 | 3810 | 0.5552 | 0.04971 | 549.9 |
| kitnet | 0.1931 | 0 | 0.7515 | 0.8124 | 0.3246 | 10.18 | 0.6561 | 2.565e+04 | 1.225 | 0.1292 | 1.697 |
