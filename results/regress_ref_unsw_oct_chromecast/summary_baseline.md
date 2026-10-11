# regress_ref_unsw_oct_chromecast

Windows: {'windows': 20724, 'bootstrap': 5760, 'validation': 2873, 'test_benign': 11437, 'test_attack': 564, 'excluded': 90}. Window length 30 s; features (32): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, arp_rep_in, n_arp_conflicts.

FPR resolution on test = 1/11437 = 8.74e-05; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.5408 | 0.1117 | 0.8099 | 0.9023 | 0.5867 | 30.47 | 0.7908 | 0 | 0.8696 | 23 | 0.07199 | 0.01126 | 0.2812 |
| mad_tail_slog | 0.4007 | 0 | 0.7187 | 0.8326 | 0.7206 | 0.5036 | 0.4007 | 1620 | 0.4348 | 23 | 0.04043 | 0.00677 | 0.25 |
| autoencoder_slog | 0.3901 | 0.3564 | 0.6992 | 0.8037 | 0.04626 | 0.7554 | 0.3901 | 90 | 0.4783 | 23 | 1.397 | 0.007489 | 2.406 |
| iforest_ext_sparse_slog | 0 | 0 | 0.5144 | 0.755 | 0.6768 | 4.533 | 0 | nan | 0 | 23 | 0.3679 | 0.2505 | 722.1 |
| hst_slog | 0 | 0 | 0.5006 | 0.6387 | 0.9738 | 10.07 | 0.001773 | 9.102e+04 | 0.04348 | 23 | 0.5281 | 0.04656 | 549.9 |
| kitnet | 0.6135 | 0.1117 | 0.8467 | 0.8761 | 0.3373 | 39.03 | 0.734 | 0 | 0.8261 | 23 | 1.574 | 0.1293 | 1.66 |
