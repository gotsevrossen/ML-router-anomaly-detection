# regress_i7_baseline_kitsune_mirai_improved

Windows: {'windows': 239, 'bootstrap': 60, 'validation': 45, 'test_benign': 44, 'test_attack': 90}. Window length 30 s; features (36): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/44 = 0.0227; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 1 | 1 | 1 | 1 | -1.11e-16 | 196.4 | 1 | 0 | 1 | 1 | 0.0009969 | 0.002334 | 0.3164 |
| mad_tail_slog | 1 | 1 | 1 | 1 | -1.11e-16 | 65.45 | 1 | 0 | 1 | 1 | 0.001409 | 0.005253 | 0.2812 |
| autoencoder_slog | 1 | 1 | 1 | 1 | -8.674e-19 | 65.45 | 1 | 0 | 1 | 1 | 5.046 | 0.007158 | 2.703 |
| iforest_ext_sparse_slog | 1 | 1 | 1 | 1 | -5.551e-17 | 65.45 | 1 | 0 | 1 | 1 | 0.2494 | 0.1559 | 241.6 |
| hst_slog | 0.9889 | 0.9889 | 0.9944 | 0.9987 | -1.11e-16 | 65.45 | 1 | 0 | 1 | 1 | 0.6037 | 0.04349 | 549.9 |
| kitnet | 1 | 1 | 1 | 1 | -2.776e-17 | 196.4 | 1 | 0 | 1 | 1 | 0.06747 | 0.1762 | 2.168 |
| ecod_tail | 1 | 1 | 1 | 1 | -1.11e-16 | 0 | 1 | 0 | 1 | 1 | 0.0003526 | 0.01171 | 8.719 |
