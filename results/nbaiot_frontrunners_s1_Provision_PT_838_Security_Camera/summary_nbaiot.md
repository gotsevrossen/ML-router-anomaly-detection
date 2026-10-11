# nbaiot_frontrunners_s1_Provision_PT_838_Security_Camera

Rows: {'benign': 98514, 'bootstrap': 49257, 'validation': 19702, 'test_benign': 29555, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.7995 | 0.7995 | 0.9897 | 0.9988 | 0.5809 | 0.0008797 | 0.7995 | 1.112 | 0.0128 | 1.011 |
| mad_tail_slog | 0.7901 | 0.04785 | 0.9463 | 0.9943 | 0.6049 | 0.0006767 | 0.789 | 1.501 | 0.02819 | 0.8984 |
| autoencoder_slog | 0.7835 | 0.1545 | 0.8926 | 0.974 | 0.02534 | 0.0007105 | 0.7556 | 8.298 | 0.03325 | 8.566 |
| kitnet | 0.9999 | 0.7998 | 0.9924 | 0.9992 | 0.1452 | 0.000609 | 0.8 | 24.6 | 0.2735 | 6.252 |

## Detection rate at tau, per attack

| attack | robust_z_router | mad_tail_slog | autoencoder_slog | kitnet |
|---|---|---|---|---|
| gafgyt/combo | 1 | 1 | 0.997 | 1 |
| gafgyt/junk | 0.9995 | 0.9995 | 0.998 | 0.9995 |
| gafgyt/scan | 0.997 | 0.8925 | 0.6005 | 1 |
| gafgyt/tcp | 0 | 0.0005 | 0 | 0.0005 |
| gafgyt/udp | 0 | 0.0005 | 0 | 0.0005 |
| mirai/ack | 0.9995 | 0.9995 | 0.9815 | 0.9995 |
| mirai/scan | 1 | 0.9975 | 0.9965 | 1 |
| mirai/syn | 0.9995 | 0.9995 | 0.9935 | 0.9995 |
| mirai/udp | 1 | 1 | 0.993 | 1 |
| mirai/udpplain | 1 | 1 | 0.9955 | 1 |
