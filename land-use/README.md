# Net sown area by state, 2004-05 to 2020-21

Net sown area is the land sown with crops and orchards in a year, counting land sown more than once only once.
It is the standard measure of how much of a state's land is under agriculture.

## Source

- **Data:** *Land Use Statistics at a Glance*, Ministry of Agriculture and Farmers' Welfare (MoA&FW)
- **Table taken from:** RBI, *Handbook of Statistics on Indian States 2022-23*, Table 56 "State-wise Pattern of Land Use - Net Sown Area" (published 15 Nov 2023)
- **Link:** https://rbi.org.in/Scripts/PublicationsView.aspx?id=22120
- **Downloaded:** 19 Oct 2026

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or Union Territory. `All India` = national total |
| `year` | Agricultural year (July to June) |
| `net_sown_area_000_ha` | Net sown area, in thousand hectares |
| `source_flag` | Empty = reported value. `estimated` = from the latest Agriculture Census or estimated (`*` in source). `provisional` = `(p)` in source. `not_applicable` = state did not exist (`.` in source) |

## Notes

- Where the source marks a whole state row with `*` (Maharashtra, Manipur, Sikkim), every year from 2012-13 is flagged `estimated`.
- Telangana appears from 2013-14; Andhra Pradesh values before that cover the undivided state.
- All India includes UTs that are not listed as separate rows, so the listed states will not add up to it.
