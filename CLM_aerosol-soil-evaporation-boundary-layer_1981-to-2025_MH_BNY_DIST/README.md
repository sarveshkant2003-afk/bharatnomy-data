# Aerosols, soil wetness, evaporation and mixing height by district, Maharashtra, monthly, 1981 to 2025

One row per district per month: aerosol optical depth (haze and dust), soil wetness, evaporation from land, the top of the boundary layer, and an approximate mixing height and ventilation coefficient (how well the air disperses pollution). Computed by Bharatnomy from NASA POWER monthly data.

## Source

- **Data:** NASA Prediction Of Worldwide Energy Resources (POWER), monthly, from the MERRA-2 reanalysis on a 0.5 x 0.625 degree grid (parameters AOD_55, GWETTOP, GWETROOT, GWETPROF, EVLAND, PBLTOP, PS, T2M, WS10M)
- **Link:** https://power.larc.nasa.gov/ (monthly point API, no login)
- **Downloaded:** 12 Nov 2026
- **District boundaries:** Census 2011 district map from DataMeet (see [`_sources/datameet-maps/`](../_sources/datameet-maps/))
- **Original files:** [`_sources/nasa-power/`](../_sources/nasa-power/) (not committed; `pipelines/nasa-power/fetch_power_monthly.py` downloads them in about 5 minutes)
- **Script:** [`pipelines/nasa-power/build_district_monthly.py`](../pipelines/nasa-power/build_district_monthly.py)

## How it is computed

- **District value** = area-weighted average of the POWER cells overlapping the district's 2011 boundary (2 to 14 cells).
- **Mixing height (approx.)** = (287.05 x T / 9.81) x ln(surface pressure / boundary-layer-top pressure), with T the 2 m temperature in kelvin: the height of the boundary-layer top above the ground, from the two pressures.
- **Ventilation coefficient (approx.)** = mixing height x 10 m wind speed. Both use monthly means, so they are rougher than values from hourly data (pollution forecasters use the daily minimum, often at night or early morning).

## Columns

| Column | Meaning |
|---|---|
| `state_ut`, `lgd_state_code`, `district`, `lgd_district_code`, `district_census_code` | Place (2011 boundary; today's name and LGD code) |
| `year`, `month` | Year; month as YYYY-MM |
| `aod_550nm` | Aerosol optical depth at 550 nm, no unit (0.1 clear, above 1 very hazy) |
| `soil_wetness_surface_frac` | Surface soil wetness, top 5 cm: 0 = completely dry, 1 = saturated |
| `soil_wetness_root_zone_frac` | Root-zone soil wetness, top ~1 m, 0 to 1 |
| `soil_wetness_profile_frac` | Soil wetness of the whole soil column, 0 to 1 |
| `evaporation_land_mm_day` | Evaporation from land (soil, plants, wet surfaces: evapotranspiration), mm per day, monthly mean |
| `pbl_top_pressure_kpa` | Air pressure at the top of the planetary boundary layer, kPa |
| `surface_pressure_kpa` | Surface air pressure, kPa |
| `temperature_2m_c` | Mean air temperature at 2 m, C |
| `wind_speed_10m_ms` | Mean wind speed at 10 m, m/s |
| `mixing_height_approx_m` | Approximate mixing height, m (see above) |
| `ventilation_coefficient_approx_m2s` | Approximate ventilation coefficient, m2/s (see above) |
| `source_flag` | `not_available` where `aod_550nm` is blank (POWER has no aerosol data before 2001) |

## Notes

- **Model data, not measurements.** MERRA-2 is a reanalysis (a weather model fitted to observations) with cells about 55 x 65 km. AOD here is MERRA-2's, not MODIS satellite retrievals (those need a NASA Earthdata login).
- Soil wetness is a 0-1 index, not volumetric soil moisture (m3/m3).
- POWER's month "13" (its annual value) is not kept.
- `Thane` includes today's Palghar (2011 boundaries).
- Checks (12 Nov 2026): 18,900 rows = 35 districts x 540 months; no duplicate keys; blanks only in `aod_550nm` before 2001 (8,400 cells); soil wetness within 0-1; no negative evaporation.
