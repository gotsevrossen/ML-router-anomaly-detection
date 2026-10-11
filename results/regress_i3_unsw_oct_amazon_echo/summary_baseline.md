# regress_i3_unsw_oct_amazon_echo

Windows: {'windows': 20723, 'bootstrap': 5760, 'validation': 2873, 'test_benign': 11874, 'test_attack': 188, 'excluded': 28}. Window length 30 s; features (35): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts.

FPR resolution on test = 1/11874 = 8.42e-05; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0 | 0 | 0.4975 | 0.8776 | 0.5749 | 77.37 | 0.9894 | 0 | 1 | 7 | 0.06121 | 0.004683 | 0.3076 |
| mad_tail_slog | 0 | 0 | 0.5098 | 0.6095 | 0.6135 | 2467 | 1 | 0 | 1 | 7 | 0.0498 | 0.007597 | 0.2734 |
| autoencoder_slog | 0.2926 | 0 | 0.6403 | 0.9025 | 0.0193 | 127.8 | 0.9681 | 0 | 1 | 7 | 1.379 | 0.008664 | 2.629 |
| iforest_ext_sparse_slog | 0.2872 | 0 | 0.6533 | 0.9095 | 0.5894 | 286.2 | 0.9894 | 0 | 1 | 7 | 0.3049 | 0.2832 | 680.7 |
| hst_slog | 0.4255 | 0.2128 | 0.7783 | 0.9463 | 0.94 | 7.034 | 0.4947 | 30 | 1 | 7 | 0.5678 | 0.05337 | 549.9 |
| kitnet | 0.3351 | 0.3351 | 0.6734 | 0.7417 | 0.3046 | 188 | 0.5479 | 0 | 0.7143 | 7 | 1.864 | 0.1903 | 2.045 |
