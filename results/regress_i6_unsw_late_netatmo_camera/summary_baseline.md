# regress_i6_unsw_late_netatmo_camera

Windows: {'windows': 18436, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 9706, 'test_attack': 126, 'excluded': 24}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/9706 = 0.000103; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.9127 | 0 | 0.942 | 0.9639 | 0.5406 | 1.187 | 0.9127 | 60 | 1 | 6 | 0.06398 | 0.003231 | 0.334 |
| mad_tail_slog | 0.9127 | 0 | 0.942 | 0.9639 | 0.5801 | 2.077 | 0.9127 | 60 | 1 | 6 | 0.05892 | 0.008357 | 0.2969 |
| autoencoder_slog | 0.9206 | 0.5873 | 0.9561 | 0.9615 | 0.002806 | 8.012 | 0.9206 | 60 | 1 | 6 | 1.323 | 0.008607 | 2.852 |
| iforest_ext_sparse_slog | 0.9127 | 0.8889 | 0.9593 | 0.9776 | 0.429 | 3.264 | 0.9127 | 60 | 1 | 6 | 0.3785 | 0.3194 | 770.6 |
| hst_slog | 0.9048 | 0.8889 | 0.9546 | 0.9661 | 0.8343 | 0 | 0.8889 | 90 | 1 | 6 | 0.5928 | 0.05227 | 550 |
| kitnet | 0.8651 | 0 | 0.9188 | 0.9276 | 0.259 | 1.78 | 0.8651 | 90 | 1 | 6 | 1.363 | 0.1397 | 1.918 |
| ecod_tail | 0.9206 | 0 | 0.9517 | 0.9711 | 0.6171 | 3.264 | 0.9286 | 60 | 1 | 6 | 0.02454 | 0.006937 | 846.4 |
