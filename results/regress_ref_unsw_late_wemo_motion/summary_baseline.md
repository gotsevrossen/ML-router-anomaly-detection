# regress_ref_unsw_late_wemo_motion

Windows: {'windows': 18436, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 9566, 'test_attack': 250, 'excluded': 40}. Window length 30 s; features (35): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/9566 = 0.000105; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.736 | 0.428 | 0.8858 | 0.9399 | 0.5971 | 0.9032 | 0.652 | 630 | 0.9 | 10 | 0.09159 | 0.00386 | 0.3076 |
| mad_tail_slog | 0.732 | 0 | 0.8598 | 0.9245 | 0.6442 | 3.613 | 0.732 | 4140 | 0.9 | 10 | 0.1162 | 0.007981 | 0.2734 |
| autoencoder_slog | 0.016 | 0 | 0.6291 | 0.9379 | 0.0227 | 2.409 | 0.004 | 2.099e+05 | 0.1 | 10 | 6.119 | 0.008662 | 2.629 |
| iforest_ext_sparse_slog | 0.124 | 0 | 0.6362 | 0.892 | 0.6452 | 0.3011 | 0.044 | 7410 | 0.3 | 10 | 0.3885 | 0.2665 | 610.2 |
| hst_slog | 0.028 | 0 | 0.5227 | 0.6806 | 0.9788 | 1.806 | 0.004 | 7680 | 0.1 | 10 | 0.8354 | 0.05567 | 549.9 |
| kitnet | 0.824 | 0 | 0.8992 | 0.9087 | 0.2956 | 1.204 | 0.732 | 600 | 0.9 | 10 | 1.907 | 0.2096 | 1.908 |
