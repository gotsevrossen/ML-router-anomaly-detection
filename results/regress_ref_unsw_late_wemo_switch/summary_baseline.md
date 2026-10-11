# regress_ref_unsw_late_wemo_switch

Windows: {'windows': 18435, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 9705, 'test_attack': 126, 'excluded': 24}. Window length 30 s; features (35): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/9705 = 0.000103; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.9841 | 0.6429 | 0.9907 | 0.999 | 0.5909 | 0.8903 | 0.9444 | 30 | 1 | 6 | 0.2557 | 0.003448 | 0.3076 |
| mad_tail_slog | 1 | 0.9603 | 0.9995 | 1 | 0.6724 | 0.8903 | 0.9841 | 0 | 1 | 6 | 0.04673 | 0.008536 | 0.2734 |
| autoencoder_slog | 0.9841 | 0.5238 | 0.996 | 0.9996 | 0.03122 | 0.2968 | 0.9206 | 30 | 1 | 6 | 2.217 | 0.01049 | 2.629 |
| iforest_ext_sparse_slog | 0.9921 | 0.05556 | 0.9804 | 0.9979 | 0.667 | 0.8903 | 0.5873 | 1620 | 0.8333 | 6 | 0.4133 | 0.2962 | 650.9 |
| hst_slog | 0.3175 | 0 | 0.933 | 0.9929 | 0.9788 | 0.5935 | 0 | nan | 0 | 6 | 0.9682 | 0.06304 | 549.9 |
| kitnet | 1 | 0 | 0.9825 | 0.9982 | 0.3102 | 1.484 | 0.9841 | 0 | 1 | 6 | 2.001 | 0.1832 | 1.826 |
