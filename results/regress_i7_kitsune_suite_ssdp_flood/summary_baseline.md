# regress_i7_kitsune_suite_ssdp_flood

Windows: {'windows': 82, 'bootstrap': 39, 'validation': 23, 'test_benign': 17, 'test_attack': 3}. Window length 30 s; features (36): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/17 = 0.0588; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 1 | 1 | 1 | 1 | -1.11e-16 | 1355 | 1 | 0 | 1 | 1 | 0.002353 | 0.00985 | 0.3164 |
| mad_tail_slog | 1 | 1 | 1 | 1 | -1.11e-16 | 169.4 | 1 | 0 | 1 | 1 | 0.0009699 | 0.01023 | 0.2812 |
| autoencoder_slog | 1 | 1 | 1 | 1 | -3.469e-18 | 2711 | 1 | 0 | 1 | 1 | 1.602 | 0.007549 | 2.703 |
| iforest_ext_sparse_slog | 1 | 1 | 1 | 1 | -5.551e-17 | 2541 | 1 | 0 | 1 | 1 | 0.07996 | 0.1897 | 247.6 |
| hst_slog | 0.3333 | 0.3333 | 0.665 | 0.7214 | -1.11e-16 | 2372 | 1 | 0 | 1 | 1 | 0.185 | 0.04425 | 549.9 |
| kitnet | 1 | 1 | 1 | 1 | -5.551e-17 | 2711 | 1 | 0 | 1 | 1 | 0.0158 | 0.1921 | 2.211 |
| ecod_tail | 1 | 1 | 1 | 1 | -1.11e-16 | 2711 | 1 | 0 | 1 | 1 | 0.000402 | 0.01137 | 5.766 |
