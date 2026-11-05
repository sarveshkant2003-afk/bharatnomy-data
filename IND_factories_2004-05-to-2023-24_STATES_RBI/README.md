# Number of factories by state, 2004-05 to 2023-24

Number of factories per state, from the Annual Survey of Industries (MoSPI), as republished by RBI.

## Source

- **Data:** MoSPI, Annual Survey of Industries
- **Table taken from:** RBI Handbook of Statistics on Indian States 2024-25, Table 116 "State-wise Number of Factories"
- **Link:** https://rbi.org.in/scripts/PublicationsView.aspx?id=23565
- **Downloaded:** 19 Oct 2026

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or Union Territory. `All India` = national total |
| `lgd_state_code` | State/UT code in the Local Government Directory (LGD), from [`_reference/geography.csv`](../_reference/geography.csv). Blank for All India and for old units LGD no longer lists |
| `year` | Financial year |
| `factories` | Number of factories |
| `source_flag` | `not_applicable` = state/UT not separate that year; `not_available` = not covered |

## Notes

- `lgd_state_code` added on 5 Nov 2026 from the LGD directory (see [`_reference/README.md`](../_reference/README.md)). LGD codes identify today's state or district; for years before a split (Telangana 2014, Ladakh 2019, new districts) the same code covers a larger area than it does now.
