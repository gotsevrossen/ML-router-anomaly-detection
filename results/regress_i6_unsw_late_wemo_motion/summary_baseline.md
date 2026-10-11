# regress_i6_unsw_late_wemo_motion

Windows: {'windows': 18436, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 9566, 'test_attack': 250, 'excluded': 40}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/9566 = 0.000105; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.696 | 0.52 | 0.8521 | 0.9267 | 0.5809 | 1.806 | 0.696 | 660 | 0.9 | 10 | 0.05812 | 0.002776 | 0.334 |
| mad_tail_slog | 0.636 | 0 | 0.8231 | 0.9174 | 0.5809 | 1.505 | 0.636 | 4200 | 0.9 | 10 | 0.1241 | 0.01113 | 0.2969 |
| autoencoder_slog | 0.648 | 0 | 0.8823 | 0.9576 | 0.009508 | 6.623 | 0.696 | 480 | 0.9 | 10 | 6.811 | 0.01058 | 2.852 |
| iforest_ext_sparse_slog | 0.536 | 0.312 | 0.7988 | 0.9259 | 0.5903 | 0.9032 | 0.5 | 1620 | 0.8 | 10 | 0.4891 | 0.3364 | 639.7 |
| hst_slog | 0.004 | 0.004 | 0.5059 | 0.7774 | 0.9016 | 1.806 | 0.004 | 7830 | 0.1 | 10 | 0.7384 | 0.05065 | 550 |
| kitnet | 0.704 | 0 | 0.8413 | 0.846 | 0.2731 | 2.107 | 0.704 | 660 | 1 | 10 | 2.033 | 0.1876 | 2.156 |
| ecod_tail | 0.808 | 0.616 | 0.9475 | 0.9592 | 0.6469 | 1.806 | 0.808 | 60 | 1 | 10 | 0.02139 | 0.01426 | 846.4 |
