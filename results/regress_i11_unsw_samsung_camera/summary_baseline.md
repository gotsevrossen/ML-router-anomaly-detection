# regress_i11_unsw_samsung_camera

Windows: {'windows': 15537, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 6134, 'test_attack': 691, 'excluded': 132}. Window length 30 s; features (41): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers, tcp_pkts, udp_pkts, icmp_pkts.

FPR resolution on test = 1/6134 = 0.000163; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.3705 | 0.3705 | 0.8033 | 0.8291 | 0 | 6.104 | 0.6614 | 240 | 1 | 33 | 0.5867 | 0.01708 | 0.3604 |
| ecod_router | 0.3603 | 0.3603 | 0.8514 | 0.9187 | 0 | 7.512 | 0.7656 | 210 | 1 | 33 | 0.2317 | 0.04263 | 23.01 |
