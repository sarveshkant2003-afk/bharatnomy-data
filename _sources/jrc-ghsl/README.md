# JRC Global Human Settlement Layer: built-up surface grids

Used for [`ENV_built-up-surface_1975-to-2030_STATES_BNY_DIST/`](../../ENV_built-up-surface_1975-to-2030_STATES_BNY_DIST/).

- **Data:** European Commission, Joint Research Centre (JRC), GHSL Data Package 2023: GHS-BUILT-S R2023A (total built-up surface, and non-residential built-up surface), epochs 1975-2030 every 5 years, WGS84, 30 arc-seconds (about 1 km)
- **Link:** https://ghsl.jrc.ec.europa.eu/ghs_buS2023.php ; files at https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_BUILT_S_GLOBE_R2023A/ (no login)
- **Citation:** Pesaresi M., Politis P. (2023): GHS-BUILT-S R2023A - GHS built-up surface grid, derived from Sentinel-2 composite and Landsat, multitemporal (1975-2030). European Commission, Joint Research Centre (JRC)
- **Downloaded:** 12 Nov 2026
- **`raw/`:** not committed (24 global GeoTIFFs, about 3 GB). Run `sh pipelines/jrc-ghsl/fetch_ghsl.sh` from the repo root to download them.
- **Script:** [`pipelines/jrc-ghsl/build_district_builtup.py`](../../pipelines/jrc-ghsl/build_district_builtup.py)
