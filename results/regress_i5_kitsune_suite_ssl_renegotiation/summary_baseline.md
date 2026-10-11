# regress_i5_kitsune_suite_ssl_renegotiation

Windows: {'windows': 78, 'bootstrap': 20, 'validation': 12, 'test_benign': 8, 'test_attack': 38}. Window length 30 s; features (36): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/8 = 0.125; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.8684 | 0.8684 | 0.9339 | 0.9307 | 0.5298 | 0 | 0.8684 | 90 | 1 | 1 | 0.001312 | 0.006432 | 0.3164 |
| mad_tail_slog | 0.7368 | 0.7368 | 0.8715 | 0.9003 | 0.5809 | 0 | 0.7368 | 90 | 1 | 1 | 0.0006484 | 0.01141 | 0.2812 |
| autoencoder_slog | 0.8421 | 0.8421 | 0.9207 | 0.9169 | 0.01547 | 1080 | 0.9737 | 0 | 1 | 1 | 2.318 | 0.01693 | 2.703 |
| iforest_ext_sparse_slog | 0.8158 | 0.8158 | 0.9074 | 0.903 | 0.4905 | 0 | 0.7895 | 90 | 1 | 1 | 0.05241 | 0.2663 | 117.4 |
| hst_slog | 0.8684 | 0.8684 | 0.9339 | 0.9307 | 0.6509 | 360 | 0.8947 | 90 | 1 | 1 | 0.246 | 0.08897 | 549.9 |
| kitnet | 1 | 1 | 1 | 1 | 0.2347 | 1800 | 1 | 0 | 1 | 1 | 0.02344 | 0.5401 | 2.867 |
| ecod_tail | 0.7895 | 0.7895 | 0.8942 | 0.8892 | 0.5961 | 360 | 0.7895 | 0 | 1 | 1 | 0.0004047 | 0.01382 | 3.094 |
