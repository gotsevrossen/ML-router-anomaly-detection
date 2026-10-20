# regress_i11_unsw_netatmo_camera

Windows: {'windows': 15537, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 6582, 'test_attack': 315, 'excluded': 60}. Window length 30 s; features (41): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers, tcp_pkts, udp_pkts, icmp_pkts.

FPR resolution on test = 1/6582 = 0.000152; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.6794 | 0.673 | 0.8918 | 0.9887 | 0 | 0 | 0.6698 | 180 | 1 | 15 | 0.5877 | 0.01983 | 0.3604 |
| ecod_router | 0.9968 | 0.9841 | 0.9982 | 0.9992 | 0 | 0 | 0.854 | 210 | 1 | 15 | 0.2774 | 0.04072 | 30.41 |
