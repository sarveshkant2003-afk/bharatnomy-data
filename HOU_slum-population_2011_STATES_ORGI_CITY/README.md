# Slum population by town, 2011

Primary Census Abstract for the slum areas of every town that reported slums in Census 2011: households, population, SC/ST, literacy and workers by category.

## Source

- **Data:** Office of the Registrar General & Census Commissioner, India (ORGI), Census of India 2011
- **Table taken from:** "PCA SLUM: Primary census abstract data for slum, India & States/UTs - Town Level - 2011", file `slum_data_census_2011.xls`
- **Link:** https://censusindia.gov.in/nada/index.php/catalog/6190
- **Downloaded:** 28 Oct 2026
- **Original file:** [`_sources/orgi-census2011/raw/`](../_sources/orgi-census2011/raw/)

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or UT as it was in 2011 |
| `city` | Town as spelled by the Census, with its civic status, e.g. `Nagpur (M Corp.)`. `State total` = the state's published total of slum population; blank on the `All India` row |
| `state_census_code`, `town_census_code` | Census 2011 codes (Nagpur M Corp. = 802710) |
| `households` ... `non_workers_*` | Same columns as `POP_census-pca_2011_STATES_ORGI_DIST`, for the slum population only |

## Notes

- The source has no district column; join to districts through the town code if needed.
- Slum population as a share of the city needs the town's total population, which is in the PCA town tables (not in this repo yet).
