# regress_i5_unsw_oct_lifx_bulb

Windows: {'windows': 20724, 'bootstrap': 5760, 'validation': 2873, 'test_benign': 11725, 'test_attack': 314, 'excluded': 52}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/11725 = 8.53e-05; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.7898 | 0.1975 | 0.9083 | 0.9301 | 0.6094 | 2.702 | 0.7261 | 0 | 0.9231 | 13 | 0.1034 | 0.004991 | 0.334 |
| mad_tail_slog | 0 | 0 | 0.9177 | 0.986 | 0.7296 | 1.474 | 0 | nan | 0 | 13 | 0.07504 | 0.01231 | 0.2969 |
| autoencoder_slog | 0.8726 | 0 | 0.9615 | 0.996 | 0.01726 | 3.684 | 0.9299 | 0 | 1 | 13 | 1.857 | 0.0105 | 2.852 |
| iforest_ext_sparse_slog | 0.7389 | 0 | 0.9554 | 0.9952 | 0.6156 | 6.878 | 0.9299 | 30 | 1 | 13 | 0.418 | 0.368 | 815.5 |
| hst_slog | 0.3567 | 0.02229 | 0.675 | 0.8539 | 0.8984 | 3.93 | 0.3567 | 30 | 0.8462 | 13 | 0.4977 | 0.05586 | 550 |
| kitnet | 0.8025 | 0.1975 | 0.9407 | 0.9606 | 0.3042 | 3.193 | 0.8917 | 0 | 1 | 13 | 2.728 | 0.2279 | 2.227 |
| ecod_tail | 0.8503 | 0 | 0.9462 | 0.9939 | 0.6997 | 2.211 | 0.4777 | 30 | 0.7692 | 13 | 0.02168 | 0.01313 | 855.3 |
