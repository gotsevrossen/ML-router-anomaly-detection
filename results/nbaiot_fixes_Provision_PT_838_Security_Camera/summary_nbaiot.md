# nbaiot_fixes_Provision_PT_838_Security_Camera

Rows: {'benign': 98514, 'bootstrap': 49257, 'validation': 19702, 'test_benign': 29555, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window |
|---|---|---|---|---|---|---|---|---|---|
| iforest | 0.1599 | 5e-05 | 0.6197 | 0.6386 | 0.6661 | 0.0006767 | 0.1588 | 1.464 | 0.02459 |
| iforest_headroom | 0.2947 | 0.0374 | 0.6636 | 0.857 | 0.5992 | 0.0006429 | 0.2805 | 1.261 | 0.07067 |
| iforest_extended | 0.7998 | 0.7931 | 0.9822 | 0.9981 | 0.6605 | 0.0005075 | 0.7997 | 1.423 | 1.344 |
| mad | 0 | 0 | 0.4975 | 0.4737 | 0.9978 | 0.0009812 | 0 | 1.272 | 0.02119 |
| mad_tail | 0.7998 | 0.7933 | 0.9846 | 0.9984 | 0.7315 | 0.000609 | 0.7998 | 1.519 | 0.02848 |
| hst | 0.03365 | 0.03365 | 0.6474 | 0.8224 | 0.9282 | 0.0008797 | 0.03365 | 10.65 | 0.1753 |
| autoencoder | 0.7997 | 0.0001 | 0.9024 | 0.9898 | 0.01458 | 0.0005075 | 0.7997 | 10.19 | 0.03002 |

## Detection rate at tau, per attack

| attack | iforest | iforest_headroom | iforest_extended | mad | mad_tail | hst | autoencoder |
|---|---|---|---|---|---|---|---|
| gafgyt/combo | 0.0015 | 0.0015 | 0.9995 | 0 | 1 | 0.0005 | 0.9995 |
| gafgyt/junk | 0.0015 | 0.0025 | 1 | 0 | 1 | 0 | 1 |
| gafgyt/scan | 0.001 | 0.002 | 0.999 | 0 | 0.999 | 0 | 0.999 |
| gafgyt/tcp | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| gafgyt/udp | 0 | 0 | 0.0005 | 0 | 0.0005 | 0 | 0 |
| mirai/ack | 0.528 | 0.877 | 0.9985 | 0 | 0.9985 | 0 | 0.9985 |
| mirai/scan | 0 | 0 | 1 | 0 | 1 | 0 | 1 |
| mirai/syn | 0 | 0 | 1 | 0 | 1 | 0 | 1 |
| mirai/udp | 0.573 | 0.978 | 1 | 0 | 1 | 0 | 1 |
| mirai/udpplain | 0.4825 | 0.944 | 1 | 0 | 1 | 0.336 | 1 |
