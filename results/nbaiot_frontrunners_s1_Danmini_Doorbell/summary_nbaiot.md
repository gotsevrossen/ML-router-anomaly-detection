# nbaiot_frontrunners_s1_Danmini_Doorbell

Rows: {'benign': 49548, 'bootstrap': 24774, 'validation': 9909, 'test_benign': 14865, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.9999 | 0.8001 | 0.9963 | 0.9996 | 0.581 | 0.00074 | 0.9999 | 0.6715 | 0.01415 | 1.011 |
| mad_tail_slog | 0.8001 | 0 | 0.958 | 0.9956 | 0.7206 | 0.0009418 | 0.8 | 0.825 | 0.03118 | 0.8984 |
| autoencoder_slog | 0.5707 | 0.1864 | 0.9362 | 0.9933 | 0.03829 | 0.0008073 | 0.5706 | 9.008 | 0.03527 | 8.566 |
| kitnet | 0.8001 | 0.8001 | 0.9236 | 0.992 | 0.1558 | 0.00074 | 0.8001 | 21.18 | 0.4683 | 6.768 |

## Detection rate at tau, per attack

| attack | robust_z_router | mad_tail_slog | autoencoder_slog | kitnet |
|---|---|---|---|---|
| gafgyt/combo | 1 | 1 | 0.9965 | 1 |
| gafgyt/junk | 0.9995 | 0.9995 | 0.9985 | 0.9995 |
| gafgyt/scan | 1 | 1 | 0.011 | 1 |
| gafgyt/tcp | 1 | 0.001 | 0.001 | 0.0015 |
| gafgyt/udp | 1 | 0 | 0 | 0.0005 |
| mirai/ack | 1 | 1 | 1 | 1 |
| mirai/scan | 0.9995 | 0.9995 | 0 | 0.9995 |
| mirai/syn | 1 | 1 | 0.6995 | 1 |
| mirai/udp | 1 | 1 | 1 | 1 |
| mirai/udpplain | 1 | 1 | 1 | 1 |
