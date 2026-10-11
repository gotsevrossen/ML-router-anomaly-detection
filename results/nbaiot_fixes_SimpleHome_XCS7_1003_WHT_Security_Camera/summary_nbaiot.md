# nbaiot_fixes_SimpleHome_XCS7_1003_WHT_Security_Camera

Rows: {'benign': 19528, 'bootstrap': 9764, 'validation': 3905, 'test_benign': 5859, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window |
|---|---|---|---|---|---|---|---|---|---|
| iforest | 0.2034 | 0.0659 | 0.7946 | 0.9697 | 0.7241 | 0.000512 | 0.1772 | 0.5096 | 0.02874 |
| iforest_headroom | 0.304 | 0.1988 | 0.8057 | 0.956 | 0.67 | 0.000512 | 0.2201 | 0.3904 | 0.0854 |
| iforest_extended | 0.7995 | 0.7994 | 0.9587 | 0.9957 | 0.6734 | 0.0003414 | 0.7995 | 0.6016 | 1.086 |
| mad | 0 | 0 | 0.4975 | 0.5561 | 0.9948 | 0.0003414 | 0 | 0.2291 | 0.01924 |
| mad_tail | 0.7995 | 0.7994 | 0.9536 | 0.9951 | 0.6664 | 0.000512 | 0.7995 | 0.2616 | 0.02118 |
| hst | 0.7693 | 0.0695 | 0.8829 | 0.9696 | 0.8729 | 0.0003414 | 0.4924 | 2.878 | 0.1248 |
| autoencoder | 0.7991 | 0.7966 | 0.9603 | 0.9958 | 0.02403 | 0.0001707 | 0.7969 | 4.344 | 0.02687 |

## Detection rate at tau, per attack

| attack | iforest | iforest_headroom | iforest_extended | mad | mad_tail | hst | autoencoder |
|---|---|---|---|---|---|---|---|
| gafgyt/combo | 0.0005 | 0.0005 | 0.9985 | 0 | 0.9985 | 0.991 | 0.998 |
| gafgyt/junk | 0.0025 | 0.019 | 1 | 0 | 1 | 0.9935 | 1 |
| gafgyt/scan | 0.003 | 0.0015 | 0.998 | 0 | 0.998 | 0.248 | 0.973 |
| gafgyt/tcp | 0 | 0 | 0.0005 | 0 | 0.0005 | 0 | 0 |
| gafgyt/udp | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| mirai/ack | 0.5355 | 0.7315 | 0.9995 | 0 | 0.9995 | 0.6375 | 0.999 |
| mirai/scan | 0 | 0 | 0.999 | 0 | 0.999 | 0.0005 | 0.9995 |
| mirai/syn | 0 | 0 | 1 | 0 | 1 | 0.7715 | 1 |
| mirai/udp | 0.5385 | 0.756 | 1 | 0 | 1 | 0.5895 | 1 |
| mirai/udpplain | 0.692 | 0.6925 | 0.9995 | 0 | 0.9995 | 0.692 | 0.9995 |
