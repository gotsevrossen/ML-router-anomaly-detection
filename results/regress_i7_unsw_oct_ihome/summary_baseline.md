# regress_i7_unsw_oct_ihome

Windows: {'windows': 20722, 'bootstrap': 5760, 'validation': 2872, 'test_benign': 12015, 'test_attack': 63, 'excluded': 12}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/12015 = 8.32e-05; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 1 | 0.9841 | 0.9998 | 1 | -1.11e-16 | 72.87 | 1 | 0 | 1 | 3 | 0.09857 | 0.005653 | 0.334 |
| mad_tail_slog | 0 | 0 | 0.5855 | 0.8854 | -1.11e-16 | 67.36 | 0.8889 | 60 | 1 | 3 | 0.06832 | 0.009211 | 0.2969 |
| autoencoder_slog | 0.9206 | 0 | 0.9799 | 0.9979 | -1.735e-18 | 78.14 | 1 | 0 | 1 | 3 | 1.696 | 0.008341 | 2.852 |
| iforest_ext_sparse_slog | 0.619 | 0.5556 | 0.8915 | 0.981 | -1.11e-16 | 71.43 | 0.9683 | 60 | 1 | 3 | 0.286 | 0.3212 | 649.7 |
| hst_slog | 0.3492 | 0.3492 | 0.9281 | 0.9782 | -1.11e-16 | 13.18 | 0.9524 | 30 | 1 | 3 | 0.4255 | 0.05197 | 550 |
| kitnet | 0.9048 | 0.9048 | 0.9573 | 0.992 | -5.551e-17 | 73.11 | 1 | 0 | 1 | 3 | 2.241 | 0.2263 | 2.613 |
| ecod_tail | 0.8889 | 0.5873 | 0.9535 | 0.9921 | -1.11e-16 | 75.27 | 1 | 0 | 1 | 3 | 0.02081 | 0.005441 | 855.3 |
