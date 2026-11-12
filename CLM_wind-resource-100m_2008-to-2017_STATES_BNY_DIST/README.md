# Wind power density and wind speed at 100 m by district, India (2008-2017 climate)

How much wind energy is available at turbine hub height (100 m) in each district: the long-term mean wind power density and wind speed, and their 90th percentile across the district (wind farms use the windiest spots). Computed by Bharatnomy from the Global Wind Atlas.

## Source

- **Data:** Global Wind Atlas 3 (Technical University of Denmark, DTU, with the World Bank / ESMAP), mean power density and mean wind speed at 100 m on a 250 m grid; modelled from ERA5 reanalysis for 2008-2017, downscaled with WRF and WAsP. Licence CC BY 4.0 (see globalwindatlas.info)
- **Link:** https://globalwindatlas.info/ (country download for India, layers "power-density" and "wind-speed" at 100 m; no login)
- **Downloaded:** 12 Nov 2026 (rasters not committed, about 425 MB; `pipelines/global-wind-atlas/fetch_gwa.sh` downloads them, see [`_sources/global-wind-atlas/`](../_sources/global-wind-atlas/))
- **District boundaries:** Census 2011 district map from DataMeet (see [`_sources/datameet-maps/`](../_sources/datameet-maps/))
- **Script:** [`pipelines/global-wind-atlas/build_district_wind_resource.py`](../pipelines/global-wind-atlas/build_district_wind_resource.py)

## How it is computed

- District mean = mean of all 250 m cells whose centre lies inside the district's 2011 boundary; 90th percentile over the same cells.
- Wind power density (W/m2) is the energy flux of the wind through a vertical area, 0.5 x air density x mean of (speed cubed); GWA computes it from the full wind-speed distribution, so it is not simply derived from the mean speed.

## Columns

| Column | Meaning |
|---|---|
| `state_ut`, `lgd_state_code`, `district`, `lgd_district_code`, `district_census_code` | Place (2011 boundary; today's name and LGD code) |
| `power_density_100m_mean_w_m2`, `power_density_100m_p90_w_m2` | Wind power density at 100 m: district mean and 90th percentile, W/m2 |
| `wind_speed_100m_mean_ms`, `wind_speed_100m_p90_ms` | Mean wind speed at 100 m: district mean and 90th percentile, m/s |
| `raster_coverage_pct` | Share of the district covered by the GWA India raster, % |
| `source_flag` | `not_available` where the raster covers less than half of the district (values left blank) |

## Notes

- **Model data, long-term average** (one value per district, no years). Not a measurement and not a site assessment.
- The GWA "India" raster follows a different national boundary from the Census map: most districts of Jammu & Kashmir, Ladakh and parts of Arunachal Pradesh are outside it, so 35 districts are blank. Uttarkashi (84% covered) keeps its values.
- Checks (12 Nov 2026): 640 districts; no duplicate keys; no negative values; highest district means are in the Tamil Nadu wind belt (Tirunelveli 390 W/m2, Theni, Tiruppur, Kanniyakumari), consistent with where India's wind farms are.
