# regress_i6_unsw_late_samsung_camera

Windows: {'windows': 18436, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 9642, 'test_attack': 186, 'excluded': 28}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/9642 = 0.000104; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.6022 | 0.4032 | 0.798 | 0.8538 | 0.5202 | 184.9 | 0.9247 | 60 | 1 | 7 | 0.07863 | 0.003839 | 0.334 |
| mad_tail_slog | 0.9247 | 0 | 0.949 | 0.9593 | 0.618 | 1.195 | 0.9247 | 60 | 1 | 7 | 0.05683 | 0.008617 | 0.2969 |
| autoencoder_slog | 0.1075 | 0.1075 | 0.5515 | 0.7062 | 0.01434 | 184.9 | 0.8172 | 660 | 1 | 7 | 1.62 | 0.01555 | 2.852 |
| iforest_ext_sparse_slog | 0.5968 | 0.5968 | 0.7974 | 0.8526 | 0.5933 | 184.9 | 0.9032 | 90 | 1 | 7 | 0.3341 | 0.2971 | 748.2 |
| hst_slog | 0 | 0 | 0.4975 | 0.6502 | 0.6813 | 184.9 | 0.8065 | 690 | 1 | 7 | 0.4887 | 0.05274 | 550 |
| kitnet | 0.6075 | 0 | 0.7943 | 0.7925 | 0.2852 | 98.87 | 0.6075 | 2.228e+05 | 0.8571 | 7 | 1.585 | 0.1565 | 2 |
| ecod_tail | 0.8656 | 0.1828 | 0.952 | 0.9629 | 0.668 | 0.8961 | 0.8011 | 660 | 1 | 7 | 0.1664 | 0.006056 | 846.4 |
