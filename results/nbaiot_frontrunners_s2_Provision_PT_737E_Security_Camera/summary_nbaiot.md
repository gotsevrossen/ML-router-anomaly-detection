# nbaiot_frontrunners_s2_Provision_PT_737E_Security_Camera

Rows: {'benign': 62154, 'bootstrap': 31077, 'validation': 12430, 'test_benign': 18647, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.9997 | 0.8 | 0.9902 | 0.999 | 0.5809 | 0.00118 | 0.9998 | 0.8502 | 0.0151 | 1.011 |
| mad_tail_slog | 0.9996 | 0.7147 | 0.9954 | 0.9995 | 0.6135 | 0.0009653 | 0.9996 | 1.02 | 0.03114 | 0.8984 |
| autoencoder_slog | 0.7724 | 0.6301 | 0.894 | 0.9771 | 0.02773 | 0.0008044 | 0.7677 | 8.374 | 0.03966 | 8.566 |
| kitnet | 0.9998 | 0.8001 | 0.9929 | 0.9993 | 0.1447 | 0.0007508 | 0.9997 | 17.19 | 0.2831 | 6.498 |

## Detection rate at tau, per attack

| attack | robust_z_router | mad_tail_slog | autoencoder_slog | kitnet |
|---|---|---|---|---|
| gafgyt/combo | 1 | 1 | 1 | 1 |
| gafgyt/junk | 1 | 0.9965 | 1 | 1 |
| gafgyt/scan | 1 | 1 | 0.6945 | 1 |
| gafgyt/tcp | 0.999 | 1 | 0.0005 | 0.9995 |
| gafgyt/udp | 0.9985 | 0.999 | 0 | 0.998 |
| mirai/ack | 1 | 1 | 0.9945 | 1 |
| mirai/scan | 1 | 1 | 0.992 | 1 |
| mirai/syn | 1 | 1 | 0.9965 | 1 |
| mirai/udp | 1 | 1 | 0.9995 | 0.9995 |
| mirai/udpplain | 1 | 1 | 0.999 | 1 |
