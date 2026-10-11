# regress_ref_nbaiot_frontrunners_Danmini_Doorbell

Rows: {'benign': 49548, 'bootstrap': 24774, 'validation': 9909, 'test_benign': 14865, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 1 | 0.8002 | 0.9963 | 0.9996 | 0.581 | 0.00074 | 1 | 0.5031 | 0.01075 | 1.011 |
| mad_tail_slog | 0.8002 | 5e-05 | 0.958 | 0.9956 | 0.7206 | 0.0009418 | 0.8001 | 0.8005 | 0.02539 | 0.8984 |
| autoencoder_slog | 0.5697 | 0.1867 | 0.9361 | 0.9933 | 0.03829 | 0.0008073 | 0.5696 | 5.687 | 0.03404 | 8.566 |
| iforest_ext_sparse_slog | 0.5937 | 0.0283 | 0.9544 | 0.9952 | 0.7385 | 0.0008073 | 0.5834 | 1.051 | 0.6993 | 769.8 |
| hst_slog | 0.05605 | 0.0123 | 0.8332 | 0.9825 | 0.972 | 0.0008073 | 0.05605 | 2.626 | 0.06966 | 550.6 |
| kitnet | 0.8002 | 0.8002 | 0.9237 | 0.992 | 0.1558 | 0.00074 | 0.8002 | 15.95 | 0.3307 | 6.768 |

## Detection rate at tau, per attack

| attack | robust_z_router | mad_tail_slog | autoencoder_slog | iforest_ext_sparse_slog | hst_slog | kitnet |
|---|---|---|---|---|---|---|
| gafgyt/combo | 1 | 1 | 0.998 | 0.999 | 0 | 1 |
| gafgyt/junk | 1 | 1 | 0.996 | 0.9985 | 0 | 1 |
| gafgyt/scan | 1 | 1 | 0.006 | 0.0065 | 0.0035 | 1 |
| gafgyt/tcp | 0.9995 | 0 | 0 | 0 | 0 | 0.001 |
| gafgyt/udp | 1 | 0.0005 | 0 | 0 | 0 | 0.001 |
| mirai/ack | 1 | 1 | 1 | 0.6625 | 0 | 1 |
| mirai/scan | 1 | 1 | 0 | 0.969 | 0 | 1 |
| mirai/syn | 1 | 1 | 0.697 | 0.9965 | 0 | 1 |
| mirai/udp | 1 | 1 | 1 | 0.6435 | 0 | 1 |
| mirai/udpplain | 1 | 1 | 0.999 | 0.558 | 0.557 | 1 |
