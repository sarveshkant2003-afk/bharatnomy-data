# Forest cover by district, 2023

Forest cover by canopy density for 750 districts, plus a `State total` row per state. Forest cover = land of 1 ha or more with tree canopy density of at least 10%.

## Source

- **Data:** Forest Survey of India (FSI), MoEFCC, *India State of Forest Report 2023*, Volume II, Table 10.x.3 of each state chapter
- **Link:** https://fsi.nic.in/forest-report-2023
- **Downloaded:** 19 Oct 2026
- **Original file:** [`_sources/fsi-isfr/raw/`](../_sources/fsi-isfr/raw/)

## Columns

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
