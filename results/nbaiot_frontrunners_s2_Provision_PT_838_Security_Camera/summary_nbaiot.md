# nbaiot_frontrunners_s2_Provision_PT_838_Security_Camera

Rows: {'benign': 98514, 'bootstrap': 49257, 'validation': 19702, 'test_benign': 29555, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.7997 | 0.7997 | 0.9898 | 0.9988 | 0.5809 | 0.0008797 | 0.7997 | 1.278 | 0.01328 | 1.011 |
| mad_tail_slog | 0.7929 | 0.051 | 0.9466 | 0.9944 | 0.6049 | 0.0006767 | 0.7921 | 1.59 | 0.02859 | 0.8984 |
| autoencoder_slog | 0.784 | 0.158 | 0.8925 | 0.974 | 0.02534 | 0.0007105 | 0.7551 | 8.324 | 0.03387 | 8.566 |
| kitnet | 0.9999 | 0.8001 | 0.9925 | 0.9992 | 0.1452 | 0.000609 | 0.8001 | 25.41 | 0.313 | 6.252 |

## Detection rate at tau, per attack

| attack | robust_z_router | mad_tail_slog | autoencoder_slog | kitnet |
|---|---|---|---|---|
| gafgyt/combo | 1 | 1 | 0.998 | 1 |
| gafgyt/junk | 1 | 1 | 0.9945 | 1 |
| gafgyt/scan | 0.997 | 0.9225 | 0.607 | 1 |
| gafgyt/tcp | 0 | 0.0005 | 0.0005 | 0.0005 |
| gafgyt/udp | 0 | 0 | 0 | 0 |
| mirai/ack | 1 | 1 | 0.9765 | 1 |
| mirai/scan | 1 | 0.998 | 0.992 | 1 |
| mirai/syn | 1 | 1 | 0.994 | 1 |
| mirai/udp | 1 | 1 | 0.9955 | 1 |
| mirai/udpplain | 1 | 1 | 0.993 | 1 |
