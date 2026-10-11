# nbaiot_improved_SimpleHome_XCS7_1002_WHT_Security_Camera

Rows: {'benign': 46585, 'bootstrap': 23292, 'validation': 9317, 'test_benign': 13976, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| hst_slog | 0 | 0 | 0.4975 | 0.619 | 0.9914 | 0.004508 | 0 | 4.955 | 0.1318 | 550.6 |
| hst_proj | 0 | 0 | 0.525 | 0.797 | 0.9922 | 0.0009302 | 0 | 3.042 | 0.1093 | 565.2 |
| autoencoder_slog | 0.9142 | 0.8907 | 0.9659 | 0.9926 | 0.02646 | 0.001646 | 0.9169 | 11.47 | 0.04674 | 8.566 |
| iforest_ext_slog | 0.8884 | 0.571 | 0.9616 | 0.9954 | 0.5898 | 0.0004293 | 0.8668 | 2.306 | 0.8678 | 5654 |
| iforest_ext_sparse_slog | 0.9644 | 0.7261 | 0.9935 | 0.9991 | 0.5747 | 0.0002862 | 0.9396 | 1.459 | 0.702 | 763.6 |
| mad_tail_slog | 0.9998 | 0.6101 | 0.99 | 0.9989 | 0.6018 | 0.0007155 | 0.9998 | 0.5096 | 0.02271 | 0.8984 |
| kitnet | 0.795 | 0.7946 | 0.8971 | 0.9501 | 0.4916 | 0 | 0.7936 | 9.582 | 0.2316 | 5.975 |
| fusion | 0.9996 | 0.6159 | 0.9901 | 0.9989 | 0.6903 | 0.001073 | 0.9997 | 4.787 | 0.1066 | 629.3 |

## Detection rate at tau, per attack

| attack | hst_slog | hst_proj | autoencoder_slog | iforest_ext_slog | iforest_ext_sparse_slog | mad_tail_slog | kitnet | fusion |
|---|---|---|---|---|---|---|---|---|
| gafgyt/combo | 0 | 0 | 0.998 | 0.9985 | 0.9995 | 1 | 1 | 1 |
| gafgyt/junk | 0 | 0 | 0.9975 | 0.997 | 0.999 | 1 | 1 | 1 |
| gafgyt/scan | 0 | 0 | 0.1835 | 0.005 | 0.426 | 0.998 | 0.9895 | 0.998 |
| gafgyt/tcp | 0 | 0 | 0.9995 | 0.999 | 0.999 | 1 | 0 | 0.9995 |
| gafgyt/udp | 0 | 0 | 0.9995 | 0.9995 | 0.9995 | 0.9995 | 0 | 0.9995 |
| mirai/ack | 0 | 0 | 1 | 0.999 | 1 | 1 | 0.9995 | 1 |
| mirai/scan | 0 | 0 | 0.991 | 0.685 | 0.9745 | 1 | 0.948 | 0.9995 |
| mirai/syn | 0 | 0 | 1 | 0.9905 | 0.9995 | 1 | 1 | 1 |
| mirai/udp | 0 | 0 | 1 | 0.999 | 0.999 | 1 | 1 | 1 |
| mirai/udpplain | 0 | 0 | 1 | 0.9955 | 1 | 1 | 0.9995 | 1 |
