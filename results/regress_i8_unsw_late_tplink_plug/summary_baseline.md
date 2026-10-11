# regress_i8_unsw_late_tplink_plug

Windows: {'windows': 18434, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 9704, 'test_attack': 126, 'excluded': 24}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/9704 = 0.000103; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.9921 | 0.9841 | 0.9988 | 0.9999 | -1.11e-16 | 19.29 | 1 | 0 | 1 | 6 | 0.06106 | 0.003986 | 0.334 |
| mad_tail_slog | 1 | 1 | 1 | 1 | -1.11e-16 | 16.32 | 1 | 0 | 1 | 6 | 0.04902 | 0.01766 | 0.2969 |
| autoencoder_slog | 1 | 0.9921 | 0.9999 | 1 | -3.469e-18 | 11.57 | 1 | 0 | 1 | 6 | 1.563 | 0.007941 | 2.852 |
| iforest_ext_sparse_slog | 1 | 0.9683 | 0.9998 | 1 | -1.11e-16 | 12.17 | 1 | 0 | 1 | 6 | 0.1968 | 0.35 | 451.8 |
| hst_slog | 0 | 0 | 0.6775 | 0.954 | -1.11e-16 | 0.5936 | 0 | nan | 0 | 6 | 0.7984 | 0.06068 | 550 |
| kitnet | 1 | 0 | 0.9875 | 0.9987 | -5.551e-17 | 8.904 | 1 | 0 | 1 | 6 | 2.408 | 0.231 | 2.223 |
| ecod_tail | 1 | 0.8889 | 0.9994 | 0.9999 | -1.11e-16 | 28.49 | 1 | 0 | 1 | 6 | 0.02125 | 0.005905 | 846.7 |
| ecod_router | 1 | 0.8889 | 0.9994 | 0.9999 | -1.11e-16 | 28.49 | 1 | 0 | 1 | 6 | 0.04011 | 0.00681 | 12.84 |
