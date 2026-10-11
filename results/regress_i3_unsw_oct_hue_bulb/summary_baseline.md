# regress_i3_unsw_oct_hue_bulb

Windows: {'windows': 20724, 'bootstrap': 5760, 'validation': 2873, 'test_benign': 12091, 'test_attack': 0, 'excluded': 0}. Window length 30 s; features (35): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts.

FPR resolution on test = 1/12091 = 8.27e-05; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | nan | nan | nan | nan | 0.7157 | 0.2382 | nan | nan | 0.05654 | 0.002725 | 0.3076 |
| mad_tail_slog | nan | nan | nan | nan | 0.6938 | 3.335 | nan | nan | 0.04012 | 0.009249 | 0.2734 |
| autoencoder_slog | nan | nan | nan | nan | 0.0446 | 62.41 | nan | nan | 4.793 | 0.007209 | 2.629 |
| iforest_ext_sparse_slog | nan | nan | nan | nan | 0.6812 | 1.429 | nan | nan | 0.4471 | 0.2447 | 727.4 |
| hst_slog | nan | nan | nan | nan | 0.9086 | 40.97 | nan | nan | 0.8166 | 0.04962 | 549.9 |
| kitnet | nan | nan | nan | nan | 0.3234 | 6.431 | nan | nan | 1.666 | 0.1564 | 1.896 |
