# Net sown area by state, 2004-05 to 2020-21

Land sown with crops in a year, counting land sown more than once only once.

## Source

- **Data:** MoA&FW, Land Use Statistics
- **Table taken from:** RBI Handbook of Statistics on Indian States 2022-23, Table 56 "State-wise Pattern of Land Use - Net Sown Area"
- **Link:** https://rbi.org.in/Scripts/PublicationsView.aspx?id=22120
- **Downloaded:** 19 Oct 2026

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or Union Territory. `All India` = national total |
| `lgd_state_code` | State/UT code in the Local Government Directory (LGD), from [`_reference/geography.csv`](../_reference/geography.csv). Blank for All India and for old units LGD no longer lists |
| `year` | Agricultural year (July to June) |
| `net_sown_area_000_ha` | Net sown area, thousand hectares |
| `source_flag` | `estimated`, `provisional`, or `not_applicable` (state did not exist) |

## Notes

- `lgd_state_code` added on 5 Nov 2026 from the LGD directory (see [`_reference/README.md`](../_reference/README.md)). LGD codes identify today's state or district; for years before a split (Telangana 2014, Ladakh 2019, new districts) the same code covers a larger area than it does now.
