# regress_i7_unsw_oct_lifx_bulb

Windows: {'windows': 20724, 'bootstrap': 5760, 'validation': 2873, 'test_benign': 11725, 'test_attack': 314, 'excluded': 52}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/11725 = 8.53e-05; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.8408 | 0.1879 | 0.9012 | 0.9719 | -1.11e-16 | 81.79 | 0.9745 | 0 | 1 | 13 | 0.08086 | 0.003852 | 0.334 |
| mad_tail_slog | 0.8025 | 0.5446 | 0.9394 | 0.9784 | -1.11e-16 | 82.29 | 0.9363 | 30 | 1 | 13 | 0.0419 | 0.007893 | 0.2969 |
| autoencoder_slog | 0.9204 | 0 | 0.9686 | 0.9937 | -8.674e-19 | 15.47 | 0.9936 | 0 | 1 | 13 | 1.309 | 0.01004 | 2.852 |
| iforest_ext_sparse_slog | 0.828 | 0.7803 | 0.9795 | 0.9963 | -5.551e-17 | 10.81 | 0.9873 | 30 | 1 | 13 | 0.4485 | 0.3475 | 815.5 |
| hst_slog | 0.8567 | 0.8503 | 0.9377 | 0.9757 | -1.11e-16 | 72.46 | 0.9363 | 30 | 1 | 13 | 0.5714 | 0.05029 | 550 |
| kitnet | 0.8025 | 0.742 | 0.956 | 0.9622 | -5.551e-17 | 3.193 | 0.9299 | 0 | 1 | 13 | 2.175 | 0.2114 | 2.227 |
| ecod_tail | 0.8694 | 0.1115 | 0.9667 | 0.9946 | -1.11e-16 | 9.334 | 0.9618 | 30 | 1 | 13 | 0.02218 | 0.006247 | 855.3 |
