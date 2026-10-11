# regress_ref_unsw_oct_hue_bulb

Windows: {'windows': 20724, 'bootstrap': 5760, 'validation': 2873, 'test_benign': 12091, 'test_attack': 0, 'excluded': 0}. Window length 30 s; features (32): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, arp_rep_in, n_arp_conflicts.

FPR resolution on test = 1/12091 = 8.27e-05; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | nan | nan | nan | nan | 0.7909 | 0.2382 | nan | nan | 0.06526 | 0.002518 | 0.2812 |
| mad_tail_slog | nan | nan | nan | nan | 0.6938 | 3.335 | nan | nan | 0.04586 | 0.008868 | 0.25 |
| autoencoder_slog | nan | nan | nan | nan | 0.05103 | 1.191 | nan | nan | 5.056 | 0.00744 | 2.406 |
| iforest_ext_sparse_slog | nan | nan | nan | nan | 0.6626 | 1.667 | nan | nan | 0.4763 | 0.2623 | 766.6 |
| hst_slog | nan | nan | nan | nan | 0.9268 | 4.287 | nan | nan | 0.8292 | 0.05408 | 549.9 |
| kitnet | nan | nan | nan | nan | 0.3284 | 6.193 | nan | nan | 1.903 | 0.1633 | 1.672 |
