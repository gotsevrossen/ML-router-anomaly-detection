# regress_i6_kitsune_suite_os_scan

Windows: {'windows': 105, 'bootstrap': 44, 'validation': 26, 'test_benign': 32, 'test_attack': 3}. Window length 30 s; features (36): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/32 = 0.0312; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0 | 0 | 0.5 | 0.5 | 0.2444 | 0 | 0 | nan | 0 | 2 | 0.000817 | 0.002492 | 0.3164 |
| mad_tail_slog | 0 | 0 | 0.5511 | 0.7697 | 0.06349 | 180 | 0.6667 | 0 | 0.5 | 2 | 0.0004696 | 0.005711 | 0.2812 |
| autoencoder_slog | 0 | 0 | 0.5511 | 0.7697 | 0.003496 | 180 | 0.6667 | 0 | 0.5 | 2 | 2.101 | 0.008333 | 2.703 |
| iforest_ext_sparse_slog | 0 | 0 | 0.4975 | 0.6601 | 0.3219 | 360 | 0.6667 | 0 | 0.5 | 2 | 0.1149 | 0.3043 | 199.8 |
| hst_slog | 0 | 0 | 0.5511 | 0.7697 | 0.3843 | 450 | 0.6667 | 0 | 0.5 | 2 | 0.5181 | 0.08273 | 549.9 |
| kitnet | 0 | 0 | 0.4975 | 0.5504 | 0.1039 | 0 | 0 | nan | 0 | 2 | 0.04721 | 0.5649 | 3.004 |
| ecod_tail | 0 | 0 | 0.5511 | 0.7697 | 0.5738 | 270 | 0.6667 | 0 | 0.5 | 2 | 0.0006216 | 0.01167 | 6.469 |
