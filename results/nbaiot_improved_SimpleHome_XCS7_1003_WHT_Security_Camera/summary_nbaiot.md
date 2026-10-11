# nbaiot_improved_SimpleHome_XCS7_1003_WHT_Security_Camera

Rows: {'benign': 19528, 'bootstrap': 9764, 'validation': 3905, 'test_benign': 5859, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| hst_slog | 0.00015 | 0 | 0.5265 | 0.9281 | 0.992 | 0.0003414 | 0 | 1.318 | 0.06449 | 550.6 |
| hst_proj | 0.5885 | 0.3874 | 0.8705 | 0.9743 | 0.9804 | 0.0001707 | 0.4778 | 0.7777 | 0.05238 | 565.2 |
| autoencoder_slog | 0.7961 | 0.7698 | 0.9804 | 0.9979 | 0.0306 | 0.000512 | 0.793 | 5.425 | 0.0262 | 8.566 |
| iforest_ext_slog | 0.7996 | 0.7458 | 0.9694 | 0.9968 | 0.619 | 0.0003414 | 0.7993 | 0.495 | 0.5686 | 4897 |
| iforest_ext_sparse_slog | 0.796 | 0.7488 | 0.9707 | 0.9969 | 0.617 | 0.000512 | 0.7846 | 0.4633 | 0.5747 | 658.6 |
| mad_tail_slog | 0.9994 | 0.7994 | 0.9938 | 0.9993 | 0.608 | 0.0001707 | 0.7995 | 0.2128 | 0.02024 | 0.8984 |
| kitnet | 0.7996 | 0.7995 | 0.9793 | 0.9978 | 0.1519 | 0.0003414 | 0.7995 | 4.098 | 0.2316 | 5.826 |
| fusion | 0.7997 | 0.7994 | 0.9227 | 0.9919 | 0.6323 | 0.0003414 | 0.7995 | 3.281 | 0.1064 | 597.6 |

## Detection rate at tau, per attack

| attack | hst_slog | hst_proj | autoencoder_slog | iforest_ext_slog | iforest_ext_sparse_slog | mad_tail_slog | kitnet | fusion |
|---|---|---|---|---|---|---|---|---|
| gafgyt/combo | 0 | 0.783 | 0.9985 | 0.9985 | 0.999 | 0.9985 | 0.9985 | 0.9985 |
| gafgyt/junk | 0 | 0.6255 | 0.999 | 1 | 1 | 1 | 1 | 1 |
| gafgyt/scan | 0 | 0 | 0.933 | 0.9965 | 0.8495 | 0.9985 | 0.998 | 0.999 |
| gafgyt/tcp | 0 | 0 | 0 | 0 | 0 | 0 | 0.0005 | 0 |
| gafgyt/udp | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| mirai/ack | 0 | 0.944 | 0.9995 | 0.999 | 0.9995 | 0.999 | 0.9995 | 0.999 |
| mirai/scan | 0 | 0.0125 | 0.9995 | 0.9995 | 0.999 | 0.9995 | 0.999 | 0.9995 |
| mirai/syn | 0 | 0.6965 | 1 | 1 | 1 | 1 | 1 | 1 |
| mirai/udp | 0 | 0.945 | 1 | 1 | 1 | 1 | 1 | 1 |
| mirai/udpplain | 0 | 0.772 | 1 | 0.9995 | 0.9995 | 0.9995 | 0.9995 | 0.9995 |
