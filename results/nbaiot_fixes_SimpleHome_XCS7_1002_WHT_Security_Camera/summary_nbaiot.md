# nbaiot_fixes_SimpleHome_XCS7_1002_WHT_Security_Camera

Rows: {'benign': 46585, 'bootstrap': 23292, 'validation': 9317, 'test_benign': 13976, 'test_attack': 20000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window |
|---|---|---|---|---|---|---|---|---|---|
| iforest | 0.2166 | 0.1832 | 0.6146 | 0.7774 | 0.6795 | 0.0002147 | 0.2133 | 0.6852 | 0.0299 |
| iforest_headroom | 0.218 | 0.2165 | 0.6271 | 0.8027 | 0.615 | 0.0005724 | 0.2173 | 0.732 | 0.08261 |
| iforest_extended | 0.7968 | 0.7797 | 0.8982 | 0.96 | 0.7135 | 0 | 0.7583 | 0.9897 | 1.126 |
| mad | 0 | 0 | 0.4975 | 0.4737 | 0.9985 | 0.0002862 | 0 | 0.6372 | 0.01905 |
| mad_tail | 0.7975 | 0.7833 | 0.8983 | 0.981 | 0.7161 | 0 | 0.7804 | 0.5888 | 0.02018 |
| hst | 0.0764 | 0.0764 | 0.5669 | 0.8079 | 0.9023 | 0.0007871 | 0.0764 | 4.765 | 0.1657 |
| autoencoder | 0.7304 | 0.7175 | 0.8859 | 0.9572 | 0.02125 | 0.004293 | 0.7836 | 6.445 | 0.03349 |

## Detection rate at tau, per attack

| attack | iforest | iforest_headroom | iforest_extended | mad | mad_tail | hst | autoencoder |
|---|---|---|---|---|---|---|---|
| gafgyt/combo | 0.0005 | 0.001 | 1 | 0 | 1 | 0.0005 | 1 |
| gafgyt/junk | 0.0015 | 0.002 | 1 | 0 | 0.947 | 0.0015 | 1 |
| gafgyt/scan | 0 | 0.0005 | 0.782 | 0 | 0.9585 | 0 | 0.854 |
| gafgyt/tcp | 0 | 0 | 0.0005 | 0 | 0.0005 | 0 | 0.0005 |
| gafgyt/udp | 0 | 0 | 0 | 0 | 0 | 0 | 0.0005 |
| mirai/ack | 0.7205 | 0.746 | 0.9995 | 0 | 0.9995 | 0.071 | 1 |
| mirai/scan | 0 | 0 | 0.802 | 0 | 0.899 | 0 | 0.981 |
| mirai/syn | 0 | 0 | 1 | 0 | 1 | 0 | 1 |
| mirai/udp | 0.723 | 0.7335 | 1 | 0 | 1 | 0.0865 | 1 |
| mirai/udpplain | 0.6875 | 0.6905 | 0.9995 | 0 | 0.9995 | 0.6045 | 1 |
