# regress_i6_unsw_late_tplink_plug

Windows: {'windows': 18434, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 9704, 'test_attack': 126, 'excluded': 24}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/9704 = 0.000103; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.9127 | 0.8889 | 0.9561 | 0.9595 | 0.5809 | 4.452 | 0.9127 | 60 | 1 | 6 | 0.09118 | 0.003186 | 0.334 |
| mad_tail_slog | 0.9127 | 0.9127 | 0.9581 | 0.961 | 0.5809 | 0.2968 | 0.9127 | 60 | 1 | 6 | 0.04111 | 0.008263 | 0.2969 |
| autoencoder_slog | 0.9127 | 0.9127 | 0.9577 | 0.9669 | 0.02166 | 2.374 | 0.9127 | 60 | 1 | 6 | 1.369 | 0.009589 | 2.852 |
| iforest_ext_sparse_slog | 0.9127 | 0.9127 | 0.9562 | 0.9578 | 0.5902 | 9.794 | 0.9127 | 60 | 1 | 6 | 0.2178 | 0.3463 | 451.8 |
| hst_slog | 0.8492 | 0 | 0.9379 | 0.9559 | 0.9525 | 0.5936 | 0 | nan | 0 | 6 | 0.4161 | 0.04926 | 550 |
| kitnet | 0.9127 | 0 | 0.9549 | 0.9678 | 0.2689 | 3.858 | 0.9127 | 60 | 1 | 6 | 1.941 | 0.1862 | 2.223 |
| ecod_tail | 0.9127 | 0.8889 | 0.9585 | 0.9591 | 0.6253 | 16.92 | 0.9206 | 60 | 1 | 6 | 0.03594 | 0.01369 | 846.4 |
