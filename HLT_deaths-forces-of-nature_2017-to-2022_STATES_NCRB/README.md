# Accidental deaths due to forces of nature by cause and state, 2017 to 2022

Deaths from heat/sun stroke, cold, lightning, floods, landslides and other natural causes reported by the police in each state, by sex.

## Source

- **Data:** National Crime Records Bureau (NCRB), Ministry of Home Affairs, *Accidental Deaths & Suicides in India* (ADSI)
- **Table taken from:** "Gender-wise Distribution of Accidental Deaths due to Forces of Nature (State & UT-wise)": Table 1.8 in ADSI 2017-2019, Table 1.9 in ADSI 2020-2022
- **Link:** https://www.ncrb.gov.in/accidental-deaths-suicides-in-india-table-content.html
- **Downloaded:** 28 Oct 2026
- **Original files:** [`_sources/ncrb-adsi/raw/`](../_sources/ncrb-adsi/raw/)

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or UT as in that year's report (Dadra & Nagar Haveli and Daman & Diu separate until 2019) |
| `lgd_state_code` | State/UT code in the Local Government Directory (LGD), from [`_reference/geography.csv`](../_reference/geography.csv). Blank for All India and for old units LGD no longer lists |
| `year` | Calendar year |
| `cause` | Avalanche, Exposure to Cold, Cyclone, Tornado, Tsunami, Earthquake, Epidemic, Flood, Heat/Sun Stroke, Landslide, Lightning, Torrential Rain, Forest Fire, Causes other than above, or Total |
| `deaths_male`, `deaths_female`, `deaths_transgender`, `deaths_total` | Number of deaths |
| `share_of_all_india_pct` | State's share of all-India deaths from forces of nature, % (only on `Total` rows, as published) |

## Notes

- NCRB publishes these causes by state only; its city tables (53 million-plus cities, Nagpur among them) give only the total of all natural causes, not heat stroke. Nagpur-level heat stroke counts are not published in ADSI.
- Police-recorded deaths; heat deaths are widely under-recorded.
- "Epidemic" excludes COVID-19 deaths from 2020 (footnote `@` in the source).
- The 2020 table leaves Andaman & Nicobar Islands' Epidemic cells empty without explanation; they are blank here.
- The "TOTAL (STATES)" and "TOTAL (UTs)" rows are left out; `All India` is kept.
- The table-wise listing on the NCRB site stops at 2022; the 2023 and 2024 reports were not available table-wise.
- `lgd_state_code` added on 5 Nov 2026 from the LGD directory (see [`_reference/README.md`](../_reference/README.md)). LGD codes identify today's state or district; for years before a split (Telangana 2014, Ladakh 2019, new districts) the same code covers a larger area than it does now.
