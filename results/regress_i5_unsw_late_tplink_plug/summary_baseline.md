# regress_i5_unsw_late_tplink_plug

Windows: {'windows': 18434, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 9704, 'test_attack': 126, 'excluded': 24}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/9704 = 0.000103; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.9921 | 0.9841 | 0.9987 | 0.9999 | 0.5809 | 15.43 | 1 | 0 | 1 | 6 | 0.1164 | 0.00531 | 0.334 |
| mad_tail_slog | 1 | 0.9841 | 0.9998 | 1 | 0.6102 | 16.32 | 1 | 0 | 1 | 6 | 0.06628 | 0.008749 | 0.2969 |
| autoencoder_slog | 0.9841 | 0.9841 | 0.9976 | 0.9997 | 0.03459 | 9.497 | 0.9921 | 0 | 1 | 6 | 1.496 | 0.008563 | 2.852 |
| iforest_ext_sparse_slog | 0.9841 | 0.9841 | 0.9983 | 0.9998 | 0.6992 | 2.374 | 0.9841 | 0 | 1 | 6 | 0.2038 | 0.2914 | 451.8 |
| hst_slog | 0 | 0 | 0.5136 | 0.9032 | 0.995 | 2.671 | 0 | nan | 0 | 6 | 0.6371 | 0.05498 | 550 |
| kitnet | 1 | 0 | 0.9874 | 0.9987 | 0.2762 | 5.936 | 1 | 0 | 1 | 6 | 2.041 | 0.1954 | 2.223 |
| ecod_tail | 0.9921 | 0.9841 | 0.9989 | 0.9999 | 0.6643 | 17.51 | 1 | 0 | 1 | 6 | 0.01971 | 0.004902 | 846.4 |
