# regress_i6_unsw_tplink_plug

Windows: {'windows': 15531, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 6426, 'test_attack': 441, 'excluded': 84}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/6426 = 0.000156; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.9048 | 0.9025 | 0.9524 | 0.957 | 0.5809 | 1.345 | 0.9048 | 60 | 1 | 21 | 0.09484 | 0.004684 | 0.334 |
| mad_tail_slog | 0.9048 | 0.9025 | 0.9546 | 0.9564 | 0.5809 | 0.4482 | 0.9048 | 60 | 1 | 21 | 0.05868 | 0.01073 | 0.2969 |
| autoencoder_slog | 0.9048 | 0.9025 | 0.9556 | 0.9606 | 0.02166 | 1.793 | 0.9048 | 60 | 1 | 21 | 2.337 | 0.009977 | 2.852 |
| iforest_ext_sparse_slog | 0.9048 | 0.5034 | 0.9494 | 0.9609 | 0.5902 | 6.275 | 0.9048 | 60 | 1 | 21 | 0.3297 | 0.3665 | 451.8 |
| hst_slog | 0.6848 | 0 | 0.9084 | 0.9523 | 0.9525 | 0.4482 | 0.2698 | 2.574e+04 | 0.4286 | 21 | 0.901 | 0.07377 | 550 |
| kitnet | 0.9048 | 0.288 | 0.9486 | 0.9537 | 0.2689 | 2.241 | 0.9048 | 60 | 1 | 21 | 2.913 | 0.2819 | 2.223 |
| ecod_tail | 0.907 | 0.8027 | 0.9552 | 0.9606 | 0.6253 | 7.619 | 0.9138 | 60 | 1 | 21 | 0.02049 | 0.006572 | 846.4 |
