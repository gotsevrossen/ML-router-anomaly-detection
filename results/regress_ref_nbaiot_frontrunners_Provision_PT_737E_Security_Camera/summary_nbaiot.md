# regress_ref_nbaiot_frontrunners_Provision_PT_737E_Security_Camera

Rows: {'benign': 62154, 'bootstrap': 31077, 'validation': 12430, 'test_benign': 18647, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.9998 | 0.8001 | 0.9903 | 0.9989 | 0.5809 | 0.00118 | 0.9999 | 0.5695 | 0.01378 | 1.011 |
| mad_tail_slog | 0.9994 | 0.7148 | 0.9954 | 0.9995 | 0.6135 | 0.0009653 | 0.9994 | 0.8228 | 0.02394 | 0.8984 |
| autoencoder_slog | 0.7749 | 0.6328 | 0.8942 | 0.9772 | 0.02773 | 0.0008044 | 0.7698 | 3.292 | 0.02721 | 8.566 |
| iforest_ext_sparse_slog | 0.6937 | 0.1734 | 0.8776 | 0.987 | 0.5874 | 0.00118 | 0.6987 | 0.9675 | 0.6713 | 1001 |
| hst_slog | 0.216 | 0.0114 | 0.6942 | 0.8624 | 0.9414 | 0.0009653 | 0.216 | 2.579 | 0.06468 | 550.6 |
| kitnet | 0.9999 | 0.8002 | 0.993 | 0.9993 | 0.1447 | 0.0007508 | 0.9999 | 13.61 | 0.2501 | 6.498 |

## Detection rate at tau, per attack

| attack | robust_z_router | mad_tail_slog | autoencoder_slog | iforest_ext_sparse_slog | hst_slog | kitnet |
|---|---|---|---|---|---|---|
| gafgyt/combo | 1 | 1 | 1 | 1 | 0.032 | 1 |
| gafgyt/junk | 1 | 0.995 | 0.9995 | 1 | 0.095 | 1 |
| gafgyt/scan | 1 | 1 | 0.716 | 0.0145 | 0.003 | 1 |
| gafgyt/tcp | 0.9995 | 0.9995 | 0.001 | 0.0015 | 0.001 | 0.9995 |
| gafgyt/udp | 0.9995 | 0.9995 | 0 | 0.0005 | 0 | 0.9995 |
| mirai/ack | 1 | 1 | 0.9945 | 0.9995 | 0.527 | 1 |
| mirai/scan | 1 | 1 | 0.992 | 0.9915 | 0.0035 | 1 |
| mirai/syn | 1 | 1 | 0.996 | 0.9795 | 0.007 | 1 |
| mirai/udp | 1 | 1 | 0.9995 | 1 | 0.5425 | 1 |
| mirai/udpplain | 1 | 1 | 0.999 | 1 | 0.9485 | 1 |
