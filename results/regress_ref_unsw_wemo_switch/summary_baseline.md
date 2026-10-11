# regress_ref_unsw_wemo_switch

Windows: {'windows': 15535, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 6505, 'test_attack': 378, 'excluded': 72}. Window length 30 s; features (30): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos.

FPR resolution on test = 1/6505 = 0.000154; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.1772 | 0.1349 | 0.7899 | 0.9128 | 0.5909 | 9.297 | 0.4947 | 210 | 0.7222 | 18 | 0.06592 | 0.01185 | 0.2637 |
| mad_tail_slog | 0.2143 | 0.172 | 0.8198 | 0.9195 | 0.6724 | 8.855 | 0.6825 | 180 | 0.8333 | 18 | 0.03541 | 0.006453 | 0.2344 |
| autoencoder_slog | 0.1164 | 0.07407 | 0.7805 | 0.9292 | 0.03492 | 8.855 | 0.4312 | 180 | 0.7778 | 18 | 1.416 | 0.007738 | 2.258 |
| iforest_ext_sparse_slog | 0.1614 | 0.01852 | 0.7982 | 0.9619 | 0.6905 | 0.4427 | 0.03968 | 1800 | 0.3333 | 18 | 0.4198 | 0.2363 | 640 |
| hst_slog | 0.02646 | 0.007937 | 0.6631 | 0.8705 | 0.9643 | 0.4427 | 0.007937 | 2.907e+04 | 0.1667 | 18 | 0.6234 | 0.05418 | 549.9 |
| kitnet | 0.1931 | 0 | 0.7514 | 0.8129 | 0.3412 | 10.18 | 0.6561 | 2.565e+04 | 0.6667 | 18 | 1.016 | 0.09929 | 1.496 |
