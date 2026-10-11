# regress_i3_unsw_oct_lifx_bulb

Windows: {'windows': 20724, 'bootstrap': 5760, 'validation': 2873, 'test_benign': 11725, 'test_attack': 314, 'excluded': 52}. Window length 30 s; features (35): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts.

FPR resolution on test = 1/11725 = 8.53e-05; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.7516 | 0.1975 | 0.909 | 0.9301 | 0.6094 | 2.702 | 0.7229 | 0 | 0.9231 | 13 | 0.084 | 0.003196 | 0.3076 |
| mad_tail_slog | 0 | 0 | 0.8998 | 0.9803 | 0.7296 | 0.7369 | 0 | nan | 0 | 13 | 0.03975 | 0.007346 | 0.2734 |
| autoencoder_slog | 0.8312 | 0 | 0.9497 | 0.992 | 0.02028 | 2.456 | 0.7484 | 0 | 1 | 13 | 1.539 | 0.0103 | 2.629 |
| iforest_ext_sparse_slog | 0.5796 | 0.003185 | 0.9438 | 0.9921 | 0.5984 | 4.421 | 0.7675 | 30 | 1 | 13 | 0.4585 | 0.3361 | 769.8 |
| hst_slog | 0.5318 | 0.01911 | 0.8198 | 0.8566 | 0.8426 | 4.176 | 0.5892 | 30 | 1 | 13 | 0.4521 | 0.0496 | 549.9 |
| kitnet | 0.6019 | 0.1975 | 0.9051 | 0.9267 | 0.304 | 3.193 | 0.8439 | 0 | 0.9231 | 13 | 2.081 | 0.2408 | 2.127 |
