# Rainfall variability by district, Maharashtra, 1971 to 2020

One row per district: average yearly rainfall over 1971-2020, its standard deviation, and the coefficient of variation (how much rainfall swings from year to year). Computed by Bharatnomy from IMD's daily gridded rainfall.

## Source

- **Data:** India Meteorological Department (IMD), Pune. Daily rainfall on a 0.25 x 0.25 degree grid (Pai et al. 2014)
- **Link:** https://imdpune.gov.in/lrfindex.php (Gridded data: `Rainfall_25_Bin.html`)
- **Downloaded:** 28 Oct 2026
- **Built from:** the yearly totals in [`CLM_rainfall-indices_1951-to-2025_MH_BNY_DIST`](../CLM_rainfall-indices_1951-to-2025_MH_BNY_DIST/) (district averages over 2011 boundaries; method described there)
- **Script:** [`pipelines/imd-gridded/build_district_indices.py`](../pipelines/imd-gridded/build_district_indices.py)

## How it is computed

Over the 50 years 1971-2020 (IMD's long period average): mean, sample standard deviation, and coefficient of variation = standard deviation / mean x 100.

## Columns

| Column | Meaning |
|---|---|
| `state_ut`, `lgd_state_code` | Maharashtra, 27 |
| `district`, `lgd_district_code` | District, by its current name and LGD code |
| `district_census_code` | Census 2011 district code; the boundary used is the 2011 one |
| `period` | Years used, `1971-2020` |
| `rainfall_annual_mean_mm`, `rainfall_annual_sd_mm`, `rainfall_annual_cv_pct` | Annual rainfall: mean and standard deviation (mm), coefficient of variation (%) |
| `rainfall_jun_sep_mean_mm`, `rainfall_jun_sep_sd_mm`, `rainfall_jun_sep_cv_pct` | The same for June-September rainfall |
| `years` | Number of years used (50) |

## Notes

- `Thane` includes today's Palghar (2011 boundaries).
- Pune's variability (57%, against 18-34% elsewhere) is driven by one year: IMD's grid gives Pune 4,342 mm in 2005. See the note in `CLM_rainfall-indices_*`.
