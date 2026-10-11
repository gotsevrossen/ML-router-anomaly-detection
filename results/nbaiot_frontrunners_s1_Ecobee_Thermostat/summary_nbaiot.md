# nbaiot_frontrunners_s1_Ecobee_Thermostat

Rows: {'benign': 13113, 'bootstrap': 6556, 'validation': 2622, 'test_benign': 3935, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.8 | 0.8 | 0.9668 | 0.9965 | 0.5895 | 0.0005083 | 0.8 | 0.1512 | 0.01651 | 1.011 |
| mad_tail_slog | 0.8 | 0.8 | 0.9885 | 0.9988 | 0.6155 | 0 | 0.8 | 0.3429 | 0.04849 | 0.8984 |
| autoencoder_slog | 0.8001 | 0.8 | 0.9872 | 0.9987 | 0.01823 | 0.0007624 | 0.8001 | 7.626 | 0.03816 | 8.566 |
| kitnet | 0.8 | 0.8 | 0.8995 | 0.9853 | 0.1264 | 0.004574 | 0.8 | 5.137 | 0.4414 | 6.467 |

## Detection rate at tau, per attack

| attack | robust_z_router | mad_tail_slog | autoencoder_slog | kitnet |
|---|---|---|---|---|
| gafgyt/combo | 1 | 1 | 1 | 1 |
| gafgyt/junk | 0.9995 | 0.9995 | 0.9995 | 0.9995 |
| gafgyt/scan | 1 | 1 | 1 | 1 |
| gafgyt/tcp | 0.0005 | 0 | 0.0005 | 0.0005 |
| gafgyt/udp | 0.001 | 0.001 | 0.0015 | 0.001 |
| mirai/ack | 1 | 1 | 1 | 1 |
| mirai/scan | 0.9995 | 0.9995 | 0.9995 | 0.9995 |
| mirai/syn | 1 | 1 | 1 | 1 |
| mirai/udp | 1 | 1 | 1 | 1 |
| mirai/udpplain | 0.9995 | 0.9995 | 0.9995 | 0.9995 |
