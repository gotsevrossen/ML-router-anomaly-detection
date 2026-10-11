# regress_i5_unsw_oct_amazon_echo

Windows: {'windows': 20723, 'bootstrap': 5760, 'validation': 2873, 'test_benign': 11874, 'test_attack': 188, 'excluded': 28}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/11874 = 8.42e-05; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0 | 0 | 0.4975 | 0.8776 | 0.5749 | 77.61 | 0.9894 | 0 | 1 | 7 | 0.09277 | 0.005012 | 0.334 |
| mad_tail_slog | 0 | 0 | 0.5098 | 0.6095 | 0.6135 | 2467 | 1 | 0 | 1 | 7 | 0.07555 | 0.01203 | 0.2969 |
| autoencoder_slog | 0.2926 | 0 | 0.6399 | 0.9017 | 0.01537 | 183.1 | 0.984 | 0 | 1 | 7 | 2.247 | 0.01151 | 2.852 |
| iforest_ext_sparse_slog | 0.01596 | 0 | 0.5052 | 0.8783 | 0.5808 | 258.1 | 0.9947 | 0 | 1 | 7 | 0.4377 | 0.3324 | 768.6 |
| hst_slog | 0.5691 | 0 | 0.8962 | 0.9719 | 0.9261 | 5.336 | 0.8138 | 30 | 1 | 7 | 0.6576 | 0.07209 | 550 |
| kitnet | 0.3351 | 0.3351 | 0.6725 | 0.6997 | 0.3181 | 52.63 | 0.3777 | 0 | 0.7143 | 7 | 3.073 | 0.2825 | 2 |
| ecod_tail | 0 | 0 | 0.4975 | 0.8791 | 0.6991 | 70.1 | 0.9255 | 0 | 1 | 7 | 0.03669 | 0.01049 | 855.3 |
