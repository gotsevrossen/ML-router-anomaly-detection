# regress_ref_unsw_oct_amazon_echo

Windows: {'windows': 20723, 'bootstrap': 5760, 'validation': 2873, 'test_benign': 11874, 'test_attack': 188, 'excluded': 28}. Window length 30 s; features (32): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, arp_rep_in, n_arp_conflicts.

FPR resolution on test = 1/11874 = 8.42e-05; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.3351 | 0.3351 | 0.6659 | 0.9171 | 0.5736 | 75.19 | 0.9894 | 0 | 0.07683 | 0.009742 | 0.2812 |
| mad_tail_slog | 0 | 0 | 0.51 | 0.5923 | 0.6135 | 2465 | 1 | 0 | 0.04081 | 0.007779 | 0.25 |
| autoencoder_slog | 0.2926 | 0.01596 | 0.6409 | 0.9047 | 0.02112 | 92.65 | 0.9628 | 0 | 1.199 | 0.007447 | 2.406 |
| iforest_ext_sparse_slog | 0.5 | 0.005319 | 0.7384 | 0.9334 | 0.5754 | 265.8 | 0.9894 | 0 | 0.3133 | 0.2452 | 675.6 |
| hst_slog | 0.07979 | 0.02128 | 0.5701 | 0.839 | 0.9574 | 23.28 | 0.1809 | 30 | 0.5592 | 0.04821 | 549.9 |
| kitnet | 0.3351 | 0.3351 | 0.6678 | 0.6927 | 0.31 | 220.7 | 0.4681 | 0 | 1.751 | 0.1674 | 1.891 |
