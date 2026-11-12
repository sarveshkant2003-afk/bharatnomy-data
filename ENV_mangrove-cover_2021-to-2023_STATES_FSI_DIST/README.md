# Mangrove cover by district, 2021 and 2023

Area under mangroves in every coastal district, by canopy density, from the 2021 and 2023 assessments of the India State of Forest Report 2023.

## Source

- **Data:** Forest Survey of India (FSI), MoEFCC, *India State of Forest Report 2023*, Volume I
- **Table taken from:** Table 3.4 "District-wise Mangrove Cover Assessment 2023" (report pages 76-98, PDF pages 130-133)
- **Link:** https://fsi.nic.in/forest-report-2023
- **Downloaded:** 19 Oct 2026 (PDF in [`_sources/fsi-isfr/raw/`](../_sources/fsi-isfr/raw/))
- **Script:** [`pipelines/fsi-isfr/build_mangrove_district.py`](../pipelines/fsi-isfr/build_mangrove_district.py)

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or Union Territory |
| `lgd_state_code` | State/UT code in the Local Government Directory (LGD), from [`_reference/geography.csv`](../_reference/geography.csv) |
| `district` | District as spelled in the report. `State total` = the report's state total |
| `lgd_district_code` | District code in the LGD, from [`_reference/geography.csv`](../_reference/geography.csv). Blank for totals and names that could not be matched |
| `year` | Assessment: `2021` (ISFR 2021, revised raster-based) or `2023` |
| `very_dense_mangrove_sq_km` | Mangrove with canopy density 70% and above, sq km |
| `moderately_dense_mangrove_sq_km` | Mangrove with canopy density 40% to 70%, sq km |
| `open_mangrove_sq_km` | Mangrove with canopy density 10% to 40%, sq km |
| `mangrove_cover_total_sq_km` | Total mangrove cover, sq km |
| `change_since_2021_sq_km` | Change in total mangrove cover from the revised 2021 assessment, sq km (2023 rows only) |
| `source_flag` | `not_applicable` on 2021 rows, where the change column does not apply |

## Notes

- The 2021 figures are FSI's revised, raster-based re-run of ISFR 2021, so they can differ from the numbers printed in ISFR 2021 itself.
- Only districts with mangroves are listed (70 districts in 12 states/UTs). Inland states have no rows.
- Districts are as the report names them (2023 boundaries). Spellings that differ from LGD (e.g. Ernakulum, Uttar Kannada, Mumbai city, Raigarh for Raigad) were matched to LGD codes by name. `North Andaman` (part of LGD's North and Middle Andaman) and `Yanam` (no LGD district code in our geography file) have no `lgd_district_code`.
- There is no All India row in this table; the national total (2021: 4,999.11; 2023: 4,991.68 sq km) is in Table 3.3 of the report and equals the sum of the state totals here.
- Checks (12 Nov 2026): 164 rows = 82 places x 2 assessments; no duplicate keys; density classes add up to the total in every row; district values add up to every state total; 2023 minus 2021 equals the published change in every row; no negative areas.
