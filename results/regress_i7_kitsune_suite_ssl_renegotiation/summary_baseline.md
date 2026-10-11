# regress_i7_kitsune_suite_ssl_renegotiation

Windows: {'windows': 78, 'bootstrap': 20, 'validation': 12, 'test_benign': 8, 'test_attack': 38}. Window length 30 s; features (36): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/8 = 0.125; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.9211 | 0.9211 | 0.9603 | 0.9584 | -5.551e-17 | 0 | 0.9211 | 90 | 1 | 1 | 0.001323 | 0.006297 | 0.3164 |
| mad_tail_slog | 0.9211 | 0.9211 | 0.9603 | 0.9584 | -5.551e-17 | 0 | 0.9211 | 90 | 1 | 1 | 0.0005237 | 0.01014 | 0.2812 |
| autoencoder_slog | 0.9474 | 0.9474 | 0.9736 | 0.9723 | -1.735e-18 | 1440 | 1 | 0 | 1 | 1 | 1.622 | 0.007692 | 2.703 |
| iforest_ext_sparse_slog | 0.9211 | 0.9211 | 0.9603 | 0.9584 | -5.551e-17 | 1800 | 0.9474 | 0 | 1 | 1 | 0.0369 | 0.1674 | 117.4 |
| hst_slog | 0.9211 | 0.9211 | 0.9603 | 0.9584 | -1.11e-16 | 2160 | 1 | 0 | 1 | 1 | 0.1872 | 0.06696 | 549.9 |
| kitnet | 1 | 1 | 1 | 1 | -2.776e-17 | 1800 | 1 | 0 | 1 | 1 | 0.01344 | 0.4204 | 2.867 |
| ecod_tail | 0.8684 | 0.8684 | 0.9339 | 0.9307 | -1.11e-16 | 720 | 1 | 0 | 1 | 1 | 0.0003168 | 0.0116 | 3.094 |
