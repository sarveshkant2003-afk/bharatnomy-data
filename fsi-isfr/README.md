# India State of Forest Report 2023 (Forest Survey of India)

Forest cover from FSI's satellite assessment: land of 1 ha or more with tree canopy density of at least 10%.

## Source

- **Data:** Forest Survey of India (FSI), MoEFCC, *India State of Forest Report 2023*, Volumes I and II
- **Link:** https://fsi.nic.in/forest-report-2023
- **Downloaded:** 19 Oct 2026

## fsi-isfr_forest-cover_district_2023.csv

Forest cover by canopy density for 750 districts (Table 10.x.3 of each state chapter, Volume II), plus a `State total` row per state.

| Column | Meaning |
|---|---|
| `state_ut` | State or Union Territory |
| `district` | District as spelled in the report. `State total` = the state's published total |
| `geographical_area_sq_km` | District area, sq km |
| `very_dense_forest_sq_km` | Canopy density 70% and above, sq km |
| `moderately_dense_forest_sq_km` | Canopy density 40% to under 70%, sq km |
| `open_forest_sq_km` | Canopy density 10% to under 40%, sq km |
| `forest_cover_total_sq_km` | Very dense + moderately dense + open forest, sq km |
| `forest_cover_pct_of_area` | Forest cover as % of geographical area |
| `change_since_2021_sq_km` | Change in forest cover since the 2021 assessment, sq km (can be negative) |
| `scrub_sq_km` | Canopy density under 10%, sq km (not forest cover) |
| `source_marks` | `district:H` = hill district; `district:**` = marked `**` in the report (no reason given) |

## fsi-isfr_forest-tree-cover_state_2023.csv

Forest and tree cover by state, from Rajya Sabha Unstarred Q. 367 (PIB, 6 Feb 2025): https://www.pib.gov.in/PressReleseDetailm.aspx?PRID=2100254

| Column | Meaning |
|---|---|
| `state_ut` | State or Union Territory. `All India` = national total |
| `geographical_area_sq_km` | Geographical area, sq km |
| `forest_cover_sq_km` | Forest cover, sq km |
| `tree_cover_sq_km` | Tree patches under 1 ha outside forests, sq km |
| `forest_and_tree_cover_sq_km` | Forest cover + tree cover, sq km |

Ladakh's area is blank; the source puts the combined figure on the Jammu & Kashmir row.
