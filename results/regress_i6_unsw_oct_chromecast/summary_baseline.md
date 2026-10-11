# regress_i6_unsw_oct_chromecast

Windows: {'windows': 20724, 'bootstrap': 5760, 'validation': 2873, 'test_benign': 11437, 'test_attack': 564, 'excluded': 90}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/11437 = 8.74e-05; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.6631 | 0 | 0.8694 | 0.9233 | 0.5809 | 4.784 | 0.7642 | 60 | 0.8696 | 23 | 0.1198 | 0.005564 | 0.334 |
| mad_tail_slog | 0.5603 | 0 | 0.7938 | 0.8599 | 0.6238 | 290.3 | 0.8085 | 60 | 0.9565 | 23 | 0.087 | 0.01235 | 0.2969 |
| autoencoder_slog | 0.4326 | 0.2482 | 0.8113 | 0.9129 | 0.008658 | 467.4 | 0.9113 | 60 | 0.9565 | 23 | 2.307 | 0.01376 | 2.852 |
| iforest_ext_sparse_slog | 0.4504 | 0.273 | 0.8659 | 0.9401 | 0.58 | 2.266 | 0.4468 | 1740 | 0.7391 | 23 | 0.4343 | 0.3432 | 746.6 |
| hst_slog | 0.4486 | 0.1667 | 0.7769 | 0.8619 | 0.7817 | 21.66 | 0.6259 | 60 | 0.8696 | 23 | 0.5998 | 0.06797 | 550 |
| kitnet | 0.6613 | 0.1011 | 0.8588 | 0.8701 | 0.3225 | 46.08 | 0.7571 | 60 | 0.8696 | 23 | 2.255 | 0.2378 | 1.926 |
| ecod_tail | 0.6064 | 0 | 0.8681 | 0.9195 | 0.6869 | 4.784 | 0.7216 | 90 | 0.8696 | 23 | 0.03557 | 0.01039 | 855.3 |
