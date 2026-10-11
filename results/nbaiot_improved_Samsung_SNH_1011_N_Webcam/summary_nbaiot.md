# nbaiot_improved_Samsung_SNH_1011_N_Webcam

Rows: {'benign': 52150, 'bootstrap': 26075, 'validation': 10430, 'test_benign': 15645, 'test_attack': 10000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| hst_slog | 0.5118 | 0.2879 | 0.7861 | 0.9662 | 0.945 | 0.0006392 | 0.4582 | 3.688 | 0.0995 | 550.6 |
| hst_proj | 0.4226 | 0.4 | 0.737 | 0.8919 | 0.8879 | 0.000767 | 0.4203 | 2.268 | 0.08348 | 565.2 |
| autoencoder_slog | 0.5832 | 0.5389 | 0.7952 | 0.9296 | 0.03859 | 0.0006392 | 0.58 | 9.313 | 0.03696 | 8.566 |
| iforest_ext_slog | 0.5964 | 0.5898 | 0.8811 | 0.9875 | 0.6468 | 0.0004474 | 0.5938 | 1.202 | 0.7819 | 6286 |
| iforest_ext_sparse_slog | 0.4097 | 0.3964 | 0.8249 | 0.9816 | 0.6802 | 0.0005113 | 0.3983 | 1.08 | 0.8279 | 875.3 |
| mad_tail_slog | 0.9995 | 0.9995 | 0.9986 | 0.9998 | 0.6273 | 6.392e-05 | 0.9995 | 0.7679 | 0.03005 | 0.8984 |
| kitnet | 0.5999 | 0.5998 | 0.7989 | 0.9258 | 0.1705 | 0.0002557 | 0.5998 | 18.61 | 0.4735 | 6.396 |
| fusion | 0.6 | 0.5904 | 0.9278 | 0.9924 | 0.6903 | 0.0006392 | 0.5994 | 12.77 | 0.1958 | 635.8 |

## Detection rate at tau, per attack

| attack | hst_slog | hst_proj | autoencoder_slog | iforest_ext_slog | iforest_ext_sparse_slog | mad_tail_slog | kitnet | fusion |
|---|---|---|---|---|---|---|---|---|
| gafgyt/combo | 0.998 | 0.9985 | 0.999 | 0.999 | 0.994 | 0.999 | 0.999 | 1 |
| gafgyt/junk | 0.9995 | 1 | 1 | 1 | 0.9965 | 1 | 1 | 1 |
| gafgyt/scan | 0.2935 | 0.103 | 0.901 | 0.97 | 0.001 | 1 | 1 | 0.997 |
| gafgyt/tcp | 0 | 0 | 0 | 0 | 0 | 0.999 | 0 | 0 |
| gafgyt/udp | 0 | 0 | 0 | 0 | 0 | 0.9995 | 0 | 0 |
