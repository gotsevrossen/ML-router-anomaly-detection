# regress_i3_unsw_samsung_camera

Windows: {'windows': 15537, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 6134, 'test_attack': 691, 'excluded': 132}. Window length 30 s; features (35): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts.

FPR resolution on test = 1/6134 = 0.000163; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.1852 | 0.1737 | 0.8264 | 0.9812 | 0.5809 | 11.74 | 0.6324 | 0 | 0.6364 | 33 | 0.08732 | 0.003639 | 0.3076 |
| mad_tail_slog | 0.2489 | 0.2475 | 0.8158 | 0.966 | 0.6774 | 10.33 | 0.6295 | 30 | 0.6364 | 33 | 0.04951 | 0.008939 | 0.2734 |
| autoencoder_slog | 0.05065 | 0.007236 | 0.7955 | 0.9783 | 0.02622 | 11.27 | 0.5687 | 0 | 0.6061 | 33 | 1.423 | 0.00776 | 2.629 |
| iforest_ext_sparse_slog | 0.259 | 0.1592 | 0.8496 | 0.9842 | 0.7048 | 2.348 | 0.2287 | 120 | 0.3636 | 33 | 0.2984 | 0.2301 | 694.6 |
| hst_slog | 0.5036 | 0.2475 | 0.8622 | 0.9563 | 0.9136 | 0.939 | 0.369 | 1830 | 0.5152 | 33 | 0.7168 | 0.05416 | 549.9 |
| kitnet | 0 | 0 | 0.706 | 0.7965 | 0.3419 | 10.8 | 0.631 | 0 | 0.6364 | 33 | 1.722 | 0.179 | 1.842 |
