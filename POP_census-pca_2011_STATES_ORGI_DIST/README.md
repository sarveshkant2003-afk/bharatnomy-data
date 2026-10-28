# Primary Census Abstract by district, 2011

Population, households, literacy, Scheduled Castes and Tribes, and workers by category (cultivators, agricultural labourers, household industry, other workers; main and marginal) for every district of India in Census 2011, each split into total, rural and urban.

## Source

- **Data:** Office of the Registrar General & Census Commissioner, India (ORGI), Census of India 2011, Primary Census Abstract (PCA)
- **Table taken from:** "PCA SD: Primary census abstract (PCA) data, India & States/UTs - State and district level - 2011", file `DDW_PCA0000_2011_Indiastatedist.xlsx`
- **Link:** https://censusindia.gov.in/nada/index.php/catalog/6191
- **Downloaded:** 28 Oct 2026
- **Original file:** [`_sources/orgi-census2011/raw/`](../_sources/orgi-census2011/raw/)

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or UT as it was in 2011 (Andhra Pradesh includes Telangana; Jammu & Kashmir includes Ladakh; Dadra & Nagar Haveli and Daman & Diu are separate) |
| `district` | District as spelled by the Census. `State total` = the state's published total; blank on the `All India` row |
| `state_census_code`, `district_census_code` | Census 2011 codes (Nagpur = 27 / 505) |
| `area` | `total`, `rural` or `urban` |
| `households` | Number of households |
| `population_*`, `population_age_0_6_*` | Population, all ages and age 0-6 |
| `scheduled_castes_*`, `scheduled_tribes_*` | SC and ST population |
| `literates_*`, `illiterates_*` | Literate and illiterate population |
| `total_workers_*` | Main + marginal workers |
| `main_workers_*` | Worked 6 months or more in the year. Split into `main_cultivators_*`, `main_agricultural_labourers_*`, `main_household_industry_workers_*`, `main_other_workers_*` |
| `marginal_workers_*` | Worked less than 6 months, with the same four categories (`marginal_cultivators_*` ...) and split by duration: `..._3_to_6_months_*` and `..._less_than_3_months_*` |
| `non_workers_*` | Did not work in the year |

Every count has three columns: `_persons`, `_males`, `_females`.

## Notes

- Workers by category are the Census's closest measure of outdoor work: cultivators and agricultural labourers work outdoors; "other workers" mixes indoor and outdoor jobs (construction, transport, street vending are inside it). For job-level detail on Nagpur see `LAB_plfs-persons-nagpur_2025_MH_MOSPI_DIST`.
- Districts are the 640 districts of 2011. Later splits are not reflected.
