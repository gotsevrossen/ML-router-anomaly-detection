# nbaiot_danmini_doorbell

Rows: {'benign': 49548, 'bootstrap': 24774, 'validation': 9909, 'test_benign': 14865, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window |
|---|---|---|---|---|---|---|---|---|---|
| hst | 0.3382 | 0.2165 | 0.9075 | 0.9903 | 0.8092 | 0.0009418 | 0.3362 | 9.947 | 0.3424 |
| iforest | 0 | 0 | 0.683 | 0.9647 | 0.8113 | 0.00074 | 0 | 1.472 | 0.05464 |
| autoencoder | 0.5773 | 0.5701 | 0.9569 | 0.9955 | 0.02002 | 0.0009418 | 0.5764 | 13.16 | 0.05135 |
| mad | 0.0016 | 0.0001 | 0.4984 | 0.4747 | 0.9967 | 0.001009 | 0.0016 | 1.384 | 0.04158 |
| kitnet | 0.8002 | 0.8002 | 0.9237 | 0.992 | 0.1558 | 0.00074 | 0.8002 | 125.9 | 2.086 |

## Detection rate at tau, per attack

| attack | hst | iforest | autoencoder | mad | kitnet |
|---|---|---|---|---|---|
| gafgyt/combo | 0.0255 | 0 | 0.9995 | 0 | 1 |
| gafgyt/junk | 0.0495 | 0 | 1 | 0.001 | 1 |
| gafgyt/scan | 0.2855 | 0 | 0.0655 | 0.015 | 1 |
| gafgyt/tcp | 0 | 0 | 0.001 | 0 | 0.001 |
| gafgyt/udp | 0 | 0 | 0.0005 | 0 | 0.001 |
| mirai/ack | 1 | 0 | 1 | 0 | 1 |
| mirai/scan | 0 | 0 | 0 | 0 | 1 |
| mirai/syn | 0.001 | 0 | 0.6975 | 0 | 1 |
| mirai/udp | 1 | 0 | 1 | 0 | 1 |
| mirai/udpplain | 1 | 0 | 1 | 0 | 1 |
