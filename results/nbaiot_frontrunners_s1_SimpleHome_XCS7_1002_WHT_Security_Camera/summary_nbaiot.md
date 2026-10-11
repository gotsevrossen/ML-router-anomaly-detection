# nbaiot_frontrunners_s1_SimpleHome_XCS7_1002_WHT_Security_Camera

Rows: {'benign': 46585, 'bootstrap': 23292, 'validation': 9317, 'test_benign': 13976, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.8001 | 0.7979 | 0.9901 | 0.9989 | 0.5809 | 0.001789 | 0.9998 | 0.5553 | 0.01063 | 1.011 |
| mad_tail_slog | 0.9997 | 0.6125 | 0.9899 | 0.9989 | 0.6018 | 0.0007155 | 0.9997 | 0.6243 | 0.02372 | 0.8984 |
| autoencoder_slog | 0.9141 | 0.8899 | 0.9657 | 0.9924 | 0.02646 | 0.001646 | 0.9166 | 5.599 | 0.02983 | 8.566 |
| kitnet | 0.7956 | 0.795 | 0.8975 | 0.9502 | 0.4916 | 0 | 0.7941 | 10.07 | 0.2399 | 5.975 |

## Detection rate at tau, per attack

| attack | robust_z_router | mad_tail_slog | autoencoder_slog | kitnet |
|---|---|---|---|---|
| gafgyt/combo | 1 | 1 | 0.9995 | 1 |
| gafgyt/junk | 0.9995 | 0.9995 | 0.999 | 0.9995 |
| gafgyt/scan | 1 | 1 | 0.182 | 0.988 |
| gafgyt/tcp | 1 | 0.9995 | 0.9995 | 0 |
| gafgyt/udp | 0.9985 | 0.9975 | 0.9975 | 0 |
| mirai/ack | 1 | 1 | 1 | 1 |
| mirai/scan | 0.9995 | 1 | 0.989 | 0.954 |
| mirai/syn | 1 | 1 | 0.9995 | 1 |
| mirai/udp | 1 | 1 | 1 | 1 |
| mirai/udpplain | 1 | 1 | 1 | 0.9995 |
