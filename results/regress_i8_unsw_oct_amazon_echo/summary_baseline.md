# regress_i8_unsw_oct_amazon_echo

Windows: {'windows': 20723, 'bootstrap': 5760, 'validation': 2873, 'test_benign': 11874, 'test_attack': 188, 'excluded': 28}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/11874 = 8.42e-05; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0 | 0 | 0.4975 | 0.8799 | -1.11e-16 | 83.92 | 0.9947 | 0 | 1 | 7 | 0.08325 | 0.002796 | 0.334 |
| mad_tail_slog | 0 | 0 | 0.5098 | 0.6083 | -1.11e-16 | 2469 | 1 | 0 | 1 | 7 | 0.04491 | 0.009033 | 0.2969 |
| autoencoder_slog | 0.2819 | 0 | 0.6349 | 0.9074 | -1.735e-18 | 462.3 | 1 | 0 | 1 | 7 | 1.471 | 0.01787 | 2.852 |
| iforest_ext_sparse_slog | 0 | 0 | 0.4975 | 0.8746 | -5.551e-17 | 2213 | 1 | 0 | 1 | 7 | 0.3359 | 0.2918 | 768.6 |
| hst_slog | 0.8085 | 0.8085 | 0.9035 | 0.9693 | -1.11e-16 | 76.16 | 0.9681 | 30 | 1 | 7 | 0.5299 | 0.0543 | 550 |
| kitnet | 0.3351 | 0.3351 | 0.6718 | 0.6933 | -5.551e-17 | 53.6 | 0.383 | 0 | 0.7143 | 7 | 1.93 | 0.1846 | 2 |
| ecod_tail | 0 | 0 | 0.4975 | 0.8598 | -1.11e-16 | 506 | 0.9947 | 0 | 1 | 7 | 0.02071 | 0.01289 | 855.6 |
| ecod_router | 0 | 0 | 0.4975 | 0.8598 | -1.11e-16 | 524.6 | 0.9947 | 0 | 1 | 7 | 0.02593 | 0.005392 | 23.04 |
