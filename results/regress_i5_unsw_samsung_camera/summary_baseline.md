# regress_i5_unsw_samsung_camera

Windows: {'windows': 15537, 'bootstrap': 5700, 'validation': 2880, 'test_benign': 6134, 'test_attack': 691, 'excluded': 132}. Window length 30 s; features (38): bytes_out, bytes_in, pkts_out, pkts_in, out_byte_frac, pkt_size_mean, pkt_size_var, iat_mean, iat_var, n_ext_dst_ips, n_new_ext_dst_ips, n_ext_dst_prefixes, lan_byte_frac, n_dst_ports, n_new_dst_ports, tcp_frac, udp_frac, icmp_frac, top3_port_frac, dns_queries, n_domains, n_new_domains, nxdomain, n_new_conns, n_failed_tcp, conn_dur_mean, arp_req_out, n_arp_targets, tod_sin, tod_cos, n_in_peers, n_new_in_peers, n_in_ports, arp_rep_in, n_arp_conflicts, n_new_in_ports, n_lan_peers, n_new_lan_peers.

FPR resolution on test = 1/6134 = 0.000163; TPR at smaller FPR targets is TPR at zero false positives.

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | false_alarms_per_day | detection_rate@tau | time_to_detect_s | event_detection@tau | n_events | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.1852 | 0.1737 | 0.8264 | 0.9812 | 0.5809 | 11.74 | 0.6324 | 0 | 0.6364 | 33 | 0.1203 | 0.005661 | 0.334 |
| mad_tail_slog | 0.2489 | 0.2475 | 0.8225 | 0.9814 | 0.6774 | 10.33 | 0.6295 | 30 | 0.6364 | 33 | 0.08239 | 0.01203 | 0.2969 |
| autoencoder_slog | 0.05933 | 0.007236 | 0.7964 | 0.9786 | 0.02609 | 11.27 | 0.5499 | 0 | 0.6061 | 33 | 2.548 | 0.02557 | 2.852 |
| iforest_ext_sparse_slog | 0.4863 | 0.1317 | 0.8922 | 0.9878 | 0.6522 | 8.921 | 0.6295 | 90 | 0.7879 | 33 | 0.5375 | 0.4429 | 748.2 |
| hst_slog | 0.06078 | 0 | 0.7678 | 0.9564 | 0.8742 | 4.226 | 0.1288 | 210 | 0.5152 | 33 | 0.795 | 0.0886 | 550 |
| kitnet | 0 | 0 | 0.706 | 0.7965 | 0.3417 | 10.8 | 0.631 | 0 | 0.6364 | 33 | 3.336 | 0.3051 | 2 |
| ecod_tail | 0.3039 | 0.2156 | 0.8476 | 0.9832 | 0.6815 | 10.8 | 0.4559 | 0 | 0.5152 | 33 | 0.045 | 0.02139 | 846.4 |
