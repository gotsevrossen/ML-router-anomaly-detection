# regress_i8_nbaiot_frontrunners_Ecobee_Thermostat

Rows: {'benign': 13113, 'bootstrap': 6556, 'validation': 2622, 'test_benign': 3935, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.8001 | 0.8001 | 0.9668 | 0.9965 | 0.5895 | 0.0005083 | 0.8001 | 0.1436 | 0.01103 | 1.011 |
| mad_tail_slog | 0.8001 | 0.8001 | 0.9885 | 0.9988 | 0.6155 | 0 | 0.8001 | 0.1659 | 0.03174 | 0.8984 |
| autoencoder_slog | 0.8002 | 0.8001 | 0.9872 | 0.9987 | 0.01823 | 0.0007624 | 0.8002 | 2.383 | 0.02731 | 8.566 |
| iforest_ext_sparse_slog | 1 | 0.8001 | 0.9987 | 0.9999 | 0.5842 | 0.0002541 | 1 | 0.576 | 0.511 | 1016 |
| hst_slog | 0.8002 | 0.8001 | 0.9809 | 0.998 | 0.8933 | 0 | 0.8001 | 0.7443 | 0.06294 | 550.6 |
| kitnet | 0.8 | 0.7999 | 0.8995 | 0.9853 | 0.1264 | 0.004574 | 0.8001 | 3.381 | 0.2904 | 6.467 |
| ecod_tail | 0.8001 | 0.8001 | 0.9668 | 0.9965 | 0.6954 | 0.00305 | 0.8001 | 0.07694 | 0.02107 | 2947 |
| ecod_router | 0.8001 | 0.8001 | 0.9668 | 0.9965 | 0.6954 | 0.00305 | 0.8001 | 0.1066 | 0.01849 | 174.7 |

## Detection rate at tau, per attack

| attack | robust_z_router | mad_tail_slog | autoencoder_slog | iforest_ext_sparse_slog | hst_slog | kitnet | ecod_tail | ecod_router |
|---|---|---|---|---|---|---|---|---|
| gafgyt/combo | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| gafgyt/junk | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| gafgyt/scan | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| gafgyt/tcp | 0.0005 | 0.0005 | 0.001 | 0.9995 | 0.0005 | 0.0005 | 0.0005 | 0.0005 |
| gafgyt/udp | 0.0005 | 0.0005 | 0.0005 | 1 | 0.0005 | 0.0005 | 0.0005 | 0.0005 |
| mirai/ack | 1 | 0.9995 | 1 | 1 | 1 | 1 | 1 | 1 |
| mirai/scan | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| mirai/syn | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| mirai/udp | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| mirai/udpplain | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
