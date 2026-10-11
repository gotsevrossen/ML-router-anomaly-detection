# regress_i6_kitsune_suite_syn_dos

Windows: {'windows': 106, 'bootstrap': 50, 'validation': 30, 'test_benign': 21, 'test_attack': 5}. Window length 30 s; features (36): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/21 = 0.0476; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.8 | 0.8 | 0.8995 | 0.8947 | 0.5449 | 0 | 0.4 | 90 | 1 | 1 | 0.001602 | 0.004606 | 0.3164 |
| mad_tail_slog | 0.4 | 0.4 | 0.702 | 0.7211 | 0.5809 | 0 | 0.4 | 90 | 1 | 1 | 0.0008422 | 0.009086 | 0.2812 |
| autoencoder_slog | 0.8 | 0.8 | 0.8995 | 0.8947 | 0.00886 | 0 | 0.4 | 90 | 1 | 1 | 2.057 | 0.01502 | 2.703 |
| iforest_ext_sparse_slog | 0.8 | 0.8 | 0.8995 | 0.8947 | 0.4515 | 0 | 0.8 | 30 | 1 | 1 | 0.1474 | 0.2905 | 251.2 |
| hst_slog | 0.8 | 0.8 | 0.8995 | 0.8947 | 0.6936 | 137.1 | 0.8 | 30 | 1 | 1 | 0.4603 | 0.07278 | 549.9 |
| kitnet | 0.8 | 0.8 | 0.8995 | 0.8947 | 0.1616 | 411.4 | 0.8 | 30 | 1 | 1 | 0.04092 | 0.3888 | 2.527 |
| ecod_tail | 0.8 | 0.8 | 0.8995 | 0.8947 | 0.6081 | 0 | 0.4 | 90 | 1 | 1 | 0.0004579 | 0.009733 | 7.312 |
