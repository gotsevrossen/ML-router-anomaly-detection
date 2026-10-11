# regress_i5_unsw_wemo_switch

Windows: {'windows': 15535, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 6505, 'test_attack': 378, 'excluded': 72}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/6505 = 0.000154; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.2989 | 0.2222 | 0.8686 | 0.98 | 0.5915 | 9.297 | 0.8095 | 0 | 0.8333 | 18 | 0.1292 | 0.005935 | 0.334 |
| mad_tail_slog | 0.1931 | 0.1508 | 0.8543 | 0.9686 | 0.6724 | 8.855 | 0.8148 | 30 | 0.8333 | 18 | 0.08657 | 0.01364 | 0.2969 |
| autoencoder_slog | 0.2593 | 0.1323 | 0.8432 | 0.9646 | 0.03789 | 8.855 | 0.6323 | 0 | 0.8333 | 18 | 2.498 | 0.01347 | 2.852 |
| iforest_ext_sparse_slog | 0.1138 | 0 | 0.7691 | 0.9295 | 0.662 | 10.18 | 0.3624 | 180 | 0.6111 | 18 | 0.4583 | 0.4469 | 726.8 |
| hst_slog | 0.06349 | 0.01852 | 0.7216 | 0.8909 | 0.9492 | 0.4427 | 0.03704 | 210 | 0.3889 | 18 | 0.9514 | 0.08411 | 550 |
| kitnet | 0.3598 | 0.1667 | 0.8352 | 0.9 | 0.3138 | 9.297 | 0.8228 | 0 | 0.8333 | 18 | 2.978 | 0.2862 | 2.047 |
| ecod_tail | 0.1323 | 0.05556 | 0.8456 | 0.9788 | 0.6911 | 10.63 | 0.7513 | 30 | 0.8889 | 18 | 0.03988 | 0.01047 | 846.4 |
