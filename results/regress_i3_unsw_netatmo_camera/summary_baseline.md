# regress_i3_unsw_netatmo_camera

Windows: {'windows': 15537, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 6582, 'test_attack': 315, 'excluded': 60}. Window length 30 s; features (35): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts.

FPR resolution on test = 1/6582 = 0.000152; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.9937 | 0.1968 | 0.9905 | 0.9974 | 0.5607 | 2.188 | 0.9937 | 0 | 1 | 15 | 0.07899 | 0.003975 | 0.3076 |
| mad_tail_slog | 0.9968 | 0 | 0.986 | 0.9983 | 0.5814 | 2.625 | 0.9968 | 0 | 1 | 15 | 0.04935 | 0.007886 | 0.2734 |
| autoencoder_slog | 0.9968 | 0.4286 | 0.9863 | 0.9972 | 0.008298 | 3.5 | 0.9968 | 0 | 1 | 15 | 1.507 | 0.008984 | 2.629 |
| iforest_ext_sparse_slog | 0.9905 | 0.009524 | 0.9751 | 0.9974 | 0.5331 | 5.251 | 0.9937 | 30 | 1 | 15 | 0.3918 | 0.316 | 706.5 |
| hst_slog | 0.02222 | 0 | 0.574 | 0.6759 | 0.9864 | 0 | 0 | nan | 0 | 15 | 0.606 | 0.04962 | 549.9 |
| kitnet | 0.946 | 0.2 | 0.979 | 0.9897 | 0.2691 | 2.188 | 0.946 | 0 | 1 | 15 | 1.43 | 0.1423 | 1.799 |
