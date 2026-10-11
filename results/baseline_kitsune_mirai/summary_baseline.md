# baseline_kitsune_mirai

Windows: {'windows': 239, 'bootstrap': 60, 'validation': 45, 'test_benign': 44, 'test_attack': 90}. Window length 30 s; features (28): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets.

FPR resolution on test = 1/44 = 0.0227; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | fit_s | score_ms_per_window |
|---|---|---|---|---|---|---|---|---|---|---|
| hst | 0.9889 | 0.9889 | 0.9944 | 0.9987 | 0.9448 | 65.45 | 0.9889 | 30 | 0.313 | 0.08857 |
| iforest | 0.9889 | 0.9889 | 0.9944 | 0.9987 | 0.618 | 65.45 | 1 | 0 | 0.136 | 0.04775 |
| autoencoder | 1 | 1 | 1 | 1 | 0.01337 | 65.45 | 1 | 0 | 0.5451 | 0.004369 |
| mad | 0.9889 | 0.9889 | 0.9944 | 0.9987 | 0.7633 | 65.45 | 0.9889 | 30 | 0.001294 | 0.003232 |
| kitsune | 0.5444 | 0.5444 | 0.7711 | 0.9455 | 0.8334 | 65.45 | 0.5444 | 0 | nan | nan |
