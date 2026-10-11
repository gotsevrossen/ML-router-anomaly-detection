# regress_ref_unsw_netatmo_camera

Windows: {'windows': 15537, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 6582, 'test_attack': 315, 'excluded': 60}. Window length 30 s; features (30): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos.

FPR resolution on test = 1/6582 = 0.000152; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.9683 | 0 | 0.9735 | 0.9873 | 0.5607 | 2.188 | 0.9683 | 150 | 1 | 15 | 0.1292 | 0.004529 | 0.2637 |
| mad_tail_slog | 0.8952 | 0.04127 | 0.9677 | 0.9905 | 0.5814 | 2.625 | 0.8952 | 180 | 1 | 15 | 0.06325 | 0.009131 | 0.2344 |
| autoencoder_slog | 0.9651 | 0.2222 | 0.9783 | 0.9952 | 0.008589 | 3.5 | 0.9841 | 30 | 1 | 15 | 1.347 | 0.005902 | 2.258 |
| iforest_ext_sparse_slog | 0.946 | 0.08254 | 0.9772 | 0.9976 | 0.5381 | 4.813 | 0.9841 | 30 | 1 | 15 | 0.3073 | 0.2164 | 708.5 |
| hst_slog | 0.0381 | 0.003175 | 0.6738 | 0.8211 | 0.9957 | 0.4376 | 0.003175 | 5.658e+04 | 0.06667 | 15 | 0.564 | 0.05828 | 549.9 |
| kitnet | 0.8667 | 0 | 0.9272 | 0.9442 | 0.2861 | 3.063 | 0.8667 | 1830 | 0.9333 | 15 | 1.134 | 0.1087 | 1.383 |
