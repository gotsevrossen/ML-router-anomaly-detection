# regress_i8_nbaiot_frontrunners_Provision_PT_737E_Security_Camera

Rows: {'benign': 62154, 'bootstrap': 31077, 'validation': 12430, 'test_benign': 18647, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.9998 | 0.8001 | 0.9903 | 0.9989 | 0.5809 | 0.00118 | 0.9999 | 0.7912 | 0.009652 | 1.011 |
| mad_tail_slog | 0.9994 | 0.7148 | 0.9954 | 0.9995 | 0.6135 | 0.0009653 | 0.9994 | 1.029 | 0.02205 | 0.8984 |
| autoencoder_slog | 0.7749 | 0.6328 | 0.8942 | 0.9772 | 0.02773 | 0.0008044 | 0.7698 | 3.013 | 0.02732 | 8.566 |
| iforest_ext_sparse_slog | 0.6937 | 0.1734 | 0.8776 | 0.987 | 0.5874 | 0.00118 | 0.6987 | 1.012 | 0.6722 | 1001 |
| hst_slog | 0.216 | 0.0114 | 0.6942 | 0.8624 | 0.9414 | 0.0009653 | 0.216 | 2.421 | 0.06343 | 550.6 |
| kitnet | 0.9999 | 0.8002 | 0.993 | 0.9993 | 0.1447 | 0.0007508 | 0.9999 | 13.49 | 0.2386 | 6.498 |
| ecod_tail | 1 | 0.8002 | 0.9967 | 0.9997 | 0.7083 | 0.001823 | 1 | 0.3994 | 0.02737 | 1.396e+04 |
| ecod_router | 1 | 0.8002 | 0.9967 | 0.9996 | 0.7083 | 0.001823 | 1 | 0.5262 | 0.02535 | 174.7 |

## Detection rate at tau, per attack

| attack | robust_z_router | mad_tail_slog | autoencoder_slog | iforest_ext_sparse_slog | hst_slog | kitnet | ecod_tail | ecod_router |
|---|---|---|---|---|---|---|---|---|
| gafgyt/combo | 1 | 1 | 1 | 1 | 0.032 | 1 | 1 | 1 |
| gafgyt/junk | 1 | 0.995 | 0.9995 | 1 | 0.095 | 1 | 1 | 1 |
| gafgyt/scan | 1 | 1 | 0.716 | 0.0145 | 0.003 | 1 | 1 | 1 |
| gafgyt/tcp | 0.9995 | 0.9995 | 0.001 | 0.0015 | 0.001 | 0.9995 | 1 | 1 |
| gafgyt/udp | 0.9995 | 0.9995 | 0 | 0.0005 | 0 | 0.9995 | 0.9995 | 0.9995 |
| mirai/ack | 1 | 1 | 0.9945 | 0.9995 | 0.527 | 1 | 1 | 1 |
| mirai/scan | 1 | 1 | 0.992 | 0.9915 | 0.0035 | 1 | 1 | 1 |
| mirai/syn | 1 | 1 | 0.996 | 0.9795 | 0.007 | 1 | 1 | 1 |
| mirai/udp | 1 | 1 | 0.9995 | 1 | 0.5425 | 1 | 1 | 1 |
| mirai/udpplain | 1 | 1 | 0.999 | 1 | 0.9485 | 1 | 1 | 1 |
