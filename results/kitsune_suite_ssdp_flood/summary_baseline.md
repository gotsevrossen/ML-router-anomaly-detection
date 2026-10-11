# kitsune_suite_ssdp_flood

Windows: {'windows': 82, 'bootstrap': 39, 'validation': 23, 'test_benign': 17, 'test_attack': 3}. Window length 30 s; features (28): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets.

FPR resolution on test = 1/17 = 0.0588; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 1 | 1 | 1 | 1 | 0.6731 | 2711 | 1 | 0 | 0.0007381 | 0.002707 | 0.2461 |
| mad_tail_slog | 1 | 1 | 1 | 1 | 0.7318 | 2033 | 1 | 0 | 0.0004558 | 0.004905 | 0.2188 |
| autoencoder_slog | 1 | 1 | 1 | 1 | 0.03898 | 2711 | 1 | 0 | 0.9479 | 0.01296 | 2.109 |
| kitnet_windows | 1 | 1 | 1 | 1 | 0.4321 | 2711 | 1 | 0 | 0.02475 | 0.2682 | 1.758 |
| hst | 1 | 1 | 1 | 1 | 0.8793 | 1864 | 1 | 0 | 0.1731 | 0.08384 | 549.9 |
