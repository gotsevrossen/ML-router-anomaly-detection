# regress_i8_unsw_wemo_switch

Windows: {'windows': 15535, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 6505, 'test_attack': 378, 'excluded': 72}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/6505 = 0.000154; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.2328 | 0.2143 | 0.8842 | 0.9826 | -1.11e-16 | 9.297 | 0.963 | 0 | 1 | 18 | 0.06365 | 0.003437 | 0.334 |
| mad_tail_slog | 0.1667 | 0.127 | 0.8516 | 0.9543 | -1.11e-16 | 8.855 | 0.9127 | 30 | 1 | 18 | 0.05979 | 0.009147 | 0.2969 |
| autoencoder_slog | 0.1958 | 0.1587 | 0.8692 | 0.9698 | -8.674e-19 | 19.04 | 0.955 | 0 | 1 | 18 | 1.537 | 0.008719 | 2.852 |
| iforest_ext_sparse_slog | 0.05556 | 0.0291 | 0.8443 | 0.9689 | -5.551e-17 | 13.28 | 0.9233 | 0 | 1 | 18 | 0.3441 | 0.3446 | 726.8 |
| hst_slog | 0.03968 | 0.03968 | 0.7809 | 0.9466 | -1.11e-16 | 21.25 | 0.8069 | 60 | 0.9444 | 18 | 0.65 | 0.05621 | 550 |
| kitnet | 0.3333 | 0.1667 | 0.8319 | 0.8984 | -5.551e-17 | 9.74 | 0.8228 | 0 | 0.8333 | 18 | 1.739 | 0.1749 | 2.047 |
| ecod_tail | 0.08201 | 0.06349 | 0.8597 | 0.9822 | -1.11e-16 | 15.5 | 0.9471 | 30 | 1 | 18 | 0.03585 | 0.008555 | 846.7 |
| ecod_router | 0.08201 | 0.06349 | 0.8596 | 0.9804 | -1.11e-16 | 15.5 | 0.9497 | 0 | 1 | 18 | 0.02554 | 0.0074 | 24.76 |
