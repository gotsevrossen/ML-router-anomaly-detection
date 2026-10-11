# regress_i2_unsw_samsung_camera

Windows: {'windows': 15537, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 6134, 'test_attack': 691, 'excluded': 132}. Window length 30 s; features (33): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports.

FPR resolution on test = 1/6134 = 0.000163; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.5499 | 0.2388 | 0.8984 | 0.9886 | 0.5809 | 6.573 | 0.5948 | 90 | 0.08077 | 0.003231 | 0.29 |
| mad_tail_slog | 0.2489 | 0.2475 | 0.8193 | 0.9619 | 0.6774 | 9.39 | 0.6179 | 90 | 0.0459 | 0.006942 | 0.2578 |
| autoencoder_slog | 0.6382 | 0 | 0.8935 | 0.9827 | 0.02698 | 1.409 | 0.5311 | 1710 | 1.313 | 0.01832 | 2.48 |
| iforest_ext_sparse_slog | 0.3097 | 0.2315 | 0.8543 | 0.9838 | 0.664 | 7.982 | 0.4182 | 90 | 0.3175 | 0.2485 | 627.3 |
| hst_slog | 0.3763 | 0 | 0.8446 | 0.9167 | 0.9382 | 0.4695 | 0.08538 | 2.592e+04 | 0.444 | 0.05653 | 549.9 |
| kitnet | 0.5557 | 0 | 0.7676 | 0.7654 | 0.3496 | 0.939 | 0.5398 | 2.568e+04 | 1.506 | 0.1591 | 1.682 |
