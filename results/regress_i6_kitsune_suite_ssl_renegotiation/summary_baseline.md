# regress_i6_kitsune_suite_ssl_renegotiation

Windows: {'windows': 78, 'bootstrap': 20, 'validation': 12, 'test_benign': 8, 'test_attack': 38}. Window length 30 s; features (36): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/8 = 0.125; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.8947 | 0.8947 | 0.9471 | 0.9446 | 0.3042 | 0 | 0.8947 | 120 | 1 | 1 | 0.001094 | 0.004903 | 0.3164 |
| mad_tail_slog | 0.8947 | 0.8947 | 0.9471 | 0.9446 | 0.3384 | 0 | 0.8947 | 120 | 1 | 1 | 0.0005501 | 0.009645 | 0.2812 |
| autoencoder_slog | 1 | 1 | 1 | 1 | 0.01163 | 720 | 1 | 0 | 1 | 1 | 1.721 | 0.01384 | 2.703 |
| iforest_ext_sparse_slog | 0.8947 | 0.8947 | 0.9471 | 0.9446 | 0.3353 | 1800 | 0.9211 | 0 | 1 | 1 | 0.06567 | 0.2978 | 117.4 |
| hst_slog | 0.8947 | 0.8947 | 0.9471 | 0.9446 | 0.5468 | 1800 | 1 | 0 | 1 | 1 | 0.2058 | 0.05899 | 549.9 |
| kitnet | 0.9474 | 0.9474 | 0.9736 | 0.9723 | 0.2006 | 720 | 0.9474 | 60 | 1 | 1 | 0.01921 | 0.4429 | 2.867 |
| ecod_tail | 0.8158 | 0.8158 | 0.9074 | 0.903 | 0.5845 | 720 | 1 | 0 | 1 | 1 | 0.0003165 | 0.01114 | 3.094 |
