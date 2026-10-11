# kitsune_suite_video_injection

Windows: {'windows': 72, 'bootstrap': 30, 'validation': 18, 'test_benign': 13, 'test_attack': 11}. Window length 30 s; features (28): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets.

FPR resolution on test = 1/13 = 0.0769; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.8182 | 0.8182 | 0.9086 | 0.9043 | 0.5913 | 0 | 0.6364 | 60 | 0.0006419 | 0.002543 | 0.2461 |
| mad_tail_slog | 0.8182 | 0.8182 | 0.9086 | 0.9043 | 0.6291 | 0 | 0.8182 | 30 | 0.0003664 | 0.005253 | 0.2188 |
| autoencoder_slog | 0.7273 | 0.7273 | 0.863 | 0.8896 | 0.01403 | 0 | 0.6364 | 120 | 0.5365 | 0.009887 | 2.109 |
| kitnet_windows | 0.9091 | 0.9091 | 0.9543 | 0.9522 | 0.2031 | 0 | 0.8182 | 30 | 0.01629 | 0.2094 | 1.773 |
| hst | 0.7273 | 0.7273 | 0.863 | 0.8675 | 0.8104 | 0 | 0.4545 | 30 | 0.324 | 0.04702 | 549.9 |
