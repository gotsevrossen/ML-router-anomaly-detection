# regress_i7_kitsune_suite_video_injection

Windows: {'windows': 72, 'bootstrap': 30, 'validation': 18, 'test_benign': 13, 'test_attack': 11}. Window length 30 s; features (36): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/13 = 0.0769; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.9091 | 0.9091 | 0.9543 | 0.9526 | -5.551e-17 | 1108 | 1 | 0 | 1 | 1 | 0.0007153 | 0.002643 | 0.3164 |
| mad_tail_slog | 0.9091 | 0.9091 | 0.9543 | 0.9522 | -5.551e-17 | 221.5 | 0.9091 | 30 | 1 | 1 | 0.0003493 | 0.005306 | 0.2812 |
| autoencoder_slog | 1 | 1 | 1 | 1 | -1.735e-18 | 221.5 | 1 | 0 | 1 | 1 | 1.673 | 0.008144 | 2.703 |
| iforest_ext_sparse_slog | 0.9091 | 0.9091 | 0.9543 | 0.9632 | -5.551e-17 | 443.1 | 1 | 0 | 1 | 1 | 0.05294 | 0.3341 | 171.5 |
| hst_slog | 0.5455 | 0.5455 | 0.7716 | 0.8049 | -1.11e-16 | 0 | 0.3636 | 30 | 1 | 1 | 0.3765 | 0.08995 | 549.9 |
| kitnet | 1 | 1 | 1 | 1 | -2.776e-17 | 221.5 | 1 | 0 | 1 | 1 | 0.02677 | 0.4251 | 2.379 |
| ecod_tail | 0.9091 | 0.9091 | 0.9543 | 0.9632 | -1.11e-16 | 221.5 | 0.9091 | 30 | 1 | 1 | 0.000452 | 0.01516 | 4.5 |
