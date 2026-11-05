# Temperature and heat wave indicators by district, Maharashtra, 1951 to 2024

One row per district per year: average and extreme daily maximum and minimum temperature, hot days, heat wave days and warm nights. Computed by Bharatnomy from IMD's daily gridded temperature; IMD does not publish these indicators as a district table.

## Source

- **Data:** India Meteorological Department (IMD), Pune. Daily maximum and minimum temperature on a 1.0 x 1.0 degree grid (Srivastava et al. 2009), 1951-2024
- **Link:** https://imdpune.gov.in/lrfindex.php (Gridded data: `Max_1_Bin.html`, `Min_1_Bin.html`)
- **Downloaded:** 28 Oct 2026
- **District boundaries:** Census 2011 district map from DataMeet (community-made, not official), used only to decide which grid cells fall in each district. See [`_sources/datameet-maps/`](../_sources/datameet-maps/)
- **Original files:** [`_sources/imd-gridded/`](../_sources/imd-gridded/) (not committed, 1.9 GB; download steps in its README)
- **Script:** [`pipelines/imd-gridded/build_district_indices.py`](../pipelines/imd-gridded/build_district_indices.py)

## How it is computed

- **District daily temperature** = area-weighted average of the 1-degree IMD cells overlapping the district's **2011 boundary** (2 to 7 cells per district).
- **Normal** = 1991-2020 (daily, smoothed with a 31-day running mean), IMD's current climatological normal.
- **Heat wave day** (IMD criteria for the plains): Tmax at least 40 C and at least 4.5 C above normal, or Tmax at least 45 C. **Severe**: at least 6.5 C above normal or at least 47 C.
- **Warm night** (IMD): Tmin at least 4.5 C above normal while Tmax is at least 40 C.
- **Above p90**: Tmax (or Tmin) above the 90th percentile of the same calendar days (5-day window) in 1991-2020.
- Same method as [`CLM_heat-indicators-nagpur_*`](../CLM_heat-indicators-nagpur_1951-to-2025_MH_BNY_DIST/), which uses a single point for Nagpur city instead of the district area.

## Columns

| Column | Meaning |
|---|---|
| `state_ut`, `lgd_state_code` | Maharashtra, 27 |
| `district`, `lgd_district_code` | District, by its current name and LGD code (from [`_reference/geography.csv`](../_reference/geography.csv)) |
| `district_census_code` | Census 2011 district code; the boundary used is the 2011 one |
| `year` | Calendar year |
| `tmax_mean_c`, `tmin_mean_c` | Mean daily maximum / minimum temperature over the year, C |
| `tmax_highest_c`, `tmin_highest_c` | Highest daily maximum / minimum of the year, C |
| `tmin_lowest_c` | Lowest daily minimum of the year, C |
| `tmax_mean_mar_may_c`, `tmin_mean_mar_may_c` | Mean daily maximum / minimum, March-May, C |
| `days_tmax_40c_or_more`, `days_tmax_45c_or_more` | Days with Tmax at or above 40 C / 45 C |
| `heatwave_days`, `severe_heatwave_days` | Days meeting the IMD heat wave / severe heat wave criteria |
| `warm_nights` | Nights meeting the IMD warm night criteria |
| `days_tmax_above_p90`, `nights_tmin_above_p90` | Days with Tmax / Tmin above the 1991-2020 90th percentile |

## Notes

- **The 1-degree grid smooths out extremes.** A 1-degree cell is about 110 km across, so gridded Tmax runs a few degrees below what stations record on the hottest days. IMD's heat wave and warm night rules are written for station readings, so `heatwave_days` and `warm_nights` here are much lower than station counts (Nagpur averages about 1 heat wave day a year here) and are best read as a trend. The percentile columns do not depend on absolute thresholds and are the better measure of change over time.
- IMD notes that its gridded temperature from 2008 onward is based on fewer stations (about 180).
- 2025 is not included: IMD had published temperature up to 2024 when this was downloaded.
- **2011 boundaries.** `Thane` includes today's Palghar. Names and LGD codes are today's.
- Checks (5 Nov 2026): 2,590 rows = 35 districts x 74 years; no duplicate or empty keys; no blank values; mean Tmin never above mean Tmax; severe heat wave days never exceed heat wave days. Nagpur's highest Tmax agrees with `CLM_heat-indicators-nagpur_*` (correlation 1.00).
