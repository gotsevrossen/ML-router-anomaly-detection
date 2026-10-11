# regress_ref_unsw_late_samsung_camera

Windows: {'windows': 18436, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 9642, 'test_attack': 186, 'excluded': 28}. Window length 30 s; features (35): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/9642 = 0.000104; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.6667 | 0.4462 | 0.8302 | 0.8858 | 0.5809 | 185.8 | 0.6667 | 2.227e+05 | 0.8571 | 7 | 0.1055 | 0.003753 | 0.3076 |
| mad_tail_slog | 0.672 | 0 | 0.9642 | 0.9963 | 0.7071 | 1.493 | 0.6613 | 2.227e+05 | 0.8571 | 7 | 0.06158 | 0.009753 | 0.2734 |
| autoencoder_slog | 0 | 0 | 0.4975 | 0.6725 | 0.02482 | 184.6 | 0.6667 | 2.227e+05 | 0.8571 | 7 | 1.673 | 0.008726 | 2.629 |
| iforest_ext_sparse_slog | 0.4355 | 0.2688 | 0.7165 | 0.8093 | 0.6604 | 184.6 | 0.5538 | 2.228e+05 | 0.8571 | 7 | 0.2908 | 0.2517 | 665.3 |
| hst_slog | 0.5 | 0.1935 | 0.7471 | 0.8228 | 0.9116 | 180.4 | 0.5 | 2.243e+05 | 0.7143 | 7 | 0.8597 | 0.07266 | 549.9 |
| kitnet | 0.6667 | 0 | 0.822 | 0.8235 | 0.3473 | 1.195 | 0.6667 | 2.227e+05 | 0.8571 | 7 | 2.78 | 0.2084 | 1.822 |
