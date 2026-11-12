# Cyclone best tracks, North Indian Ocean, 1982 to 2026

Position and strength of every depression and cyclone over the Bay of Bengal and Arabian Sea, every 3 or 6 hours, as finalised by IMD (one row per track point).

## Source

- **Data:** India Meteorological Department (IMD), Regional Specialised Meteorological Centre (RSMC) for Tropical Cyclones, New Delhi, *Best track data of tropical cyclonic disturbances over the North Indian Ocean*
- **Link:** https://rsmcnewdelhi.imd.gov.in/report.php?internal_menu=MzM= (file "Best Tracks Data 1982-2026", xlsx)
- **Downloaded:** 12 Nov 2026 (original in [`_sources/imd-rsmc/raw/`](../_sources/imd-rsmc/raw/))
- **Script:** [`pipelines/imd-rsmc/build_best_tracks.py`](../pipelines/imd-rsmc/build_best_tracks.py)

## Columns

| Column | Meaning |
|---|---|
| `year` | Year (the sheet of the source file) |
| `serial` | Serial number of the system in that year |
| `basin` | Basin of origin as printed: `BOB` Bay of Bengal, `ARB` / `AS` Arabian Sea, `LAND` (also `Land`, `land`) formed over land |
| `name` | Cyclone name, blank for unnamed systems (`--` in some years) |
| `date` | Date, YYYY-MM-DD |
| `time_utc` | Time, HHMM UTC |
| `latitude_deg_n`, `longitude_deg_e` | Centre position, degrees north / east |
| `ci_number` | Dvorak current intensity (CI / T) number |
| `central_pressure_hpa` | Estimated central pressure, hPa |
| `max_sustained_wind_kt` | Maximum sustained surface wind, knots (1 kt = 1.852 km/h) |
| `pressure_drop_hpa` | Pressure drop at the centre (delta P), hPa |
| `grade` | Intensity as printed: `D` depression (17-27 kt), `DD` deep depression (28-33), `CS` cyclonic storm (34-47), `SCS` severe (48-63), `VSCS` very severe (64-89), `ESCS` extremely severe (90-119), `SuCS`/`SUCS` super cyclonic storm (120+); also `L`, `D Over land` |
| `outermost_isobar_hpa`, `outermost_isobar_size_deg` | Outermost closed isobar (hPa) and its diameter (degrees) |
| `remark` | IMD's text note for the system at that point, e.g. landfall place and time, weakening into a low (rows below the track in the source) |
| `source_marks` | Text printed in a numeric column, as `<column>:<text>` (e.g. `outermost_isobar_hpa:over land`, size written `4x3`) |

## Notes

- The source has one sheet per year with merged cells: serial, basin, name and date are printed once per system or day. They are carried to every row they cover. From 2018 the serial is printed only on each system's first row and is carried down the same way.
- Remark rows (free text such as "Crossed Odisha coast near Paradip...") are attached to the last track point before them, joined with ` | ` when there are several.
- 2026 is tentative ("subject to finalisation after the ACR 2026 meeting"). 2025 and 2026 sheets also have DD / MM / YYYY helper columns; they repeat the date and are not kept.
- Some cells look like typing slips; they are kept as printed: 2016 system 8 (NADA) on 2 Dec 0000 UTC has its values shifted one column left (CI number blank, pressure 1006 in the CI column); 1997 system 4 on 5 Aug 0300 has central pressure 896 hPa. A few systems print two positions for the same time (1997 system 4, a split system; 2011, 2014, 2018, 2022, 2023: 2 rows each), so `year` + `serial` + `date` + `time_utc` is not always unique.
- Checks (12 Nov 2026): 7,448 track points, 411 systems; latitudes 1.5 to 40.8 N, longitudes 42.9 to 103.0 E; no blank keys.
