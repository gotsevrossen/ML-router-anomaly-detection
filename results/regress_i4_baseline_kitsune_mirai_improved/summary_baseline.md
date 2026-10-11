# regress_i4_baseline_kitsune_mirai_improved

Windows: {'windows': 239, 'bootstrap': 60, 'validation': 45, 'test_benign': 44, 'test_attack': 90}. Window length 30 s; features (36): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/44 = 0.0227; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 1 | 1 | 1 | 1 | 0.5841 | 0 | 1 | 0 | 1 | 1 | 0.002264 | 0.00507 | 0.3164 |
| mad_tail_slog | 1 | 1 | 1 | 1 | 0.5889 | 65.45 | 1 | 0 | 1 | 1 | 0.001937 | 0.008758 | 0.2812 |
| autoencoder_slog | 1 | 1 | 1 | 1 | 0.01486 | 65.45 | 1 | 0 | 1 | 1 | 5.823 | 0.008377 | 2.703 |
| iforest_ext_sparse_slog | 1 | 1 | 1 | 1 | 0.4959 | 65.45 | 1 | 0 | 1 | 1 | 0.188 | 0.08085 | 241.6 |
| hst_slog | 0.9889 | 0.9889 | 0.9944 | 0.9987 | 0.8437 | 65.45 | 1 | 0 | 1 | 1 | 0.5232 | 0.03833 | 549.9 |
| kitnet | 1 | 1 | 1 | 1 | 0.3671 | 0 | 1 | 0 | 1 | 1 | 0.04911 | 0.185 | 2.168 |
