# regress_i7_unsw_late_wemo_switch

Windows: {'windows': 18435, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 9705, 'test_attack': 126, 'excluded': 24}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/9705 = 0.000103; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.9841 | 0.5794 | 0.994 | 0.9994 | -1.11e-16 | 2.077 | 0.9762 | 30 | 1 | 6 | 0.06866 | 0.003932 | 0.334 |
| mad_tail_slog | 0.9921 | 0.873 | 0.9952 | 0.9957 | -1.11e-16 | 1.187 | 0.9921 | 0 | 1 | 6 | 0.05873 | 0.01722 | 0.2969 |
| autoencoder_slog | 0.9524 | 0.9127 | 0.9818 | 0.9873 | -8.674e-19 | 7.716 | 0.9603 | 60 | 1 | 6 | 1.64 | 0.009812 | 2.852 |
| iforest_ext_sparse_slog | 0.9286 | 0.9048 | 0.9791 | 0.9953 | -5.551e-17 | 5.342 | 0.9524 | 60 | 1 | 6 | 0.2832 | 0.2905 | 726.8 |
| hst_slog | 0.9206 | 0.9048 | 0.9752 | 0.9965 | -1.11e-16 | 5.342 | 0.9206 | 60 | 1 | 6 | 0.7092 | 0.05304 | 550 |
| kitnet | 0.9921 | 0 | 0.9789 | 0.9972 | -5.551e-17 | 1.484 | 0.9921 | 0 | 1 | 6 | 1.565 | 0.1656 | 2.047 |
| ecod_tail | 0.9762 | 0.6984 | 0.9919 | 0.9992 | -1.11e-16 | 5.045 | 0.9762 | 30 | 1 | 6 | 0.02636 | 0.006782 | 846.4 |
