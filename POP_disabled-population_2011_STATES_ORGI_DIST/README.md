# Disabled population by type of disability, age and sex, India, states and districts, 2011

Number of people with a disability, by type (seeing, hearing, speech, movement, mental retardation, mental illness, any other, multiple), age group and sex, for total, rural and urban areas of every district, state and India, from Census 2011.

## Source

- **Data:** Office of the Registrar General & Census Commissioner, India (ORGI), Census of India 2011, Table C-20 "Disabled population by type of disability, age and sex"
- **Link:** https://censusindia.gov.in/nada/index.php/catalog (one file per state/UT plus India; catalog ids in [`_sources/orgi-census2011/raw/orgi-census2011_c20-catalog-ids_2011.tsv`](../_sources/orgi-census2011/raw/orgi-census2011_c20-catalog-ids_2011.tsv))
- **Downloaded:** 12 Nov 2026 (originals in [`_sources/orgi-census2011/raw/c20/`](../_sources/orgi-census2011/raw/c20/))
- **Scripts:** [`pipelines/orgi-census2011/fetch_c20.sh`](../pipelines/orgi-census2011/fetch_c20.sh), [`pipelines/orgi-census2011/build_c20.py`](../pipelines/orgi-census2011/build_c20.py)

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or UT as in 2011 (`Dadra & Nagar Haveli` and `Daman & Diu` separately); `All India` |
| `lgd_state_code` | State/UT code in the Local Government Directory (LGD), from [`_reference/geography.csv`](../_reference/geography.csv); blank for All India and the two pre-2020 UTs |
| `state_census_code` | Census 2011 state code (`00` = India) |
| `district` | District (today's name from [`_reference/geography.csv`](../_reference/geography.csv), 2011 boundary); `State total`; `All India` |
| `lgd_district_code` | District code in the LGD; blank for totals and for Mahe and Yanam |
| `district_census_code` | Census 2011 district code; blank for state and India rows |
| `census2011_name` | Area name as printed in the table |
| `area` | `total`, `rural` or `urban` |
| `age_group` | `Total`, `0-4`, `5-9`, `10-19`, then 10-year groups to `80-89`, `90+`, `Age Not Stated` |
| `disabled_total_persons`, `_males`, `_females` | All disabled persons |
| `disabled_seeing_*`, `disabled_hearing_*`, `disabled_speech_*`, `disabled_movement_*` | Disabled in seeing, hearing, speech, movement |
| `disabled_mental_retardation_*`, `disabled_mental_illness_*` | Mental retardation, mental illness (Census 2011 terms) |
| `disabled_any_other_*`, `disabled_multiple_*` | Any other disability; multiple disability |

## Notes

- Counts of persons. For a share of the population, divide by `population_persons` in [`POP_census-pca_2011_STATES_ORGI_DIST`](../POP_census-pca_2011_STATES_ORGI_DIST/) (same Census codes).
- District names are today's (LGD) for the 2011 district; `census2011_name` keeps the 2011 spelling. Districts created after 2011 (e.g. Palghar) are inside their 2011 parent.
- The C-20 tables for Scheduled Castes, Scheduled Tribes and million-plus cities are separate catalog entries and are not taken yet.
- Checks (12 Nov 2026): 26,364 rows = 676 places (India, 35 states/UTs, 640 districts) x 3 areas x 13 age groups; no duplicate keys or negatives; persons = males + females; the eight types add up to the total; age groups add up to Total; rural + urban = total; districts add up to their state; the India file's state rows equal the state files' (1,365 rows, no difference); the states add up to All India, 26,814,994.
