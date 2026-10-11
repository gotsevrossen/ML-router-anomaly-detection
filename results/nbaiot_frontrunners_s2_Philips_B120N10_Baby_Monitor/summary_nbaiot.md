# nbaiot_frontrunners_s2_Philips_B120N10_Baby_Monitor

Rows: {'benign': 175240, 'bootstrap': 87620, 'validation': 35048, 'test_benign': 52572, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.9997 | 0.7999 | 0.9941 | 0.9993 | 0.5809 | 0.0009701 | 0.9997 | 1.898 | 0.01148 | 1.011 |
| mad_tail_slog | 0.9998 | 0.7999 | 0.9989 | 0.9999 | 0.649 | 0.0007799 | 0.9997 | 2.365 | 0.02717 | 0.8984 |
| autoencoder_slog | 0.7979 | 0.7806 | 0.9546 | 0.9952 | 0.02501 | 0.000875 | 0.7977 | 10.82 | 0.03365 | 8.566 |
| kitnet | 0.9998 | 0.8 | 0.9972 | 0.9997 | 0.1537 | 0.000875 | 0.9998 | 55.21 | 0.3512 | 6.178 |

## Detection rate at tau, per attack

| attack | robust_z_router | mad_tail_slog | autoencoder_slog | kitnet |
|---|---|---|---|---|
| gafgyt/combo | 0.9995 | 0.9995 | 0.9995 | 0.9995 |
| gafgyt/junk | 1 | 1 | 1 | 1 |
| gafgyt/scan | 1 | 1 | 0.978 | 1 |
| gafgyt/tcp | 0.999 | 0.999 | 0 | 0.999 |
| gafgyt/udp | 0.999 | 0.999 | 0 | 0.999 |
| mirai/ack | 1 | 1 | 1 | 1 |
| mirai/scan | 1 | 1 | 1 | 1 |
| mirai/syn | 1 | 1 | 1 | 1 |
| mirai/udp | 1 | 1 | 1 | 1 |
| mirai/udpplain | 0.9995 | 0.9995 | 1 | 1 |
