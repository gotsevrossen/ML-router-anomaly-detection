## detection_rate@tau

| device | iforest | iforest_headroom | iforest_extended | mad | mad_tail | hst | autoencoder |
|---|---|---|---|---|---|---|---|
| Ecobee_Thermostat | 0.00035 | 0.09945 | 0.8001 | 0 | 0.8001 | 0.7983 | 1 |
| Ennio_Doorbell | 0.0013 | 0.001 | 0.5998 | 0.0003 | 0.5998 | 0.4003 | 0.5864 |
| Philips_B120N10_Baby_Monitor | 0 | 0 | 0.7998 | 0 | 0.9995 | 0 | 0.7995 |
| Provision_PT_737E_Security_Camera | 0.00035 | 0.1433 | 0.8002 | 0 | 0.7995 | 0.04085 | 0.8002 |
| Provision_PT_838_Security_Camera | 0.1588 | 0.2805 | 0.7997 | 0 | 0.7998 | 0.03365 | 0.7997 |
| Samsung_SNH_1011_N_Webcam | 0 | 0 | 0.5998 | 0 | 0.5998 | 0.0005 | 0.5635 |
| SimpleHome_XCS7_1002_WHT_Security_Camera | 0.2133 | 0.2173 | 0.7583 | 0 | 0.7804 | 0.0764 | 0.7836 |
| SimpleHome_XCS7_1003_WHT_Security_Camera | 0.1772 | 0.2201 | 0.7995 | 0 | 0.7995 | 0.4924 | 0.7969 |
| dev(Danmini_Doorbell) | 0 | 0.00145 | 0.3025 | 0.0016 | 0.753 | 0.3362 | 0.5764 |
| mean (held-out) | 0.06891 | 0.1202 | 0.7447 | 3.75e-05 | 0.7723 | 0.2303 | 0.7662 |
| median (held-out) | 0.000825 | 0.1214 | 0.7996 | 0 | 0.7995 | 0.05862 | 0.7982 |

## test_fpr@tau

| device | iforest | iforest_headroom | iforest_extended | mad | mad_tail | hst | autoencoder |
|---|---|---|---|---|---|---|---|
| Ecobee_Thermostat | 0.001017 | 0.001271 | 0.003812 | 0.001525 | 0.005845 | 0.002541 | 0.005083 |
| Ennio_Doorbell | 0.003581 | 0.000682 | 0.0007673 | 0.001023 | 0.0009378 | 0.003751 | 0.000682 |
| Philips_B120N10_Baby_Monitor | 0.0006848 | 0.0006277 | 0.0007418 | 0.0006467 | 0.000875 | 0.0006848 | 0.0008369 |
| Provision_PT_737E_Security_Camera | 0.0009653 | 0.001019 | 0.0008044 | 0.000858 | 0.0008044 | 0.002145 | 0.0009117 |
| Provision_PT_838_Security_Camera | 0.0006767 | 0.0006429 | 0.0005075 | 0.0009812 | 0.000609 | 0.0008797 | 0.0005075 |
| Samsung_SNH_1011_N_Webcam | 0.0005113 | 0.0003835 | 0.0001918 | 0.0005113 | 0.0003196 | 6.392e-05 | 0.0002557 |
| SimpleHome_XCS7_1002_WHT_Security_Camera | 0.0002147 | 0.0005724 | 0 | 0.0002862 | 0 | 0.0007871 | 0.004293 |
| SimpleHome_XCS7_1003_WHT_Security_Camera | 0.000512 | 0.000512 | 0.0003414 | 0.0003414 | 0.000512 | 0.0003414 | 0.0001707 |
| dev(Danmini_Doorbell) | 0.00074 | 0.0009418 | 0.0008745 | 0.001009 | 0.0009418 | 0.0009418 | 0.0009418 |
| mean (held-out) | 0.00102 | 0.0007138 | 0.0008958 | 0.0007716 | 0.001238 | 0.001399 | 0.001593 |
| median (held-out) | 0.0006807 | 0.0006353 | 0.0006247 | 0.0007524 | 0.0007067 | 0.0008334 | 0.0007595 |

## tpr@fpr=0.001

| device | iforest | iforest_headroom | iforest_extended | mad | mad_tail | hst | autoencoder |
|---|---|---|---|---|---|---|---|
| Ecobee_Thermostat | 0.00035 | 0.0035 | 0.7999 | 0 | 0.8 | 0.7966 | 0.8001 |
| Ennio_Doorbell | 0.0011 | 0.0013 | 0.5998 | 0.0003 | 0.5998 | 0.0013 | 0.5871 |
| Philips_B120N10_Baby_Monitor | 0 | 0 | 0.7998 | 0 | 0.9995 | 0 | 0.7997 |
| Provision_PT_737E_Security_Camera | 0.00125 | 0.1433 | 0.8002 | 0 | 0.7998 | 0.04085 | 0.8002 |
| Provision_PT_838_Security_Camera | 0.1599 | 0.2947 | 0.7998 | 0 | 0.7998 | 0.03365 | 0.7997 |
| Samsung_SNH_1011_N_Webcam | 0 | 0 | 0.5998 | 0.0003 | 0.5998 | 0.1627 | 0.5881 |
| SimpleHome_XCS7_1002_WHT_Security_Camera | 0.2166 | 0.218 | 0.7968 | 0 | 0.7975 | 0.0764 | 0.7304 |
| SimpleHome_XCS7_1003_WHT_Security_Camera | 0.2034 | 0.304 | 0.7995 | 0 | 0.7995 | 0.7693 | 0.7991 |
| dev(Danmini_Doorbell) | 0 | 0.00145 | 0.6053 | 0.0016 | 0.7574 | 0.3382 | 0.5773 |
| mean (held-out) | 0.07283 | 0.1206 | 0.7495 | 7.5e-05 | 0.7745 | 0.2351 | 0.7381 |
| median (held-out) | 0.001175 | 0.0734 | 0.7997 | 0 | 0.7996 | 0.05862 | 0.7994 |

