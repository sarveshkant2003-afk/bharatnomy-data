# Cyclone rainfall, deaths and damage, North Indian Ocean, 1990 to 2025

One row per cyclone: heavy rainfall recorded, deaths and damage reported, as described by IMD. All cells are text, as published.

## Source

- **Data:** India Meteorological Department (IMD), RSMC New Delhi, cyclone climatology: "Heavy Rainfall & Loss in Association with Tropical Cyclone over North Indian Ocean"
- **Link:** https://rsmcnewdelhi.imd.gov.in/report.php?internal_menu=MzM= (file `tcintensity.xls`, sheet "TC RAINFALL")
- **Downloaded:** 12 Nov 2026 (original in [`_sources/imd-rsmc/raw/`](../_sources/imd-rsmc/raw/))
- **Script:** [`pipelines/imd-rsmc/build_cyclone_climatology.py`](../pipelines/imd-rsmc/build_cyclone_climatology.py)

## Columns

| Column | Meaning |
|---|---|
| `year` | Year |
| `year_from_tc_data` | `yes` where the year cell is blank in this sheet and was taken from the same cyclone's row in the "TC DATA" sheet (MORA and OCKHI, 2017) |
| `basin` | Bay of Bengal or Arabian Sea |
| `cyclone` | Category, name and dates, as printed |
| `heavy_rainfall` | Heavy rainfall by date and place, station amounts in cm (text) |
| `deaths` | Deaths reported, by state or country (text) |
| `damage` | Houses, crops, livestock, infrastructure damaged (text) |

## Notes

- Text kept as printed. Many older cyclones have blank `deaths` and `damage`; the source gives no reason.
- Rows that only continue the text of the cyclone above are joined to it.
- 145 cyclones here against 148 in the "TC DATA" sheet ([`CLM_cyclone-intensity-landfall_1990-to-2025_IN_IMD`](../CLM_cyclone-intensity-landfall_1990-to-2025_IN_IMD/)); the source's two sheets are not row-for-row identical.
