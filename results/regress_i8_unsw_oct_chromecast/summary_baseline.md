# regress_i8_unsw_oct_chromecast

Windows: {'windows': 20724, 'bootstrap': 5760, 'validation': 2873, 'test_benign': 11437, 'test_attack': 564, 'excluded': 90}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/11437 = 8.74e-05; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.5479 | 0 | 0.8136 | 0.909 | -1.11e-16 | 48.1 | 0.8351 | 0 | 0.913 | 23 | 0.07571 | 0.002922 | 0.334 |
| mad_tail_slog | 0.5603 | 0 | 0.7946 | 0.8664 | -1.11e-16 | 290.3 | 0.8262 | 60 | 0.9565 | 23 | 0.0442 | 0.007247 | 0.2969 |
| autoencoder_slog | 0.4326 | 0.2482 | 0.8113 | 0.9132 | -1.735e-18 | 467.4 | 0.9149 | 60 | 0.9565 | 23 | 1.545 | 0.01692 | 2.852 |
| iforest_ext_sparse_slog | 0.3493 | 0.273 | 0.7127 | 0.922 | -1.11e-16 | 18.13 | 0.4521 | 1740 | 0.7391 | 23 | 0.2752 | 0.3261 | 746.6 |
| hst_slog | 0.4486 | 0.1667 | 0.775 | 0.8557 | -1.11e-16 | 22.92 | 0.6259 | 60 | 0.8696 | 23 | 0.439 | 0.06264 | 550 |
| kitnet | 0.7145 | 0.1117 | 0.86 | 0.9054 | -5.551e-17 | 94.43 | 0.8316 | 0 | 0.8696 | 23 | 1.636 | 0.1801 | 1.926 |
| ecod_tail | 0.6472 | 0 | 0.8607 | 0.9133 | -1.11e-16 | 17.88 | 0.7872 | 30 | 0.8696 | 23 | 0.03111 | 0.008755 | 855.6 |
| ecod_router | 0.5674 | 0 | 0.8462 | 0.9093 | -1.11e-16 | 21.91 | 0.7872 | 30 | 0.8696 | 23 | 0.02536 | 0.006955 | 29.3 |
