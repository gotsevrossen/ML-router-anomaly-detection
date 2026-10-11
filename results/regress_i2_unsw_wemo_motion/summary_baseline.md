# regress_i2_unsw_wemo_motion

Windows: {'windows': 15537, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 6358, 'test_attack': 503, 'excluded': 96}. Window length 30 s; features (33): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports.

FPR resolution on test = 1/6358 = 0.000157; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.5467 | 0.4056 | 0.7774 | 0.8534 | 0.5971 | 0.453 | 0.4771 | 2.574e+04 | 0.05535 | 0.002376 | 0.29 |
| mad_tail_slog | 0.7654 | 0 | 0.8872 | 0.9377 | 0.6442 | 2.265 | 0.7654 | 270 | 0.04089 | 0.008735 | 0.2578 |
| autoencoder_slog | 0.03181 | 0.005964 | 0.6094 | 0.8878 | 0.02893 | 0.9059 | 0.03181 | 540 | 4.63 | 0.006722 | 2.48 |
| iforest_ext_sparse_slog | 0.1571 | 0.07753 | 0.6632 | 0.8839 | 0.6635 | 0 | 0.02187 | 4.47e+04 | 0.3526 | 0.2338 | 541.4 |
| hst_slog | 0 | 0 | 0.5023 | 0.687 | 0.9941 | 0 | 0 | nan | 0.7033 | 0.04676 | 549.9 |
| kitnet | 0.5109 | 0 | 0.7513 | 0.7468 | 0.3076 | 0.453 | 0.4473 | 2.571e+04 | 1.516 | 0.1539 | 1.701 |
