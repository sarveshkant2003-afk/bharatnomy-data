# Days by air quality category per city per year, 2015 to 2026

One row per city per year: how many days the CPCB daily bulletin put the city in each Air Quality Index category (Good to Severe), days with very poor or severe air, the average and highest AQI, which pollutant drove the index, and how many monitoring stations reported. Counted by Bharatnomy from CPCB's daily AQI bulletins.

## Source

- **Data:** Central Pollution Control Board (CPCB), National Air Quality Index daily bulletins (4 pm)
- **Built from:** [`ENV_aqi-daily_2015-to-2026_STATES_CPCB_CITY`](../ENV_aqi-daily_2015-to-2026_STATES_CPCB_CITY/), which holds every bulletin parsed into one row per city per day (original PDFs in [`_sources/cpcb-aqi-bulletin/`](../_sources/cpcb-aqi-bulletin/))
- **Link:** https://cpcb.nic.in/AQI_Bulletin.php
- **Downloaded:** 28 Oct 2026 (bulletins); counted 5 Nov 2026
- **Script:** [`pipelines/cpcb-aqi/build_aqi_days.py`](../pipelines/cpcb-aqi/build_aqi_days.py)

## How it is computed

Counts of bulletin days per calendar year, using the category as printed in the bulletin: Good (0-50), Satisfactory (51-100), Moderate (101-200), Poor (201-300), Very Poor (301-400), Severe (401-500).

## Columns

| Column | Meaning |
|---|---|
| `city` | City as printed in the bulletin |
| `year` | Calendar year |
| `days_reported` | Days the city appears in a bulletin that year |
| `days_good`, `days_satisfactory`, `days_moderate`, `days_poor`, `days_very_poor`, `days_severe` | Days in each AQI category, as printed |
| `days_very_poor_or_severe` | Very Poor plus Severe days (AQI above 300) |
| `days_aqi_above_100` | Days with AQI above 100 (Moderate or worse), counted from the AQI value |
| `aqi_mean`, `aqi_highest` | Mean and highest daily AQI of the year |
| `days_pm25_prominent`, `days_pm10_prominent`, `days_o3_prominent` | Days on which PM2.5 / PM10 / ozone was named a prominent pollutant (a day can name more than one) |
| `stations_reporting_max` | Most stations that reported on any day of the year: a lower bound on the city's number of monitoring stations (continuous stations only; the bulletin does not cover manual NAMP stations) |

## Notes

- **Compare days with `days_reported`.** Cities join the bulletin over the years and miss days when data is unavailable; 2015 starts on 1 May and 2026 ends on 27 Oct. A low count can mean few bulletin days, not clean air.
- `days_aqi_above_100` differs from Moderate + Poor + Very Poor + Severe in 53 city-years: in 2018 the bulletin labels an AQI of exactly 100 as Moderate (103 city-days), and two 2015 bulletins print a category that does not match the AQI (71 printed Moderate, 111 printed Satisfactory). Both columns are kept as they come from the bulletin.
- No `state_ut` column: the bulletin gives only city names (see the daily dataset's notes).
- Checks (5 Nov 2026): 1,991 rows (city x year); category days add up to `days_reported` in every row.
