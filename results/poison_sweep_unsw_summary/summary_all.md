# poison_sweep_unsw (all)

Window FNR on the final attack, by number of chaff days before it (d0 = no chaff):

| device | variant | rule | d0 | d1 | d3 | d4 | d7 | d8 | d12 | d14 | d15 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| samsung_camera | beh_s02_a30 | frozen | 0.096 | nan | nan | 0.1 | nan | 0.1 | 0.096 | nan | 0.096 |
| samsung_camera | beh_s02_a30 | full | 0.096 | nan | nan | 0.1 | nan | 0.1 | 0.096 | nan | 0.096 |
| samsung_camera | beh_s02_a30 | gated | 0.096 | nan | nan | 0.1 | nan | 0.1 | 0.1 | nan | 0.096 |
| samsung_camera | beh_s02_a30 | naive | 0.896 | nan | nan | 0.858 | nan | 0.8 | 0.958 | nan | 0.962 |
| samsung_camera | beh_s50_a05 | frozen | 0.096 | 0.1 | 0.096 | nan | 0.1 | nan | nan | 0.1 | nan |
| samsung_camera | beh_s50_a05 | full | 0.096 | 0.1 | 0.096 | nan | 0.1 | nan | nan | 0.1 | nan |
| samsung_camera | beh_s50_a05 | gated | 0.096 | 0.1 | 0.096 | nan | 0.1 | nan | nan | 0.1 | nan |
| samsung_camera | beh_s50_a05 | naive | 0.896 | 0.712 | 0.888 | nan | 1 | nan | nan | 1 | nan |
| samsung_camera | vol_s02_a30 | frozen | 0.958 | nan | nan | 1 | nan | 1 | 0.958 | nan | 0.958 |
| samsung_camera | vol_s02_a30 | full | 0.958 | nan | nan | 1 | nan | 1 | 0.958 | nan | 0.958 |
| samsung_camera | vol_s02_a30 | gated | 0.958 | nan | nan | 1 | nan | 1 | 1 | nan | 1 |
| samsung_camera | vol_s02_a30 | naive | 0.996 | nan | nan | 1 | nan | 1 | 0.996 | nan | 0.996 |
| samsung_camera | vol_s50_a05 | frozen | 0.958 | 1 | 0.958 | nan | 1 | nan | nan | 1 | nan |
| samsung_camera | vol_s50_a05 | full | 0.958 | 1 | 0.958 | nan | 1 | nan | nan | 1 | nan |
| samsung_camera | vol_s50_a05 | gated | 0.958 | 1 | 1 | nan | 1 | nan | nan | 1 | nan |
| samsung_camera | vol_s50_a05 | naive | 0.996 | 1 | 1 | nan | 1 | nan | nan | 1 | nan |
| tplink_plug | beh_s02_a30 | frozen | 0.1 | nan | nan | 0.1 | nan | 0.1 | 0.1 | nan | 0.1 |
| tplink_plug | beh_s02_a30 | full | 0.1 | nan | nan | 0.1 | nan | 0.1 | 0.1 | nan | 0.1 |
| tplink_plug | beh_s02_a30 | gated | 0.1 | nan | nan | 0.1 | nan | 0.1 | 0.1 | nan | 0.1 |
| tplink_plug | beh_s02_a30 | naive | 1 | nan | nan | 0.992 | nan | 1 | 1 | nan | 1 |
| tplink_plug | beh_s50_a05 | frozen | 0.1 | 0.1 | 0.1 | nan | 0.1 | nan | nan | 0.1 | nan |
| tplink_plug | beh_s50_a05 | full | 0.1 | 0.1 | 0.1 | nan | 0.1 | nan | nan | 0.1 | nan |
| tplink_plug | beh_s50_a05 | gated | 0.1 | 0.1 | 0.1 | nan | 0.1 | nan | nan | 0.096 | nan |
| tplink_plug | beh_s50_a05 | naive | 1 | 0.983 | 1 | nan | 0.992 | nan | nan | 1 | nan |
| tplink_plug | vol_s02_a30 | frozen | 0.1 | nan | nan | 0.1 | nan | 0.1 | 0.1 | nan | 0.1 |
| tplink_plug | vol_s02_a30 | full | 0.1 | nan | nan | 0.1 | nan | 0.1 | 0.1 | nan | 0.1 |
| tplink_plug | vol_s02_a30 | gated | 0.1 | nan | nan | 0.1 | nan | 0.1 | 0.1 | nan | 0.1 |
| tplink_plug | vol_s02_a30 | naive | 1 | nan | nan | 0.983 | nan | 1 | 1 | nan | 1 |
| tplink_plug | vol_s50_a05 | frozen | 0.1 | 0.1 | 0.1 | nan | 0.1 | nan | nan | 0.1 | nan |
| tplink_plug | vol_s50_a05 | full | 0.1 | 0.1 | 0.1 | nan | 0.1 | nan | nan | 0.1 | nan |
| tplink_plug | vol_s50_a05 | gated | 0.1 | 0.1 | 0.1 | nan | 0.1 | nan | nan | 0.096 | nan |
| tplink_plug | vol_s50_a05 | naive | 1 | 0.983 | 1 | nan | 0.983 | nan | nan | 1 | nan |

