# regress_i7_unsw_netatmo_camera

Windows: {'windows': 15537, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 6582, 'test_attack': 315, 'excluded': 60}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/6582 = 0.000152; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.9968 | 0.1841 | 0.9918 | 0.9982 | -1.11e-16 | 2.625 | 0.9937 | 0 | 1 | 15 | 0.07928 | 0.01635 | 0.334 |
| mad_tail_slog | 0.9968 | 0 | 0.986 | 0.9983 | -1.11e-16 | 3.5 | 0.9968 | 0 | 1 | 15 | 0.08332 | 0.01199 | 0.2969 |
| autoencoder_slog | 0.9968 | 0.1905 | 0.9844 | 0.9969 | -4.337e-19 | 14 | 0.9968 | 0 | 1 | 15 | 1.585 | 0.01177 | 2.852 |
| iforest_ext_sparse_slog | 0.9619 | 0 | 0.9847 | 0.998 | -5.551e-17 | 7.438 | 0.9937 | 30 | 1 | 15 | 0.3094 | 0.3506 | 770.6 |
| hst_slog | 0.7048 | 0 | 0.9115 | 0.9384 | -1.11e-16 | 3.938 | 0.873 | 30 | 1 | 15 | 0.8016 | 0.04937 | 550 |
| kitnet | 0.9778 | 0.2 | 0.981 | 0.9878 | -5.551e-17 | 3.938 | 0.9778 | 0 | 1 | 15 | 1.448 | 0.1405 | 1.918 |
| ecod_tail | 0.9175 | 0 | 0.9852 | 0.9983 | -1.11e-16 | 6.126 | 0.9937 | 0 | 1 | 15 | 0.02251 | 0.007547 | 846.4 |
