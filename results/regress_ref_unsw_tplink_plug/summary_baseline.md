# regress_ref_unsw_tplink_plug

Windows: {'windows': 15531, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 6426, 'test_attack': 441, 'excluded': 84}. Window length 30 s; features (30): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos.

FPR resolution on test = 1/6426 = 0.000156; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.8798 | 0.6553 | 0.9611 | 0.9805 | 0.5809 | 11.2 | 0.9569 | 240 | 1 | 21 | 0.06262 | 0.003138 | 0.2637 |
| mad_tail_slog | 0.8617 | 0.2857 | 0.9685 | 0.9951 | 0.5954 | 13 | 0.9955 | 30 | 1 | 21 | 0.04141 | 0.005792 | 0.2344 |
| autoencoder_slog | 0.8526 | 0.7052 | 0.9484 | 0.9888 | 0.03967 | 5.378 | 0.8685 | 240 | 1 | 21 | 1.198 | 0.007199 | 2.258 |
| iforest_ext_sparse_slog | 0.4762 | 0 | 0.8902 | 0.9819 | 0.6887 | 6.275 | 0.8277 | 240 | 1 | 21 | 0.328 | 0.2188 | 420.8 |
| hst_slog | 0 | 0 | 0.5508 | 0.8931 | 0.9936 | 1.793 | 0 | nan | 0 | 21 | 0.4163 | 0.04915 | 549.9 |
| kitnet | 0.9048 | 0.1814 | 0.9766 | 0.9879 | 0.2915 | 5.826 | 0.9705 | 240 | 1 | 21 | 1.92 | 0.1665 | 1.691 |
