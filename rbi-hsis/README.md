# RBI Handbook of Statistics on Indian States (selected tables)

State-level series that the Reserve Bank of India republishes from the ministries that collect them.
Each file is one Handbook table. The original agency is named under each file.

## rbi-hsis_factories_state_2004-05-to-2023-24.csv

How many factories each state/UT has, year by year, as counted by the Annual Survey of Industries (ASI).
ASI mainly covers factories registered under the Factories Act, 1948.

### Source

- **Data:** Annual Survey of Industries (ASI), Ministry of Statistics and Programme Implementation (MoSPI)
- **Table taken from:** RBI, *Handbook of Statistics on Indian States 2024-25*, Table 116 "State-wise Number of Factories" (published 11 Dec 2025)
- **Link:** https://rbi.org.in/scripts/PublicationsView.aspx?id=23565
- **Downloaded:** 19 Oct 2026

### Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or Union Territory. `All India` = national total |
| `year` | ASI reference year (financial year) |
| `factories` | Number of factories (units) |
| `source_flag` | Empty = value reported. `not_applicable` = state/UT not separate that year (`.` in source). `not_available` = not covered (`-` in source) |

### Notes

- The full ASI series (all 57 indicators, by industry, back to 1992-93) is in [`../mospi-asi/`](../mospi-asi/).
- Andhra Pradesh includes Telangana up to 2011-12; the two are separate from 2012-13.
- Arunachal Pradesh is covered from 2014-15, Mizoram from 2019-20, Lakshadweep from 2023-24. Ladakh is separate from 2019-20.
- From 2020-21 the merged UT is listed as `Dadra & Nagar Haveli and Daman & Diu` (the source prints it in its Dadra & Nagar Haveli column, per its note 6). Earlier years keep the two old UTs separate.
- States add up to All India in every year except 2004-05, 2008-09 and 2021-22, where the published table is off by 1.

## rbi-hsis_net-sown-area_state_2004-05-to-2020-21.csv

Net sown area is the land sown with crops and orchards in a year, counting land sown more than once only once.
It is the standard measure of how much of a state's land is under agriculture.

### Source

- **Data:** *Land Use Statistics at a Glance*, Ministry of Agriculture and Farmers' Welfare (MoA&FW)
- **Table taken from:** RBI, *Handbook of Statistics on Indian States 2022-23*, Table 56 "State-wise Pattern of Land Use - Net Sown Area" (published 15 Nov 2023)
- **Link:** https://rbi.org.in/Scripts/PublicationsView.aspx?id=22120
- **Downloaded:** 19 Oct 2026

### Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or Union Territory. `All India` = national total |
| `year` | Agricultural year (July to June) |
| `net_sown_area_000_ha` | Net sown area, in thousand hectares |
| `source_flag` | Empty = reported value. `estimated` = from the latest Agriculture Census or estimated (`*` in source). `provisional` = `(p)` in source. `not_applicable` = state did not exist (`.` in source) |

### Notes

- The ministry's own full land-use tables (2015-16 to 2024-25 by state) are in [`../moafw-lus/`](../moafw-lus/).
- Where the source marks a whole state row with `*` (Maharashtra, Manipur, Sikkim), every year from 2012-13 is flagged `estimated`.
- Telangana appears from 2013-14; Andhra Pradesh values before that cover the undivided state.
- All India includes UTs that are not listed as separate rows, so the listed states will not add up to it.

## rbi-hsis_net-irrigated-area_state_2004-05-to-2020-21.csv

Net irrigated area is the land irrigated from any source in a year, counting land irrigated more than once only once.
With net sown area it gives the irrigated vs rain-fed split: rain-fed area = net sown area - net irrigated area.

### Source

- **Data:** *Land Use Statistics at a Glance*, Ministry of Agriculture and Farmers' Welfare (MoA&FW)
- **Table taken from:** RBI, *Handbook of Statistics on Indian States 2022-23*, Table 58 "State-wise Pattern of Land Use - Net Irrigated Area" (published 15 Nov 2023)
- **Link:** https://www.rbi.org.in/Scripts/PublicationsView.aspx?id=22122
- **Downloaded:** 19 Oct 2026

### Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or Union Territory. `All India` = national total |
| `year` | Agricultural year (July to June) |
| `net_irrigated_area_000_ha` | Net irrigated area, in thousand hectares |
| `source_flag` | Empty = reported value. `estimated` = from the latest Agriculture Census or estimated (`*` in source). `provisional` = `(p)` in source. `not_applicable` = state did not exist (`.` in source) |

### Notes

- Where the source marks a whole state row with `*` (Maharashtra, Manipur, Sikkim, West Bengal), every year from 2012-13 is flagged `estimated`.
- Same states and years as the net sown area file, so the two join on `state_ut` + `year`.
- All India includes UTs that are not listed as separate rows, so the listed states will not add up to it.
