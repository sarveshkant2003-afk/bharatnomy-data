# Number of factories by state, 2004-05 to 2023-24

How many factories each state/UT has, year by year, as counted by the Annual Survey of Industries (ASI).
ASI mainly covers factories registered under the Factories Act, 1948.

## Source

- **Data:** Annual Survey of Industries (ASI), Ministry of Statistics and Programme Implementation (MoSPI)
- **Table taken from:** RBI, *Handbook of Statistics on Indian States 2024-25*, Table 116 "State-wise Number of Factories" (published 11 Dec 2025)
- **Link:** https://rbi.org.in/scripts/PublicationsView.aspx?id=23565
- **Downloaded:** 19 Oct 2026

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or Union Territory. `All India` = national total |
| `year` | ASI reference year (financial year) |
| `factories` | Number of factories (units) |
| `source_flag` | Empty = value reported. `not_applicable` = state/UT not separate that year (`.` in source). `not_available` = not covered (`-` in source) |

## Notes

- Andhra Pradesh includes Telangana up to 2011-12; the two are separate from 2012-13.
- Arunachal Pradesh is covered from 2014-15, Mizoram from 2019-20, Lakshadweep from 2023-24. Ladakh is separate from 2019-20.
- From 2020-21 the merged UT is listed as `Dadra & Nagar Haveli and Daman & Diu` (the source prints it in its Dadra & Nagar Haveli column, per its note 6). Earlier years keep the two old UTs separate.
- States add up to All India in every year except 2004-05, 2008-09 and 2021-22, where the published table is off by 1.
