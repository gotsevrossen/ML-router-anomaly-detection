# regress_i5_unsw_late_wemo_motion

Windows: {'windows': 18436, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 9566, 'test_attack': 250, 'excluded': 40}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/9566 = 0.000105; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.736 | 0.428 | 0.8858 | 0.9391 | 0.5971 | 0.9032 | 0.66 | 630 | 0.9 | 10 | 0.061 | 0.003145 | 0.334 |
| mad_tail_slog | 0.732 | 0 | 0.8588 | 0.9178 | 0.6442 | 3.613 | 0.732 | 4140 | 0.9 | 10 | 0.09348 | 0.006909 | 0.2969 |
| autoencoder_slog | 0.012 | 0 | 0.6461 | 0.9415 | 0.02348 | 1.806 | 0.004 | 2.099e+05 | 0.1 | 10 | 4.327 | 0.008216 | 2.852 |
| iforest_ext_sparse_slog | 0.256 | 0.004 | 0.7184 | 0.9125 | 0.6872 | 0.3011 | 0.004 | 2.099e+05 | 0.1 | 10 | 0.4089 | 0.2725 | 639.7 |
| hst_slog | 0 | 0 | 0.5227 | 0.6103 | 0.9863 | 0.6021 | 0 | nan | 0 | 10 | 0.7439 | 0.04987 | 550 |
| kitnet | 0.828 | 0 | 0.8997 | 0.9112 | 0.2911 | 1.204 | 0.732 | 600 | 0.9 | 10 | 1.801 | 0.1724 | 2.156 |
| ecod_tail | 0.904 | 0.388 | 0.9521 | 0.9884 | 0.6935 | 1.505 | 0.68 | 630 | 0.9 | 10 | 0.02158 | 0.01264 | 846.4 |
