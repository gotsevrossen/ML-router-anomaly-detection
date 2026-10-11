# regress_i5_unsw_late_samsung_camera

Windows: {'windows': 18436, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 9642, 'test_attack': 186, 'excluded': 28}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/9642 = 0.000104; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.6667 | 0.4462 | 0.8302 | 0.8853 | 0.5809 | 184.9 | 0.6667 | 2.227e+05 | 0.8571 | 7 | 0.06411 | 0.003368 | 0.334 |
| mad_tail_slog | 0.672 | 0 | 0.9695 | 0.9968 | 0.6774 | 1.195 | 0.6667 | 2.227e+05 | 0.8571 | 7 | 0.05048 | 0.00738 | 0.2969 |
| autoencoder_slog | 0.2312 | 0 | 0.6125 | 0.7605 | 0.02609 | 184.3 | 0.6667 | 2.227e+05 | 0.8571 | 7 | 1.402 | 0.009693 | 2.852 |
| iforest_ext_sparse_slog | 0.6613 | 0.5806 | 0.8292 | 0.8847 | 0.6522 | 185.2 | 0.8118 | 630 | 1 | 7 | 0.3197 | 0.2555 | 748.2 |
| hst_slog | 0 | 0 | 0.4975 | 0.6445 | 0.8742 | 184.6 | 0.07527 | 2.806e+05 | 0.2857 | 7 | 0.5474 | 0.0547 | 550 |
| kitnet | 0.6667 | 0 | 0.822 | 0.8235 | 0.3417 | 1.195 | 0.6667 | 2.227e+05 | 0.8571 | 7 | 1.8 | 0.1601 | 2 |
| ecod_tail | 0.871 | 0.2043 | 0.9678 | 0.9964 | 0.6815 | 1.195 | 0.6667 | 2.227e+05 | 0.8571 | 7 | 0.02205 | 0.005455 | 846.4 |
