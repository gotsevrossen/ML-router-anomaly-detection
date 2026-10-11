# nbaiot_fixes_Ennio_Doorbell

Rows: {'benign': 39100, 'bootstrap': 19550, 'validation': 7820, 'test_benign': 11730, 'test_attack': 10000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window |
|---|---|---|---|---|---|---|---|---|---|
| iforest | 0.0011 | 0.0009 | 0.4986 | 0.9054 | 0.671 | 0.003581 | 0.0013 | 1.01 | 0.04336 |
| iforest_headroom | 0.0013 | 0.001 | 0.5593 | 0.9173 | 0.6593 | 0.000682 | 0.001 | 0.8606 | 0.1321 |
| iforest_extended | 0.5998 | 0 | 0.785 | 0.9583 | 0.6526 | 0.0007673 | 0.5998 | 1.766 | 1.609 |
| mad | 0.0003 | 0 | 0.4977 | 0.5237 | 0.9985 | 0.001023 | 0.0003 | 0.5711 | 0.02599 |
| mad_tail | 0.5998 | 0 | 0.7849 | 0.8074 | 0.6963 | 0.0009378 | 0.5998 | 0.6625 | 0.02405 |
| hst | 0.0013 | 0.0012 | 0.6619 | 0.9237 | 0.8824 | 0.003751 | 0.4003 | 4.546 | 0.1881 |
| autoencoder | 0.5871 | 0.5776 | 0.7972 | 0.9705 | 0.03451 | 0.000682 | 0.5864 | 7.275 | 0.03318 |

## Detection rate at tau, per attack

| attack | iforest | iforest_headroom | iforest_extended | mad | mad_tail | hst | autoencoder |
|---|---|---|---|---|---|---|---|
| gafgyt/combo | 0 | 0 | 0.9995 | 0 | 0.9995 | 0.996 | 0.9995 |
| gafgyt/junk | 0.0015 | 0.001 | 1 | 0 | 1 | 0.9985 | 1 |
| gafgyt/scan | 0.004 | 0.0025 | 0.998 | 0.0015 | 0.998 | 0.0055 | 0.931 |
| gafgyt/tcp | 0.0005 | 0.001 | 0.001 | 0 | 0.001 | 0.001 | 0.001 |
| gafgyt/udp | 0.0005 | 0.0005 | 0.0005 | 0 | 0.0005 | 0.0005 | 0.0005 |
