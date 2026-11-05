# Forest and tree cover by state, 2023

Forest cover and tree cover (tree patches under 1 ha outside forests) per state, from the India State of Forest Report 2023.

## Source

- **Data:** Forest Survey of India (FSI), MoEFCC, *India State of Forest Report 2023*
- **Table taken from:** Rajya Sabha Unstarred Question 367 (PIB, 6 Feb 2025)
- **Link:** https://www.pib.gov.in/PressReleseDetailm.aspx?PRID=2100254
- **Downloaded:** 19 Oct 2026

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or Union Territory. `All India` = national total |
| `lgd_state_code` | State/UT code in the Local Government Directory (LGD), from [`_reference/geography.csv`](../_reference/geography.csv). Blank for All India and for old units LGD no longer lists |
| `geographical_area_sq_km` | Geographical area, sq km |
| `forest_cover_sq_km` | Forest cover, sq km |
| `tree_cover_sq_km` | Tree patches under 1 ha outside forests, sq km |
| `forest_and_tree_cover_sq_km` | Forest cover + tree cover, sq km |

## Notes

- Ladakh's area is blank; the source puts the combined figure on the Jammu & Kashmir row.
- `lgd_state_code` added on 5 Nov 2026 from the LGD directory (see [`_reference/README.md`](../_reference/README.md)). LGD codes identify today's state or district; for years before a split (Telangana 2014, Ladakh 2019, new districts) the same code covers a larger area than it does now.
