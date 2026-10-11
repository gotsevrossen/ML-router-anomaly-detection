# regress_ref_unsw_late_tplink_plug

Windows: {'windows': 18434, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 9704, 'test_attack': 126, 'excluded': 24}. Window length 30 s; features (35): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/9704 = 0.000103; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.9921 | 0.3175 | 0.9918 | 0.9991 | 0.5809 | 15.43 | 1 | 0 | 1 | 6 | 0.1079 | 0.004652 | 0.3076 |
| mad_tail_slog | 1 | 0 | 0.9896 | 0.9989 | 0.6102 | 16.32 | 1 | 0 | 1 | 6 | 0.06361 | 0.009622 | 0.2734 |
| autoencoder_slog | 0.9921 | 0.9841 | 0.999 | 0.9999 | 0.03307 | 15.14 | 1 | 0 | 1 | 6 | 2.065 | 0.009402 | 2.629 |
| iforest_ext_sparse_slog | 0.9841 | 0.7619 | 0.9952 | 0.9995 | 0.679 | 7.42 | 0.9841 | 0 | 1 | 6 | 0.2472 | 0.3226 | 400.7 |
| hst_slog | 0.05556 | 0 | 0.5889 | 0.9519 | 0.986 | 1.781 | 0.007937 | 4.944e+04 | 0.1667 | 6 | 0.8421 | 0.06652 | 549.9 |
| kitnet | 1 | 0 | 0.9876 | 0.9987 | 0.2798 | 5.936 | 1 | 0 | 1 | 6 | 2.825 | 0.284 | 1.998 |
