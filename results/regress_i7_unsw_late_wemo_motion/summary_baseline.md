# regress_i7_unsw_late_wemo_motion

Windows: {'windows': 18436, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 9566, 'test_attack': 250, 'excluded': 40}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/9566 = 0.000105; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.756 | 0.476 | 0.8788 | 0.9412 | -1.11e-16 | 2.107 | 0.756 | 630 | 0.9 | 10 | 0.07806 | 0.004771 | 0.334 |
| mad_tail_slog | 0.732 | 0 | 0.8643 | 0.9488 | -1.11e-16 | 3.613 | 0.732 | 4140 | 0.9 | 10 | 0.0562 | 0.007254 | 0.2969 |
| autoencoder_slog | 0.568 | 0 | 0.872 | 0.9573 | -1.735e-18 | 7.828 | 0.696 | 480 | 0.9 | 10 | 2.211 | 0.008892 | 2.852 |
| iforest_ext_sparse_slog | 0.524 | 0.312 | 0.7988 | 0.9399 | -1.11e-16 | 1.204 | 0.5 | 1620 | 0.8 | 10 | 0.2384 | 0.2917 | 639.7 |
| hst_slog | 0.004 | 0.004 | 0.5193 | 0.6633 | -1.11e-16 | 2.409 | 0.004 | 7830 | 0.1 | 10 | 0.7 | 0.05235 | 550 |
| kitnet | 0.808 | 0 | 0.891 | 0.8991 | -5.551e-17 | 2.409 | 0.808 | 600 | 1 | 10 | 2.066 | 0.1933 | 2.156 |
| ecod_tail | 0.872 | 0.616 | 0.978 | 0.9966 | -1.11e-16 | 3.312 | 0.88 | 60 | 1 | 10 | 0.02281 | 0.00804 | 846.4 |
