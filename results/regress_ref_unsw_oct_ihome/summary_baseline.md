# regress_ref_unsw_oct_ihome

Windows: {'windows': 20722, 'bootstrap': 5760, 'validation': 2872, 'test_benign': 12015, 'test_attack': 63, 'excluded': 12}. Window length 30 s; features (32): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, arp_rep_in, n_arp_conflicts.

FPR resolution on test = 1/12015 = 8.32e-05; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 1 | 0.9683 | 0.9993 | 0.9999 | 0.5809 | 16.3 | 1 | 0 | 0.05838 | 0.00246 | 0.2812 |
| mad_tail_slog | 0 | 0 | 0.8711 | 0.9148 | 0.8757 | 15.58 | 0.8413 | 60 | 0.03687 | 0.006047 | 0.25 |
| autoencoder_slog | 1 | 0 | 0.9904 | 0.999 | 0.04924 | 7.91 | 1 | 0 | 1.225 | 0.01398 | 2.406 |
| iforest_ext_sparse_slog | 0.3016 | 0 | 0.816 | 0.9788 | 0.7418 | 1.678 | 0.1429 | 120 | 0.257 | 0.2118 | 601.2 |
| hst_slog | 0.8413 | 0.01587 | 0.9038 | 0.9899 | 0.9387 | 8.869 | 0.8413 | 60 | 0.4553 | 0.05734 | 549.9 |
| kitnet | 1 | 0.9683 | 0.9997 | 1 | 0.9732 | 10.31 | 1 | 0 | 1.987 | 0.1851 | 2.051 |
