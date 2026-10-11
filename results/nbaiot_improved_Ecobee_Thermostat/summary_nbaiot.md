# nbaiot_improved_Ecobee_Thermostat

Rows: {'benign': 13113, 'bootstrap': 6556, 'validation': 2622, 'test_benign': 3935, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| hst_slog | 0.8002 | 0.8001 | 0.9809 | 0.998 | 0.8933 | 0 | 0.8001 | 2.948 | 0.188 | 550.6 |
| hst_proj | 0.8 | 0.7995 | 0.8995 | 0.96 | 0.8765 | 0.002033 | 0.8 | 1.834 | 0.2 | 565.2 |
| autoencoder_slog | 0.8002 | 0.8001 | 0.9872 | 0.9987 | 0.01823 | 0.0007624 | 0.8002 | 14.15 | 0.07438 | 8.566 |
| iforest_ext_slog | 1 | 0.8001 | 0.9936 | 0.9993 | 0.5459 | 0.0005083 | 0.8001 | 1.598 | 1.072 | 6725 |
| iforest_ext_sparse_slog | 1 | 0.8001 | 0.9987 | 0.9999 | 0.5842 | 0.0002541 | 1 | 1.507 | 1.119 | 1016 |
| mad_tail_slog | 0.8001 | 0.8001 | 0.9885 | 0.9988 | 0.6155 | 0 | 0.8001 | 0.486 | 0.06971 | 0.8984 |
| kitnet | 0.8 | 0.7999 | 0.8995 | 0.9853 | 0.1264 | 0.004574 | 0.8001 | 13.94 | 1.119 | 6.467 |
| fusion | 1 | 0.8 | 0.9987 | 0.9999 | 0.648 | 0.0002541 | 0.9999 | 6.871 | 0.2956 | 590 |

## Detection rate at tau, per attack

| attack | hst_slog | hst_proj | autoencoder_slog | iforest_ext_slog | iforest_ext_sparse_slog | mad_tail_slog | kitnet | fusion |
|---|---|---|---|---|---|---|---|---|
| gafgyt/combo | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| gafgyt/junk | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| gafgyt/scan | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| gafgyt/tcp | 0.0005 | 0 | 0.001 | 0.0005 | 0.9995 | 0.0005 | 0.0005 | 0.9995 |
| gafgyt/udp | 0.0005 | 0.0005 | 0.0005 | 0.0005 | 1 | 0.0005 | 0.0005 | 1 |
| mirai/ack | 1 | 0.9995 | 1 | 1 | 1 | 0.9995 | 1 | 0.9995 |
| mirai/scan | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| mirai/syn | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| mirai/udp | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| mirai/udpplain | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
