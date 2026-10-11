# regress_ref_unsw_oct_lifx_bulb

Windows: {'windows': 20724, 'bootstrap': 5760, 'validation': 2873, 'test_benign': 11725, 'test_attack': 314, 'excluded': 52}. Window length 30 s; features (32): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, arp_rep_in, n_arp_conflicts.

FPR resolution on test = 1/11725 = 8.53e-05; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.7452 | 0.1975 | 0.9064 | 0.9238 | 0.6094 | 2.702 | 0.7229 | 0 | 0.8462 | 13 | 0.06757 | 0.002999 | 0.2812 |
| mad_tail_slog | 0 | 0 | 0.9007 | 0.9799 | 0.88 | 0.2456 | 0 | nan | 0 | 13 | 0.05319 | 0.006741 | 0.25 |
| autoencoder_slog | 0.742 | 0 | 0.9299 | 0.9839 | 0.02101 | 2.702 | 0.742 | 0 | 1 | 13 | 1.176 | 0.01607 | 2.406 |
| iforest_ext_sparse_slog | 0.4236 | 0 | 0.9356 | 0.9902 | 0.5862 | 3.684 | 0.6338 | 30 | 1 | 13 | 0.3638 | 0.2792 | 740.1 |
| hst_slog | 0.2803 | 0.01274 | 0.6752 | 0.7164 | 0.9232 | 1.228 | 0.1178 | 30 | 0.9231 | 13 | 0.4016 | 0.06176 | 549.9 |
| kitnet | 0.6019 | 0.1975 | 0.8743 | 0.8903 | 0.3136 | 3.193 | 0.7898 | 0 | 0.9231 | 13 | 2.175 | 0.18 | 1.973 |
