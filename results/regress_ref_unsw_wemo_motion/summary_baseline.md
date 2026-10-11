# regress_ref_unsw_wemo_motion

Windows: {'windows': 15537, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 6358, 'test_attack': 503, 'excluded': 96}. Window length 30 s; features (30): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos.

FPR resolution on test = 1/6358 = 0.000157; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.5467 | 0.4056 | 0.7774 | 0.858 | 0.5971 | 0.453 | 0.4592 | 2.574e+04 | 0.05467 | 0.002311 | 0.2637 |
| mad_tail_slog | 0.4354 | 0.02386 | 0.7306 | 0.851 | 0.6442 | 2.265 | 0.4294 | 270 | 0.04142 | 0.007567 | 0.2344 |
| autoencoder_slog | 0.02783 | 0.007952 | 0.5924 | 0.8716 | 0.03272 | 2.718 | 0.02783 | 540 | 4.346 | 0.006498 | 2.258 |
| iforest_ext_sparse_slog | 0.2962 | 0.1531 | 0.6895 | 0.8494 | 0.6521 | 0 | 0.1511 | 270 | 0.5084 | 0.215 | 530.8 |
| hst_slog | 0 | 0 | 0.5059 | 0.6528 | 0.9945 | 1.812 | 0 | nan | 0.7725 | 0.05433 | 549.9 |
| kitnet | 0.5666 | 0 | 0.7819 | 0.8002 | 0.2899 | 1.359 | 0.4831 | 2.571e+04 | 1.425 | 0.138 | 1.473 |
