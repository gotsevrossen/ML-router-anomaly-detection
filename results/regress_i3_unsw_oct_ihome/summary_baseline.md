# regress_i3_unsw_oct_ihome

Windows: {'windows': 20722, 'bootstrap': 5760, 'validation': 2872, 'test_benign': 12015, 'test_attack': 63, 'excluded': 12}. Window length 30 s; features (35): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts.

FPR resolution on test = 1/12015 = 8.32e-05; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 1 | 0.9683 | 0.9997 | 1 | 0.5809 | 16.3 | 1 | 0 | 0.06619 | 0.002688 | 0.3076 |
| mad_tail_slog | 0 | 0 | 0.5067 | 0.5337 | 0.7296 | 9.109 | 0.01587 | 600 | 0.03899 | 0.007219 | 0.2734 |
| autoencoder_slog | 0.8413 | 0 | 0.9565 | 0.9954 | 0.05445 | 14.62 | 0.9524 | 30 | 1.189 | 0.01412 | 2.629 |
| iforest_ext_sparse_slog | 0.04762 | 0 | 0.7038 | 0.9475 | 0.731 | 4.075 | 0.06349 | 600 | 0.2787 | 0.297 | 580.3 |
| hst_slog | 0.8571 | 0 | 0.922 | 0.9808 | 0.9395 | 1.918 | 0.8571 | 60 | 0.4311 | 0.05679 | 549.9 |
| kitnet | 1 | 0.9683 | 0.9997 | 1 | 0.9727 | 9.828 | 1 | 0 | 2.156 | 0.1974 | 2.275 |
