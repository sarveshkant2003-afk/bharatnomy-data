# Wind and humidity by district, Maharashtra, 1981 to 2025

One row per district per year: mean wind speed at 10 m and 50 m, highest wind, prevailing wind direction, calm and strong-wind days, relative humidity and wet-bulb temperature. Computed by Bharatnomy from NASA POWER daily data.

## Source

- **Data:** NASA Prediction Of Worldwide Energy Resources (POWER), daily, meteorology from the MERRA-2 reanalysis on a 0.5 x 0.625 degree grid (parameters WS10M, WS10M_MAX, WD10M, WS50M, RH2M, T2MWET)
- **Link:** https://power.larc.nasa.gov/ (daily point API)
- **Downloaded:** 5 Nov 2026
- **District boundaries:** Census 2011 district map from DataMeet (see [`_sources/datameet-maps/`](../_sources/datameet-maps/))
- **Original files:** [`_sources/nasa-power/`](../_sources/nasa-power/) (not committed; `pipelines/nasa-power/fetch_power.py` downloads them)
- **Script:** [`pipelines/nasa-power/build_district_wind_humidity.py`](../pipelines/nasa-power/build_district_wind_humidity.py)

## How it is computed

- **District daily value** = area-weighted average of the POWER cells overlapping the district's 2011 boundary (2 to 14 cells). Wind direction is the direction of the average wind vector.
- **Prevailing direction** = the most frequent of 8 compass sectors among the year's daily directions (direction the wind blows from).
- **Calm day** (our definition): daily mean 10 m wind below 1 m/s. **Strong-wind day** (our definition): daily maximum 10 m wind at least 10.8 m/s (Beaufort 6, "strong breeze").

## Columns

| Column | Meaning |
|---|---|
| `state_ut`, `lgd_state_code`, `district`, `lgd_district_code`, `district_census_code` | Place (2011 boundary; today's name and LGD code) |
| `year` | Calendar year |
| `wind_speed_10m_mean_ms`, `wind_speed_50m_mean_ms` | Mean wind speed at 10 m / 50 m, m/s |
| `wind_speed_10m_max_highest_ms` | Highest daily maximum wind speed at 10 m, m/s (hourly model values, not gusts) |
| `wind_direction_prevailing`, `wind_direction_prevailing_days` | Most frequent daily wind direction (N, NE, ... NW) and on how many days |
| `calm_days_below_1ms` | Days with mean 10 m wind below 1 m/s |
| `strong_wind_days_10_8ms` | Days with maximum 10 m wind at least 10.8 m/s |
| `relative_humidity_mean_pct`, `relative_humidity_mean_mar_may_pct`, `relative_humidity_mean_jun_sep_pct` | Mean relative humidity at 2 m: year, March-May, June-September, % |
| `wet_bulb_temp_highest_c`, `wet_bulb_temp_mean_mar_may_c` | Wet-bulb temperature at 2 m (combined heat and humidity): highest daily mean of the year, and March-May mean, C |

## Notes

- **Model data, not station readings.** MERRA-2 is a reanalysis (a weather model fitted to observations) with cells about 55 x 65 km. It smooths local extremes; storm gusts, thunderstorm squalls and dust storms are not captured. IMD station data would be better but is not free.
- 50 m is the highest level POWER provides; turbine hub height (100-120 m) is not available here.
- No heat index: it needs humidity at the hour of peak heat, which daily data cannot give. Wet-bulb temperature is given instead.
- `Thane` includes today's Palghar (2011 boundaries).
- Checks (5 Nov 2026): 1,575 rows = 35 districts x 45 years; no blanks; no duplicate keys.
