# regress_i5_kitsune_suite_ssdp_flood

Windows: {'windows': 82, 'bootstrap': 39, 'validation': 23, 'test_benign': 17, 'test_attack': 3}. Window length 30 s; features (36): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/17 = 0.0588; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 1 | 1 | 1 | 1 | 0.5518 | 0 | 1 | 0 | 1 | 1 | 0.001928 | 0.006801 | 0.3164 |
| mad_tail_slog | 1 | 1 | 1 | 1 | 0.5809 | 169.4 | 1 | 0 | 1 | 1 | 0.001143 | 0.01307 | 0.2812 |
| autoencoder_slog | 1 | 1 | 1 | 1 | 0.03081 | 2711 | 1 | 0 | 1 | 1 | 2.241 | 0.01471 | 2.703 |
| iforest_ext_sparse_slog | 1 | 1 | 1 | 1 | 0.4988 | 2541 | 1 | 0 | 1 | 1 | 0.1313 | 0.3837 | 247.6 |
| hst_slog | 1 | 1 | 1 | 1 | 0.8881 | 677.6 | 1 | 0 | 1 | 1 | 0.4663 | 0.07718 | 549.9 |
| kitnet | 1 | 1 | 1 | 1 | 0.4013 | 2711 | 1 | 0 | 1 | 1 | 0.03393 | 0.4453 | 2.211 |
| ecod_tail | 1 | 1 | 1 | 1 | 0.6218 | 2711 | 1 | 0 | 1 | 1 | 0.0004756 | 0.01283 | 5.766 |
