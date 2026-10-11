# regress_i5_unsw_late_wemo_switch

Windows: {'windows': 18435, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 9705, 'test_attack': 126, 'excluded': 24}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/9705 = 0.000103; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.9841 | 0.6429 | 0.9907 | 0.999 | 0.5915 | 0.8903 | 0.9444 | 30 | 1 | 6 | 0.0699 | 0.003014 | 0.334 |
| mad_tail_slog | 1 | 0.9603 | 0.9995 | 1 | 0.6724 | 0.8903 | 0.9841 | 0 | 1 | 6 | 0.03905 | 0.008168 | 0.2969 |
| autoencoder_slog | 0.9841 | 0.1032 | 0.9931 | 0.9993 | 0.03789 | 0.2968 | 0.6825 | 90 | 1 | 6 | 1.459 | 0.01751 | 2.852 |
| iforest_ext_sparse_slog | 1 | 0 | 0.9758 | 0.9975 | 0.662 | 1.484 | 0.5952 | 1620 | 0.6667 | 6 | 0.3245 | 0.2792 | 726.8 |
| hst_slog | 0.7937 | 0 | 0.9689 | 0.9967 | 0.9492 | 0.2968 | 0.04762 | 1740 | 0.8333 | 6 | 0.659 | 0.05112 | 550 |
| kitnet | 1 | 0 | 0.9827 | 0.9982 | 0.3138 | 1.187 | 0.9841 | 0 | 1 | 6 | 1.448 | 0.1433 | 2.047 |
| ecod_tail | 0.9444 | 0.6032 | 0.9916 | 0.9991 | 0.6911 | 2.077 | 0.9127 | 30 | 1 | 6 | 0.02008 | 0.005957 | 846.4 |
