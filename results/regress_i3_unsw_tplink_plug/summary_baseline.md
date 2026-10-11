# regress_i3_unsw_tplink_plug

Windows: {'windows': 15531, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 6426, 'test_attack': 441, 'excluded': 84}. Window length 30 s; features (35): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts.

FPR resolution on test = 1/6426 = 0.000156; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.9977 | 0.9864 | 0.9989 | 0.9999 | 0.5809 | 11.2 | 0.9977 | 0 | 1 | 21 | 0.06735 | 0.002862 | 0.3076 |
| mad_tail_slog | 0.6145 | 0.5624 | 0.9721 | 0.9971 | 0.5954 | 13 | 1 | 0 | 1 | 21 | 0.051 | 0.006743 | 0.2734 |
| autoencoder_slog | 0.9365 | 0.6576 | 0.9905 | 0.9989 | 0.03519 | 9.86 | 0.9977 | 0 | 1 | 21 | 1.428 | 0.008074 | 2.629 |
| iforest_ext_sparse_slog | 0.5782 | 0.2404 | 0.9219 | 0.9896 | 0.6728 | 9.86 | 0.8889 | 240 | 1 | 21 | 0.4188 | 0.2929 | 403.4 |
| hst_slog | 0.02494 | 0.02268 | 0.5899 | 0.9033 | 0.9932 | 2.241 | 0.02494 | 2.901e+04 | 0.2381 | 21 | 0.4556 | 0.04966 | 549.9 |
| kitnet | 0.9977 | 0.3197 | 0.9934 | 0.9988 | 0.2819 | 7.171 | 0.9977 | 0 | 1 | 21 | 1.99 | 0.1899 | 2.021 |
