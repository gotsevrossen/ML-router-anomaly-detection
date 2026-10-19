# regress_i9_unsw_oct_chromecast

Windows: {'windows': 20724, 'bootstrap': 5760, 'validation': 2873, 'test_benign': 11437, 'test_attack': 564, 'excluded': 90}. Window length 30 s; features (41): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers, tcp_pkts, udp_pkts, icmp_pkts.

FPR resolution on test = 1/11437 = 8.74e-05; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.789 | 0.3351 | 0.9066 | 0.9245 | 0 | 1.007 | 0.7376 | 0 | 0.8696 | 23 | 0.162 | 0.01162 | 0.3604 |
| ecod_router | 0.6046 | 0.5887 | 0.8189 | 0.8807 | 0 | 74.03 | 0.7199 | 210 | 1 | 23 | 0.05885 | 0.01222 | 31.84 |
