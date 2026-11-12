# Built-up surface by district, India, 1975 to 2030 (every 5 years)

Area covered by buildings in every district, and its share of the district's area, every five years from 1975 (2025 and 2030 are JRC projections). Computed by Bharatnomy from the EU Global Human Settlement Layer.

## Source

- **Data:** European Commission, Joint Research Centre (JRC), GHSL Data Package 2023, GHS-BUILT-S R2023A: built-up surface (total and non-residential), 30 arc-second grid (about 1 km), epochs 1975-2030
- **Link:** https://ghsl.jrc.ec.europa.eu/ghs_buS2023.php (no login)
- **Downloaded:** 12 Nov 2026 (grids not committed, about 3 GB; `pipelines/jrc-ghsl/fetch_ghsl.sh` downloads them, see [`_sources/jrc-ghsl/`](../_sources/jrc-ghsl/))
- **District boundaries:** Census 2011 district map from DataMeet (see [`_sources/datameet-maps/`](../_sources/datameet-maps/))
- **Script:** [`pipelines/jrc-ghsl/build_district_builtup.py`](../pipelines/jrc-ghsl/build_district_builtup.py)

## How it is computed

- Each grid cell holds square metres of built-up surface (building footprint area, from satellite images). A cell belongs to the district that contains its centre.
- District built-up = sum of its cells. District area = sum of the same cells' areas on the WGS84 ellipsoid (`grid_land_area_sq_km`), so the share is built-up / that area.

## Columns

| Column | Meaning |
|---|---|
| `state_ut`, `lgd_state_code`, `district`, `lgd_district_code`, `district_census_code` | Place (2011 boundary; today's name and LGD code) |
| `year` | GHSL epoch: 1975, 1980, ... 2030 |
| `built_up_sq_km` | Built-up surface (all buildings), sq km |
| `built_up_non_residential_sq_km` | Built-up surface of non-residential buildings, sq km |
| `grid_land_area_sq_km` | District area as covered by the grid cells, sq km (close to, not equal to, the official area) |
| `built_up_pct_of_area` | Built-up surface as % of `grid_land_area_sq_km` |
| `source_flag` | `estimated` for 2025 and 2030 (JRC's projections; the epochs up to 2020 are from satellite data) |

## Notes

- **Our calculation from a modelled satellite product.** GHSL measures building footprints (roofs), not all paved surface: roads, parking and yards are not included, so this understates total impervious surface. Values at 1 km are approximate for small districts.
- 2011 boundaries throughout, so a district's series is comparable over time. `Thane` includes today's Palghar, etc.
- Checks (12 Nov 2026): 7,680 rows = 640 districts x 12 epochs; no duplicate keys; non-residential never above total; shares within 0-100; no district's built-up area falls between 2015 and 2020. India total built-up: 8,381 sq km (1975), 38,232 sq km (2020), 1.2% of the grid area; highest 2020 shares: Kolkata 40.6%, Hyderabad 37.9%, Delhi North East 37.8%, Chennai 34.1%. Nagpur: 1.6% (2020).
