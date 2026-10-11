# nbaiot_frontrunners_s0_Provision_PT_737E_Security_Camera

Rows: {'benign': 62154, 'bootstrap': 31077, 'validation': 12430, 'test_benign': 18647, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.9998 | 0.8001 | 0.9903 | 0.9989 | 0.5809 | 0.00118 | 0.9999 | 0.7029 | 0.01326 | 1.011 |
| mad_tail_slog | 0.9994 | 0.7148 | 0.9954 | 0.9995 | 0.6135 | 0.0009653 | 0.9994 | 0.9041 | 0.02786 | 0.8984 |
| autoencoder_slog | 0.7749 | 0.6328 | 0.8942 | 0.9772 | 0.02773 | 0.0008044 | 0.7698 | 7.832 | 0.03299 | 8.566 |
| kitnet | 0.9999 | 0.8002 | 0.993 | 0.9993 | 0.1447 | 0.0007508 | 0.9999 | 15.9 | 0.2691 | 6.498 |

## Detection rate at tau, per attack

| attack | robust_z_router | mad_tail_slog | autoencoder_slog | kitnet |
|---|---|---|---|---|
| gafgyt/combo | 1 | 1 | 1 | 1 |
| gafgyt/junk | 1 | 0.995 | 0.9995 | 1 |
| gafgyt/scan | 1 | 1 | 0.716 | 1 |
| gafgyt/tcp | 0.9995 | 0.9995 | 0.001 | 0.9995 |
| gafgyt/udp | 0.9995 | 0.9995 | 0 | 0.9995 |
| mirai/ack | 1 | 1 | 0.9945 | 1 |
| mirai/scan | 1 | 1 | 0.992 | 1 |
| mirai/syn | 1 | 1 | 0.996 | 1 |
| mirai/udp | 1 | 1 | 0.9995 | 1 |
| mirai/udpplain | 1 | 1 | 0.999 | 1 |
