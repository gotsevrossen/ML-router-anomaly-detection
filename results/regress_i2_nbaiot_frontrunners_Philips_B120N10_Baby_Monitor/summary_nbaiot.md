# regress_i2_nbaiot_frontrunners_Philips_B120N10_Baby_Monitor

Rows: {'benign': 175240, 'bootstrap': 87620, 'validation': 35048, 'test_benign': 52572, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.9995 | 0.7997 | 0.994 | 0.9993 | 0.5809 | 0.0009701 | 0.9995 | 3.458 | 0.02065 | 1.011 |
| mad_tail_slog | 0.9996 | 0.7997 | 0.9989 | 0.9998 | 0.649 | 0.0007799 | 0.9995 | 3.976 | 0.0415 | 0.8984 |
| autoencoder_slog | 0.7977 | 0.7802 | 0.9546 | 0.9952 | 0.02501 | 0.000875 | 0.7974 | 10.11 | 0.04873 | 8.566 |
| iforest_ext_sparse_slog | 0.6667 | 0.4746 | 0.865 | 0.9719 | 0.6751 | 0.001065 | 0.6682 | 4.34 | 0.9659 | 776.7 |
| hst_slog | 0.0005 | 0 | 0.5104 | 0.8457 | 0.9928 | 0.0005516 | 0 | 7.927 | 0.0654 | 550.6 |
| kitnet | 0.9997 | 0.7999 | 0.9972 | 0.9996 | 0.1537 | 0.000875 | 0.9997 | 39.64 | 0.2517 | 6.178 |

## Detection rate at tau, per attack

| attack | robust_z_router | mad_tail_slog | autoencoder_slog | iforest_ext_sparse_slog | hst_slog | kitnet |
|---|---|---|---|---|---|---|
| gafgyt/combo | 0.999 | 0.999 | 0.999 | 0.997 | 0 | 0.999 |
| gafgyt/junk | 1 | 1 | 1 | 0.997 | 0 | 1 |
| gafgyt/scan | 1 | 1 | 0.9745 | 0.031 | 0 | 1 |
| gafgyt/tcp | 0.9985 | 0.9985 | 0.0005 | 0 | 0 | 0.9985 |
| gafgyt/udp | 0.999 | 0.999 | 0 | 0 | 0 | 0.999 |
| mirai/ack | 0.999 | 0.999 | 1 | 0.999 | 0 | 1 |
| mirai/scan | 1 | 1 | 1 | 0.6595 | 0 | 1 |
| mirai/syn | 1 | 1 | 1 | 0.9985 | 0 | 1 |
| mirai/udp | 1 | 1 | 1 | 1 | 0 | 1 |
| mirai/udpplain | 0.9995 | 0.9995 | 1 | 0.9995 | 0 | 1 |
