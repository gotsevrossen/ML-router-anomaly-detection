# nbaiot_improved

Rows: {'benign': 49548, 'bootstrap': 24774, 'validation': 9909, 'test_benign': 14865, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| hst_slog | 0.05605 | 0.0123 | 0.8332 | 0.9825 | 0.972 | 0.0008073 | 0.05605 | 7.799 | 0.1957 | 550.6 |
| hst_proj | 0.0002 | 0 | 0.5952 | 0.7538 | 0.04066 | 0.001009 | 0.1144 | 4.883 | 0.185 | 565.2 |
| autoencoder_slog | 0.5697 | 0.1867 | 0.9361 | 0.9933 | 0.03829 | 0.0008073 | 0.5696 | 17.31 | 0.08211 | 8.566 |
| iforest_ext_slog | 0.6086 | 5e-05 | 0.9343 | 0.9931 | 0.7214 | 0.0009418 | 0.5617 | 2.97 | 1.305 | 5848 |
| iforest_ext_sparse_slog | 0.5937 | 0.0283 | 0.9544 | 0.9952 | 0.7385 | 0.0008073 | 0.5834 | 2.726 | 1.099 | 769.8 |
| mad_tail_slog | 0.8002 | 5e-05 | 0.958 | 0.9956 | 0.7206 | 0.0009418 | 0.8001 | 1.76 | 0.06358 | 0.8984 |
| kitnet | 0.8002 | 0.8002 | 0.9237 | 0.992 | 0.1558 | 0.00074 | 0.8002 | 54.58 | 1.281 | 6.768 |
| fusion | 0.8001 | 0.1867 | 0.9604 | 0.9959 | 0.7688 | 0.0008745 | 0.8001 | 16.98 | 0.3249 | 632.7 |

## Detection rate at tau, per attack

| attack | hst_slog | hst_proj | autoencoder_slog | iforest_ext_slog | iforest_ext_sparse_slog | mad_tail_slog | kitnet | fusion |
|---|---|---|---|---|---|---|---|---|
| gafgyt/combo | 0 | 0 | 0.998 | 0.992 | 0.999 | 1 | 1 | 1 |
| gafgyt/junk | 0 | 0.0005 | 0.996 | 0.937 | 0.9985 | 1 | 1 | 1 |
| gafgyt/scan | 0.0035 | 0.002 | 0.006 | 0.004 | 0.0065 | 1 | 1 | 1 |
| gafgyt/tcp | 0 | 0 | 0 | 0 | 0 | 0 | 0.001 | 0 |
| gafgyt/udp | 0 | 0.0005 | 0 | 0.0005 | 0 | 0.0005 | 0.001 | 0.0005 |
| mirai/ack | 0 | 0.3385 | 1 | 1 | 0.6625 | 1 | 1 | 1 |
| mirai/scan | 0 | 0.0025 | 0 | 0 | 0.969 | 1 | 1 | 1 |
| mirai/syn | 0 | 0.0005 | 0.697 | 0.684 | 0.9965 | 1 | 1 | 1 |
| mirai/udp | 0 | 0.3565 | 1 | 1 | 0.6435 | 1 | 1 | 1 |
| mirai/udpplain | 0.557 | 0.443 | 0.999 | 1 | 0.558 | 1 | 1 | 1 |
