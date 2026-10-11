# regress_i6_unsw_oct_amazon_echo

Windows: {'windows': 20723, 'bootstrap': 5760, 'validation': 2873, 'test_benign': 11874, 'test_attack': 188, 'excluded': 28}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/11874 = 8.42e-05; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0 | 0 | 0.4975 | 0.8583 | 0.5345 | 76.4 | 0.9255 | 60 | 1 | 7 | 0.0987 | 0.00515 | 0.334 |
| mad_tail_slog | 0 | 0 | 0.5098 | 0.6083 | 0.5809 | 2453 | 1 | 0 | 1 | 7 | 0.07029 | 0.01357 | 0.2969 |
| autoencoder_slog | 0.2394 | 0.2394 | 0.6178 | 0.8803 | 0.008107 | 393.7 | 0.9415 | 60 | 1 | 7 | 2.269 | 0.01251 | 2.852 |
| iforest_ext_sparse_slog | 0 | 0 | 0.4975 | 0.8607 | 0.4618 | 2197 | 1 | 0 | 1 | 7 | 0.7064 | 0.3185 | 768.6 |
| hst_slog | 0.8085 | 0.8085 | 0.9035 | 0.9516 | 0.8076 | 71.55 | 0.9202 | 60 | 1 | 7 | 0.5797 | 0.06301 | 550 |
| kitnet | 0.3032 | 0.3032 | 0.6575 | 0.6735 | 0.3157 | 5.579 | 0.3138 | 60 | 0.5714 | 7 | 2.551 | 0.2568 | 2 |
| ecod_tail | 0 | 0 | 0.4975 | 0.8589 | 0.6281 | 504.7 | 0.9628 | 0 | 1 | 7 | 0.04675 | 0.02332 | 855.3 |
