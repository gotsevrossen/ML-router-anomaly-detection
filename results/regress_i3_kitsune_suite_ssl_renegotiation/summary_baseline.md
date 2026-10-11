# regress_i3_kitsune_suite_ssl_renegotiation

Windows: {'windows': 78, 'bootstrap': 20, 'validation': 12, 'test_benign': 8, 'test_attack': 38}. Window length 30 s; features (33): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts.

FPR resolution on test = 1/8 = 0.125; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.8684 | 0.8684 | 0.9339 | 0.9307 | 0.4368 | 720 | 0.9474 | 60 | 1 | 1 | 0.0005074 | 0.002421 | 0.29 |
| mad_tail_slog | 0.9211 | 0.9211 | 0.9603 | 0.9584 | 0.5809 | 0 | 0.7368 | 90 | 1 | 1 | 0.0002704 | 0.00479 | 0.2578 |
| autoencoder_slog | 0.8421 | 0.8421 | 0.9207 | 0.9169 | 0.01866 | 1080 | 1 | 0 | 1 | 1 | 1.324 | 0.01172 | 2.48 |
| iforest_ext_sparse_slog | 0.8421 | 0.8421 | 0.9207 | 0.9169 | 0.4524 | 720 | 0.9211 | 90 | 1 | 1 | 0.04953 | 0.2896 | 121.8 |
| hst_slog | 0.8684 | 0.8684 | 0.9339 | 0.9307 | 0.6571 | 360 | 0.9211 | 90 | 1 | 1 | 0.1873 | 0.03718 | 549.9 |
| kitnet | 1 | 1 | 1 | 1 | 0.2456 | 1800 | 1 | 0 | 1 | 1 | 0.009585 | 0.2127 | 2.729 |
