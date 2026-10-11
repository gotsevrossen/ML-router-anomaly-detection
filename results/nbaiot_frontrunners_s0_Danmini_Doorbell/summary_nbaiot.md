# nbaiot_frontrunners_s0_Danmini_Doorbell

Rows: {'benign': 49548, 'bootstrap': 24774, 'validation': 9909, 'test_benign': 14865, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 1 | 0.8002 | 0.9963 | 0.9996 | 0.581 | 0.00074 | 1 | 0.5825 | 0.01125 | 1.011 |
| mad_tail_slog | 0.8002 | 5e-05 | 0.958 | 0.9956 | 0.7206 | 0.0009418 | 0.8001 | 0.78 | 0.02846 | 0.8984 |
| autoencoder_slog | 0.5697 | 0.1867 | 0.9361 | 0.9933 | 0.03829 | 0.0008073 | 0.5696 | 6.954 | 0.0366 | 8.566 |
| kitnet | 0.8002 | 0.8002 | 0.9237 | 0.992 | 0.1558 | 0.00074 | 0.8002 | 16.62 | 0.3758 | 6.768 |

## Detection rate at tau, per attack

| attack | robust_z_router | mad_tail_slog | autoencoder_slog | kitnet |
|---|---|---|---|---|
| gafgyt/combo | 1 | 1 | 0.998 | 1 |
| gafgyt/junk | 1 | 1 | 0.996 | 1 |
| gafgyt/scan | 1 | 1 | 0.006 | 1 |
| gafgyt/tcp | 0.9995 | 0 | 0 | 0.001 |
| gafgyt/udp | 1 | 0.0005 | 0 | 0.001 |
| mirai/ack | 1 | 1 | 1 | 1 |
| mirai/scan | 1 | 1 | 0 | 1 |
| mirai/syn | 1 | 1 | 0.697 | 1 |
| mirai/udp | 1 | 1 | 1 | 1 |
| mirai/udpplain | 1 | 1 | 0.999 | 1 |
