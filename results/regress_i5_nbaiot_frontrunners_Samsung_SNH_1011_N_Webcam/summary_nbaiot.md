# regress_i5_nbaiot_frontrunners_Samsung_SNH_1011_N_Webcam

Rows: {'benign': 52150, 'bootstrap': 26075, 'validation': 10430, 'test_benign': 15645, 'test_attack': 10000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.5998 | 0.5814 | 0.9534 | 0.995 | 0.5867 | 0.0008949 | 0.5998 | 0.648 | 0.0104 | 1.011 |
| mad_tail_slog | 0.9995 | 0.9995 | 0.9986 | 0.9998 | 0.6273 | 6.392e-05 | 0.5998 | 0.873 | 0.0251 | 0.8984 |
| autoencoder_slog | 0.5832 | 0.5389 | 0.7952 | 0.9296 | 0.03859 | 0.0006392 | 0.58 | 2.729 | 0.02861 | 8.566 |
| iforest_ext_sparse_slog | 0.4097 | 0.3964 | 0.8249 | 0.9816 | 0.6802 | 0.0005113 | 0.3983 | 1.072 | 0.714 | 875.3 |
| hst_slog | 0.5118 | 0.2879 | 0.7861 | 0.9662 | 0.945 | 0.0006392 | 0.4582 | 2.924 | 0.08157 | 550.6 |
| kitnet | 0.5999 | 0.5998 | 0.7989 | 0.9258 | 0.1705 | 0.0002557 | 0.5998 | 14.42 | 0.3164 | 6.396 |
| ecod_tail | 0.5998 | 0.5911 | 0.949 | 0.9946 | 0.7089 | 0.0005753 | 0.5998 | 0.4566 | 0.0338 | 1.171e+04 |

## Detection rate at tau, per attack

| attack | robust_z_router | mad_tail_slog | autoencoder_slog | iforest_ext_sparse_slog | hst_slog | kitnet | ecod_tail |
|---|---|---|---|---|---|---|---|
| gafgyt/combo | 0.999 | 0.999 | 0.999 | 0.994 | 0.998 | 0.999 | 0.999 |
| gafgyt/junk | 1 | 1 | 1 | 0.9965 | 0.9995 | 1 | 1 |
| gafgyt/scan | 1 | 1 | 0.901 | 0.001 | 0.2935 | 1 | 1 |
| gafgyt/tcp | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| gafgyt/udp | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
