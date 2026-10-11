# nbaiot_frontrunners_s2_SimpleHome_XCS7_1002_WHT_Security_Camera

Rows: {'benign': 46585, 'bootstrap': 23292, 'validation': 9317, 'test_benign': 13976, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.8 | 0.7978 | 0.9902 | 0.999 | 0.5809 | 0.001789 | 0.9999 | 0.9606 | 0.01806 | 1.011 |
| mad_tail_slog | 0.9999 | 0.6095 | 0.9899 | 0.9989 | 0.6018 | 0.0007155 | 0.9999 | 0.9359 | 0.03408 | 0.8984 |
| autoencoder_slog | 0.9157 | 0.8892 | 0.9663 | 0.9925 | 0.02646 | 0.001646 | 0.9187 | 7.503 | 0.04215 | 8.566 |
| kitnet | 0.7955 | 0.7949 | 0.8975 | 0.9502 | 0.4916 | 0 | 0.7935 | 11.78 | 0.3569 | 5.975 |

## Detection rate at tau, per attack

| attack | robust_z_router | mad_tail_slog | autoencoder_slog | kitnet |
|---|---|---|---|---|
| gafgyt/combo | 1 | 1 | 0.999 | 1 |
| gafgyt/junk | 1 | 1 | 0.9985 | 1 |
| gafgyt/scan | 1 | 1 | 0.2025 | 0.988 |
| gafgyt/tcp | 1 | 0.9995 | 0.9995 | 0 |
| gafgyt/udp | 0.9995 | 0.9995 | 0.9995 | 0 |
| mirai/ack | 1 | 1 | 1 | 1 |
| mirai/scan | 0.9995 | 1 | 0.99 | 0.948 |
| mirai/syn | 1 | 1 | 0.9985 | 1 |
| mirai/udp | 1 | 1 | 1 | 1 |
| mirai/udpplain | 1 | 1 | 1 | 0.9995 |
