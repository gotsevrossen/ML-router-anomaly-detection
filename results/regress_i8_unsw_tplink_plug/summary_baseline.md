# regress_i8_unsw_tplink_plug

Windows: {'windows': 15531, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 6426, 'test_attack': 441, 'excluded': 84}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/6426 = 0.000156; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.9977 | 0.9864 | 0.9994 | 0.9999 | -1.11e-16 | 12.1 | 1 | 0 | 1 | 21 | 0.1024 | 0.01418 | 0.334 |
| mad_tail_slog | 0.9365 | 0.6054 | 0.9886 | 0.9988 | -1.11e-16 | 12.1 | 1 | 0 | 1 | 21 | 0.0416 | 0.007893 | 0.2969 |
| autoencoder_slog | 0.9796 | 0.78 | 0.994 | 0.9994 | -3.469e-18 | 11.65 | 0.9932 | 30 | 1 | 21 | 1.328 | 0.008129 | 2.852 |
| iforest_ext_sparse_slog | 0.9637 | 0.5034 | 0.9838 | 0.9974 | -1.11e-16 | 11.2 | 0.9796 | 60 | 1 | 21 | 0.2475 | 0.3356 | 451.8 |
| hst_slog | 0.2698 | 0 | 0.7186 | 0.9477 | -1.11e-16 | 1.345 | 0.2698 | 2.574e+04 | 0.4286 | 21 | 0.5738 | 0.04758 | 550 |
| kitnet | 0.9977 | 0.3016 | 0.9943 | 0.9994 | -5.551e-17 | 7.171 | 1 | 0 | 1 | 21 | 2.546 | 0.2185 | 2.223 |
| ecod_tail | 0.9887 | 0.8027 | 0.9968 | 0.9997 | -1.11e-16 | 19.72 | 1 | 0 | 1 | 21 | 0.03427 | 0.005954 | 846.7 |
| ecod_router | 0.9887 | 0.8027 | 0.9968 | 0.9997 | -1.11e-16 | 19.72 | 1 | 0 | 1 | 21 | 0.02677 | 0.005119 | 12.84 |
