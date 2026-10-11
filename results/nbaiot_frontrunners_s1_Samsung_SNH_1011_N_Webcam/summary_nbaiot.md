# nbaiot_frontrunners_s1_Samsung_SNH_1011_N_Webcam

Rows: {'benign': 52150, 'bootstrap': 26075, 'validation': 10430, 'test_benign': 15645, 'test_attack': 10000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.5999 | 0.5423 | 0.9517 | 0.9947 | 0.5874 | 0.0009588 | 0.5999 | 0.5734 | 0.01082 | 1.011 |
| mad_tail_slog | 0.9995 | 0.9995 | 0.9986 | 0.9998 | 0.6273 | 6.392e-05 | 0.5999 | 0.7929 | 0.02852 | 0.8984 |
| autoencoder_slog | 0.5854 | 0.5381 | 0.7954 | 0.9296 | 0.03859 | 0.0006392 | 0.5813 | 7.554 | 0.03117 | 8.566 |
| kitnet | 0.5999 | 0.5999 | 0.7989 | 0.9258 | 0.1705 | 0.0002557 | 0.5999 | 13.57 | 0.2704 | 6.396 |

## Detection rate at tau, per attack

| attack | robust_z_router | mad_tail_slog | autoencoder_slog | kitnet |
|---|---|---|---|---|
| gafgyt/combo | 1 | 1 | 1 | 1 |
| gafgyt/junk | 0.9995 | 0.9995 | 0.9995 | 0.9995 |
| gafgyt/scan | 1 | 1 | 0.907 | 1 |
| gafgyt/tcp | 0 | 0 | 0 | 0 |
| gafgyt/udp | 0 | 0 | 0 | 0 |
