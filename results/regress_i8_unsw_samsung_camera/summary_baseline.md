# regress_i8_unsw_samsung_camera

Windows: {'windows': 15537, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 6134, 'test_attack': 691, 'excluded': 132}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/6134 = 0.000163; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.1592 | 0.1592 | 0.8484 | 0.9837 | -1.11e-16 | 12.21 | 0.958 | 0 | 1 | 33 | 0.1029 | 0.005189 | 0.334 |
| mad_tail_slog | 0.2229 | 0.2229 | 0.8612 | 0.9702 | -1.11e-16 | 10.8 | 0.631 | 30 | 0.6364 | 33 | 0.05912 | 0.00871 | 0.2969 |
| autoencoder_slog | 0.05933 | 0.04631 | 0.8106 | 0.9685 | -1.735e-18 | 12.21 | 0.7612 | 0 | 0.8485 | 33 | 1.845 | 0.009247 | 2.852 |
| iforest_ext_sparse_slog | 0.4805 | 0.2981 | 0.9062 | 0.9874 | -1.11e-16 | 11.27 | 0.8755 | 90 | 0.9394 | 33 | 0.2847 | 0.3295 | 748.2 |
| hst_slog | 0.1375 | 0 | 0.8123 | 0.9699 | -1.11e-16 | 11.27 | 0.8119 | 60 | 0.9394 | 33 | 0.6825 | 0.04936 | 550 |
| kitnet | 0 | 0 | 0.7059 | 0.7951 | -5.551e-17 | 10.8 | 0.6324 | 0 | 0.6364 | 33 | 1.598 | 0.1533 | 2 |
| ecod_tail | 0.2952 | 0.2764 | 0.8654 | 0.9841 | -1.11e-16 | 11.27 | 0.7916 | 0 | 0.8788 | 33 | 0.02468 | 0.005881 | 846.7 |
| ecod_router | 0.2952 | 0.2764 | 0.8654 | 0.9841 | -1.11e-16 | 11.27 | 0.7916 | 0 | 0.8788 | 33 | 0.0345 | 0.005062 | 22.09 |
