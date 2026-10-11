# nbaiot_frontrunners_s0_Samsung_SNH_1011_N_Webcam

Rows: {'benign': 52150, 'bootstrap': 26075, 'validation': 10430, 'test_benign': 15645, 'test_attack': 10000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window | model_kb |
|---|---|---|---|---|---|---|---|---|---|---|
| robust_z_router | 0.5998 | 0.5458 | 0.9518 | 0.9948 | 0.5874 | 0.0009588 | 0.5998 | 0.5491 | 0.01029 | 1.011 |
| mad_tail_slog | 0.9995 | 0.9995 | 0.9986 | 0.9998 | 0.6273 | 6.392e-05 | 0.5998 | 0.8166 | 0.02698 | 0.8984 |
| autoencoder_slog | 0.5832 | 0.5389 | 0.7952 | 0.9296 | 0.03859 | 0.0006392 | 0.58 | 6.768 | 0.03 | 8.566 |
| kitnet | 0.5999 | 0.5998 | 0.7989 | 0.9258 | 0.1705 | 0.0002557 | 0.5998 | 15.78 | 0.3367 | 6.396 |

## Detection rate at tau, per attack

| attack | robust_z_router | mad_tail_slog | autoencoder_slog | kitnet |
|---|---|---|---|---|
| gafgyt/combo | 0.999 | 0.999 | 0.999 | 0.999 |
| gafgyt/junk | 1 | 1 | 1 | 1 |
| gafgyt/scan | 1 | 1 | 0.901 | 1 |
| gafgyt/tcp | 0 | 0 | 0 | 0 |
| gafgyt/udp | 0 | 0 | 0 | 0 |
