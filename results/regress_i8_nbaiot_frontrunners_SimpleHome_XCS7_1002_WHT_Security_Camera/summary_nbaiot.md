# regress_i8_nbaiot_frontrunners_SimpleHome_XCS7_1002_WHT_Security_Camera

Rows: {'benign': 46585, 'bootstrap': 23292, 'validation': 9317, 'test_benign': 13976, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.7998 | 0.7975 | 0.9901 | 0.999 | 0.5809 | 0.001789 | 0.9997 | 0.4682 | 0.01283 | 1.011 |
| mad_tail_slog | 0.9998 | 0.6101 | 0.99 | 0.9989 | 0.6018 | 0.0007155 | 0.9998 | 0.5266 | 0.02469 | 0.8984 |
| autoencoder_slog | 0.9142 | 0.8907 | 0.9659 | 0.9926 | 0.02646 | 0.001646 | 0.9169 | 2.742 | 0.0277 | 8.566 |
| iforest_ext_sparse_slog | 0.9644 | 0.7261 | 0.9935 | 0.9991 | 0.5747 | 0.0002862 | 0.9396 | 0.9454 | 0.7737 | 763.6 |
| hst_slog | 0 | 0 | 0.4975 | 0.619 | 0.9914 | 0 | 0 | 1.97 | 0.06472 | 550.6 |
| kitnet | 0.795 | 0.7946 | 0.8971 | 0.9501 | 0.4916 | 0 | 0.7936 | 9.705 | 0.246 | 5.975 |
| ecod_tail | 0.9992 | 0.7954 | 0.9948 | 0.9995 | 0.7061 | 0.002147 | 0.9992 | 0.3117 | 0.02568 | 1.046e+04 |
| ecod_router | 0.9992 | 0.7954 | 0.9947 | 0.9994 | 0.7061 | 0.002147 | 0.9992 | 0.3861 | 0.02621 | 174.7 |

## Detection rate at tau, per attack

| attack | robust_z_router | mad_tail_slog | autoencoder_slog | iforest_ext_sparse_slog | hst_slog | kitnet | ecod_tail | ecod_router |
|---|---|---|---|---|---|---|---|---|
| gafgyt/combo | 1 | 1 | 0.998 | 0.9995 | 0 | 1 | 1 | 1 |
| gafgyt/junk | 1 | 1 | 0.9975 | 0.999 | 0 | 1 | 1 | 1 |
| gafgyt/scan | 0.998 | 0.998 | 0.1835 | 0.426 | 0 | 0.9895 | 0.994 | 0.994 |
| gafgyt/tcp | 1 | 1 | 0.9995 | 0.999 | 0 | 0 | 0.9995 | 0.9995 |
| gafgyt/udp | 1 | 0.9995 | 0.9995 | 0.9995 | 0 | 0 | 1 | 1 |
| mirai/ack | 1 | 1 | 1 | 1 | 0 | 0.9995 | 1 | 1 |
| mirai/scan | 0.999 | 1 | 0.991 | 0.9745 | 0 | 0.948 | 0.999 | 0.999 |
| mirai/syn | 1 | 1 | 1 | 0.9995 | 0 | 1 | 1 | 1 |
| mirai/udp | 1 | 1 | 1 | 0.999 | 0 | 1 | 1 | 1 |
| mirai/udpplain | 1 | 1 | 1 | 1 | 0 | 0.9995 | 1 | 1 |
