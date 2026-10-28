# MODIS land surface temperature for Nagpur (NASA)

Original files used for:

- [`CLM_heat-indicators-nagpur_1951-to-2025_MH_BNY_DIST/`](../../CLM_heat-indicators-nagpur_1951-to-2025_MH_BNY_DIST/)

## Source

- **Data:** NASA LP DAAC, MOD11A2 v6.1 (Terra MODIS, 8-day land surface temperature and emissivity, 1 km), served by the ORNL DAAC MODIS web service
- **Link:** https://modis.ornl.gov/rst/api/v1/ (product `MOD11A2`, bands `LST_Day_1km` and `LST_Night_1km`, 21 x 21 km box centred on 21.1458 N, 79.0882 E)
- **Downloaded:** 28 Oct 2026
- **`raw/`:** one gzipped JSON-lines file per band, one line per 8-day composite (raw pixel values; multiply by 0.02 for kelvin, 0 = no data). Partial so far: 1,087 of 1,221 day composites and 570 night composites (download stopped on 28 Oct 2026).
