# regress_i6_unsw_wemo_switch

Windows: {'windows': 15535, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 6505, 'test_attack': 378, 'excluded': 72}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/6505 = 0.000154; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.2328 | 0.2143 | 0.862 | 0.9526 | 0.5156 | 7.969 | 0.8915 | 60 | 1 | 18 | 0.116 | 0.004531 | 0.334 |
| mad_tail_slog | 0.1667 | 0.127 | 0.8303 | 0.9247 | 0.5809 | 7.969 | 0.8466 | 60 | 1 | 18 | 0.07751 | 0.01238 | 0.2969 |
| autoencoder_slog | 0.1958 | 0.1587 | 0.8544 | 0.9476 | 0.00699 | 18.15 | 0.9048 | 30 | 1 | 18 | 2.365 | 0.01038 | 2.852 |
| iforest_ext_sparse_slog | 0.05556 | 0.0291 | 0.8366 | 0.9484 | 0.4257 | 11.51 | 0.9021 | 0 | 1 | 18 | 0.3875 | 0.3057 | 726.8 |
| hst_slog | 0.03968 | 0.03968 | 0.781 | 0.9298 | 0.8027 | 20.81 | 0.8069 | 60 | 0.9444 | 18 | 0.9233 | 0.07286 | 550 |
| kitnet | 0.3175 | 0.2831 | 0.8129 | 0.8588 | 0.2915 | 8.412 | 0.7434 | 60 | 0.8333 | 18 | 2.396 | 0.2075 | 2.047 |
| ecod_tail | 0.08201 | 0.06349 | 0.8424 | 0.9496 | 0.6132 | 12.84 | 0.8968 | 60 | 1 | 18 | 0.02388 | 0.007168 | 846.4 |
