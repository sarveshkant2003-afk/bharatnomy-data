# Heat and rainfall indicators for Nagpur, 1951 to 2025

One row per year for Nagpur: hottest day and night, heat wave days, warm nights, hot days and nights relative to normal, annual and monsoon rainfall with departure from normal, and land surface temperature from satellite. Computed by Bharatnomy from IMD gridded data and NASA MODIS; IMD does not publish these figures for Nagpur as a table.

## Source

- **Data:** India Meteorological Department (IMD) Pune daily gridded data: maximum and minimum temperature, 1.0 x 1.0 degree, 1951-2024; rainfall, 0.25 x 0.25 degree, 1951-2025. NASA MOD11A2 v6.1 land surface temperature (Terra MODIS, 8-day, 1 km)
- **Link:** https://imdpune.gov.in/lrfindex.php ; https://modis.ornl.gov/rst/api/v1/
- **Downloaded:** 28 Oct 2026
- **Original files:** [`_sources/imd-gridded/`](../_sources/imd-gridded/) (not committed, 1.9 GB; download steps in its README) and [`_sources/nasa-modis-lst/raw/`](../_sources/nasa-modis-lst/raw/)

## How it is computed

- **Temperature** is the IMD grid interpolated (bilinear) to Nagpur city, 21.1458 N 79.0882 E.
- **Rainfall** is the average of the 42 IMD 0.25-degree cells with centres in 20.50-21.75 N, 78.25-79.75 E, a box around Nagpur district (not its exact boundary).
- **Normal** = 1991-2020 for temperature (daily, smoothed with a 31-day running mean); 1971-2020 for rainfall (IMD's long period average).
- **Heat wave day** (IMD criteria for the plains): Tmax at least 40 C and at least 4.5 C above normal, or Tmax at least 45 C. **Severe**: at least 6.5 C above normal or Tmax at least 47 C.
- **Warm night** (IMD): Tmin at least 4.5 C above normal while Tmax is at least 40 C.
- **Above p90**: Tmax (or Tmin) above the 90th percentile of the same calendar days (5-day window) in 1991-2020.
- **LST**: mean of clear 1 km pixels in a 21 x 21 km box centred on the city, for each 8-day composite with at least half the box clear.

## Columns

| Column | Meaning |
|---|---|
| `state_ut`, `district` | Maharashtra, Nagpur |
| `year` | Calendar year |
| `tmax_highest_c`, `tmin_highest_c` | Highest daily maximum / minimum temperature of the year, C |
| `tmax_mean_mar_may_c`, `tmin_mean_mar_may_c` | Mean daily max / min temperature, March-May, C |
| `days_tmax_40c_or_more`, `days_tmax_45c_or_more` | Days with Tmax at or above 40 C / 45 C |
| `heatwave_days`, `severe_heatwave_days` | Days meeting the IMD heat wave / severe heat wave criteria |
| `warm_nights` | Nights meeting the IMD warm night criteria |
| `days_tmax_above_p90`, `nights_tmin_above_p90` | Days with Tmax / Tmin above the 1991-2020 90th percentile |
| `rainfall_annual_mm`, `rainfall_jun_sep_mm` | Rainfall in the year / in the south-west monsoon (June-September), mm |
| `rainfall_annual_departure_pct`, `rainfall_jun_sep_departure_pct` | Departure from the 1971-2020 average, % |
| `lst_day_mean_mar_may_c`, `lst_night_mean_mar_may_c` | Mean land surface temperature (about 10:30 and 22:30 local time), March-May, C |
| `lst_day_highest_8day_c`, `lst_night_highest_8day_c` | Highest 8-day mean land surface temperature of the year, C |

## Notes

- **The 1-degree grid smooths out extremes.** Gridded Tmax for Nagpur peaks around 42-45 C, while the Nagpur (Sonegaon) observatory reaches 46-47 C in hot years. IMD's heat wave and warm night rules are written for station readings, so `heatwave_days` and `warm_nights` here are much lower than station-based counts and are best read as a trend, not a count of declared heat waves. The percentile columns do not depend on absolute thresholds and are the better measure of change over time.
- IMD notes that its gridded temperature from 2008 onward is based on fewer stations (about 180).
- Temperature is not yet available for 2025 (IMD has published 2024 so far).
- **LST is incomplete for now:** day LST covers 2002-2022 and night LST 2002-2011, because the download was stopped partway; only years with all 8-day composites downloaded are filled. 2001 has gaps in the MODIS record and is left blank.
- Land surface temperature is the temperature of the ground and roofs, not of the air; it runs well above air temperature on summer afternoons.
- Blank cells are years outside a source's coverage.
