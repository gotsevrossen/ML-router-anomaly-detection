# regress_i4_unsw_oct_chromecast

Windows: {'windows': 20724, 'bootstrap': 5760, 'validation': 2873, 'test_benign': 11437, 'test_attack': 564, 'excluded': 90}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/11437 = 8.74e-05; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.5426 | 0 | 0.8017 | 0.9048 | 0.5867 | 47.84 | 0.805 | 0 | 0.913 | 23 | 0.09623 | 0.003712 | 0.334 |
| mad_tail_slog | 0.4007 | 0 | 0.7187 | 0.8324 | 0.7206 | 0.5036 | 0.4007 | 1620 | 0.4348 | 23 | 0.0464 | 0.007816 | 0.2969 |
| autoencoder_slog | 0.1046 | 0.1028 | 0.5863 | 0.8292 | 0.0431 | 0 | 0.1028 | 120 | 0.2174 | 23 | 1.704 | 0.01013 | 2.852 |
| iforest_ext_sparse_slog | 0.04078 | 0.03014 | 0.5669 | 0.8405 | 0.6499 | 16.12 | 0.1188 | 2130 | 0.3913 | 23 | 0.3356 | 0.3454 | 746.6 |
| hst_slog | 0 | 0 | 0.5121 | 0.7269 | 0.9563 | 1.511 | 0 | nan | 0 | 23 | 0.6724 | 0.0514 | 550 |
| kitnet | 0.6986 | 0.1117 | 0.8547 | 0.9044 | 0.3312 | 67.49 | 0.8298 | 0 | 0.8696 | 23 | 1.558 | 0.1524 | 1.926 |
