# Daily Air Quality Index by city, May 2015 to Oct 2026

The National Air Quality Index for each city with continuous monitoring stations, every day: AQI value (24-hour average at 4 PM), category, prominent pollutant and number of stations. Coverage grows from 11 cities in mid-2015 to over 300 in 2026. Nagpur is covered from 2016.

## Source

- **Data:** Central Pollution Control Board (CPCB), Ministry of Environment, Forest and Climate Change, daily National AQI bulletin
- **Link:** https://cpcb.nic.in/AQI_Bulletin.php (each day's PDF: `https://cpcb.nic.in/upload/Downloads/AQI_Bulletin_YYYYMMDD.pdf`)
- **Downloaded:** 28 Oct 2026
- **Original files:** not committed (4,193 PDFs, 213 MB); see [`_sources/cpcb-aqi-bulletin/`](../_sources/cpcb-aqi-bulletin/)

## Columns

| Column | Meaning |
|---|---|
| `city` | City as printed in the bulletin. Names printed in lower case (mid-2026) are capitalised; a few cities carry their state, e.g. `Aurangabad (Maharashtra)` |
| `date` | Bulletin date, `YYYY-MM-DD` |
| `air_quality` | Category as printed: Good (0-50), Satisfactory (51-100), Moderate (101-200), Poor (201-300), Very Poor (301-400), Severe (401-500) |
| `aqi` | Air Quality Index, average of the city's stations over the past 24 hours |
| `prominent_pollutants` | Pollutant(s) driving the index: PM2.5, PM10, O3, NO2, SO2, CO, NH3 |
| `stations_reporting` | Stations that reported (blank in May 2015, before the bulletin printed it) |
| `stations_total` | Stations in the city (printed from Oct 2023) |

## Notes

- The bulletin has no state column, so there is no `state_ut` here. Several city names exist in more than one state (e.g. Aurangabad); the bulletin only adds the state in some years.
- Days without a bulletin or with an unreadable one (9 days: 2015-06-12, 2015-06-29, 2015-06-30, 2015-08-28, 2015-10-22, 2016-07-04, 2016-07-21 to 2016-07-23, mostly "server problem" notices) are missing. A city is also missing on days its data "was not available", as the bulletin notes.
- In 2018 the bulletin sometimes labels values exactly at a boundary (50, 100) with the higher category; categories are kept as printed.
- Read from the PDFs by code; spot checks against the PDFs matched.
