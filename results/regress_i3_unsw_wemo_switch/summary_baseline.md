# regress_i3_unsw_wemo_switch

Windows: {'windows': 15535, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 6505, 'test_attack': 378, 'excluded': 72}. Window length 30 s; features (35): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts.

FPR resolution on test = 1/6505 = 0.000154; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.2989 | 0.2222 | 0.8686 | 0.98 | 0.5915 | 9.297 | 0.8095 | 0 | 0.06377 | 0.00355 | 0.3076 |
| mad_tail_slog | 0.1931 | 0.1508 | 0.8543 | 0.9686 | 0.6724 | 8.855 | 0.8148 | 30 | 0.04698 | 0.007228 | 0.2734 |
| autoencoder_slog | 0.2937 | 0.209 | 0.8506 | 0.973 | 0.03237 | 8.855 | 0.7487 | 0 | 1.715 | 0.009338 | 2.629 |
| iforest_ext_sparse_slog | 0.0291 | 0.005291 | 0.809 | 0.9677 | 0.6676 | 3.985 | 0.1349 | 1800 | 0.3239 | 0.3109 | 660.5 |
| hst_slog | 0.3254 | 0.01058 | 0.7411 | 0.9048 | 0.9512 | 1.771 | 0.1984 | 210 | 0.4267 | 0.04686 | 549.9 |
| kitnet | 0.3598 | 0.1667 | 0.8352 | 0.9004 | 0.3134 | 10.18 | 0.8228 | 0 | 1.47 | 0.1707 | 1.822 |
