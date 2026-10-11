# regress_i7_unsw_late_netatmo_camera

Windows: {'windows': 18436, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 9706, 'test_attack': 126, 'excluded': 24}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/9706 = 0.000103; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 1 | 0 | 0.9844 | 0.9984 | -1.11e-16 | 1.78 | 1 | 0 | 1 | 6 | 0.07723 | 0.003286 | 0.334 |
| mad_tail_slog | 1 | 0 | 0.9841 | 0.9983 | -1.11e-16 | 2.671 | 1 | 0 | 1 | 6 | 0.04739 | 0.008638 | 0.2969 |
| autoencoder_slog | 1 | 0.6905 | 0.996 | 0.9996 | -4.337e-19 | 10.39 | 1 | 0 | 1 | 6 | 1.583 | 0.01076 | 2.852 |
| iforest_ext_sparse_slog | 0.9921 | 0.8889 | 0.9978 | 0.9998 | -5.551e-17 | 5.341 | 1 | 0 | 1 | 6 | 0.3184 | 0.3498 | 770.6 |
| hst_slog | 0.9762 | 0.5 | 0.9881 | 0.9988 | -1.11e-16 | 0.8902 | 0.9762 | 30 | 1 | 6 | 0.6083 | 0.04657 | 550 |
| kitnet | 0.9603 | 0 | 0.9651 | 0.9776 | -5.551e-17 | 2.967 | 0.9603 | 30 | 1 | 6 | 1.38 | 0.1356 | 1.918 |
| ecod_tail | 1 | 0 | 0.9841 | 0.9983 | -1.11e-16 | 3.561 | 1 | 0 | 1 | 6 | 0.02103 | 0.006457 | 846.4 |
