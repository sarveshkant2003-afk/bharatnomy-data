# Population by single year of age, Maharashtra districts, 2011

Census 2011 population of each age from 0 to 99, 100+ and "age not stated", by sex and rural/urban, for Maharashtra and its 35 districts. Use it for the share of elderly people (e.g. 60+ or 65+).

## Source

- **Data:** Office of the Registrar General & Census Commissioner, India (ORGI), Census of India 2011
- **Table taken from:** "C-13: Single year age returns by residence and sex, Maharashtra - 2011", file `DDW-2700C-13.xls`
- **Link:** https://censusindia.gov.in/nada/index.php/catalog/1457
- **Downloaded:** 28 Oct 2026
- **Original file:** [`_sources/orgi-census2011/raw/`](../_sources/orgi-census2011/raw/)

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | Maharashtra |
| `district` | District as spelled by the Census. `State total` = Maharashtra's published total |
| `lgd_state_code` | State/UT code in the Local Government Directory (LGD), from [`_reference/geography.csv`](../_reference/geography.csv). Blank for All India and for old units LGD no longer lists |
| `lgd_district_code` | District code in the Local Government Directory (LGD), from [`_reference/geography.csv`](../_reference/geography.csv). Blank for totals and names that could not be matched |
| `district_census_code` | Census 2011 district code (Nagpur = 505) |
| `age` | `All ages`, `0` ... `99`, `100+`, `Age not stated` |
| `persons_total`, `males_total`, `females_total` | Population, rural + urban |
| `persons_rural` ... `females_urban` | Same, rural and urban |

## Notes

- Only Maharashtra is here; other states' C-13 tables are separate files on the same portal (catalog "C-13 ... <state> - 2011").
- `All ages` rows are the published totals; leave them out before adding ages up.
- `lgd_state_code` and `lgd_district_code` added on 5 Nov 2026 from the LGD directory (see [`_reference/README.md`](../_reference/README.md)). LGD codes identify today's state or district; for years before a split (Telangana 2014, Ladakh 2019, new districts) the same code covers a larger area than it does now.