Window FNR reaching 50% (day = first sampled launch day; the crossing lies in (prev_day, day]):

| device | variant | rule | status | day | prev_day | chaff_packets | chaff_frac | fnr_at_0 |
|---|---|---|---|---|---|---|---|---|
| samsung_camera | beh_s02_a30 | frozen | not_reached | nan | nan | nan | nan | 0.0958 |
| samsung_camera | beh_s02_a30 | full | not_reached | nan | nan | nan | nan | 0.0958 |
| samsung_camera | beh_s02_a30 | gated | not_reached | nan | nan | nan | nan | 0.0958 |
| samsung_camera | beh_s02_a30 | naive | baseline | nan | nan | nan | nan | 0.8958 |
| samsung_camera | beh_s50_a05 | frozen | not_reached | nan | nan | nan | nan | 0.0958 |
| samsung_camera | beh_s50_a05 | full | not_reached | nan | nan | nan | nan | 0.0958 |
| samsung_camera | beh_s50_a05 | gated | not_reached | nan | nan | nan | nan | 0.0958 |
| samsung_camera | beh_s50_a05 | naive | baseline | nan | nan | nan | nan | 0.8958 |
| samsung_camera | vol_s02_a30 | frozen | baseline | nan | nan | nan | nan | 0.9583 |
| samsung_camera | vol_s02_a30 | full | baseline | nan | nan | nan | nan | 0.9583 |
| samsung_camera | vol_s02_a30 | gated | baseline | nan | nan | nan | nan | 0.9583 |
| samsung_camera | vol_s02_a30 | naive | baseline | nan | nan | nan | nan | 0.9958 |
| samsung_camera | vol_s50_a05 | frozen | baseline | nan | nan | nan | nan | 0.9583 |
| samsung_camera | vol_s50_a05 | full | baseline | nan | nan | nan | nan | 0.9583 |
| samsung_camera | vol_s50_a05 | gated | baseline | nan | nan | nan | nan | 0.9583 |
| samsung_camera | vol_s50_a05 | naive | baseline | nan | nan | nan | nan | 0.9958 |
| tplink_plug | beh_s02_a30 | frozen | not_reached | nan | nan | nan | nan | 0.1 |
| tplink_plug | beh_s02_a30 | full | not_reached | nan | nan | nan | nan | 0.1 |
| tplink_plug | beh_s02_a30 | gated | not_reached | nan | nan | nan | nan | 0.1 |
| tplink_plug | beh_s02_a30 | naive | baseline | nan | nan | nan | nan | 1 |
| tplink_plug | beh_s50_a05 | frozen | not_reached | nan | nan | nan | nan | 0.1 |
| tplink_plug | beh_s50_a05 | full | not_reached | nan | nan | nan | nan | 0.1 |
| tplink_plug | beh_s50_a05 | gated | not_reached | nan | nan | nan | nan | 0.1 |
| tplink_plug | beh_s50_a05 | naive | baseline | nan | nan | nan | nan | 1 |
| tplink_plug | vol_s02_a30 | frozen | not_reached | nan | nan | nan | nan | 0.1 |
| tplink_plug | vol_s02_a30 | full | not_reached | nan | nan | nan | nan | 0.1 |
| tplink_plug | vol_s02_a30 | gated | not_reached | nan | nan | nan | nan | 0.1 |
| tplink_plug | vol_s02_a30 | naive | baseline | nan | nan | nan | nan | 1 |
| tplink_plug | vol_s50_a05 | frozen | not_reached | nan | nan | nan | nan | 0.1 |
| tplink_plug | vol_s50_a05 | full | not_reached | nan | nan | nan | nan | 0.1 |
| tplink_plug | vol_s50_a05 | gated | not_reached | nan | nan | nan | nan | 0.1 |
| tplink_plug | vol_s50_a05 | naive | baseline | nan | nan | nan | nan | 1 |

All levels and the event-level FNR: `crossings_all.csv`; per-run values: `curves_all.csv`.
