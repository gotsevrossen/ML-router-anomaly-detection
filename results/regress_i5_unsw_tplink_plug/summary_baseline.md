# regress_i5_unsw_tplink_plug

Windows: {'windows': 15531, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 6426, 'test_attack': 441, 'excluded': 84}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/6426 = 0.000156; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.9977 | 0.9864 | 0.9994 | 0.9999 | 0.5809 | 11.2 | 1 | 0 | 1 | 21 | 0.1362 | 0.005659 | 0.334 |
| mad_tail_slog | 0.6145 | 0.5624 | 0.9725 | 0.9971 | 0.6102 | 12.1 | 1 | 0 | 1 | 21 | 0.07306 | 0.01182 | 0.2969 |
| autoencoder_slog | 0.9252 | 0.5714 | 0.9845 | 0.9984 | 0.03459 | 9.86 | 0.9887 | 30 | 1 | 21 | 2.408 | 0.01228 | 2.852 |
| iforest_ext_sparse_slog | 0.8639 | 0.002268 | 0.9554 | 0.9949 | 0.6992 | 5.378 | 0.9161 | 240 | 1 | 21 | 0.3584 | 0.4347 | 451.8 |
| hst_slog | 0 | 0 | 0.5409 | 0.909 | 0.995 | 4.482 | 0 | nan | 0 | 21 | 0.9271 | 0.084 | 550 |
| kitnet | 0.9977 | 0.3197 | 0.9944 | 0.9994 | 0.2762 | 6.275 | 1 | 0 | 1 | 21 | 3.85 | 0.3587 | 2.223 |
| ecod_tail | 0.9864 | 0.8889 | 0.9954 | 0.9995 | 0.6643 | 15.24 | 0.9977 | 0 | 1 | 21 | 0.04522 | 0.009371 | 846.4 |
