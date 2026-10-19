# Net irrigated area by state, 2004-05 to 2020-21

Net irrigated area is the land irrigated from any source in a year, counting land irrigated more than once only once.
With net sown area from `land-use/` it gives the irrigated vs rain-fed split: rain-fed area = net sown area - net irrigated area.

## Source

- **Data:** *Land Use Statistics at a Glance*, Ministry of Agriculture and Farmers' Welfare (MoA&FW)
- **Table taken from:** RBI, *Handbook of Statistics on Indian States 2022-23*, Table 58 "State-wise Pattern of Land Use - Net Irrigated Area" (published 15 Nov 2023)
- **Link:** https://www.rbi.org.in/Scripts/PublicationsView.aspx?id=22122
- **Downloaded:** 19 Oct 2026

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or Union Territory. `All India` = national total |
| `year` | Agricultural year (July to June) |
| `net_irrigated_area_000_ha` | Net irrigated area, in thousand hectares |
| `source_flag` | Empty = reported value. `estimated` = from the latest Agriculture Census or estimated (`*` in source). `provisional` = `(p)` in source. `not_applicable` = state did not exist (`.` in source) |

## Notes

- Where the source marks a whole state row with `*` (Maharashtra, Manipur, Sikkim, West Bengal), every year from 2012-13 is flagged `estimated`.
- Same states and years as `land-use/`, so the two files join on `state_ut` + `year`.
- All India includes UTs that are not listed as separate rows, so the listed states will not add up to it.
