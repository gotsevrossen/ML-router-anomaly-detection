# regress_i6_unsw_wemo_motion

Windows: {'windows': 15537, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 6358, 'test_attack': 503, 'excluded': 96}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/6358 = 0.000157; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.6163 | 0.5924 | 0.8068 | 0.8692 | 0.5809 | 1.812 | 0.6163 | 60 | 0.7083 | 24 | 0.09985 | 0.00411 | 0.334 |
| mad_tail_slog | 0.7654 | 0.7654 | 0.8845 | 0.9136 | 0.5809 | 0.453 | 0.7654 | 90 | 0.875 | 24 | 0.07008 | 0.01185 | 0.2969 |
| autoencoder_slog | 0.5209 | 0.1372 | 0.8572 | 0.9274 | 0.009508 | 8.154 | 0.6839 | 60 | 0.875 | 24 | 2.085 | 0.01009 | 2.852 |
| iforest_ext_sparse_slog | 0.6501 | 0.3101 | 0.8669 | 0.9249 | 0.5903 | 2.265 | 0.6044 | 180 | 0.7917 | 24 | 0.5047 | 0.4064 | 639.7 |
| hst_slog | 0.005964 | 0 | 0.5184 | 0.7584 | 0.9016 | 1.812 | 0.005964 | 240 | 0.08333 | 24 | 0.7519 | 0.06593 | 550 |
| kitnet | 0.6362 | 0.6362 | 0.8172 | 0.8085 | 0.2731 | 2.718 | 0.6362 | 60 | 0.75 | 24 | 2.832 | 0.2772 | 2.156 |
| ecod_tail | 0.837 | 0.837 | 0.9312 | 0.9463 | 0.6469 | 1.359 | 0.837 | 60 | 0.9583 | 24 | 0.03167 | 0.02123 | 846.4 |
