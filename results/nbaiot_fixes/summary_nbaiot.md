# nbaiot_fixes

Rows: {'benign': 49548, 'bootstrap': 24774, 'validation': 9909, 'test_benign': 14865, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window |
|---|---|---|---|---|---|---|---|---|---|
| iforest | 0 | 0 | 0.683 | 0.9647 | 0.8113 | 0.00074 | 0 | 0.4024 | 0.01563 |
| iforest_headroom | 0.00145 | 0 | 0.7151 | 0.9664 | 0.749 | 0.0009418 | 0.00145 | 0.3424 | 0.04459 |
| iforest_extended | 0.6053 | 0.04905 | 0.9116 | 0.9907 | 0.8177 | 0.0008745 | 0.3025 | 0.6604 | 0.9459 |
| mad | 0.0016 | 0.0001 | 0.4984 | 0.4747 | 0.9967 | 0.001009 | 0.0016 | 0.418 | 0.01903 |
| mad_tail | 0.7574 | 0.665 | 0.9258 | 0.9922 | 0.8726 | 0.0009418 | 0.753 | 0.681 | 0.02421 |
| hst | 0.3382 | 0.2165 | 0.9075 | 0.9903 | 0.8092 | 0.0009418 | 0.3362 | 5.942 | 0.186 |
| autoencoder | 0.5773 | 0.5701 | 0.9569 | 0.9955 | 0.02002 | 0.0009418 | 0.5764 | 6.06 | 0.03315 |

## Detection rate at tau, per attack

| attack | iforest | iforest_headroom | iforest_extended | mad | mad_tail | hst | autoencoder |
|---|---|---|---|---|---|---|---|
| gafgyt/combo | 0 | 0 | 0.523 | 0 | 0.9915 | 0.0255 | 0.9995 |
| gafgyt/junk | 0 | 0 | 0.7275 | 0.001 | 0.974 | 0.0495 | 1 |
| gafgyt/scan | 0 | 0.003 | 0.037 | 0.015 | 0.564 | 0.2855 | 0.0655 |
| gafgyt/tcp | 0 | 0 | 0 | 0 | 0 | 0 | 0.001 |
| gafgyt/udp | 0 | 0.0005 | 0 | 0 | 0 | 0 | 0.0005 |
| mirai/ack | 0 | 0 | 0.3325 | 0 | 1 | 1 | 1 |
| mirai/scan | 0 | 0 | 0.551 | 0 | 1 | 0 | 0 |
| mirai/syn | 0 | 0 | 0.2945 | 0 | 1 | 0.001 | 0.6975 |
| mirai/udp | 0 | 0 | 0.348 | 0 | 1 | 1 | 1 |
| mirai/udpplain | 0 | 0.011 | 0.212 | 0 | 1 | 1 | 1 |
