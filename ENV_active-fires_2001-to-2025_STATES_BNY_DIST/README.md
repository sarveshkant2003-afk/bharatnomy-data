# Satellite fire detections by district, India, 2001 to 2025

One row per district per year: number of vegetation fires detected by NASA's MODIS satellites (Terra and Aqua), in total and by season. Used as a measure of crop-residue and forest burning. Counted by Bharatnomy from NASA FIRMS.

## Source

- **Data:** NASA Fire Information for Resource Management System (FIRMS), MODIS Collection 6.1 active fire detections (1 km), India country files
- **Link:** https://firms.modaps.eosdis.nasa.gov/country/ (files `data/country/modis/<year>/modis_<year>_India.csv`)
- **Downloaded:** 5 Nov 2026
- **District boundaries:** Census 2011 district map from DataMeet (see [`_sources/datameet-maps/`](../_sources/datameet-maps/))
- **Original files:** [`_sources/nasa-firms/`](../_sources/nasa-firms/) (not committed, 31 MB; `pipelines/nasa-firms/fetch_firms.sh` downloads them)
- **Script:** [`pipelines/nasa-firms/build_district_fires.py`](../pipelines/nasa-firms/build_district_fires.py)

## How it is computed

Each detection of type 0 (presumed vegetation fire) is placed in the Census 2011 district whose boundary contains it. Detections of type 2 (static industrial heat sources such as steel plants) and 3 (offshore) are left out. Counts are by date of detection.

## Columns

| Column | Meaning |
|---|---|
| `state_ut`, `lgd_state_code` | State/UT today (Telangana and Ladakh districts are under their current state) |
| `district`, `lgd_district_code` | District by its current name and LGD code (from [`_reference/geography.csv`](../_reference/geography.csv)) |
| `district_census_code` | Census 2011 district code; the boundary used is the 2011 one |
| `year` | Calendar year |
| `fire_detections` | Vegetation fire detections in the year (count) |
| `fire_detections_confidence_30_plus` | Detections with confidence 30% or more (FIRMS "nominal" and "high"); the rest are low-confidence |
| `fire_detections_jan_feb`, `_mar_may`, `_jun_sep`, `_oct_dec` | Detections by season; they add up to `fire_detections` |

## Notes

- **Detections, not fires or area burnt.** A large fire can be detected several times, and small or short fires and fires under cloud are missed. Use the counts to compare places and years.
- The data do not say whether a fire is on farmland; crop-residue burning shows up as the October-December peak in Punjab and Haryana and the March-May peak elsewhere.
- **2011 boundaries:** a district split after 2011 is counted in its parent (Palghar in Thane). Districts with no detection in a year have 0.
- 2000 is left out (MODIS starts in November 2000). Each year 119 to 760 detections fall outside every district polygon (on coasts, borders and in an area the map leaves without a district code in Jammu & Kashmir).
- Checks (5 Nov 2026): 16,000 rows = 640 districts x 25 years; seasons add up to the annual total in every row.
