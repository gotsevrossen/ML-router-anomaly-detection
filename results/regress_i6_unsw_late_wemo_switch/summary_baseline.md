# regress_i6_unsw_late_wemo_switch

Windows: {'windows': 18435, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 9705, 'test_attack': 126, 'excluded': 24}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/9705 = 0.000103; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.9127 | 0.5794 | 0.9601 | 0.9656 | 0.5156 | 1.484 | 0.9127 | 60 | 1 | 6 | 0.06706 | 0.003337 | 0.334 |
| mad_tail_slog | 0.9048 | 0.873 | 0.9527 | 0.9579 | 0.5809 | 0.5935 | 0.9048 | 60 | 1 | 6 | 0.04299 | 0.01614 | 0.2969 |
| autoencoder_slog | 0.9048 | 0.9048 | 0.9554 | 0.9613 | 0.00699 | 7.419 | 0.9127 | 60 | 1 | 6 | 1.579 | 0.007474 | 2.852 |
| iforest_ext_sparse_slog | 0.9048 | 0.9048 | 0.9549 | 0.9649 | 0.4257 | 3.858 | 0.9048 | 60 | 1 | 6 | 0.3436 | 0.2793 | 726.8 |
| hst_slog | 0.9206 | 0.9048 | 0.9618 | 0.9676 | 0.8027 | 5.045 | 0.9206 | 60 | 1 | 6 | 0.6234 | 0.05391 | 550 |
| kitnet | 0.9048 | 0 | 0.9428 | 0.9489 | 0.2915 | 0.8903 | 0.9048 | 60 | 1 | 6 | 1.551 | 0.1454 | 2.047 |
| ecod_tail | 0.9127 | 0.6984 | 0.9595 | 0.971 | 0.6132 | 3.264 | 0.9127 | 60 | 1 | 6 | 0.02248 | 0.006461 | 846.4 |
