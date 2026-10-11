# nbaiot_fixes_Samsung_SNH_1011_N_Webcam

Rows: {'benign': 52150, 'bootstrap': 26075, 'validation': 10430, 'test_benign': 15645, 'test_attack': 10000, 'features': 115}. Per-row metrics on N-BaIoT's 115 pre-extracted features (secondary benchmark; not our window features).

| detector | tpr@fpr=0.001 | tpr@fpr=0.0001 | pauc@0.01 | pauc@0.1 | tau | test_fpr@tau | detection_rate@tau | fit_s | score_ms_per_window |
|---|---|---|---|---|---|---|---|---|---|
| iforest | 0 | 0 | 0.4977 | 0.847 | 0.7853 | 0.0005113 | 0 | 1.16 | 0.03779 |
| iforest_headroom | 0 | 0 | 0.4978 | 0.8171 | 0.7413 | 0.0003835 | 0 | 1.018 | 0.09736 |
| iforest_extended | 0.5998 | 0.5998 | 0.7989 | 0.9737 | 0.7396 | 0.0001918 | 0.5998 | 1.325 | 1.224 |
| mad | 0.0003 | 0 | 0.5446 | 0.6027 | 0.9791 | 0.0005113 | 0 | 0.6512 | 0.02384 |
| mad_tail | 0.5998 | 0.5998 | 0.8727 | 0.9867 | 0.6926 | 0.0003196 | 0.5998 | 0.9505 | 0.02521 |
| hst | 0.1627 | 0.0006 | 0.7659 | 0.972 | 0.9341 | 6.392e-05 | 0.0005 | 6.672 | 0.2087 |
| autoencoder | 0.5881 | 0.3978 | 0.8293 | 0.9821 | 0.03679 | 0.0002557 | 0.5635 | 9.974 | 0.0389 |

## Detection rate at tau, per attack

| attack | iforest | iforest_headroom | iforest_extended | mad | mad_tail | hst | autoencoder |
|---|---|---|---|---|---|---|---|
| gafgyt/combo | 0 | 0 | 0.999 | 0 | 0.999 | 0.0015 | 0.998 |
| gafgyt/junk | 0 | 0 | 1 | 0 | 1 | 0 | 1 |
| gafgyt/scan | 0 | 0 | 1 | 0 | 1 | 0.001 | 0.8195 |
| gafgyt/tcp | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| gafgyt/udp | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
