# regress_i4_unsw_wemo_motion

Windows: {'windows': 15537, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 6358, 'test_attack': 503, 'excluded': 96}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/6358 = 0.000157; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.672 | 0.5328 | 0.8391 | 0.8736 | 0.5971 | 0.453 | 0.6024 | 0 | 0.7083 | 24 | 0.07512 | 0.002993 | 0.334 |
| mad_tail_slog | 0.8608 | 0 | 0.9238 | 0.9453 | 0.6442 | 2.265 | 0.829 | 270 | 0.875 | 24 | 0.05035 | 0.009292 | 0.2969 |
| autoencoder_slog | 0.175 | 0.1292 | 0.6902 | 0.924 | 0.02348 | 0.9059 | 0.1352 | 0 | 0.1667 | 24 | 1.686 | 0.02375 | 2.852 |
| iforest_ext_sparse_slog | 0.3658 | 0.00994 | 0.7579 | 0.9286 | 0.6872 | 0.453 | 0.0159 | 1740 | 0.1667 | 24 | 0.3672 | 0.3799 | 639.7 |
| hst_slog | 0 | 0 | 0.506 | 0.6415 | 0.9863 | 0.453 | 0 | nan | 0 | 24 | 0.4673 | 0.06065 | 550 |
| kitnet | 0.7197 | 0.1252 | 0.8534 | 0.8519 | 0.2911 | 0.453 | 0.664 | 0 | 0.7083 | 24 | 2.02 | 0.1967 | 2.156 |
