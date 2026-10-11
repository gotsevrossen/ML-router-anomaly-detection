# regress_i2_nbaiot_frontrunners_Danmini_Doorbell

Rows: {'benign': 49548, 'bootstrap': 24774, 'validation': 9909, 'test_benign': 14865, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 1 | 0.8002 | 0.9963 | 0.9996 | 0.581 | 0.00074 | 1 | 0.8982 | 0.01647 | 1.011 |
| mad_tail_slog | 0.8002 | 0 | 0.958 | 0.9956 | 0.7206 | 0.0009418 | 0.8 | 1.11 | 0.03908 | 0.8984 |
| autoencoder_slog | 0.5697 | 0.1867 | 0.9361 | 0.9933 | 0.03829 | 0.0008073 | 0.5696 | 10.56 | 0.0486 | 8.566 |
| iforest_ext_sparse_slog | 0.7007 | 0.4553 | 0.9482 | 0.9946 | 0.713 | 0.0008745 | 0.6975 | 2.026 | 0.8353 | 870.5 |
| hst_slog | 0.05605 | 0.0123 | 0.8332 | 0.9825 | 0.972 | 0.0008073 | 0.05605 | 4.322 | 0.1288 | 550.6 |
| kitnet | 0.8002 | 0.8002 | 0.9237 | 0.992 | 0.1558 | 0.00074 | 0.8002 | 30.25 | 0.695 | 6.768 |

## Detection rate at tau, per attack

| attack | robust_z_router | mad_tail_slog | autoencoder_slog | iforest_ext_sparse_slog | hst_slog | kitnet |
|---|---|---|---|---|---|---|
| gafgyt/combo | 1 | 1 | 0.998 | 0.999 | 0 | 1 |
| gafgyt/junk | 1 | 1 | 0.996 | 0.999 | 0 | 1 |
| gafgyt/scan | 1 | 1 | 0.006 | 0.006 | 0.0035 | 1 |
| gafgyt/tcp | 0.9995 | 0 | 0 | 0 | 0 | 0.001 |
| gafgyt/udp | 1 | 0 | 0 | 0.0005 | 0 | 0.001 |
| mirai/ack | 1 | 1 | 1 | 1 | 0 | 1 |
| mirai/scan | 1 | 1 | 0 | 0.974 | 0 | 1 |
| mirai/syn | 1 | 1 | 0.697 | 0.996 | 0 | 1 |
| mirai/udp | 1 | 1 | 1 | 1 | 0 | 1 |
| mirai/udpplain | 1 | 1 | 0.999 | 1 | 0.557 | 1 |
