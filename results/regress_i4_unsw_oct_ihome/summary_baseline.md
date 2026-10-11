# regress_i4_unsw_oct_ihome

Windows: {'windows': 20722, 'bootstrap': 5760, 'validation': 2872, 'test_benign': 12015, 'test_attack': 63, 'excluded': 12}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/12015 = 8.32e-05; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 1 | 0.9683 | 0.9997 | 1 | 0.5809 | 19.66 | 1 | 0 | 1 | 3 | 0.09983 | 0.004927 | 0.334 |
| mad_tail_slog | 0 | 0 | 0.5064 | 0.5335 | 0.7296 | 9.588 | 0.01587 | 600 | 0.3333 | 3 | 0.1924 | 0.008545 | 0.2969 |
| autoencoder_slog | 0.9524 | 0 | 0.9803 | 0.9979 | 0.0324 | 21.09 | 1 | 0 | 1 | 3 | 1.544 | 0.008974 | 2.852 |
| iforest_ext_sparse_slog | 0.7143 | 0 | 0.8861 | 0.9731 | 0.7249 | 14.62 | 0.8254 | 60 | 1 | 3 | 0.2944 | 0.3404 | 649.7 |
| hst_slog | 0.5714 | 0 | 0.8616 | 0.9854 | 0.9308 | 7.91 | 0.8095 | 60 | 1 | 3 | 0.5945 | 0.05203 | 550 |
| kitnet | 1 | 0.9683 | 0.9997 | 1 | 0.9722 | 16.3 | 1 | 0 | 1 | 3 | 2.402 | 0.2211 | 2.613 |
