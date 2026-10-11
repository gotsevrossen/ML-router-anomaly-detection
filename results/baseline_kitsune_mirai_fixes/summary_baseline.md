# baseline_kitsune_mirai_fixes

Windows: {'windows': 239, 'bootstrap': 60, 'validation': 45, 'test_benign': 44, 'test_attack': 90}. Window length 30 s; features (28): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets.

FPR resolution on test = 1/44 = 0.0227; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|
| hst | 0.9889 | 0.9889 | 0.9944 | 0.9987 | 0.9448 | 65.45 | 0.9889 | 30 | 0.4861 | 0.08196 | 549.9 |
| iforest | 0.9889 | 0.9889 | 0.9944 | 0.9987 | 0.618 | 65.45 | 1 | 0 | 0.1954 | 0.04619 | 65.32 |
| autoencoder | 1 | 1 | 1 | 1 | 0.01337 | 65.45 | 1 | 0 | 2.408 | 0.01081 | 2.109 |
| mad | 0.9889 | 0.9889 | 0.9944 | 0.9987 | 0.7633 | 65.45 | 0.9889 | 30 | 0.0009393 | 0.003855 | 0.2188 |
| iforest_headroom | 1 | 1 | 1 | 1 | 0.4999 | 65.45 | 1 | 0 | 0.1468 | 0.2096 | 125.2 |
| iforest_extended | 1 | 1 | 1 | 1 | 0.51 | 65.45 | 1 | 0 | 0.289 | 0.3508 | 774.3 |
| mad_tail | 1 | 1 | 1 | 1 | 0.6113 | 130.9 | 1 | 0 | 0.001098 | 0.0078 | 0.2188 |
