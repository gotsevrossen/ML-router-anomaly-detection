# kitsune_suite_ssl_renegotiation

Windows: {'windows': 78, 'bootstrap': 20, 'validation': 12, 'test_benign': 8, 'test_attack': 38}. Window length 30 s; features (28): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets.

FPR resolution on test = 1/8 = 0.125; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.8421 | 0.8421 | 0.9207 | 0.9169 | 0.6683 | 1080 | 0.9211 | 0 | 0.0006753 | 0.003217 | 0.2461 |
| mad_tail_slog | 0.7368 | 0.7368 | 0.8678 | 0.8615 | 0.67 | 1440 | 0.8158 | 0 | 0.0004057 | 0.005642 | 0.2188 |
| autoencoder_slog | 0.8158 | 0.8158 | 0.9074 | 0.903 | 0.02021 | 1080 | 0.9474 | 0 | 0.6537 | 0.03094 | 2.109 |
| kitnet_windows | 1 | 1 | 1 | 1 | 0.2693 | 1800 | 1 | 0 | 0.02242 | 0.4303 | 2.07 |
| hst | 0.7895 | 0.7895 | 0.8942 | 0.8892 | 0.7553 | 360 | 0.9211 | 90 | 0.168 | 0.04069 | 549.9 |
