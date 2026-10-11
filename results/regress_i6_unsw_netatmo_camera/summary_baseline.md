# regress_i6_unsw_netatmo_camera

Windows: {'windows': 15537, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 6582, 'test_attack': 315, 'excluded': 60}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/6582 = 0.000152; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.9079 | 0.1778 | 0.9505 | 0.9576 | 0.5406 | 1.75 | 0.8984 | 60 | 1 | 15 | 0.09824 | 0.01589 | 0.334 |
| mad_tail_slog | 0.9016 | 0 | 0.9455 | 0.9578 | 0.5801 | 3.063 | 0.9079 | 60 | 1 | 15 | 0.06771 | 0.009145 | 0.2969 |
| autoencoder_slog | 0.9016 | 0.1778 | 0.9461 | 0.959 | 0.002806 | 11.38 | 0.9111 | 30 | 1 | 15 | 1.845 | 0.01164 | 2.852 |
| iforest_ext_sparse_slog | 0.9016 | 0 | 0.9445 | 0.9607 | 0.429 | 5.688 | 0.9079 | 30 | 1 | 15 | 0.3832 | 0.3972 | 770.6 |
| hst_slog | 0.781 | 0.419 | 0.9205 | 0.9529 | 0.8343 | 0.8751 | 0.7714 | 90 | 0.8667 | 15 | 0.8748 | 0.07285 | 550 |
| kitnet | 0.8825 | 0.181 | 0.9339 | 0.9381 | 0.259 | 3.063 | 0.8825 | 60 | 1 | 15 | 2.298 | 0.2249 | 1.918 |
| ecod_tail | 0.9048 | 0 | 0.9454 | 0.9574 | 0.6171 | 6.126 | 0.9079 | 60 | 1 | 15 | 0.03218 | 0.008884 | 846.4 |
