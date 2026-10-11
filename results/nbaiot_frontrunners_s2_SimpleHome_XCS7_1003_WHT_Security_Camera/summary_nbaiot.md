# nbaiot_frontrunners_s2_SimpleHome_XCS7_1003_WHT_Security_Camera

Rows: {'benign': 19528, 'bootstrap': 9764, 'validation': 3905, 'test_benign': 5859, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.8 | 0.8 | 0.9897 | 0.9989 | 0.581 | 0.0006827 | 0.8 | 0.2676 | 0.01534 | 1.011 |
| mad_tail_slog | 0.9999 | 0.7998 | 0.9939 | 0.9993 | 0.608 | 0.0001707 | 0.7998 | 0.4145 | 0.02898 | 0.8984 |
| autoencoder_slog | 0.7966 | 0.771 | 0.9805 | 0.998 | 0.0306 | 0.000512 | 0.7931 | 6.635 | 0.04475 | 8.566 |
| kitnet | 0.7999 | 0.7998 | 0.9794 | 0.9978 | 0.1519 | 0.0003414 | 0.7998 | 4.992 | 0.2767 | 5.826 |

## Detection rate at tau, per attack

| attack | robust_z_router | mad_tail_slog | autoencoder_slog | kitnet |
|---|---|---|---|---|
| gafgyt/combo | 0.9995 | 0.9995 | 1 | 0.9995 |
| gafgyt/junk | 1 | 1 | 0.9995 | 1 |
| gafgyt/scan | 1 | 1 | 0.932 | 1 |
| gafgyt/tcp | 0 | 0 | 0 | 0 |
| gafgyt/udp | 0 | 0 | 0 | 0 |
| mirai/ack | 1 | 1 | 1 | 1 |
| mirai/scan | 1 | 0.9995 | 0.9995 | 0.9995 |
| mirai/syn | 1 | 1 | 1 | 1 |
| mirai/udp | 1 | 1 | 1 | 1 |
| mirai/udpplain | 1 | 0.9995 | 1 | 0.9995 |
