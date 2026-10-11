# regress_i7_unsw_wemo_motion

Windows: {'windows': 15537, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 6358, 'test_attack': 503, 'excluded': 96}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/6358 = 0.000157; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.6839 | 0.5507 | 0.8399 | 0.8763 | -1.11e-16 | 1.812 | 0.6839 | 0 | 0.7083 | 24 | 0.09869 | 0.004157 | 0.334 |
| mad_tail_slog | 0.8588 | 0.7256 | 0.9289 | 0.9551 | -1.11e-16 | 2.718 | 0.8588 | 90 | 0.875 | 24 | 0.05456 | 0.01043 | 0.2969 |
| autoencoder_slog | 0.5328 | 0.1491 | 0.86 | 0.9333 | -1.735e-18 | 8.606 | 0.6958 | 0 | 0.875 | 24 | 1.87 | 0.01038 | 2.852 |
| iforest_ext_sparse_slog | 0.6183 | 0.3101 | 0.8697 | 0.9511 | -1.11e-16 | 2.718 | 0.6064 | 180 | 0.7917 | 24 | 0.4841 | 0.3407 | 639.7 |
| hst_slog | 0.005964 | 0 | 0.512 | 0.6775 | -1.11e-16 | 2.265 | 0.005964 | 240 | 0.08333 | 24 | 0.493 | 0.05542 | 550 |
| kitnet | 0.7097 | 0.1252 | 0.8495 | 0.8467 | -5.551e-17 | 3.171 | 0.7097 | 0 | 0.75 | 24 | 2.001 | 0.2009 | 2.156 |
| ecod_tail | 0.8887 | 0.8867 | 0.961 | 0.9838 | -1.11e-16 | 3.171 | 0.8887 | 60 | 0.9583 | 24 | 0.02527 | 0.01848 | 846.4 |
