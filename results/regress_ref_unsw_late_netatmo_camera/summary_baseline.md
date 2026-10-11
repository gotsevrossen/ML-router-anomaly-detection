# regress_ref_unsw_late_netatmo_camera

Windows: {'windows': 18436, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 9706, 'test_attack': 126, 'excluded': 24}. Window length 30 s; features (35): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/9706 = 0.000103; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 1 | 0 | 0.9843 | 0.9984 | 0.5607 | 1.484 | 0.9921 | 0 | 1 | 6 | 0.1112 | 0.004398 | 0.3076 |
| mad_tail_slog | 1 | 0 | 0.9841 | 0.9983 | 0.5814 | 1.484 | 1 | 0 | 1 | 6 | 0.0682 | 0.01079 | 0.2734 |
| autoencoder_slog | 1 | 0.7778 | 0.9966 | 0.9996 | 0.007322 | 2.671 | 1 | 0 | 1 | 6 | 2.059 | 0.02656 | 2.629 |
| iforest_ext_sparse_slog | 1 | 0.6746 | 0.9955 | 0.9995 | 0.5277 | 2.077 | 1 | 0 | 1 | 6 | 0.4516 | 0.3697 | 679.3 |
| hst_slog | 0.007937 | 0 | 0.5035 | 0.6476 | 0.9876 | 0 | 0 | nan | 0 | 6 | 0.5639 | 0.07144 | 549.9 |
| kitnet | 0.9603 | 0 | 0.9651 | 0.9776 | 0.2772 | 2.077 | 0.9603 | 30 | 1 | 6 | 1.83 | 0.178 | 1.76 |
