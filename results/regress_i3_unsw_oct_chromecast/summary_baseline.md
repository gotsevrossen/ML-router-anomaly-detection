# regress_i3_unsw_oct_chromecast

Windows: {'windows': 20724, 'bootstrap': 5760, 'validation': 2873, 'test_benign': 11437, 'test_attack': 564, 'excluded': 90}. Window length 30 s; features (35): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts.

FPR resolution on test = 1/11437 = 8.74e-05; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.5426 | 0 | 0.8059 | 0.9045 | 0.5867 | 36.26 | 0.7943 | 0 | 0.913 | 23 | 0.09209 | 0.01071 | 0.3076 |
| mad_tail_slog | 0.4007 | 0 | 0.7187 | 0.8324 | 0.7206 | 0.5036 | 0.4007 | 1620 | 0.4348 | 23 | 0.0421 | 0.008162 | 0.2734 |
| autoencoder_slog | 0.09752 | 0.08865 | 0.5895 | 0.8249 | 0.0419 | 18.89 | 0.1206 | 30 | 0.2609 | 23 | 1.726 | 0.01145 | 2.629 |
| iforest_ext_sparse_slog | 0.195 | 0.1454 | 0.6202 | 0.8216 | 0.6367 | 23.42 | 0.2943 | 150 | 0.5217 | 23 | 0.3204 | 0.31 | 731.9 |
| hst_slog | 0 | 0 | 0.5152 | 0.7308 | 0.9619 | 10.07 | 0.003546 | 3510 | 0.04348 | 23 | 0.6936 | 0.05303 | 549.9 |
| kitnet | 0.7092 | 0.1117 | 0.8611 | 0.9058 | 0.332 | 84.11 | 0.8316 | 0 | 0.8696 | 23 | 1.694 | 0.1559 | 1.736 |
