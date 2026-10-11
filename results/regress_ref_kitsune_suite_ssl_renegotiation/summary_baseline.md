# regress_ref_kitsune_suite_ssl_renegotiation

Windows: {'windows': 78, 'bootstrap': 20, 'validation': 12, 'test_benign': 8, 'test_attack': 38}. Window length 30 s; features (28): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets.

FPR resolution on test = 1/8 = 0.125; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.8421 | 0.8421 | 0.9207 | 0.9169 | 0.6683 | 1080 | 0.9211 | 0 | 1 | 1 | 0.00108 | 0.006367 | 0.2461 |
| mad_tail_slog | 0.7368 | 0.7368 | 0.8678 | 0.8615 | 0.67 | 1440 | 0.8158 | 0 | 1 | 1 | 0.0004167 | 0.005928 | 0.2188 |
| autoencoder_slog | 0.8158 | 0.8158 | 0.9074 | 0.903 | 0.02171 | 1080 | 0.9474 | 0 | 1 | 1 | 1.215 | 0.01157 | 2.109 |
| iforest_ext_sparse_slog | 0.7632 | 0.7632 | 0.881 | 0.8753 | 0.4976 | 1080 | 0.9474 | 60 | 1 | 1 | 0.04369 | 0.14 | 131.6 |
| hst_slog | 0.7895 | 0.7895 | 0.8942 | 0.8892 | 0.7286 | 720 | 0.9211 | 90 | 1 | 1 | 0.1719 | 0.06546 | 549.9 |
| kitnet | 1 | 1 | 1 | 1 | 0.2693 | 1800 | 1 | 0 | 1 | 1 | 0.01714 | 0.1852 | 2.07 |
