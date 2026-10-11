# regress_i5_nbaiot_frontrunners_SimpleHome_XCS7_1003_WHT_Security_Camera

Rows: {'benign': 19528, 'bootstrap': 9764, 'validation': 3905, 'test_benign': 5859, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.7998 | 0.7998 | 0.9896 | 0.9989 | 0.581 | 0.0006827 | 0.7998 | 0.2206 | 0.01225 | 1.011 |
| mad_tail_slog | 0.9994 | 0.7994 | 0.9938 | 0.9993 | 0.608 | 0.0001707 | 0.7995 | 0.304 | 0.03328 | 0.8984 |
| autoencoder_slog | 0.7961 | 0.7698 | 0.9804 | 0.9979 | 0.0306 | 0.000512 | 0.793 | 2.291 | 0.02668 | 8.566 |
| iforest_ext_sparse_slog | 0.796 | 0.7488 | 0.9707 | 0.9969 | 0.617 | 0.000512 | 0.7846 | 0.4518 | 0.7187 | 658.6 |
| hst_slog | 0.00015 | 0 | 0.5265 | 0.9281 | 0.992 | 0.0003414 | 0 | 1.232 | 0.07405 | 550.6 |
| kitnet | 0.7996 | 0.7995 | 0.9793 | 0.9978 | 0.1519 | 0.0003414 | 0.7995 | 5.06 | 0.2538 | 5.826 |
| ecod_tail | 0.9997 | 0.7997 | 0.9982 | 0.9998 | 0.6989 | 0.001536 | 0.9997 | 0.1239 | 0.02198 | 4387 |

## Detection rate at tau, per attack

| attack | robust_z_router | mad_tail_slog | autoencoder_slog | iforest_ext_sparse_slog | hst_slog | kitnet | ecod_tail |
|---|---|---|---|---|---|---|---|
| gafgyt/combo | 0.9985 | 0.9985 | 0.9985 | 0.999 | 0 | 0.9985 | 0.9985 |
| gafgyt/junk | 1 | 1 | 0.999 | 1 | 0 | 1 | 1 |
| gafgyt/scan | 0.9995 | 0.9985 | 0.933 | 0.8495 | 0 | 0.998 | 1 |
| gafgyt/tcp | 0.0005 | 0 | 0 | 0 | 0 | 0.0005 | 0.9995 |
| gafgyt/udp | 0 | 0 | 0 | 0 | 0 | 0 | 0.9995 |
| mirai/ack | 1 | 0.999 | 0.9995 | 0.9995 | 0 | 0.9995 | 1 |
| mirai/scan | 0.9995 | 0.9995 | 0.9995 | 0.999 | 0 | 0.999 | 1 |
| mirai/syn | 1 | 1 | 1 | 1 | 0 | 1 | 1 |
| mirai/udp | 1 | 1 | 1 | 1 | 0 | 1 | 1 |
| mirai/udpplain | 1 | 0.9995 | 1 | 0.9995 | 0 | 0.9995 | 0.9995 |
