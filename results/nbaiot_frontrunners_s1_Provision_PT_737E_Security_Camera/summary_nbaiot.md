# nbaiot_frontrunners_s1_Provision_PT_737E_Security_Camera

Rows: {'benign': 62154, 'bootstrap': 31077, 'validation': 12430, 'test_benign': 18647, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 1 | 0.7998 | 0.9903 | 0.999 | 0.5809 | 0.00118 | 1 | 0.8171 | 0.01372 | 1.011 |
| mad_tail_slog | 0.9997 | 0.7122 | 0.9954 | 0.9995 | 0.6135 | 0.0009653 | 0.9997 | 0.8982 | 0.02892 | 0.8984 |
| autoencoder_slog | 0.7728 | 0.6304 | 0.8939 | 0.9771 | 0.02773 | 0.0008044 | 0.7685 | 7.364 | 0.03068 | 8.566 |
| kitnet | 1 | 0.7998 | 0.993 | 0.9993 | 0.1447 | 0.0007508 | 1 | 16.57 | 0.2801 | 6.498 |

## Detection rate at tau, per attack

| attack | robust_z_router | mad_tail_slog | autoencoder_slog | kitnet |
|---|---|---|---|---|
| gafgyt/combo | 1 | 1 | 1 | 1 |
| gafgyt/junk | 1 | 0.9985 | 0.9995 | 0.9995 |
| gafgyt/scan | 1 | 1 | 0.7025 | 1 |
| gafgyt/tcp | 1 | 1 | 0.0005 | 1 |
| gafgyt/udp | 1 | 1 | 0 | 1 |
| mirai/ack | 1 | 1 | 0.994 | 1 |
| mirai/scan | 1 | 0.9995 | 0.994 | 1 |
| mirai/syn | 1 | 0.9995 | 0.996 | 1 |
| mirai/udp | 1 | 1 | 0.9995 | 1 |
| mirai/udpplain | 1 | 0.9995 | 0.999 | 1 |
