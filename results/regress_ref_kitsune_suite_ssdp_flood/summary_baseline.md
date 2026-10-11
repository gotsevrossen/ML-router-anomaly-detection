# regress_ref_kitsune_suite_ssdp_flood

Windows: {'windows': 82, 'bootstrap': 39, 'validation': 23, 'test_benign': 17, 'test_attack': 3}. Window length 30 s; features (28): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets.

FPR resolution on test = 1/17 = 0.0588; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 1 | 1 | 1 | 1 | 0.6731 | 2711 | 1 | 0 | 1 | 1 | 0.0006539 | 0.002237 | 0.2461 |
| mad_tail_slog | 1 | 1 | 1 | 1 | 0.7318 | 2033 | 1 | 0 | 1 | 1 | 0.0003668 | 0.00446 | 0.2188 |
| autoencoder_slog | 1 | 1 | 1 | 1 | 0.0423 | 2711 | 1 | 0 | 1 | 1 | 1.108 | 0.008412 | 2.109 |
| iforest_ext_sparse_slog | 1 | 1 | 1 | 1 | 0.5488 | 2711 | 1 | 0 | 1 | 1 | 0.0765 | 0.3212 | 244.9 |
| hst_slog | 1 | 1 | 1 | 1 | 0.8696 | 1864 | 1 | 0 | 1 | 1 | 0.1565 | 0.0467 | 549.9 |
| kitnet | 1 | 1 | 1 | 1 | 0.4321 | 2711 | 1 | 0 | 1 | 1 | 0.02803 | 0.3289 | 1.758 |
