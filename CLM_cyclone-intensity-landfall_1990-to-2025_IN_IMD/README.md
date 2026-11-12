# Cyclone intensity and landfall, North Indian Ocean, 1990 to 2025

One row per cyclone: peak intensity, where and when it crossed the coast, wind and pressure at landfall, and storm surge, as described by IMD. Most cells are text, as published.

## Source

- **Data:** India Meteorological Department (IMD), RSMC New Delhi, cyclone climatology: "Intensity (Maximum / at the time of landfall) and weather in association with Tropical Cyclones over North Indian Ocean"
- **Link:** https://rsmcnewdelhi.imd.gov.in/report.php?internal_menu=MzM= (file `tcintensity.xls`, sheet "TC DATA")
- **Downloaded:** 12 Nov 2026 (original in [`_sources/imd-rsmc/raw/`](../_sources/imd-rsmc/raw/))
- **Script:** [`pipelines/imd-rsmc/build_cyclone_climatology.py`](../pipelines/imd-rsmc/build_cyclone_climatology.py)

## Columns

| Column | Meaning |
|---|---|
| `year` | Year |
| `basin` | Bay of Bengal or Arabian Sea |
| `cyclone` | Category, name and dates, as printed |
| `max_wind_intensity` | Maximum sustained wind reached (text with unit, mostly knots) |
| `max_wind_duration` | When the maximum wind occurred (text) |
| `lowest_central_pressure_and_time` | Lowest estimated central pressure and its time (text) |
| `max_pressure_drop_hpa` | Largest pressure drop at the centre, hPa (some cells carry text) |
| `landfall_max_sustained_wind` | Maximum sustained wind at landfall (text with unit; "Weakened over sea" if no landfall) |
| `landfall_central_pressure` | Central pressure at landfall (text) |
| `landfall_pressure_drop_hpa` | Pressure drop at landfall, hPa (some cells carry text) |
| `landfall_place` | Where it crossed the coast (text, e.g. "Crossed Odisha coast near Paradip") |
| `landfall_point_lat_lon` | Landfall position (text) |
| `landfall_time` | Landfall time (text) |
| `storm_surge` | Storm surge reported or estimated (text, heights in metres or cm) |

## Notes

- Values are text because the source mixes numbers, units and explanations in one cell; they are kept as printed (line breaks inside a cell kept).
- Rows that only continue the cell text of the cyclone above (no basin or name) are joined to it.
- Storms that crossed two coasts (e.g. HUDHUD 2014: Andaman Islands, then Andhra Pradesh) list both in one cell.
- Checks (12 Nov 2026): 148 cyclones, 1990-2025; no blank years.
