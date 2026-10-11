# regress_ref_unsw_samsung_camera

Windows: {'windows': 15537, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 6134, 'test_attack': 691, 'excluded': 132}. Window length 30 s; features (30): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos.

FPR resolution on test = 1/6134 = 0.000163; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.5514 | 0 | 0.9079 | 0.9877 | 0.5809 | 6.573 | 0.5991 | 90 | 0.6364 | 33 | 0.07322 | 0.003021 | 0.2637 |
| mad_tail_slog | 0.005789 | 0.005789 | 0.7658 | 0.9241 | 0.7071 | 9.39 | 0.6165 | 90 | 0.6364 | 33 | 0.04129 | 0.006617 | 0.2344 |
| autoencoder_slog | 0.6512 | 0 | 0.8955 | 0.9841 | 0.02425 | 2.348 | 0.5904 | 1710 | 0.6667 | 33 | 1.239 | 0.007309 | 2.258 |
| iforest_ext_sparse_slog | 0.2793 | 0.1606 | 0.838 | 0.9819 | 0.6611 | 10.33 | 0.4906 | 90 | 0.6061 | 33 | 0.2895 | 0.1959 | 691.7 |
| hst_slog | 0.1505 | 0 | 0.7665 | 0.8416 | 0.8976 | 1.409 | 0.1013 | 2.754e+04 | 0.2121 | 33 | 0.5465 | 0.05119 | 549.9 |
| kitnet | 0.5702 | 0 | 0.7751 | 0.7749 | 0.3432 | 0.939 | 0.5456 | 1830 | 0.5758 | 33 | 1.775 | 0.1632 | 1.609 |
