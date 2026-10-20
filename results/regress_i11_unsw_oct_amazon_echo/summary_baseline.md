# regress_i11_unsw_oct_amazon_echo

Windows: {'windows': 20723, 'bootstrap': 5760, 'validation': 2873, 'test_benign': 11874, 'test_attack': 188, 'excluded': 28}. Window length 30 s; features (41): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers, tcp_pkts, udp_pkts, icmp_pkts.

FPR resolution on test = 1/11874 = 8.42e-05; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.7394 | 0.7394 | 0.8835 | 0.8931 | 0 | 2381 | 1 | 0 | 1 | 7 | 0.7528 | 0.01881 | 0.3604 |
| ecod_router | 0.7447 | 0.6436 | 0.8765 | 0.8881 | 0 | 2059 | 1 | 0 | 1 | 7 | 0.2872 | 0.03313 | 23.65 |
