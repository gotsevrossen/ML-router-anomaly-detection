# regress_i6_unsw_samsung_camera

Windows: {'windows': 15537, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 6134, 'test_attack': 691, 'excluded': 132}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/6134 = 0.000163; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.1592 | 0.1592 | 0.8314 | 0.9459 | 0.5202 | 11.27 | 0.9001 | 60 | 1 | 33 | 0.08947 | 0.003943 | 0.334 |
| mad_tail_slog | 0.2229 | 0.2229 | 0.8478 | 0.9417 | 0.618 | 9.86 | 0.6585 | 60 | 0.7273 | 33 | 0.06986 | 0.01925 | 0.2969 |
| autoencoder_slog | 0.05789 | 0.04486 | 0.8008 | 0.9429 | 0.01434 | 11.27 | 0.7135 | 60 | 0.8485 | 33 | 2.045 | 0.008147 | 2.852 |
| iforest_ext_sparse_slog | 0.4776 | 0.2981 | 0.883 | 0.9464 | 0.5933 | 10.33 | 0.8249 | 120 | 0.9394 | 33 | 0.3369 | 0.2687 | 748.2 |
| hst_slog | 0.1375 | 0 | 0.8003 | 0.9393 | 0.6813 | 11.27 | 0.8075 | 60 | 0.9394 | 33 | 0.8296 | 0.07288 | 550 |
| kitnet | 0 | 0 | 0.6988 | 0.7669 | 0.2852 | 9.39 | 0.5745 | 60 | 0.6364 | 33 | 2.262 | 0.24 | 2 |
| ecod_tail | 0.288 | 0.2692 | 0.8507 | 0.9423 | 0.668 | 9.86 | 0.7511 | 60 | 0.8788 | 33 | 0.02703 | 0.008396 | 846.4 |
