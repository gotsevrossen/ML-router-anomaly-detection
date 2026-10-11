# nbaiot_frontrunners_s0_SimpleHome_XCS7_1002_WHT_Security_Camera

Rows: {'benign': 46585, 'bootstrap': 23292, 'validation': 9317, 'test_benign': 13976, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.7998 | 0.7975 | 0.9901 | 0.999 | 0.5809 | 0.001789 | 0.9997 | 0.5537 | 0.01181 | 1.011 |
| mad_tail_slog | 0.9998 | 0.6101 | 0.99 | 0.9989 | 0.6018 | 0.0007155 | 0.9998 | 0.7755 | 0.03176 | 0.8984 |
| autoencoder_slog | 0.9142 | 0.8907 | 0.9659 | 0.9926 | 0.02646 | 0.001646 | 0.9169 | 6.971 | 0.03263 | 8.566 |
| kitnet | 0.795 | 0.7946 | 0.8971 | 0.9501 | 0.4916 | 0 | 0.7936 | 11.27 | 0.341 | 5.975 |

## Detection rate at tau, per attack

| attack | robust_z_router | mad_tail_slog | autoencoder_slog | kitnet |
|---|---|---|---|---|
| gafgyt/combo | 1 | 1 | 0.998 | 1 |
| gafgyt/junk | 1 | 1 | 0.9975 | 1 |
| gafgyt/scan | 0.998 | 0.998 | 0.1835 | 0.9895 |
| gafgyt/tcp | 1 | 1 | 0.9995 | 0 |
| gafgyt/udp | 1 | 0.9995 | 0.9995 | 0 |
| mirai/ack | 1 | 1 | 1 | 0.9995 |
| mirai/scan | 0.999 | 1 | 0.991 | 0.948 |
| mirai/syn | 1 | 1 | 1 | 1 |
| mirai/udp | 1 | 1 | 1 | 1 |
| mirai/udpplain | 1 | 1 | 1 | 0.9995 |
