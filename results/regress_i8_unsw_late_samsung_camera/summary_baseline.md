# regress_i8_unsw_late_samsung_camera

Windows: {'windows': 18436, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 9642, 'test_attack': 186, 'excluded': 28}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/9642 = 0.000104; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.6505 | 0.4032 | 0.8217 | 0.8816 | -1.11e-16 | 185.5 | 0.9892 | 60 | 1 | 7 | 0.09165 | 0.01409 | 0.334 |
| mad_tail_slog | 0.9892 | 0 | 0.9787 | 0.9927 | -1.11e-16 | 1.195 | 0.672 | 2.227e+05 | 0.8571 | 7 | 0.05691 | 0.01074 | 0.2969 |
| autoencoder_slog | 0.1075 | 0.1075 | 0.5515 | 0.7155 | -1.735e-18 | 185.5 | 0.8817 | 660 | 1 | 7 | 1.702 | 0.009936 | 2.852 |
| iforest_ext_sparse_slog | 0.5968 | 0.5968 | 0.7974 | 0.8639 | -1.11e-16 | 185.8 | 0.9677 | 90 | 1 | 7 | 0.3165 | 0.3335 | 748.2 |
| hst_slog | 0 | 0 | 0.4975 | 0.6583 | -1.11e-16 | 185.5 | 0.8118 | 690 | 1 | 7 | 0.5909 | 0.04874 | 550 |
| kitnet | 0.6667 | 0 | 0.8219 | 0.8235 | -5.551e-17 | 99.17 | 0.6667 | 2.227e+05 | 0.8571 | 7 | 1.637 | 0.1663 | 2 |
| ecod_tail | 0.9355 | 0.1828 | 0.9781 | 0.9971 | -1.11e-16 | 1.195 | 0.8656 | 660 | 1 | 7 | 0.02153 | 0.005815 | 846.7 |
| ecod_router | 0.9355 | 0.1828 | 0.9781 | 0.9971 | -1.11e-16 | 1.195 | 0.8656 | 660 | 1 | 7 | 0.03014 | 0.005494 | 22.09 |
