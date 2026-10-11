# nbaiot_frontrunners_s2_Danmini_Doorbell

Rows: {'benign': 49548, 'bootstrap': 24774, 'validation': 9909, 'test_benign': 14865, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 1 | 0.8007 | 0.9963 | 0.9996 | 0.581 | 0.00074 | 1 | 0.477 | 0.009684 | 1.011 |
| mad_tail_slog | 0.8005 | 0 | 0.958 | 0.9956 | 0.7206 | 0.0009418 | 0.8002 | 0.6894 | 0.02497 | 0.8984 |
| autoencoder_slog | 0.5681 | 0.1902 | 0.9361 | 0.9933 | 0.03829 | 0.0008073 | 0.5678 | 6.316 | 0.0291 | 8.566 |
| kitnet | 0.8007 | 0.8006 | 0.9239 | 0.992 | 0.1558 | 0.00074 | 0.8007 | 13.91 | 0.5175 | 6.768 |

## Detection rate at tau, per attack

| attack | robust_z_router | mad_tail_slog | autoencoder_slog | kitnet |
|---|---|---|---|---|
| gafgyt/combo | 1 | 1 | 0.998 | 1 |
| gafgyt/junk | 1 | 1 | 0.9975 | 1 |
| gafgyt/scan | 1 | 1 | 0.0075 | 1 |
| gafgyt/tcp | 1 | 0.0005 | 0.001 | 0.004 |
| gafgyt/udp | 1 | 0.0015 | 0.0015 | 0.0035 |
| mirai/ack | 1 | 1 | 1 | 1 |
| mirai/scan | 1 | 1 | 0 | 1 |
| mirai/syn | 0.9995 | 0.9995 | 0.673 | 0.9995 |
| mirai/udp | 1 | 1 | 1 | 1 |
| mirai/udpplain | 1 | 1 | 1 | 1 |
