# regress_i11_unsw_late_wemo_motion

Windows: {'windows': 18436, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 9566, 'test_attack': 250, 'excluded': 40}. Window length 30 s; features (41): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers, tcp_pkts, udp_pkts, icmp_pkts.

FPR resolution on test = 1/9566 = 0.000105; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.596 | 0.592 | 0.814 | 0.8994 | 0 | 11.74 | 0.6 | 210 | 0.9 | 10 | 0.5925 | 0.02911 | 0.3604 |
| ecod_router | 0.728 | 0.648 | 0.9347 | 0.965 | 0 | 3.613 | 0.756 | 210 | 1 | 10 | 0.3315 | 0.04044 | 29.91 |
